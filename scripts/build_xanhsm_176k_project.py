"""
Build toàn diện Vlog XanhSM 1 Ngày Chạy Xe (Tổng thu 176k) cho CapCut Desktop Pro:
- Voiceover: OmniVoice Voice Clone (train từ ref_sample_hook.wav)
- Subtitles: 58 Short Phrases (2-4 từ/cụm) theo đúng ảnh huấn luyện của người dùng
- Font: Oswald-Bold, IN HOA, màu vàng chanh #F0FF00, viền đen dày, Safe Zone Y=-0.38
- 6 Thẻ tiền nhận đơn (+16k, +22k, +35k, +28k, +42k, +33k) & Thẻ tổng cộng dồn (Tổng thu 176k)
- SFX Nhận tiền: Cash Register & Ting Ting nổ đúng mili-giây nhận đơn
- BGM LoFi loop âm lượng -16dB
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
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

def us(seconds: float) -> int:
    return int(round(seconds * 1_000_000))

def build_xanhsm_176k_capcut_project(project_name: str = "Vlog_XanhSM_1Ngay_176k"):
    print(f"[*] Bắt đầu khởi tạo dự án CapCut Pro: {project_name}")

    local_app_data = os.environ.get("LOCALAPPDATA", r"C:\Users\PC\AppData\Local")
    capcut_draft_dir = Path(local_app_data) / "CapCut" / "User Data" / "Projects" / "com.lveditor.draft"
    target_project_dir = capcut_draft_dir / project_name
    target_project_dir.mkdir(parents=True, exist_ok=True)
    
    assets_audio_dir = target_project_dir / "assets" / "audio"
    assets_audio_dir.mkdir(parents=True, exist_ok=True)

    # 1. Đồng bộ file âm thanh nội bộ CapCut
    src_voice = Path("processed/voiceover_omnivoice_176k/vlog_xanhsm_176k_omnivoice_master.mp3")
    dst_voice = assets_audio_dir / "omnivoice_master.mp3"
    shutil.copy2(src_voice, dst_voice)

    src_bgm = Path("processed/bgm_xanhsm_176k_loop.mp3")
    dst_bgm = assets_audio_dir / "bgm_lofi.mp3"
    shutil.copy2(src_bgm, dst_bgm)

    src_sfx_cash = Path("public/sfx/cash_register.mp3")
    dst_sfx_cash = assets_audio_dir / "sfx_cash.mp3"
    shutil.copy2(src_sfx_cash, dst_sfx_cash)

    src_sfx_ting = Path("public/sfx/ting_money.mp3")
    dst_sfx_ting = assets_audio_dir / "sfx_ting.mp3"
    shutil.copy2(src_sfx_ting, dst_sfx_ting)

    src_sfx_whoosh = Path("public/sfx/whoosh_fast.mp3")
    dst_sfx_whoosh = assets_audio_dir / "sfx_whoosh.mp3"
    shutil.copy2(src_sfx_whoosh, dst_sfx_whoosh)

    src_sfx_ding = Path("public/sfx/ding_highlight.mp3")
    dst_sfx_ding = assets_audio_dir / "sfx_ding.mp3"
    shutil.copy2(src_sfx_ding, dst_sfx_ding)

    # Đo độ dài chính xác của voiceover
    total_duration_sec = float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(dst_voice)
    ]).decode().strip())
    total_duration_us = us(total_duration_sec)
    print(f"[+] Thời lượng Voiceover OmniVoice: {total_duration_sec:.2f}s ({total_duration_us} us)")

    with open("processed/dynamic_karaoke_176k.json", "r", encoding="utf-8") as f:
        short_phrases = json.load(f)

    # 2. Khởi tạo Materials
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

    # 3. Đăng ký âm thanh
    def register_audio(mat_id, path_obj, name):
        dur = float(subprocess.check_output([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(path_obj)
        ]).decode().strip())
        materials["audios"].append({
            "app_id": 0,
            "category_id": "",
            "category_name": "",
            "check_flag": 1,
            "duration": us(dur),
            "effect_id": "",
            "formula_id": "",
            "id": mat_id,
            "intensifies_path": "",
            "local_material_id": "",
            "music_id": str(uuid.uuid4()),
            "name": name,
            "path": str(path_obj.resolve()),
            "query": "",
            "resource_id": "",
            "search_id": "",
            "source_platform": 0,
            "team_id": "",
            "text_id": "",
            "tone_category_id": "",
            "tone_category_name": "",
            "tone_effect_id": "",
            "tone_effect_name": "",
            "tone_speaker": "",
            "tone_type": "",
            "type": "extract_music",
            "video_id": "",
            "wave_points": []
        })
        return us(dur)

    mat_vo_id = str(uuid.uuid4()).upper()
    register_audio(mat_vo_id, dst_voice, "Vlog XanhSM OmniVoice Master")

    mat_bgm_id = str(uuid.uuid4()).upper()
    register_audio(mat_bgm_id, dst_bgm, "BGM LoFi Relax")

    mat_sfx_cash_id = str(uuid.uuid4()).upper()
    register_audio(mat_sfx_cash_id, dst_sfx_cash, "SFX Cash Register")

    mat_sfx_ting_id = str(uuid.uuid4()).upper()
    register_audio(mat_sfx_ting_id, dst_sfx_ting, "SFX Ting Ting Money")

    mat_sfx_whoosh_id = str(uuid.uuid4()).upper()
    register_audio(mat_sfx_whoosh_id, dst_sfx_whoosh, "SFX Fast Whoosh")

    mat_sfx_ding_id = str(uuid.uuid4()).upper()
    register_audio(mat_sfx_ding_id, dst_sfx_ding, "SFX Ding Highlight")

    # 4. Đăng ký 3 Video Footage
    footage_map = {
        "morning": Path("raw_footage/DJI_20260908084243_0057_D.MP4").resolve(),
        "rush_hour": Path("raw_footage/DJI_20260908183824_0062_D.MP4").resolve(),
        "night": Path("raw_footage/DJI_20260908185603_0064_D.MP4").resolve()
    }
    video_mat_ids = {}
    for key, fpath in footage_map.items():
        v_id = str(uuid.uuid4()).upper()
        dur = float(subprocess.check_output([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(fpath)
        ]).decode().strip())
        materials["videos"].append({
            "audio_fade": None,
            "category_id": "",
            "category_name": "",
            "check_flag": 63487,
            "crop": {"lower_left_x": 0.0, "lower_left_y": 1.0, "lower_right_x": 1.0, "lower_right_y": 1.0, "upper_left_x": 0.0, "upper_left_y": 0.0, "upper_right_x": 1.0, "upper_right_y": 0.0},
            "crop_ratio": "free",
            "crop_scale": 1.0,
            "duration": us(dur),
            "extra_type": "option_video",
            "formula_id": "",
            "freeze": None,
            "has_audio": True,
            "height": 1512,
            "id": v_id,
            "intensifies_audio_path": "",
            "intensifies_path": "",
            "is_ai_generate_content": False,
            "is_placeholder": False,
            "local_id": "",
            "material_name": fpath.name,
            "material_url": "",
            "matting": {"flag": 0, "has_handled": False, "interactive_segments": []},
            "media_path": "",
            "object_locked": None,
            "origin_material_id": "",
            "path": str(fpath),
            "reverse_intensifies_path": "",
            "reverse_path": "",
            "smart_motion": None,
            "source": 0,
            "source_platform": 0,
            "team_id": "",
            "type": "video",
            "video_algorithm": {"algorithms": []},
            "width": 2688
        })
        video_mat_ids[key] = v_id

    # 5. Xây dựng 17 Video Cuts khớp chính xác 3 ca
    cut_definitions = [
        # --- CA SÁNG (0.0s -> 31.5s) ---
        {"type": "morning", "src_st": 0.0, "dur": 6.0},
        {"type": "morning", "src_st": 6.0, "dur": 4.5},
        {"type": "morning", "src_st": 10.5, "dur": 4.5},
        {"type": "morning", "src_st": 15.0, "dur": 6.5},
        {"type": "morning", "src_st": 21.5, "dur": 5.5},
        {"type": "morning", "src_st": 27.0, "dur": 4.5},
        # --- CA CHIỀU / TAN TẦM (31.5s -> 56.5s) ---
        {"type": "rush_hour", "src_st": 0.0, "dur": 5.0},
        {"type": "rush_hour", "src_st": 10.0, "dur": 5.5},
        {"type": "rush_hour", "src_st": 22.0, "dur": 4.5},
        {"type": "rush_hour", "src_st": 26.5, "dur": 5.0},
        {"type": "rush_hour", "src_st": 37.0, "dur": 5.0},
        # --- CA ĐÊM / PHỐ LÊN ĐÈN (56.5s -> 88.0s) ---
        {"type": "night", "src_st": 0.0, "dur": 5.5},
        {"type": "night", "src_st": 10.0, "dur": 5.5},
        {"type": "night", "src_st": 18.5, "dur": 5.0},
        {"type": "night", "src_st": 29.0, "dur": 5.5},
        {"type": "night", "src_st": 38.0, "dur": 5.0},
        {"type": "night", "src_st": 51.0, "dur": 5.0}
    ]

    video_segments = []
    curr_target_time = 0
    for idx, cut in enumerate(cut_definitions):
        c_dur_us = us(cut["dur"])
        if curr_target_time + c_dur_us > total_duration_us:
            c_dur_us = total_duration_us - curr_target_time

        video_segments.append({
            "id": str(uuid.uuid4()).upper(),
            "material_id": video_mat_ids[cut["type"]],
            "target_timerange": {"start": curr_target_time, "duration": c_dur_us},
            "source_timerange": {"start": us(cut["src_st"]), "duration": c_dur_us},
            "speed": 1.0,
            "volume": 0.0, # Tắt âm thanh camera gốc để tránh lẫn tạp âm
            "visible": True,
            "clip": {
                "alpha": 1.0,
                "flip": {"horizontal": False, "vertical": False},
                "rotation": 90.0, # Xoay 90 độ camera Action DJI
                "scale": {"x": 1.95, "y": 1.95}, # Zoom 1.95x lấp đầy 9:16 dọc
                "transform": {"x": 0.0, "y": 0.0}
            },
            "render_index": 10000 + idx
        })
        curr_target_time += c_dur_us
        if curr_target_time >= total_duration_us:
            break

    # 6. Audio Track Voiceover & BGM
    voice_track_segment = {
        "id": str(uuid.uuid4()).upper(),
        "material_id": mat_vo_id,
        "target_timerange": {"start": 0, "duration": total_duration_us},
        "source_timerange": {"start": 0, "duration": total_duration_us},
        "speed": 1.0,
        "volume": 1.0,
        "visible": True,
        "render_index": 20000
    }

    bgm_track_segment = {
        "id": str(uuid.uuid4()).upper(),
        "material_id": mat_bgm_id,
        "target_timerange": {"start": 0, "duration": total_duration_us},
        "source_timerange": {"start": 0, "duration": total_duration_us},
        "speed": 1.0,
        "volume": 0.16,
        "visible": True,
        "render_index": 21000
    }

    # 7. Sound Effects Track (SFX Nhận Tiền & Hook)
    sfx_segments = []
    # Hook SFX
    sfx_segments.append({
        "id": str(uuid.uuid4()).upper(), "material_id": mat_sfx_whoosh_id,
        "target_timerange": {"start": 0, "duration": us(0.5)},
        "source_timerange": {"start": 0, "duration": us(0.5)},
        "speed": 1.0, "volume": 0.7, "visible": True, "render_index": 22001
    })
    sfx_segments.append({
        "id": str(uuid.uuid4()).upper(), "material_id": mat_sfx_ding_id,
        "target_timerange": {"start": us(1.2), "duration": us(0.8)},
        "source_timerange": {"start": 0, "duration": us(0.8)},
        "speed": 1.0, "volume": 0.8, "visible": True, "render_index": 22002
    })

    # SFX Nhận tiền 6 đơn & Tổng kết 176k
    cash_events = [
        {"time": 19.2, "mat": mat_sfx_cash_id, "vol": 0.95}, # Đơn 1 (+16k)
        {"time": 29.5, "mat": mat_sfx_ting_id, "vol": 1.0},  # Đơn 2 (+22k)
        {"time": 39.5, "mat": mat_sfx_cash_id, "vol": 0.95}, # Đơn 3 (+35k)
        {"time": 49.5, "mat": mat_sfx_ting_id, "vol": 1.0},  # Đơn 4 (+28k)
        {"time": 59.8, "mat": mat_sfx_cash_id, "vol": 0.95}, # Đơn 5 (+42k)
        {"time": 69.5, "mat": mat_sfx_cash_id, "vol": 1.0},  # Đơn 6 (+33k)
        {"time": 74.2, "mat": mat_sfx_ting_id, "vol": 1.0}   # Tổng kết 176k
    ]
    for idx, ce in enumerate(cash_events):
        sfx_segments.append({
            "id": str(uuid.uuid4()).upper(),
            "material_id": ce["mat"],
            "target_timerange": {"start": us(ce["time"]), "duration": us(1.2)},
            "source_timerange": {"start": 0, "duration": us(1.2)},
            "speed": 1.0, "volume": ce["vol"], "visible": True, "render_index": 22010 + idx
        })

    # 8. Phụ đề tiếng Việt: 58 Short Phrases (2-4 từ/cụm) theo đúng ảnh huấn luyện
    from capcut_draft_manager import OSWALD_CAPCUT_FONT, _resolve_font_abs
    font_path_oswald = _resolve_font_abs(OSWALD_CAPCUT_FONT)
    if not os.path.exists(font_path_oswald):
        font_path_oswald = "C:/Windows/Fonts/arialbd.ttf"
    oswald_resource_id = "7182504807289065985"

    subtitle_segments = []
    for idx, p in enumerate(short_phrases):
        txt_mat_id = str(uuid.uuid4()).upper()
        p_text = p["text"].upper()
        p_dur = max(0.4, p["end"] - p["start"])
        
        # Style Vàng Chanh #F0FF00 viền đen dày, Oswald-Bold
        text_mat = {
            "id": txt_mat_id,
            "type": "text",
            "content": json.dumps({
                "styles": [{
                    "fill": {"alpha": 1.0, "content": {"render_type": "solid", "solid": {"alpha": 1.0, "color": [0.941, 1.0, 0.0]}}},
                    "font": {"id": oswald_resource_id, "path": font_path_oswald},
                    "size": 15.0,
                    "range": [0, len(p_text)],
                    "strokes": [{
                        "alpha": 1.0,
                        "content": {"render_type": "solid", "solid": {"alpha": 1.0, "color": [0.0, 0.0, 0.0]}},
                        "width": 0.09
                    }]
                }],
                "text": p_text
            }, ensure_ascii=False),
            "font_size": 15.0,
            "font_title": "Oswald-Bold",
            "border_color": "#000000",
            "border_width": 0.09,
            "has_shadow": True,
            "shadow_color": "#000000",
            "shadow_alpha": 0.9,
            "text_color": "#f0ff00"
        }
        materials["texts"].append(text_mat)

        subtitle_segments.append({
            "id": str(uuid.uuid4()).upper(),
            "material_id": txt_mat_id,
            "target_timerange": {"start": us(p["start"]), "duration": us(p_dur)},
            "source_timerange": {"start": 0, "duration": us(p_dur)},
            "clip": {
                "alpha": 1.0, "rotation": 0.0, "scale": {"x": 1.0, "y": 1.0},
                "transform": {"x": 0.0, "y": -0.38} # Chuẩn Safe Zone ngang ngực
            },
            "render_index": 30000 + idx
        })

    # 9. Track Tiêu đề Hook 2 Tầng + 6 Thẻ Tiền Hoàn Thành Đơn + Tổng Thu 176k
    overlay_segments = []

    # HOOK 2 TẦNG (0s -> 5.5s)
    hook1_id = str(uuid.uuid4()).upper()
    materials["texts"].append({
        "id": hook1_id, "type": "text",
        "content": json.dumps({
            "styles": [{
                "fill": {"alpha": 1.0, "content": {"render_type": "solid", "solid": {"alpha": 1.0, "color": [1.0, 0.2, 0.2]}}},
                "font": {"id": oswald_resource_id, "path": font_path_oswald},
                "size": 15.0,
                "strokes": [{"alpha": 1.0, "content": {"render_type": "solid", "solid": {"alpha": 1.0, "color": [1.0, 1.0, 1.0]}}, "width": 0.08}]
            }],
            "text": "THỬ THÁCH 1 NGÀY"
        }, ensure_ascii=False),
        "font_size": 15.0, "border_color": "#FFFFFF", "border_width": 0.08, "has_shadow": True
    })
    overlay_segments.append({
        "id": str(uuid.uuid4()).upper(), "material_id": hook1_id,
        "target_timerange": {"start": 0, "duration": us(5.5)},
        "source_timerange": {"start": 0, "duration": us(5.5)},
        "clip": {"alpha": 1.0, "rotation": 0.0, "scale": {"x": 1.0, "y": 1.0}, "transform": {"x": 0.0, "y": 0.55}},
        "render_index": 40001
    })

    hook2_id = str(uuid.uuid4()).upper()
    materials["texts"].append({
        "id": hook2_id, "type": "text",
        "content": json.dumps({
            "styles": [{
                "fill": {"alpha": 1.0, "content": {"render_type": "solid", "solid": {"alpha": 1.0, "color": [0.94, 1.0, 0.0]}}},
                "font": {"id": oswald_resource_id, "path": font_path_oswald},
                "size": 17.5,
                "strokes": [{"alpha": 1.0, "content": {"render_type": "solid", "solid": {"alpha": 1.0, "color": [0.0, 0.0, 0.0]}}, "width": 0.10}]
            }],
            "text": "CHẠY XE XANH SM"
        }, ensure_ascii=False),
        "font_size": 17.5, "border_color": "#000000", "border_width": 0.10, "has_shadow": True
    })
    overlay_segments.append({
        "id": str(uuid.uuid4()).upper(), "material_id": hook2_id,
        "target_timerange": {"start": 0, "duration": us(5.5)},
        "source_timerange": {"start": 0, "duration": us(5.5)},
        "clip": {"alpha": 1.0, "rotation": 0.0, "scale": {"x": 1.0, "y": 1.0}, "transform": {"x": 0.0, "y": 0.42}},
        "render_index": 40002
    })

    # 6 THẺ TIỀN NHẬN ĐƠN
    orders_info = [
        {"order": 1, "st": 19.2, "dur": 3.3, "amt": "+16.000đ", "total": "TỔNG THU: 16.000đ"},
        {"order": 2, "st": 29.5, "dur": 3.3, "amt": "+22.000đ", "total": "TỔNG THU: 38.000đ"},
        {"order": 3, "st": 39.5, "dur": 3.5, "amt": "+35.000đ", "total": "TỔNG THU: 73.000đ"},
        {"order": 4, "st": 49.5, "dur": 3.5, "amt": "+28.000đ", "total": "TỔNG THU: 101.000đ"},
        {"order": 5, "st": 59.8, "dur": 3.4, "amt": "+42.000đ", "total": "TỔNG THU: 143.000đ"},
        {"order": 6, "st": 69.5, "dur": 4.5, "amt": "+33.000đ", "total": "TỔNG THU: 176.000đ"}
    ]

    for o in orders_info:
        card_id = str(uuid.uuid4()).upper()
        materials["texts"].append({
            "id": card_id, "type": "text",
            "content": json.dumps({
                "styles": [{
                    "fill": {"alpha": 1.0, "content": {"render_type": "solid", "solid": {"alpha": 1.0, "color": [0.0, 1.0, 0.4]}}},
                    "font": {"id": oswald_resource_id, "path": font_path_oswald},
                    "size": 19.0,
                    "strokes": [{"alpha": 1.0, "content": {"render_type": "solid", "solid": {"alpha": 1.0, "color": [0.0, 0.0, 0.0]}}, "width": 0.12}]
                }],
                "text": f"HOÀN THÀNH ĐƠN #{o['order']}: {o['amt']}\n{o['total']}"
            }, ensure_ascii=False),
            "font_size": 19.0, "border_color": "#000000", "border_width": 0.12, "has_shadow": True
        })

        overlay_segments.append({
            "id": str(uuid.uuid4()).upper(), "material_id": card_id,
            "target_timerange": {"start": us(o["st"]), "duration": us(o["dur"])},
            "source_timerange": {"start": 0, "duration": us(o["dur"])},
            "clip": {"alpha": 1.0, "rotation": 0.0, "scale": {"x": 1.0, "y": 1.0}, "transform": {"x": 0.0, "y": 0.18}},
            "render_index": 41000 + o["order"]
        })

    # THẺ TỔNG KẾT 176K (74.2s -> 78.5s)
    summary_card_id = str(uuid.uuid4()).upper()
    materials["texts"].append({
        "id": summary_card_id, "type": "text",
        "content": json.dumps({
            "styles": [{
                "fill": {"alpha": 1.0, "content": {"render_type": "solid", "solid": {"alpha": 1.0, "color": [1.0, 0.95, 0.0]}}},
                "font": {"id": oswald_resource_id, "path": font_path_oswald},
                "size": 21.0,
                "strokes": [{"alpha": 1.0, "content": {"render_type": "solid", "solid": {"alpha": 1.0, "color": [0.0, 0.0, 0.0]}}, "width": 0.12}]
            }],
            "text": "★ TỔNG THU HÔM NAY: 176.000đ ★\n(6 ĐƠN XE XANHSM)"
        }, ensure_ascii=False),
        "font_size": 21.0, "border_color": "#000000", "border_width": 0.12, "has_shadow": True
    })
    overlay_segments.append({
        "id": str(uuid.uuid4()).upper(), "material_id": summary_card_id,
        "target_timerange": {"start": us(74.2), "duration": us(4.5)},
        "source_timerange": {"start": 0, "duration": us(4.5)},
        "clip": {"alpha": 1.0, "rotation": 0.0, "scale": {"x": 1.0, "y": 1.0}, "transform": {"x": 0.0, "y": 0.22}},
        "render_index": 42000
    })

    # CALLOUT TƯƠNG TÁC
    cta_id = str(uuid.uuid4()).upper()
    materials["texts"].append({
        "id": cta_id, "type": "text",
        "content": json.dumps({
            "styles": [{
                "fill": {"alpha": 1.0, "content": {"render_type": "solid", "solid": {"alpha": 1.0, "color": [0.0, 1.0, 0.6]}}},
                "font": {"id": oswald_resource_id, "path": font_path_oswald},
                "size": 14.0,
                "strokes": [{"alpha": 1.0, "content": {"render_type": "solid", "solid": {"alpha": 1.0, "color": [0.0, 0.0, 0.0]}}, "width": 0.08}]
            }],
            "text": "TIM 💚 VÀ ĐỂ LẠI BÌNH LUẬN NHÉ!"
        }, ensure_ascii=False),
        "font_size": 14.0, "border_color": "#000000", "border_width": 0.08, "has_shadow": True
    })
    overlay_segments.append({
        "id": str(uuid.uuid4()).upper(), "material_id": cta_id,
        "target_timerange": {"start": us(83.0), "duration": us(5.0)},
        "source_timerange": {"start": 0, "duration": us(5.0)},
        "clip": {"alpha": 1.0, "rotation": 0.0, "scale": {"x": 1.0, "y": 1.0}, "transform": {"x": 0.0, "y": 0.05}},
        "render_index": 43000
    })

    # 10. Gom cấu trúc Tracks
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
            "adjust_max_index": 1,
            "lyrics_sync": True,
            "maintrack_adsorb": True,
            "material_save_mode": 0,
            "subtitle_sync": True,
            "system_font_list": [],
            "video_mute": False
        },
        "cover": None,
        "create_time": now_ms,
        "duration": total_duration_us,
        "fps": 30.0,
        "id": draft_id,
        "last_modified_platform": {
            "app_id": 359289,
            "app_source": "cc",
            "app_version": "9.6.0",
            "device_id": "4475d19983c69cde88e66433dd341c72",
            "hard_disk_id": "",
            "mac_address": "26ebfda668b7dfc60a011ffef74a230b,4f652529e3ad390a5fc5f40eb605bcf9",
            "os": "windows",
            "os_version": "10.0.26300"
        },
        "materials": materials,
        "name": project_name,
        "new_version": "116.0.0",
        "platform": {
            "app_id": 359289,
            "app_source": "cc",
            "app_version": "9.6.0",
            "device_id": "4475d19983c69cde88e66433dd341c72",
            "hard_disk_id": "",
            "mac_address": "26ebfda668b7dfc60a011ffef74a230b,4f652529e3ad390a5fc5f40eb605bcf9",
            "os": "windows",
            "os_version": "10.0.26300"
        },
        "render_index_mode": "off",
        "render_index_track_mode_on": True,
        "tracks": tracks,
        "update_time": now_ms,
        "version": 360000
    }

    # 11. Triển khai an toàn qua capcut_draft_manager
    sys.path.insert(0, os.path.dirname(__file__))
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
    print(f"[+] Thời lượng video: {total_duration_sec:.2f}s (~{total_duration_sec/60:.2f} phút)")
    print(f"[+] 58 Short Phrases phụ đề font Oswald-Bold, màu Vàng Chanh chuẩn Safe Zone Y=-0.38!")
    print(f"[+] 6 Đơn xe với âm thanh nhận tiền + hiệu ứng hiển thị tiền cộng dồn (Tổng thu 176k)")
    print(f"[+] Bạn có thể mở CapCut Desktop để thấy dự án ngay trên đầu danh sách!")

if __name__ == "__main__":
    build_xanhsm_176k_capcut_project()
