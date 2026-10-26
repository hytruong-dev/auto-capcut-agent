"""
Render hoàn chỉnh video Vlog XanhSM 1 Ngày Chạy Xe (Tổng thu 176k):
- Đầu ra: processed/Vlog_XanhSM_1Ngay_176k_FINAL.mp4 (1080x1920 dọc, 30fps)
- Ghép 17 cảnh quay chuẩn khớp kịch bản từ 3 footage thô:
  + Sáng (Đơn 1: 16k, Đơn 2: 22k)
  + Chiều kẹt xe (Đơn 3: 35k, Đơn 4: 28k)
  + Đêm lên đèn (Đơn 5: 42k, Đơn 6: 33k, Chốt 176k)
- Xoay 90 độ, scale dọc 9:16 chuẩn TikTok / Reels / Shorts
- Trộn 4 tầng âm thanh: OmniVoice Voice Clone + BGM LoFi (-16dB) + SFX Cash/Ting Ting nhận tiền + SFX Hook
- Ép cứng phụ đề ASS Dynamic Word-by-Word Karaoke (Cyan highlight, Vàng Chanh inactive, Oswald-Bold) + 6 Thẻ tiền nhận đơn
"""

import os
import sys
import json
import subprocess
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

def render_vlog():
    print("[*] Bắt đầu quy trình Render Video Vlog XanhSM 176k với Dynamic Karaoke & OmniVoice Voice...")
    
    out_dir = Path("processed")
    temp_dir = out_dir / "temp_render_176k"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    final_video = out_dir / "Vlog_XanhSM_1Ngay_176k_FINAL.mp4"
    
    # 1. Trộn Master Audio
    print("[1/3] Trộn toàn bộ các tầng âm thanh (OmniVoice Clone + BGM LoFi + SFX Nhận Tiền)...")
    
    vo_file = "processed/voiceover_omnivoice_176k/vlog_xanhsm_176k_omnivoice_master.mp3"
    bgm_file = "processed/bgm_xanhsm_176k_loop.mp3"
    sfx_cash = "public/sfx/cash_register.mp3"
    sfx_ting = "public/sfx/ting_money.mp3"
    sfx_whoosh = "public/sfx/whoosh_fast.mp3"
    sfx_ding = "public/sfx/ding_highlight.mp3"
    
    # Timeline SFX nhận tiền khớp từng mili-giây với lúc câu nói nhận tiền vang lên
    sfx_events = [
        {"file": sfx_whoosh, "delay": 0},      # Hook whoosh
        {"file": sfx_ding, "delay": 1200},     # Hook ding
        {"file": sfx_cash, "delay": 19200},    # Đơn 1 (+16k, Tổng 16k)
        {"file": sfx_ting, "delay": 29500},    # Đơn 2 (+22k, Tổng 38k)
        {"file": sfx_cash, "delay": 39500},    # Đơn 3 (+35k, Tổng 73k)
        {"file": sfx_ting, "delay": 49500},    # Đơn 4 (+28k, Tổng 101k)
        {"file": sfx_cash, "delay": 59800},    # Đơn 5 (+42k, Tổng 143k)
        {"file": sfx_cash, "delay": 69500},    # Đơn 6 (+33k, Tổng 176k)
        {"file": sfx_ting, "delay": 74200}     # Chốt sổ 176k
    ]
    
    inputs = ["-i", vo_file, "-i", bgm_file]
    filter_parts = []
    
    # [0:a] là OmniVoice voiceover: volume 1.05
    filter_parts.append("[0:a]volume=1.05[avo];")
    # [1:a] là bgm: volume 0.16
    filter_parts.append("[1:a]volume=0.16[abgm];")
    
    mix_labels = ["[avo]", "[abgm]"]
    
    for idx, se in enumerate(sfx_events, start=2):
        inputs.extend(["-i", se["file"]])
        d = se["delay"]
        filter_parts.append(f"[{idx}:a]adelay={d}|{d},volume=0.9[asfx{idx}];")
        mix_labels.append(f"[asfx{idx}]")
        
    total_audio_inputs = len(mix_labels)
    filter_parts.append(f"{''.join(mix_labels)}amix=inputs={total_audio_inputs}:duration=first:dropout_transition=0,volume={total_audio_inputs * 0.75}[aout]")
    
    master_audio = temp_dir / "master_audio_mixed.wav"
    cmd_audio = ["ffmpeg", "-y"] + inputs + ["-filter_complex", "".join(filter_parts), "-map", "[aout]", str(master_audio)]
    subprocess.run(cmd_audio, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[+] Đã tạo Master Audio hoàn chỉnh: {master_audio}")

    # 2. Render các đoạn video cuts
    print("[2/3] Cắt ghép và định dạng 17 phân cảnh 9:16 dọc từ 3 footage...")
    
    cut_definitions = [
        # --- CA SÁNG (0.0s -> 31.5s) ---
        {"foot": "raw_footage/DJI_20260908084243_0057_D.MP4", "src_st": 0.0, "dur": 6.0},   # Hook
        {"foot": "raw_footage/DJI_20260908084243_0057_D.MP4", "src_st": 6.0, "dur": 4.5},   # Cùng cày thực tế
        {"foot": "raw_footage/DJI_20260908084243_0057_D.MP4", "src_st": 10.5, "dur": 4.5},  # Bắt đầu ca sáng
        {"foot": "raw_footage/DJI_20260908084243_0057_D.MP4", "src_st": 15.0, "dur": 6.5},  # Đón bạn học sinh
        {"foot": "raw_footage/DJI_20260908084243_0057_D.MP4", "src_st": 21.5, "dur": 5.5},  # Đơn 1 (+16k)
        {"foot": "raw_footage/DJI_20260908084243_0057_D.MP4", "src_st": 27.0, "dur": 4.5},  # Đơn 2 (+22k)
        
        # --- CA CHIỀU / TAN TẦM (31.5s -> 56.5s) ---
        {"foot": "raw_footage/DJI_20260908183824_0062_D.MP4", "src_st": 0.0, "dur": 5.0},   # Trà đá & Đơn 3
        {"foot": "raw_footage/DJI_20260908183824_0062_D.MP4", "src_st": 10.0, "dur": 5.5},  # Đơn 3 (+35k)
        {"foot": "raw_footage/DJI_20260908183824_0062_D.MP4", "src_st": 22.0, "dur": 4.5},  # Zoom & Giờ tan tầm
        {"foot": "raw_footage/DJI_20260908183824_0062_D.MP4", "src_st": 26.5, "dur": 5.0},  # Luồn lách hẻm nhỏ
        {"foot": "raw_footage/DJI_20260908183824_0062_D.MP4", "src_st": 37.0, "dur": 5.0},  # Đơn 4 (+28k)
        
        # --- CA ĐÊM / PHỐ LÊN ĐÈN (56.5s -> 88.5s) ---
        {"foot": "raw_footage/DJI_20260908185603_0064_D.MP4", "src_st": 0.0, "dur": 5.5},   # 7h tối lên đèn
        {"foot": "raw_footage/DJI_20260908185603_0064_D.MP4", "src_st": 10.0, "dur": 5.5},  # Gió mát đường đêm, Đơn 5 (+42k)
        {"foot": "raw_footage/DJI_20260908185603_0064_D.MP4", "src_st": 18.5, "dur": 5.0},  # Thấm mệt tìm đơn về
        {"foot": "raw_footage/DJI_20260908185603_0064_D.MP4", "src_st": 29.0, "dur": 5.5},  # Đơn 6 tiện đường (+33k)
        {"foot": "raw_footage/DJI_20260908185603_0064_D.MP4", "src_st": 38.0, "dur": 5.0},  # Tổng kết ngày 176k
        {"foot": "raw_footage/DJI_20260908185603_0064_D.MP4", "src_st": 51.0, "dur": 5.5}   # Outro tim & bình luận
    ]
    
    seg_files = []
    for i, c in enumerate(cut_definitions):
        seg_mp4 = temp_dir / f"seg_{i:02d}.mp4"
        seg_files.append(str(seg_mp4.resolve()))
        if not seg_mp4.exists():
            vf = "transpose=1,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,eq=brightness=0.04:saturation=1.2:contrast=1.06"
            cmd_cut = [
                "ffmpeg", "-y",
                "-ss", str(c["src_st"]),
                "-t", str(c["dur"]),
                "-i", c["foot"],
                "-vf", vf,
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                "-r", "30", "-an",
                str(seg_mp4)
            ]
            subprocess.run(cmd_cut, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"  [+] Đã cắt phân cảnh {i+1}/{len(cut_definitions)} ({c['dur']}s)")

    # Nối các phân cảnh thành 1 video thô liên tục
    concat_txt = temp_dir / "concat_video.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for sf in seg_files:
            f.write(f"file '{sf.replace(chr(92), '/')}'\n")

    raw_stitched_video = temp_dir / "stitched_raw_video.mp4"
    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_txt),
        "-c", "copy",
        str(raw_stitched_video)
    ]
    subprocess.run(cmd_concat, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[+] Đã nối xong chuỗi 17 phân cảnh: {raw_stitched_video}")

    # 3. Ép phụ đề ASS Dynamic Karaoke và ghép Master Audio hoàn chỉnh
    print("[3/3] Ép phụ đề ASS Dynamic Karaoke (Word Highlight Cyan/Vàng) & Xuất Bản Video...")
    
    ass_path = str(Path("processed/vlog_xanhsm_176k_master.ass").resolve()).replace("\\", "/")
    ass_filter_path = ass_path.replace(":", "\\:")
    
    cmd_final = [
        "ffmpeg", "-y",
        "-i", str(raw_stitched_video),
        "-i", str(master_audio),
        "-vf", f"ass='{ass_filter_path}'",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(final_video)
    ]
    subprocess.run(cmd_final, check=True)
    
    dur_final = float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(final_video)
    ]).decode().strip())
    size_mb = os.path.getsize(final_video) / (1024 * 1024)
    
    print("\n" + "="*60)
    print("🎉 CHÚC MỪNG! VIDEO VLOG XANHSM 176K ĐÃ ĐƯỢC RENDER HOÀN TẤT!")
    print(f"🎬 File xuất bản: {final_video}")
    print(f"⏱️ Thời lượng: {dur_final:.2f}s (~{dur_final/60:.2f} phút)")
    print(f"💾 Dung lượng: {size_mb:.2f} MB")
    print(f"✨ Độ phân giải: 1080x1920 (9:16 dọc chuẩn TikTok/Reels/Shorts)")
    print(f"🎙️ Giọng đọc: OmniVoice Voice Clone (được train từ mẫu ref_sample_hook.wav)")
    print(f"🔤 Phụ đề: Dynamic Word Karaoke (Từ active màu Cyan #66FFFF, từ khác màu Vàng #F0FF00, Oswald-Bold)")
    print(f"💵 6 Đơn xe (+16k, +22k, +35k, +28k, +42k, +33k) & Thẻ Tổng Thu 176k kèm SFX")
    print("="*60)

if __name__ == "__main__":
    render_vlog()
