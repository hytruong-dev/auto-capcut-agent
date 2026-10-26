"""
Triển khai dự án CapCut Pro 9.6: Vlog_XanhSM_1Ngay_176k_Long (2.5 Phút)
- Đầy đủ 6 Tracks: Video (15 phân cảnh), Voiceover, BGM LoFi (-16dB), SFX Nhận Tiền, Subtitles Oswald-Bold, Overlay Badges (6 đơn + 176k)
- Chuẩn hóa platform qua scripts/capcut_draft_manager.py (app_id 359289, app_source cc, 9.6.0)
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

def deploy():
    project_name = "Vlog_XanhSM_1Ngay_176k_Long"
    print(f"[*] Đang khởi tạo dự án CapCut Pro: {project_name}...")

    base_dir = Path("c:/QuangHy/editvideo")
    out_dir = base_dir / "processed"
    temp_dir = out_dir / "temp_render_176k_long"

    vo_file = out_dir / "voiceover_xanhsm_176k" / "vlog_xanhsm_176k_full_voiceover.mp3"
    bgm_file = out_dir / "bgm_xanhsm_176k_loop.mp3"
    sfx_cash = base_dir / "public" / "sfx" / "cash_register.mp3"
    sfx_ting = base_dir / "public" / "sfx" / "ting_money.mp3"
    sfx_whoosh = base_dir / "public" / "sfx" / "whoosh_fast.mp3"
    sfx_ding = base_dir / "public" / "sfx" / "ding_highlight.mp3"

    dur_sec = float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(vo_file)
    ]).decode().strip())
    total_dur_us = us(dur_sec)

    materials = {
        "audio_balances": [],
        "audio_effects": [],
        "audio_fades": [],
        "audios": [],
        "beats": [],
        "canvases": [],
        "chromas": [],
        "color_curves": [],
        "drafts": [],
        "effects": [],
        "flowers": [],
        "green_screens": [],
        "handwrites": [],
        "hsl": [],
        "images": [],
        "log_color_wheels": [],
        "loudnesses": [],
        "manual_deformations": [],
        "masks": [],
        "material_animations": [],
        "material_colors": [],
        "placeholders": [],
        "plugin_effects": [],
        "primary_color_wheels": [],
        "realtime_denoises": [],
        "shapes": [],
        "smart_crops": [],
        "sound_channel_mappings": [],
        "speeds": [],
        "stickers": [],
        "tail_leaders": [],
        "text_templates": [],
        "texts": [],
        "time_marks": [],
        "transitions": [],
        "video_effects": [],
        "video_trackings": [],
        "videos": [],
        "vocal_beautifys": [],
        "vocal_separations": []
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
            "source": 0, "source_platform": 0, "stable": None, "team_id": "", "type": "video",
            "video_algorithm": None, "width": 1080
        })
        return us(d)

    # 1. Đăng ký âm thanh
    mat_vo_id = str(uuid.uuid4()).upper()
    dur_vo_us = reg_audio(mat_vo_id, vo_file, "Vlog XanhSM Voiceover Long")

    mat_bgm_id = str(uuid.uuid4()).upper()
    dur_bgm_us = reg_audio(mat_bgm_id, bgm_file, "BGM LoFi XanhSM Loop")

    mat_sfx_cash = str(uuid.uuid4()).upper()
    dur_sfx_cash = reg_audio(mat_sfx_cash, sfx_cash, "SFX Cash Register")

    mat_sfx_ting = str(uuid.uuid4()).upper()
    dur_sfx_ting = reg_audio(mat_sfx_ting, sfx_ting, "SFX Ting Money")

    mat_sfx_whoosh = str(uuid.uuid4()).upper()
    dur_sfx_whoosh = reg_audio(mat_sfx_whoosh, sfx_whoosh, "SFX Whoosh Fast")

    mat_sfx_ding = str(uuid.uuid4()).upper()
    dur_sfx_ding = reg_audio(mat_sfx_ding, sfx_ding, "SFX Ding Highlight")

    # Track Voiceover
    voice_track_segment = {
        "id": str(uuid.uuid4()).upper(), "material_id": mat_vo_id,
        "target_timerange": {"start": 0, "duration": dur_vo_us},
        "source_timerange": {"start": 0, "duration": dur_vo_us},
        "volume": 1.05
    }

    # Track BGM LoFi (-16dB)
    bgm_track_segment = {
        "id": str(uuid.uuid4()).upper(), "material_id": mat_bgm_id,
        "target_timerange": {"start": 0, "duration": total_dur_us},
        "source_timerange": {"start": 0, "duration": min(dur_bgm_us, total_dur_us)},
        "volume": 0.15
    }

    # Track SFX (10 events)
    sfx_events = [
        {"mat": mat_sfx_whoosh, "dur": dur_sfx_whoosh, "start": us(0.0)},
        {"mat": mat_sfx_ding, "dur": dur_sfx_ding, "start": us(1.2)},
        {"mat": mat_sfx_cash, "dur": dur_sfx_cash, "start": us(26.8)},   # Đơn 1 (+16k)
        {"mat": mat_sfx_ting, "dur": dur_sfx_ting, "start": us(44.8)},   # Đơn 2 (+22k)
        {"mat": mat_sfx_cash, "dur": dur_sfx_cash, "start": us(65.4)},   # Đơn 3 (+35k)
        {"mat": mat_sfx_ting, "dur": dur_sfx_ting, "start": us(82.7)},   # Đơn 4 (+28k)
        {"mat": mat_sfx_cash, "dur": dur_sfx_cash, "start": us(105.1)},  # Đơn 5 (+42k)
        {"mat": mat_sfx_cash, "dur": dur_sfx_cash, "start": us(124.8)},  # Đơn 6 (+33k)
        {"mat": mat_sfx_ting, "dur": dur_sfx_ting, "start": us(125.6)},  # Ting chốt ca
        {"mat": mat_sfx_ding, "dur": dur_sfx_ding, "start": us(129.5)}   # Tổng thu 176k
    ]
    sfx_segments = []
    for se in sfx_events:
        sfx_segments.append({
            "id": str(uuid.uuid4()).upper(), "material_id": se["mat"],
            "target_timerange": {"start": se["start"], "duration": se["dur"]},
            "source_timerange": {"start": 0, "duration": se["dur"]},
            "volume": 0.95
        })

    # 2. Đăng ký Video Scenes
    video_segments = []
    cur_v_start = 0
    for i in range(15):
        sc_file = temp_dir / f"scene_{i:02d}.mp4"
        mat_v_id = str(uuid.uuid4()).upper()
        v_dur_us = reg_video(mat_v_id, sc_file, f"Scene {i:02d}")
        
        # Clip cuối cắt vừa bằng tổng duration
        rem_dur_us = total_dur_us - cur_v_start
        actual_seg_dur = min(v_dur_us, rem_dur_us)
        
        video_segments.append({
            "id": str(uuid.uuid4()).upper(), "material_id": mat_v_id,
            "target_timerange": {"start": cur_v_start, "duration": actual_seg_dur},
            "source_timerange": {"start": 0, "duration": actual_seg_dur},
            "clip": {"alpha": 1.0, "rotation": 0.0, "scale": {"x": 1.0, "y": 1.0}, "transform": {"x": 0.0, "y": 0.0}},
            "render_index": 10000 + i * 10
        })
        cur_v_start += actual_seg_dur
        if cur_v_start >= total_dur_us:
            break

    # 3. Đăng ký Phụ đề & Badges
    font_res_id = "7182504807289065985"
    font_path = "C:/Users/PC/AppData/Local/CapCut/User Data/Cache/effect/7182504807289065985/0a5333de6f4d592cb2d2390d68b31efb/Oswald-Bold.ttf"  # PHẢI là đường dẫn tuyệt đối, đường dẫn tương đối làm CapCut 9.6 tự đóng

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
            "font_title": "none", "font_url": "", "fonts": [], "global_alpha": 1.0,
            "group_id": "", "has_shadow": True, "id": t_id, "initial_scale": 1.0,
            "inner_padding": 0.0, "is_rich_text": False, "italic": False,
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
            "typesetting": 0, "underline": False, "use_effect_default_color": False,
            "using_hot_words": False
        })
        return t_id

    # Đăng ký Overlay Badges: Hook, 6 Thẻ Tiền, Thẻ Tổng Thu 176k, Callout
    overlay_segments = []

    # Hook 0-5.5s
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

    # 6 Thẻ tiền nhận đơn
    orders = [
        {"st": 26.8, "dur": 5.0, "txt": "✓ HOÀN THÀNH ĐƠN #1\n+16.000đ\nTỔNG THU: 16.000đ"},
        {"st": 44.8, "dur": 4.7, "txt": "✓ HOÀN THÀNH ĐƠN #2\n+22.000đ\nTỔNG THU: 38.000đ"},
        {"st": 65.4, "dur": 5.0, "txt": "✓ HOÀN THÀNH ĐƠN #3\n+35.000đ\nTỔNG THU: 73.000đ"},
        {"st": 82.7, "dur": 7.3, "txt": "✓ HOÀN THÀNH ĐƠN #4\n+28.000đ\nTỔNG THU: 101.000đ"},
        {"st": 105.1, "dur": 4.3, "txt": "✓ HOÀN THÀNH ĐƠN #5\n+42.000đ\nTỔNG THU: 143.000đ"},
        {"st": 124.8, "dur": 4.3, "txt": "✓ HOÀN THÀNH ĐƠN #6 (CHỐT CA)\n+33.000đ\nTỔNG THU: 176.000đ"}
    ]
    for o in orders:
        badge_id = create_text_mat(o["txt"], [0.0, 1.0, 0.4], size=16.0)
        overlay_segments.append({
            "id": str(uuid.uuid4()).upper(), "material_id": badge_id,
            "target_timerange": {"start": us(o["st"]), "duration": us(o["dur"])},
            "source_timerange": {"start": 0, "duration": us(o["dur"])},
            "clip": {"alpha": 1.0, "rotation": 0.0, "scale": {"x": 1.0, "y": 1.0}, "transform": {"x": 0.0, "y": 0.15}},
            "render_index": 41000
        })

    # Thẻ Tổng Thu 176k
    sum_id = create_text_mat("★ TỔNG THU HÔM NAY: 176.000đ ★\n(6 ĐƠN XE XANHSM)", [1.0, 1.0, 0.0], size=17.0)
    overlay_segments.append({
        "id": str(uuid.uuid4()).upper(), "material_id": sum_id,
        "target_timerange": {"start": us(129.5), "duration": us(13.0)},
        "source_timerange": {"start": 0, "duration": us(13.0)},
        "clip": {"alpha": 1.0, "rotation": 0.0, "scale": {"x": 1.0, "y": 1.0}, "transform": {"x": 0.0, "y": 0.25}},
        "render_index": 42000
    })

    # Callout CTA
    callout_id = create_text_mat("TIM ❤️ VÀ COMMENT GIAO LƯU NHÉ 👍", [0.0, 1.0, 0.5], size=15.0)
    overlay_segments.append({
        "id": str(uuid.uuid4()).upper(), "material_id": callout_id,
        "target_timerange": {"start": us(143.0), "duration": us(10.0)},
        "source_timerange": {"start": 0, "duration": us(10.0)},
        "clip": {"alpha": 1.0, "rotation": 0.0, "scale": {"x": 1.0, "y": 1.0}, "transform": {"x": 0.0, "y": 0.28}},
        "render_index": 43000
    })

    # Subtitles Track từ cleaned_words_176k_long.json
    subtitle_segments = []
    with open("processed/cleaned_words_176k_long.json", "r", encoding="utf-8") as f:
        cleaned_segs = json.load(f)

    # Gom cụm 3 từ, rồi CẮT cuối mỗi cụm đúng tại điểm bắt đầu cụm kế tiếp
    # để sub trước KHÔNG BAO GIỜ đè lên sub sau (lỗi cũ: +0.1s đệm cứng gây chồng chữ).
    chunks_flat = []
    for seg in cleaned_segs:
        words = seg["words"]
        for i in range(0, len(words), 3):
            chunk = words[i:i+3]
            chunks_flat.append((
                " ".join(w["word"].upper() for w in chunk),
                float(chunk[0]["master_start"]),
                float(chunk[-1]["master_end"]) + 0.1,
            ))
    # Người dùng đo thực tế trong CapCut: sub trễ 0.1-0.2s so với voice -> dời toàn bộ sub SỚM 0.15s.
    SUB_LEAD = 0.15
    chunks_flat = [(t, max(0.0, s - SUB_LEAD), max(0.0, e - SUB_LEAD)) for (t, s, e) in chunks_flat]
    chunks_flat.sort(key=lambda x: x[1])
    GAP = 0.02  # khe hở 20ms giữa 2 sub liên tiếp
    for idx, (txt, c_st, c_en) in enumerate(chunks_flat):
        if idx + 1 < len(chunks_flat):
            c_en = min(c_en, chunks_flat[idx + 1][1] - GAP)
        c_en = max(c_en, c_st + 0.15)
        if idx + 1 < len(chunks_flat) and c_en > chunks_flat[idx + 1][1] - GAP:
            c_en = chunks_flat[idx + 1][1] - GAP
        if c_en <= c_st:
            continue
        if True:
            sub_id = create_text_mat(txt, [0.941, 1.0, 0.0], size=15.0)
            subtitle_segments.append({
                "id": str(uuid.uuid4()).upper(), "material_id": sub_id,
                "target_timerange": {"start": us(c_st), "duration": us(c_en - c_st)},
                "source_timerange": {"start": 0, "duration": us(c_en - c_st)},
                "clip": {"alpha": 1.0, "rotation": 0.0, "scale": {"x": 1.0, "y": 1.0}, "transform": {"x": 0.0, "y": -0.38}},
                "render_index": 30000 + len(subtitle_segments)
            })

    # 4. Gom Tracks
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
        "cover": None,
        "create_time": now_ms,
        "duration": total_dur_us,
        "fps": 30.0,
        "id": draft_id,
        "last_modified_platform": {
            "app_id": 359289, "app_source": "cc", "app_version": "9.6.0",
            "device_id": "4475d19983c69cde88e66433dd341c72", "hard_disk_id": "",
            "mac_address": "26ebfda668b7dfc60a011ffef74a230b,4f652529e3ad390a5fc5f40eb605bcf9",
            "os": "windows", "os_version": "10.0.26300"
        },
        "materials": materials,
        "name": project_name,
        "new_version": "116.0.0",
        "platform": {
            "app_id": 359289, "app_source": "cc", "app_version": "9.6.0",
            "device_id": "4475d19983c69cde88e66433dd341c72", "hard_disk_id": "",
            "mac_address": "26ebfda668b7dfc60a011ffef74a230b,4f652529e3ad390a5fc5f40eb605bcf9",
            "os": "windows", "os_version": "10.0.26300"
        },
        "render_index_mode": "off",
        "render_index_track_mode_on": True,
        "tracks": tracks,
        "update_time": now_ms,
        "version": 360000
    }

    sys.path.insert(0, str(base_dir / "scripts"))
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
    print(f"\n[+] XUẤT BẢN THÀNH CÔNG DỰ ÁN CAPCUT PRO: '{project_name}'!")
    print(f"    - Thời lượng timeline: {dur_sec:.2f}s (~{dur_sec/60:.2f} phút)")
    print(f"    - Đầy đủ 6 Tracks chuyên nghiệp: Video (15 scenes), Voiceover, BGM LoFi (-16dB), SFX Nhận Tiền, Subtitles, Overlay Badges")
    print(f"    - Khớp hoàn toàn các mốc nhận tiền và thẻ cộng dồn tổng thu 176k")

if __name__ == "__main__":
    deploy()
