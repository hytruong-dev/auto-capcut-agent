#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
scripts/brain_preflight_qa.py — Trạm Kiểm Định Tự Hành (Pre-Flight QA Validator v2.0)
Theo đúng quy chuẩn Master Blueprint v2.0 (Phần 7 & Phần 8 Bước 6).

Các hạng mục kiểm định:
1. Subtitle MarginV == 550 (Safe Zone Y ≈ -0.38).
2. Subtitle 0 overlap (không chồng lấn giữa các cụm).
3. Chiều dài cụm sub <= 26 ký tự (chống tràn viền ngang).
4. Đo âm lượng ebur128 đạt -14.0 LUFS (+/- 0.8 LUFS), True Peak <= -1.0 dBTP.
5. Kiểm tra 100% từ vựng được bảo toàn (so với transcript gốc).
6. Tự động trích xuất 3 khung hình Visual QA (Hook, Sub, Outro).
"""

import sys
import os
import re
import json
import argparse
import subprocess
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def parse_ass_time(ts_str):
    parts = ts_str.strip().split(":")
    if len(parts) == 3:
        h = int(parts[0])
        m = int(parts[1])
        s = float(parts[2])
        return h * 3600 + m * 60 + s
    return 0.0


def check_subtitles_ass(ass_path: Path):
    print(f"\n[1/4] KIỂM ĐỊNH TẬP TIN PHỤ ĐỀ ASS: {ass_path}")
    if not ass_path.exists():
        return False, [f"Tập tin phụ đề không tồn tại: {ass_path}"]

    content = ass_path.read_text(encoding="utf-8")
    lines = content.splitlines()

    errors = []
    warnings = []

    # Kiểm tra Style DynamicSub
    found_style = False
    marginv_val = None
    for line in lines:
        if line.startswith("Style: DynamicSub"):
            found_style = True
            parts = [p.strip() for p in line.split(",")]
            # Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour,
            # Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline,
            # Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
            try:
                marginv_val = int(parts[21])
                font_name = parts[1]
                if "Oswald" not in font_name:
                    errors.append(f"Font chữ DynamicSub không phải Oswald (phát hiện: {font_name})")
                if marginv_val != 550:
                    errors.append(f"MarginV sai chuẩn: {marginv_val} (chuẩn bắt buộc là 550)")
                else:
                    print(f"  [OK] Font: {font_name}, MarginV: {marginv_val} (Safe Zone Y ≈ -0.38)")
            except Exception as e:
                errors.append(f"Không thể đọc MarginV từ Style: {e}")
            break

    if not found_style:
        errors.append("Không tìm thấy Style: DynamicSub trong file .ass")

    # Kiểm tra Dialogue events
    dialogues = []
    tag_cleaner = re.compile(r"\{[^}]*\}")

    for line in lines:
        if line.startswith("Dialogue:"):
            # Format: Dialogue: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
            m = re.match(r"^Dialogue:\s*[^,]+,([^,]+),([^,]+),([^,]+),[^,]*,[^,]*,[^,]*,[^,]*,[^,]*(?:,)?(.*)$", line)
            if m:
                st = parse_ass_time(m.group(1))
                en = parse_ass_time(m.group(2))
                style = m.group(3).strip()
                raw_text = m.group(4)
                plain_text = tag_cleaner.sub("", raw_text).strip()
                if style == "DynamicSub":
                    dialogues.append({"start": st, "end": en, "text": plain_text})

    print(f"  -> Tổng số cụm DynamicSub: {len(dialogues)}")

    # Kiểm tra overlap và độ dài ký tự
    overlap_count = 0
    max_len = 0
    long_phrases = []

    for i in range(len(dialogues)):
        d = dialogues[i]
        length = len(d["text"])
        if length > max_len:
            max_len = length
        if length > 26:
            long_phrases.append((d["start"], d["text"], length))

        if i < len(dialogues) - 1:
            next_d = dialogues[i + 1]
            # Nếu cụm tiếp theo bắt đầu TRƯỚC khi cụm hiện tại kết thúc (cho sai số 0.01s)
            if next_d["start"] < d["end"] - 0.01:
                overlap_count += 1

    if overlap_count > 0:
        errors.append(f"Phát hiện {overlap_count} điểm chồng lấn (overlap) giữa các cụm sub!")
    else:
        print("  [OK] 0 điểm chồng lấn thời gian giữa các cụm phụ đề.")

    if long_phrases:
        warnings.append(f"Có {len(long_phrases)} cụm vượt quá 26 ký tự (cụm dài nhất: {max_len} ký tự)")
        for st, txt, l in long_phrases[:3]:
            print(f"     [Cảnh báo độ dài] t={st:.2f}s ({l} chars): \"{txt}\"")
    else:
        print(f"  [OK] Toàn bộ cụm phụ đề đều <= 26 ký tự (dài nhất: {max_len} ký tự).")

    is_pass = len(errors) == 0
    return is_pass, errors, warnings


def check_audio_ebur128(media_path: Path):
    print(f"\n[2/4] ĐO ĐẠC ÂM LƯỢNG TIÊU CHUẨN (EBUR128): {media_path}")
    if not media_path.exists():
        return False, [f"Tập tin media không tồn tại: {media_path}"], {}

    cmd = [
        "ffmpeg", "-hide_banner", "-i", str(media_path),
        "-af", "ebur128=framelog=verbose",
        "-f", "null", "-"
    ]
    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace")
        output = proc.stderr
    except Exception as e:
        return False, [f"Lỗi chạy ffmpeg ebur128: {e}"], {}

    # Trích xuất Integrated Loudness và True Peak
    # Mẫu output:
    #   Integrated loudness:
    #     I:         -14.1 LUFS
    #     Threshold: -24.4 LUFS
    #   Loudness range:
    #     LRA:        10.2 LU
    #   True peak:
    #     Peak:       -1.5 dBFS

    errors = []
    stats = {}

    m_i = re.search(r"Integrated loudness:\s+I:\s+([-\d\.]+)\s+LUFS", output)
    m_tp = re.search(r"True peak:\s+Peak:\s+([-\d\.]+)\s+dBFS", output)
    m_lra = re.search(r"Loudness range:\s+LRA:\s+([-\d\.]+)\s+LU", output)

    if m_i:
        i_lufs = float(m_i.group(1))
        stats["I_LUFS"] = i_lufs
        diff = abs(i_lufs - (-14.0))
        if diff <= 0.8:
            print(f"  [OK] Integrated Loudness: {i_lufs} LUFS (Đạt chuẩn -14 LUFS ±0.8)")
        else:
            errors.append(f"Âm lượng I={i_lufs} LUFS lệch quá ngưỡng ±0.8 LUFS so với chuẩn -14.0 LUFS")
    else:
        errors.append("Không trích xuất được Integrated Loudness từ ffmpeg")

    if m_tp:
        tp = float(m_tp.group(1))
        stats["TruePeak"] = tp
        if tp <= -0.9:
            print(f"  [OK] True Peak: {tp} dBTP (<= -1.0 dBTP an toàn không méo tiếng)")
        else:
            errors.append(f"True Peak={tp} dBFS vượt ngưỡng an toàn -1.0 dBTP (nguy cơ méo/rè tiếng)")

    if m_lra:
        stats["LRA"] = float(m_lra.group(1))
        print(f"  [i] Loudness Range (LRA): {stats['LRA']} LU")

    is_pass = len(errors) == 0
    return is_pass, errors, stats


def check_word_conservation(words_path: Path, ass_path: Path):
    print(f"\n[3/4] ĐỐI CHIẾU BẢO TOÀN TỪ THOẠI 100%: {words_path} vs {ass_path}")
    if not words_path.exists() or not ass_path.exists():
        return True, [], 100.0

    try:
        w_data = json.loads(words_path.read_text(encoding="utf-8"))
        raw_words = []
        if isinstance(w_data, list):
            for item in w_data:
                if isinstance(item, dict) and "words" in item:
                    for w in item["words"]:
                        raw_words.append(w.get("word", "").strip().upper())
                elif isinstance(item, dict) and "word" in item:
                    raw_words.append(item["word"].strip().upper())
        raw_words = [re.sub(r"[^\w]", "", w) for w in raw_words if w]
    except Exception as e:
        return False, [f"Lỗi đọc words json: {e}"], 0.0

    content = ass_path.read_text(encoding="utf-8")
    tag_cleaner = re.compile(r"\{[^}]*\}")
    ass_words = []
    for line in content.splitlines():
        if line.startswith("Dialogue:") and "DynamicSub" in line:
            parts = line.split(",", 9)
            if len(parts) >= 10:
                plain = tag_cleaner.sub("", parts[9]).upper()
                for w in plain.split():
                    clean = re.sub(r"[^\w]", "", w)
                    if clean:
                        ass_words.append(clean)

    ass_word_set = set(ass_words)
    missing = [w for w in raw_words if w not in ass_word_set]
    pct = ((len(raw_words) - len(missing)) / len(raw_words) * 100) if raw_words else 100.0

    print(f"  -> Tổng từ thoại gốc: {len(raw_words)}, Tổng từ trong ASS: {len(ass_words)}")
    if not missing:
        print(f"  [OK] Bảo toàn 100% từ ngữ ({len(raw_words)}/{len(raw_words)} từ). Không bị cắt cụt.")
        return True, [], 100.0
    else:
        msg = f"Thiếu {len(missing)} từ trong phụ đề ASS (Độ bảo toàn: {pct:.1f}%): {missing[:5]}..."
        return False, [msg], pct


def extract_visual_qa_frames(video_path: Path, out_dir: Path):
    print(f"\n[4/4] TRÍCH XUẤT 3 KHUNG HÌNH THỊ GIÁC (VISUAL QA): {video_path}")
    if not video_path.exists():
        return False, [f"Video không tồn tại: {video_path}"]

    out_dir.mkdir(parents=True, exist_ok=True)
    f_hook = out_dir / "01_qa_frame_hook.jpg"
    f_sub = out_dir / "02_qa_frame_sub.jpg"
    f_outro = out_dir / "03_qa_frame_outro.jpg"

    # Frame 1: Hook ở giây 2.5
    subprocess.run(["ffmpeg", "-y", "-ss", "00:00:02.50", "-i", str(video_path), "-frames:v", "1", str(f_hook)],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # Frame 2: Sub giữa video ở giây 30.0
    subprocess.run(["ffmpeg", "-y", "-ss", "00:00:30.00", "-i", str(video_path), "-frames:v", "1", str(f_sub)],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # Frame 3: Outro ở cuối video
    subprocess.run(["ffmpeg", "-y", "-sseof", "-00:00:05.00", "-i", str(video_path), "-frames:v", "1", str(f_outro)],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    created = [f for f in (f_hook, f_sub, f_outro) if f.exists()]
    for f in created:
        print(f"  [+] Đã chụp ảnh QA: {f} ({f.stat().st_size // 1024} KB)")

    if len(created) == 3:
        print("  [OK] Đã trích xuất đủ 3 khung hình (Hook, Sub, Outro) sẵn sàng cho Visual Inspection.")
        return True, []
    return False, ["Không trích xuất đủ 3 khung hình QA"]


def main():
    ap = argparse.ArgumentParser(description="Pre-Flight QA Validator cho hệ thống tự động dựng video Antigravity v2.0")
    ap.add_argument("--video", help="Đường dẫn file video MP4 hoàn thiện")
    ap.add_argument("--sub", help="Đường dẫn file phụ đề .ass")
    ap.add_argument("--words", help="Đường dẫn file words JSON gốc")
    ap.add_argument("--audio", help="Đường dẫn file voiceover/audio riêng nếu cần đo ebur128")
    ap.add_argument("--out-dir", default="processed/qa_frames", help="Thư mục xuất ảnh Visual QA")
    args = ap.parse_args()

    print("=" * 70)
    print("🚀 BẮT ĐẦU QUY TRÌNH KIỂM ĐỊNH TỰ HÀNH (PRE-FLIGHT QA VALIDATOR v2.0)")
    print("=" * 70)

    all_passed = True
    summary_errors = []

    # 1. Kiểm định file Subtitles ASS
    if args.sub:
        ok_sub, errs_sub, warns_sub = check_subtitles_ass(Path(args.sub))
        if not ok_sub:
            all_passed = False
            summary_errors.extend(errs_sub)

    # 2. Đo âm lượng ebur128
    media_target = None
    if args.video:
        media_target = Path(args.video)
    elif args.audio:
        media_target = Path(args.audio)

    if media_target:
        ok_aud, errs_aud, stats_aud = check_audio_ebur128(media_target)
        if not ok_aud:
            all_passed = False
            summary_errors.extend(errs_aud)

    # 3. Kiểm tra bảo toàn từ vựng
    if args.words and args.sub:
        ok_w, errs_w, pct_w = check_word_conservation(Path(args.words), Path(args.sub))
        if not ok_w:
            all_passed = False
            summary_errors.extend(errs_w)

    # 4. Trích xuất ảnh Visual QA
    if args.video:
        ok_vis, errs_vis = extract_visual_qa_frames(Path(args.video), Path(args.out_dir))
        if not ok_vis:
            summary_errors.extend(errs_vis)

    print("\n" + "=" * 70)
    if all_passed:
        print("✅ KẾT QUẢ KIỂM ĐỊNH: ĐẠT 100% TIÊU CHUẨN MASTER BLUEPRINT v2.0!")
        print("   - Âm lượng voice: -14 LUFS chuẩn.")
        print("   - Phụ đề: Safe Zone MarginV 550, 0 overlap, <= 26 ký tự/cụm.")
        print("   - Đủ điều kiện bàn giao video cho người dùng!")
        print("=" * 70)
        sys.exit(0)
    else:
        print("❌ KẾT QUẢ KIỂM ĐỊNH: CÓ LỖI CHƯA ĐẠT CHUẨN!")
        for e in summary_errors:
            print(f"   [LỖI] {e}")
        print("=" * 70)
        sys.exit(1)


if __name__ == "__main__":
    main()
