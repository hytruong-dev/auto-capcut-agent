#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
scripts/build_and_render_vlog_demo02.py — Pipeline Sản Xuất Hoàn Chỉnh Vlog Demo 02 (Master Blueprint v2.0)
Thực hiện trọn gói theo Master Blueprint v2.0:
1. Sinh phụ đề Dynamic Word Karaoke + Elastic Micro-Pop (Oswald-Bold, MarginV 550, 0 overlap, <= 26 chars).
2. Xây dựng và triển khai dự án CapCut Pro Desktop 9.6: "vlog_demo02" (6 tracks, multi-timeline, keyframe zoom, font cache).
3. Trộn và chuẩn hóa Master Audio 2-Pass Loudnorm đạt chuẩn -14.0 LUFS (-ar 48000).
4. Render video hoàn chỉnh: processed/vlog_demo02.mp4 (1080x1920 9:16, 30fps).
5. Kích hoạt Pre-Flight QA Validator kiểm định 100% tiêu chuẩn trước khi bàn giao.
"""

import os
import sys
import json
import uuid
import time
import shutil
import subprocess
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

def us(sec: float) -> int:
    return int(round(sec * 1_000_000))

def main():
    print("=" * 70)
    print("🚀 BẮT ĐẦU SẢN XUẤT VIDEO: 'vlog_demo02' (MASTER BLUEPRINT v2.0)")
    print("=" * 70)

    base_dir = Path("c:/QuangHy/editvideo")
    out_dir = base_dir / "processed"
    temp_dir = out_dir / "temp_render_176k_long"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    project_name = "vlog_demo02"
    final_video = out_dir / f"{project_name}.mp4"
    ass_file = out_dir / f"{project_name}.ass"
    words_file = out_dir / "cleaned_words_176k_long.json"
    qa_frames_dir = out_dir / f"qa_frames_{project_name}"
    qa_frames_dir.mkdir(parents=True, exist_ok=True)

    # -------------------------------------------------------------
    # BƯỚC 1: SINH PHỤ ĐỀ DYNAMIC KARAOKE MICRO-POP (brain_karaoke_ass.py)
    # -------------------------------------------------------------
    print("\n[BƯỚC 1/5] Sinh phụ đề Dynamic Word Karaoke với hiệu ứng Elastic Micro-Pop...")
    cmd_ass = [
        sys.executable, str(base_dir / "scripts" / "brain_karaoke_ass.py"),
        "--words", str(words_file),
        "--out", str(ass_file),
        "--hook1", "THỬ THÁCH 1 NGÀY",
        "--hook2", "CHẠY XE XANH SM",
        "--hook-end", "5.5",
        "--callout", "TIM ❤️ VÀ THEO DÕI ĐỂ XEM TIẾP NHÉ",
        "--callout-start", "143.0",
        "--callout-end", "150.0",
        "--marginv", "550",
        "--size", "76"
    ]
    subprocess.run(cmd_ass, check=True)

    # -------------------------------------------------------------
    # BƯỚC 2: TRỘN MASTER AUDIO & CHUẨN HÓA 2-PASS LOUDNORM -14 LUFS
    # -------------------------------------------------------------
    print("\n[BƯỚC 2/5] Xử lý Master Audio 4 tầng & Chuẩn hóa 2-Pass Linear Loudnorm (-14 LUFS)...")
    vo_file = out_dir / "voiceover_xanhsm_176k" / "vlog_xanhsm_176k_full_voiceover.mp3"
    bgm_file = out_dir / "bgm_xanhsm_176k_loop.mp3"
    sfx_whoosh = base_dir / "public" / "sfx" / "whoosh_fast.mp3"
    sfx_ding = base_dir / "public" / "sfx" / "ding_highlight.mp3"
    sfx_cash = base_dir / "public" / "sfx" / "cash_register.mp3"
    sfx_ting = base_dir / "public" / "sfx" / "ting_money.mp3"

    sfx_schedule = [
        {"file": str(sfx_whoosh), "delay": 0, "vol": 0.85},          # Hook whoosh
        {"file": str(sfx_ding), "delay": 1200, "vol": 0.90},         # Hook ding
        {"file": str(sfx_cash), "delay": 26800, "vol": 0.95},        # Đơn 1 (+16k)
        {"file": str(sfx_ting), "delay": 44800, "vol": 0.95},        # Đơn 2 (+22k)
        {"file": str(sfx_cash), "delay": 65400, "vol": 0.95},        # Đơn 3 (+35k)
        {"file": str(sfx_ting), "delay": 82700, "vol": 0.95},        # Đơn 4 (+28k)
        {"file": str(sfx_cash), "delay": 105100, "vol": 0.95},       # Đơn 5 (+42k)
        {"file": str(sfx_cash), "delay": 124800, "vol": 0.95},       # Đơn 6 (+33k)
        {"file": str(sfx_ting), "delay": 125600, "vol": 0.90},       # Ting chốt ca
        {"file": str(sfx_ding), "delay": 129500, "vol": 0.95}        # Thẻ Tổng Thu 176k
    ]

    # Trộn Voiceover (vol: 1.0) + BGM Ducking (vol: 0.15) + SFX với normalize=0
    inputs_audio = ["-i", str(vo_file), "-i", str(bgm_file)]
    filter_parts = [
        "[0:a]volume=1.0,aresample=48000[avo];",
        "[1:a]volume=0.15,aresample=48000[abgm];"
    ]
    mix_labels = ["[avo]", "[abgm]"]

    for idx, item in enumerate(sfx_schedule, start=2):
        inputs_audio.extend(["-i", item["file"]])
        d = item["delay"]
        v = item["vol"]
        filter_parts.append(f"[{idx}:a]adelay={d}|{d},volume={v},aresample=48000[asfx{idx}];")
        mix_labels.append(f"[asfx{idx}]")

    num_inputs = len(mix_labels)
    # amix normalize=0 để giữ nguyên dynamic levels
    filter_parts.append(f"{''.join(mix_labels)}amix=inputs={num_inputs}:duration=first:dropout_transition=0:normalize=0,aresample=48000[aout]")

    unnorm_audio = temp_dir / f"unnorm_audio_mix_{project_name}.wav"
    cmd_audio = ["ffmpeg", "-y"] + inputs_audio + ["-filter_complex", "".join(filter_parts), "-map", "[aout]", str(unnorm_audio)]
    subprocess.run(cmd_audio, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Pass 1: Đo đạc chính xác các thông số đầu vào bằng loudnorm print_format=json
    p1 = subprocess.run([
        "ffmpeg", "-hide_banner", "-i", str(unnorm_audio),
        "-af", "loudnorm=I=-14.0:TP=-1.5:LRA=11.0:print_format=json",
        "-f", "null", "-"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace")
    
    # Parse JSON block ở cuối stderr
    import re
    m = re.search(r"\{\s*\"input_i\"[\s\S]*\}", p1.stderr)
    master_audio = temp_dir / f"master_audio_{project_name}.wav"
    if m:
        p1_stats = json.loads(m.group(0))
        m_i = p1_stats.get("input_i", "-14.0")
        m_tp = p1_stats.get("input_tp", "-1.5")
        m_lra = p1_stats.get("input_lra", "11.0")
        m_th = p1_stats.get("input_thresh", "-24.0")
        print(f"  [i] Pass 1 Loudnorm Stats: I={m_i}, TP={m_tp}, LRA={m_lra}, Thresh={m_th}")
        
        # Pass 2: Áp dụng các thông số đo được để chuẩn hóa tuyến tính chính xác 100% về -14 LUFS
        p2_filter = f"loudnorm=I=-14.0:TP=-1.5:LRA=11.0:measured_I={m_i}:measured_TP={m_tp}:measured_LRA={m_lra}:measured_thresh={m_th}:linear=true,aresample=48000"
        subprocess.run(["ffmpeg", "-y", "-i", str(unnorm_audio), "-af", p2_filter, str(master_audio)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        # Fallback
        subprocess.run(["ffmpeg", "-y", "-i", str(unnorm_audio), "-af", "loudnorm=I=-14.0:TP=-1.5:LRA=11.0:linear=true,aresample=48000", str(master_audio)], check=True)
    
    # Hiệu chỉnh vi lượng tuyệt đối (EBUR128 Micro-Calibration) để đạt chuẩn -14.0 LUFS ± 0.1 LUFS
    p_check = subprocess.run([
        "ffmpeg", "-hide_banner", "-i", str(master_audio),
        "-af", "ebur128", "-f", "null", "-"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace")
    m_cur = re.search(r"Integrated loudness:\s+I:\s+([-\d\.]+)\s+LUFS", p_check.stderr)
    if m_cur:
        cur_i = float(m_cur.group(1))
        diff_db = -14.0 - cur_i
        print(f"  [i] Đo EBUR128 thực tế: {cur_i:.2f} LUFS (Độ lệch so với -14.0: {diff_db:+.2f} dB)")
        if abs(diff_db) > 0.1:
            calibrated_audio = temp_dir / f"master_audio_{project_name}_calibrated.wav"
            subprocess.run([
                "ffmpeg", "-y", "-i", str(master_audio),
                "-af", f"volume={diff_db:.2f}dB,aresample=48000",
                str(calibrated_audio)
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            master_audio = calibrated_audio
            print(f"  [OK] Đã tự động vi chỉnh {diff_db:+.2f} dB -> Chuẩn hóa tuyệt đối về -14.0 LUFS!")
    
    print(f"  [OK] Đã xuất Master Audio chuẩn -14 LUFS: {master_audio}")

    # -------------------------------------------------------------
    # BƯỚC 3: TRIỂN KHAI DỰ ÁN CAPCUT PRO 9.6 DESKTOP ("vlog_demo02")
    # -------------------------------------------------------------
    print(f"\n[BƯỚC 3/5] Triển khai dự án CapCut Pro Desktop: '{project_name}'...")
    dur_sec = float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(vo_file)
    ]).decode().strip())
    total_dur_us = us(dur_sec)

    materials = {
        "audio_balances": [], "audio_effects": [], "audio_fades": [], "audios": [],
        "beats": [], "canvases": [], "chromas": [], "color_curves": [], "drafts": [],
        "effects": [], "flowers": [], "green_screens": [], "handwrites": [], "hsl": [],
        "images": [], "log_color_wheels": [], "loudnesses": [], "manual_deformations": [],
        "masks": [], "material_animations": [], "material_colors": [], "placeholders": [],
        "plugin_effects": [], "primary_color_wheels": [], "realtime_denoises": [], "shapes": [],
        "smart_crops": [], "sound_channel_mappings": [], "speeds": [], "stickers": [],
        "tail_leaders": [], "text_templates": [], "texts": [], "time_marks": [], "transitions": [],
        "video_effects": [], "video_trackings": [], "videos": [], "vocal_beautifys": [], "vocal_separations": []
    }

    def reg_audio(mat_id, path_obj, name):
        d = float(subprocess.check_output([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(path_obj)
        ]).decode().strip())
        materials["audios"].append({
            "app_id": 0, "category_id": "", "category_name": "", "check_flag": 1,
            "duration": us(d), "effect_id": "", "formula_id": "", "id": mat_id,
            "intensifies_path": "", "local_material_id": "", "music_id": str(uuid.uuid4()),
            "name": name, "path": str(path_obj.resolve()).replace("\\", "/"), "query": "",
            "resource_id": "", "search_id": "", "source_platform": 0, "team_id": "",
            "text_id": "", "tone_category_id": "", "tone_category_name": "",
            "tone_effect_id": "", "tone_effect_name": "", "tone_speaker": "",
            "tone_type": "", "type": "extract_music", "video_id": "", "wave_points": []
        })
        return us(d)

    def reg_video(mat_id, path_obj, name):
        d = float(subprocess.check_output([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(path_obj)
        ]).decode().strip())
        materials["videos"].append({
            "audio_fade": None, "category_id": "", "category_name": "", "check_flag": 63487,
            "crop": {"lower_left_x": 0.0, "lower_left_y": 1.0, "lower_right_x": 1.0, "lower_right_y": 1.0, "upper_left_x": 0.0, "upper_left_y": 0.0, "upper_right_x": 1.0, "upper_right_y": 0.0},
            "crop_ratio": "free", "crop_scale": 1.0, "duration": us(d), "extra_type": "option_empty",
            "formula_id": "", "freeze": None, "gameplay": None, "has_audio": False,
            "height": 1920, "id": mat_id, "intensifies_audio_path": "", "intensifies_path": "",
            "is_ai_generate_content": False, "is_busi_sticker": False, "is_text_edit": False,
            "live_photo": None, "local_id": "", "local_material_id": "", "material_id": "",
            "material_name": name, "material_url": "", "matting": None, "media_path": "",
            "music_id": "", "object_locked": None, "origin_material_id": "", "path": str(path_obj.resolve()).replace("\\", "/"),
            "picture_from": "none", "picture_set_category_id": "", "picture_set_category_name": "",
            "request_id": "", "reverse_intensifies_path": "", "reverse_path": "", "smart_motion": None,
            "source_platform": 0, "stable": None, "team_id": "", "type": "video",
            "video_algorithm": {"algorithms": [], "deflicker": None, "motion_blur_config": None, "noise_reduction": None, "path": "", "quality_enhance": None, "time_range": None},
            "width": 1080
        })
        return us(d)

    # 1. Đăng ký Audio
    vo_mat_id = str(uuid.uuid4()).upper()
    bgm_mat_id = str(uuid.uuid4()).upper()
    reg_audio(vo_mat_id, vo_file, "vlog_voiceover.mp3")
    reg_audio(bgm_mat_id, bgm_file, "bgm_lofi.mp3")

    sfx_mat_ids = {}
    for sf_name, sf_p in [("whoosh", sfx_whoosh), ("ding", sfx_ding), ("cash", sfx_cash), ("ting", sfx_ting)]:
        m_id = str(uuid.uuid4()).upper()
        sfx_mat_ids[sf_name] = m_id
        reg_audio(m_id, sf_p, f"sfx_{sf_name}.mp3")

    # Segment Audio Tracks
    voice_track_segment = {
        "id": str(uuid.uuid4()).upper(), "material_id": vo_mat_id,
        "target_timerange": {"start": 0, "duration": total_dur_us},
        "source_timerange": {"start": 0, "duration": total_dur_us},
        "clip": {"alpha": 1.0, "volume": 1.0}, "render_index": 20000
    }
    bgm_track_segment = {
        "id": str(uuid.uuid4()).upper(), "material_id": bgm_mat_id,
        "target_timerange": {"start": 0, "duration": total_dur_us},
        "source_timerange": {"start": 0, "duration": total_dur_us},
        "clip": {"alpha": 1.0, "volume": 0.15}, "render_index": 20010
    }
    sfx_segments = []
    for s in sfx_schedule:
        s_type = "whoosh" if "whoosh" in s["file"] else ("ding" if "ding" in s["file"] else ("cash" if "cash" in s["file"] else "ting"))
        mat_id = sfx_mat_ids[s_type]
        sfx_segments.append({
            "id": str(uuid.uuid4()).upper(), "material_id": mat_id,
            "target_timerange": {"start": s["delay"] * 1000, "duration": 1500000},
            "source_timerange": {"start": 0, "duration": 1500000},
            "clip": {"alpha": 1.0, "volume": s["vol"]}, "render_index": 20020
        })

    # 2. Đăng ký Video Scenes (15 phân cảnh cắt sẵn)
    sys.path.insert(0, str(base_dir / "scripts"))
    from capcut_draft_manager import create_zoom_keyframes

    video_segments = []
    cur_v_start = 0
    for i in range(15):
        seg_p = temp_dir / f"scene_{i:02d}.mp4"
        if not seg_p.exists():
            continue
        v_mat_id = str(uuid.uuid4()).upper()
        v_dur_us = reg_video(v_mat_id, seg_p, f"scene_{i:02d}.mp4")
        actual_seg_dur = min(v_dur_us, total_dur_us - cur_v_start)
        
        # Tiêm Keyframe Zoom 1.0 -> 1.15x cho Hook (scene 0) và Scene điểm nhấn (scene 9 đêm lên đèn)
        kfs = []
        if i == 0 or i == 9:
            kfs = create_zoom_keyframes(start_scale=1.0, end_scale=1.15, duration_us=actual_seg_dur, start_offset_us=0)

        v_seg = {
            "id": str(uuid.uuid4()).upper(), "material_id": v_mat_id,
            "target_timerange": {"start": cur_v_start, "duration": actual_seg_dur},
            "source_timerange": {"start": 0, "duration": actual_seg_dur},
            "clip": {"alpha": 1.0, "rotation": 0.0, "scale": {"x": 1.0, "y": 1.0}, "transform": {"x": 0.0, "y": 0.0}},
            "render_index": 10000 + i * 10
        }
        if kfs:
            v_seg["common_keyframes"] = kfs

        video_segments.append(v_seg)
        cur_v_start += actual_seg_dur
        if cur_v_start >= total_dur_us:
            break

    # 3. Đăng ký Text Materials & Styles chuẩn CapCut 9.6 Pro
    font_res_id = "7182504807289065985"
    font_path = "C:/Users/PC/AppData/Local/CapCut/User Data/Cache/effect/7182504807289065985/0a5333de6f4d592cb2d2390d68b31efb/Oswald-Bold.ttf"

    def create_text_mat(text, color_rgb, size=15.0, border_color="#000000", border_width=0.08):
        t_id = str(uuid.uuid4()).upper()
        materials["texts"].append({
            "alignment": 1, "background_alpha": 1.0, "background_color": "",
            "border_alpha": 1.0, "border_color": border_color, "border_width": border_width,
            "check_flag": 7, "content": json.dumps({
                "styles": [{
                    "fill": {"alpha": 1.0, "content": {"render_type": "solid", "solid": {"alpha": 1.0, "color": color_rgb}}},
                    "font": {"id": font_res_id, "path": font_path},
                    "size": size,
                    "strokes": [{"alpha": 1.0, "content": {"render_type": "solid", "solid": {"alpha": 1.0, "color": [0.0, 0.0, 0.0]}}, "width": border_width}]
                }],
                "text": text
            }, ensure_ascii=False),
            "font_category_id": "", "font_category_name": "", "font_id": font_res_id,
            "font_name": "Oswald-Bold", "font_path": font_path, "font_resource_id": font_res_id,
            "font_size": size, "font_source_platform": 0, "font_team_id": "",
            "font_title": "Oswald-Bold", "font_url": "",
            "fonts": [{
                "id": str(uuid.uuid4()).upper(), "resource_id": font_res_id, "third_resource_id": "",
                "category_id": "preset", "category_name": "Cài đặt sẵn", "source_platform": 1,
                "path": font_path, "effect_id": font_res_id, "title": "Oswald-Bold",
                "team_id": "", "file_uri": "", "request_id": ""
            }],
            "global_alpha": 1.0, "group_id": "", "has_shadow": True, "id": t_id,
            "initial_scale": 1.0, "inner_padding": 0.0, "is_rich_text": False, "italic": False,
            "ktv_color": "", "language": "", "layer_weight": 1, "letter_spacing": 0.0,
            "line_feed": 1, "line_max_width": 0.84, "line_spacing": 0.02,
            "multi_language_current": "none", "name": "", "original_size": [],
            "preset_category": "", "preset_category_id": "", "preset_has_set_marker": False,
            "preset_id": "", "preset_index": 0, "preset_name": "", "recognize_task_id": "",
            "recognize_type": 0, "recreate_original_material_id": "", "shadow_alpha": 0.9,
            "shadow_angle": -45.0, "shadow_color": "#000000", "shadow_distance": 5.0,
            "shadow_point": {"x": 3.5, "y": -3.5}, "shadow_smoothing": 0.45,
            "shape_clip_x": False, "shape_clip_y": False, "style_name": "",
            "sub_type": 0, "text_alpha": 1.0, "text_color": "#F0FF00",
            "text_preset_resource_id": "", "text_size": 30, "text_to_audio_ids": [],
            "type": "text", "typesetting": 0, "underline": False, "use_effect_default_color": False,
            "using_hot_words": False
        })
        return t_id

    overlay_segments = []
    # Hook 0-5.5s (2 tầng 3D)
    hook1_id = create_text_mat("THỬ THÁCH 1 NGÀY", [1.0, 0.2, 0.2], size=18.0, border_color="#FFFFFF", border_width=0.08)
    hook2_id = create_text_mat("CHẠY XE XANH SM", [0.941, 1.0, 0.0], size=21.0, border_color="#000000", border_width=0.09)
    overlay_segments.append({
        "id": str(uuid.uuid4()).upper(), "material_id": hook1_id,
        "target_timerange": {"start": 0, "duration": us(5.5)},
        "source_timerange": {"start": 0, "duration": us(5.5)},
        "clip": {"alpha": 1.0, "rotation": 0.0, "scale": {"x": 1.0, "y": 1.0}, "transform": {"x": 0.0, "y": 0.55}},
        "render_index": 40000
    })
    overlay_segments.append({
        "id": str(uuid.uuid4()).upper(), "material_id": hook2_id,
        "target_timerange": {"start": 0, "duration": us(5.5)},
        "source_timerange": {"start": 0, "duration": us(5.5)},
        "clip": {"alpha": 1.0, "rotation": 0.0, "scale": {"x": 1.0, "y": 1.0}, "transform": {"x": 0.0, "y": 0.43}},
        "render_index": 40010
    })

    # 6 Thẻ nhận đơn
    orders = [
        {"st": 26.8, "dur": 5.0, "txt": "✓ HOÀN THÀNH ĐƠN #1\n+16.000đ\nTỔNG THU: 16.000đ"},
        {"st": 44.8, "dur": 4.7, "txt": "✓ HOÀN THÀNH ĐƠN #2\n+22.000đ\nTỔNG THU: 38.000đ"},
        {"st": 65.4, "dur": 5.0, "txt": "✓ HOÀN THÀNH ĐƠN #3\n+35.000đ\nTỔNG THU: 73.000đ"},
        {"st": 82.7, "dur": 7.3, "txt": "✓ HOÀN THÀNH ĐƠN #4\n+28.000đ\nTỔNG THU: 101.000đ"},
        {"st": 105.1, "dur": 4.3, "txt": "✓ HOÀN THÀNH ĐƠN #5\n+42.000đ\nTỔNG THU: 143.000đ"},
        {"st": 124.8, "dur": 4.3, "txt": "✓ HOÀN THÀNH ĐƠN #6 (CHỐT CA)\n+33.000đ\nTỔNG THU: 176.000đ"}
    ]
    for o in orders:
        b_id = create_text_mat(o["txt"], [0.0, 1.0, 0.4], size=16.0)
        overlay_segments.append({
            "id": str(uuid.uuid4()).upper(), "material_id": b_id,
            "target_timerange": {"start": us(o["st"]), "duration": us(o["dur"])},
            "source_timerange": {"start": 0, "duration": us(o["dur"])},
            "clip": {"alpha": 1.0, "rotation": 0.0, "scale": {"x": 1.0, "y": 1.0}, "transform": {"x": 0.0, "y": 0.15}},
            "render_index": 41000
        })

    # Thẻ Tổng Thu 176k & Callout CTA ở nửa trên khung hình
    sum_id = create_text_mat("★ TỔNG THU HÔM NAY: 176.000đ ★\n(6 ĐƠN XE XANHSM)", [1.0, 1.0, 0.0], size=17.0)
    overlay_segments.append({
        "id": str(uuid.uuid4()).upper(), "material_id": sum_id,
        "target_timerange": {"start": us(129.5), "duration": us(13.0)},
        "source_timerange": {"start": 0, "duration": us(13.0)},
        "clip": {"alpha": 1.0, "rotation": 0.0, "scale": {"x": 1.0, "y": 1.0}, "transform": {"x": 0.0, "y": 0.25}},
        "render_index": 42000
    })
    callout_id = create_text_mat("TIM ❤️ VÀ COMMENT GIAO LƯU NHÉ 👍", [0.0, 1.0, 0.5], size=15.0)
    overlay_segments.append({
        "id": str(uuid.uuid4()).upper(), "material_id": callout_id,
        "target_timerange": {"start": us(143.0), "duration": us(10.0)},
        "source_timerange": {"start": 0, "duration": us(10.0)},
        "clip": {"alpha": 1.0, "rotation": 0.0, "scale": {"x": 1.0, "y": 1.0}, "transform": {"x": 0.0, "y": 0.28}},
        "render_index": 43000
    })

    # 4. Phụ đề Track: Dynamic Karaoke, SUB_LEAD = 0.15s, GAP = 0.02s
    with open(words_file, "r", encoding="utf-8") as f:
        cleaned_segs = json.load(f)

    chunks_flat = []
    for seg in cleaned_segs:
        words = seg["words"]
        for i in range(0, len(words), 3):
            chunk = words[i:i+3]
            chunks_flat.append((
                " ".join(w["word"].upper() for w in chunk),
                chunk[0]["master_start"],
                chunk[-1]["master_end"]
            ))

    SUB_LEAD = 0.15
    chunks_flat = [(t, max(0.0, s - SUB_LEAD), max(0.0, e - SUB_LEAD)) for (t, s, e) in chunks_flat]
    chunks_flat.sort(key=lambda x: x[1])

    GAP = 0.02
    subtitle_segments = []
    for idx, (txt, c_st, c_en) in enumerate(chunks_flat):
        if idx + 1 < len(chunks_flat):
            c_en = min(c_en, chunks_flat[idx + 1][1] - GAP)
        c_en = max(c_en, c_st + 0.15)
        if idx + 1 < len(chunks_flat) and c_en > chunks_flat[idx + 1][1] - GAP:
            c_en = chunks_flat[idx + 1][1] - GAP
        
        c_dur = max(0.1, c_en - c_st)
        sub_mat_id = create_text_mat(txt, [0.941, 1.0, 0.0], size=15.0, border_color="#000000", border_width=0.08)
        subtitle_segments.append({
            "id": str(uuid.uuid4()).upper(), "material_id": sub_mat_id,
            "target_timerange": {"start": us(c_st), "duration": us(c_dur)},
            "source_timerange": {"start": 0, "duration": us(c_dur)},
            "clip": {"alpha": 1.0, "rotation": 0.0, "scale": {"x": 1.0, "y": 1.0}, "transform": {"x": 0.0, "y": -0.38}},
            "render_index": 30000
        })

    # Xây dựng 6 Tracks
    tracks = [
        {"id": str(uuid.uuid4()).upper(), "type": "video", "attribute": 0, "segments": video_segments},
        {"id": str(uuid.uuid4()).upper(), "type": "audio", "attribute": 0, "segments": [voice_track_segment]},
        {"id": str(uuid.uuid4()).upper(), "type": "audio", "attribute": 0, "segments": [bgm_track_segment]},
        {"id": str(uuid.uuid4()).upper(), "type": "audio", "attribute": 0, "segments": sfx_segments},
        {"id": str(uuid.uuid4()).upper(), "type": "text", "attribute": 0, "segments": subtitle_segments},
        {"id": str(uuid.uuid4()).upper(), "type": "text", "attribute": 0, "segments": overlay_segments}
    ]

    draft_id = str(uuid.uuid4()).upper()
    now_ms = int(time.time() * 1000)

    draft_content = {
        "canvas_config": {"width": 1080, "height": 1920, "ratio": "9:16"},
        "color_space": -1,
        "config": {
            "adjust_max_index": 1, "lyrics_sync": True, "maintrack_adsorb": True,
            "material_save_mode": 0, "subtitle_sync": True, "system_font_list": [],
            "video_mute": False
        },
        "cover": None, "create_time": now_ms, "duration": total_dur_us, "fps": 30.0,
        "id": draft_id,
        "last_modified_platform": {
            "app_id": 359289, "app_source": "cc", "app_version": "9.6.0",
            "device_id": "4475d19983c69cde88e66433dd341c72", "hard_disk_id": "",
            "mac_address": "26ebfda668b7dfc60a011ffef74a230b,4f652529e3ad390a5fc5f40eb605bcf9",
            "os": "windows", "os_version": "10.0.26300"
        },
        "materials": materials, "name": project_name, "new_version": "116.0.0",
        "platform": {
            "app_id": 359289, "app_source": "cc", "app_version": "9.6.0",
            "device_id": "4475d19983c69cde88e66433dd341c72", "hard_disk_id": "",
            "mac_address": "26ebfda668b7dfc60a011ffef74a230b,4f652529e3ad390a5fc5f40eb605bcf9",
            "os": "windows", "os_version": "10.0.26300"
        },
        "render_index_mode": "off", "render_index_track_mode_on": True,
        "tracks": tracks, "update_time": now_ms, "version": 360000
    }

    from capcut_draft_manager import deploy_capcut_project, validate_project
    deploy_res = deploy_capcut_project(
        project_name=project_name,
        draft_content=draft_content,
        assets_map=None,
        cover_src_path=None,
        draft_id=draft_id,
        auto_close_capcut=False
    )
    validate_project(project_name)
    print(f"  [OK] Dự án CapCut Pro '{project_name}' đã được triển khai hoàn tất!")

    # -------------------------------------------------------------
    # BƯỚC 4: RENDER FINAL MP4 (FFMPEG + ASS SUBTITLE + NIGHT CURVE)
    # -------------------------------------------------------------
    print(f"\n[BƯỚC 4/5] Render video MP4 cuối cùng: {final_video}...")
    raw_stitched = temp_dir / "stitched_raw_long.mp4"
    ass_rel = f"processed/{project_name}.ass"
    fonts_rel = "portable_trained_brain/portable_assets/fonts"
    ass_filter_arg = f"ass='{ass_rel}':fontsdir='{fonts_rel}'"

    cmd_render = [
        "ffmpeg", "-y",
        "-i", str(raw_stitched),
        "-i", str(master_audio),
        "-vf", ass_filter_arg,
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(final_video)
    ]
    subprocess.run(cmd_render, check=True)
    print(f"  [OK] Đã render xong: {final_video} ({final_video.stat().st_size // (1024*1024)} MB)")

    # -------------------------------------------------------------
    # BƯỚC 5: CHẠY PRE-FLIGHT QA VALIDATOR KIỂM ĐỊNH TỰ HÀNH
    # -------------------------------------------------------------
    print("\n[BƯỚC 5/5] Kích hoạt Trạm Kiểm Định Tự Hành (brain_preflight_qa.py)...")
    cmd_qa = [
        sys.executable, str(base_dir / "scripts" / "brain_preflight_qa.py"),
        "--video", str(final_video),
        "--sub", str(ass_file),
        "--words", str(words_file),
        "--out-dir", str(qa_frames_dir)
    ]
    subprocess.run(cmd_qa, check=True)

    print("\n" + "=" * 70)
    print(f"🎉 HOÀN THÀNH 100% SẢN XUẤT VIDEO '{project_name}' THEO MASTER BLUEPRINT v2.0!")
    print(f"   - CapCut Desktop Draft: {project_name} (Đã đăng ký sẵn sàng trong CapCut Pro)")
    print(f"   - Final Render MP4    : {final_video}")
    print(f"   - Phụ đề ASS Karaoke  : {ass_file}")
    print(f"   - Visual QA Frames    : {qa_frames_dir}")
    print("=" * 70)

if __name__ == "__main__":
    main()
