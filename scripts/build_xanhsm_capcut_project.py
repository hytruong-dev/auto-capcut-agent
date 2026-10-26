import os
import sys
import json
import uuid
import time
import shutil
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

def us(seconds: float) -> int:
    return int(seconds * 1_000_000)

def build_upgraded_xanhsm_project(project_name: str = "Vlog_XanhSM_1Ngay_ChayXe_POV"):
    local_app_data = os.environ.get("LOCALAPPDATA", "")
    capcut_draft_dir = Path(local_app_data) / "CapCut" / "User Data" / "Projects" / "com.lveditor.draft"
    target_project_dir = capcut_draft_dir / project_name
    target_project_dir.mkdir(parents=True, exist_ok=True)
    
    assets_audio_dir = target_project_dir / "assets" / "audio"
    assets_audio_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"[*] Nâng cấp CapCut Project theo chuẩn Viral vừa học được: {project_name}")

    with open("processed/vlog_aligned_script.json", "r", encoding="utf-8") as f:
        script_items = json.load(f)

    src_full_voice = Path("processed/voiceover/full_voiceover.mp3")
    dst_voice = assets_audio_dir / "vlog_voiceover.mp3"
    shutil.copy(src_full_voice, dst_voice)
    
    src_bgm = Path("public/bgm/bgm_lofi_xanhsm.mp3")
    dst_bgm = assets_audio_dir / "bgm_lofi.mp3"
    shutil.copy(src_bgm, dst_bgm)
    
    import subprocess
    total_duration_sec = float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(dst_voice)
    ]).decode().strip())
    total_duration_us = us(total_duration_sec)

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
        "music_track_syncs": [],
        "placeholder_materials": [],
        "placeholders": [],
        "plugin_effects": [],
        "primary_color_wheels": [],
        "realtime_denoises": [],
        "shapes": [],
        "smart_crops": [],
        "smart_relights": [],
        "sound_channel_mappings": [],
        "speeds": [],
        "stickers": [],
        "tail_leaders": [],
        "text_templates": [],
        "texts": [],
        "time_marks": [],
        "transitions": [
            {
                "id": str(uuid.uuid4()),
                "name": "Woosh",
                "effect_id": "CD580815-D706-4c17-8DA1-D31CDD568A44",
                "resource_id": "6724239584663704071",
                "type": "transition",
                "duration": 500000,
                "is_overlap": False,
                "platform": "all"
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Pull in",
                "effect_id": "E27206B3-FFA0-4ea4-B6E7-44350CED4574",
                "resource_id": "6724226861666144779",
                "type": "transition",
                "duration": 500000,
                "is_overlap": False,
                "platform": "all"
            },
            {
                "id": str(uuid.uuid4()),
                "name": "White Flash",
                "effect_id": "B5F63066-4B98-4c8a-B4AD-1398E1D313F2",
                "resource_id": "6724845376098013708",
                "type": "transition",
                "duration": 400000,
                "is_overlap": False,
                "platform": "all"
            }
        ],
        "video_effects": [],
        "video_trackings": [],
        "videos": [],
        "vocal_beautifys": [],
        "vocal_separations": []
    }

    footage_map = {
        "DJI_20260908084243_0057_D.MP4": str(Path("raw_footage/DJI_20260908084243_0057_D.MP4").resolve()).replace("\\", "/"),
        "DJI_20260908183824_0062_D.MP4": str(Path("raw_footage/DJI_20260908183824_0062_D.MP4").resolve()).replace("\\", "/"),
        "DJI_20260908185603_0064_D.MP4": str(Path("raw_footage/DJI_20260908185603_0064_D.MP4").resolve()).replace("\\", "/")
    }
    
    video_mat_ids = {}
    for f_name, f_path in footage_map.items():
        v_id = str(uuid.uuid4())
        video_mat_ids[f_name] = v_id
        materials["videos"].append({
            "id": v_id,
            "type": "video",
            "path": f_path,
            "material_name": f_name,
            "width": 2688,
            "height": 1512,
            "duration": 300000000
        })

    voice_mat_id = str(uuid.uuid4())
    materials["audios"].append({
        "id": voice_mat_id,
        "type": "extract_music",
        "path": str(dst_voice.resolve()).replace("\\", "/"),
        "name": "vlog_voiceover.mp3",
        "duration": total_duration_us
    })
    
    bgm_mat_id = str(uuid.uuid4())
    materials["audios"].append({
        "id": bgm_mat_id,
        "type": "music",
        "path": str(dst_bgm.resolve()).replace("\\", "/"),
        "name": "bgm_lofi.mp3",
        "duration": total_duration_us
    })

    # Chia nhỏ các đoạn video thành các nhịp cắt 2.7s - 3.5s (học từ ASL của video mẫu)
    # Đoạn 4 (check app) zoom mạnh 2.4x vào điện thoại!
    video_segments = []
    current_target_start = 0
    for idx, item in enumerate(script_items):
        seg_dur_us = us(item["voice_duration"])
        v_ref = item["video_ref"]
        v_mat_id = video_mat_ids[v_ref]
        src_start_us = us(item["video_start"])
        
        # Nếu là đoạn 4 (check app): zoom mạnh 2.35x vào màn hình điện thoại
        scale_val = 2.35 if idx == 3 else 1.95
        trans_y = -0.15 if idx == 3 else 0.0
        
        seg = {
            "id": str(uuid.uuid4()),
            "material_id": v_mat_id,
            "target_timerange": {"start": current_target_start, "duration": seg_dur_us},
            "source_timerange": {"start": src_start_us, "duration": seg_dur_us},
            "speed": 1.0,
            "volume": 0.12,
            "visible": True,
            "clip": {
                "alpha": 1.0,
                "rotation": 90.0,
                "scale": {"x": scale_val, "y": scale_val},
                "transform": {"x": 0.0, "y": trans_y},
                "flip": {"horizontal": False, "vertical": False}
            },
            "render_index": 14000 + idx,
            "extra_material_refs": []
        }
        
        if idx < len(script_items) - 1:
            trans = materials["transitions"][idx % len(materials["transitions"])]
            seg["extra_material_refs"].append(trans["id"])
            
        video_segments.append(seg)
        current_target_start += seg_dur_us

    voice_track_segment = {
        "id": str(uuid.uuid4()),
        "material_id": voice_mat_id,
        "target_timerange": {"start": 0, "duration": total_duration_us},
        "source_timerange": {"start": 0, "duration": total_duration_us},
        "speed": 1.0,
        "volume": 1.0,
        "visible": True,
        "render_index": 20000
    }
    
    bgm_track_segment = {
        "id": str(uuid.uuid4()),
        "material_id": bgm_mat_id,
        "target_timerange": {"start": 0, "duration": total_duration_us},
        "source_timerange": {"start": 0, "duration": total_duration_us},
        "speed": 1.0,
        "volume": 0.16,
        "visible": True,
        "render_index": 21000
    }

    # Phụ đề chữ IN HOA (UPPERCASE) học từ video mẫu, đặt ở Y = -0.38
    text_segments = []
    for idx, item in enumerate(script_items):
        t_id = str(uuid.uuid4())
        start_us = us(item["timeline_start"])
        dur_us = us(item["voice_duration"])
        text_content = item["text"].upper() # Chữ IN HOA toàn bộ
        
        text_mat = {
            "id": t_id,
            "type": "text",
            "content": json.dumps({
                "styles": [
                    {
                        "fill": {"alpha": 1.0, "content": {"render_type": "solid", "solid": {"color": [1.0, 1.0, 1.0]}}},
                        "font": {"id": "", "path": "C:/Windows/Fonts/arialbd.ttf"},
                        "size": 8.0
                    }
                ],
                "text": text_content
            }, ensure_ascii=False),
            "font_size": 8.0,
            "font_title": "Arial",
            "border_color": "#000000",
            "border_width": 50,
            "has_shadow": True,
            "shadow_color": "#000000",
            "shadow_alpha": 0.9
        }
        materials["texts"].append(text_mat)
        
        text_segments.append({
            "id": str(uuid.uuid4()),
            "material_id": t_id,
            "target_timerange": {"start": start_us, "duration": dur_us},
            "source_timerange": {"start": 0, "duration": dur_us},
            "clip": {
                "alpha": 1.0,
                "rotation": 0.0,
                "scale": {"x": 1.0, "y": 1.0},
                "transform": {"x": 0.0, "y": -0.38} # Vị trí ngang ngực/bụng như video mẫu!
            },
            "render_index": 30000 + idx
        })

    # Hook Title 2 Tầng 3D học từ video mẫu (Đỏ Cam + Vàng Tươi)
    # Dòng 1: Đỏ Cam viền trắng
    hook1_id = str(uuid.uuid4())
    materials["texts"].append({
        "id": hook1_id,
        "type": "text",
        "content": json.dumps({
            "styles": [
                {
                    "fill": {"alpha": 1.0, "content": {"render_type": "solid", "solid": {"color": [1.0, 0.2, 0.2]}}}, # Đỏ Cam #FF3333
                    "font": {"id": "", "path": "C:/Windows/Fonts/arialbd.ttf"},
                    "size": 10.0
                }
            ],
            "text": "THỬ THÁCH CHẠY XANH SM"
        }, ensure_ascii=False),
        "font_size": 10.0,
        "border_color": "#FFFFFF",
        "border_width": 60,
        "has_shadow": True
    })
    
    # Dòng 2: Vàng Tươi viền đen 3D
    hook2_id = str(uuid.uuid4())
    materials["texts"].append({
        "id": hook2_id,
        "type": "text",
        "content": json.dumps({
            "styles": [
                {
                    "fill": {"alpha": 1.0, "content": {"render_type": "solid", "solid": {"color": [1.0, 0.95, 0.0]}}}, # Vàng Tươi #FFEE00
                    "font": {"id": "", "path": "C:/Windows/Fonts/arialbd.ttf"},
                    "size": 11.5
                }
            ],
            "text": "FULL TIME 11 TIẾNG"
        }, ensure_ascii=False),
        "font_size": 11.5,
        "border_color": "#000000",
        "border_width": 70,
        "has_shadow": True
    })
    
    hook1_segment = {
        "id": str(uuid.uuid4()),
        "material_id": hook1_id,
        "target_timerange": {"start": 0, "duration": us(6.0)},
        "source_timerange": {"start": 0, "duration": us(6.0)},
        "clip": {"alpha": 1.0, "rotation": 0.0, "scale": {"x": 1.0, "y": 1.0}, "transform": {"x": 0.0, "y": 0.55}},
        "render_index": 35000
    }
    
    hook2_segment = {
        "id": str(uuid.uuid4()),
        "material_id": hook2_id,
        "target_timerange": {"start": 0, "duration": us(6.0)},
        "source_timerange": {"start": 0, "duration": us(6.0)},
        "clip": {"alpha": 1.0, "rotation": 0.0, "scale": {"x": 1.0, "y": 1.0}, "transform": {"x": 0.0, "y": 0.43}},
        "render_index": 35001
    }

    # Hộp Callout Tương Tác Cuối Video (học từ frame 57)
    cta_id = str(uuid.uuid4())
    materials["texts"].append({
        "id": cta_id,
        "type": "text",
        "content": json.dumps({
            "styles": [
                {
                    "fill": {"alpha": 1.0, "content": {"render_type": "solid", "solid": {"color": [0.0, 1.0, 0.5]}}}, # Xanh Neon
                    "font": {"id": "", "path": "C:/Windows/Fonts/arialbd.ttf"},
                    "size": 8.5
                }
            ],
            "text": "TIM ❤️ VÀ COMMENT GIAO LƯU NHÉ 👍"
        }, ensure_ascii=False),
        "font_size": 8.5,
        "border_color": "#000000",
        "border_width": 50,
        "has_shadow": True
    })
    
    cta_segment = {
        "id": str(uuid.uuid4()),
        "material_id": cta_id,
        "target_timerange": {"start": us(total_duration_sec - 7.0), "duration": us(7.0)},
        "source_timerange": {"start": 0, "duration": us(7.0)},
        "clip": {"alpha": 1.0, "rotation": 0.0, "scale": {"x": 1.0, "y": 1.0}, "transform": {"x": 0.0, "y": 0.20}},
        "render_index": 36000
    }

    tracks = [
        {"id": str(uuid.uuid4()), "type": "video", "attribute": 0, "segments": video_segments},
        {"id": str(uuid.uuid4()), "type": "audio", "attribute": 0, "segments": [voice_track_segment]},
        {"id": str(uuid.uuid4()), "type": "audio", "attribute": 0, "segments": [bgm_track_segment]},
        {"id": str(uuid.uuid4()), "type": "text", "attribute": 0, "segments": text_segments},
        {"id": str(uuid.uuid4()), "type": "text", "attribute": 0, "segments": [hook1_segment, hook2_segment, cta_segment]}
    ]

    draft_content = {
        "canvas_config": {"width": 1080, "height": 1920, "ratio": "9:16"},
        "color_space": 0,
        "config": {"adjust_max_index": 1, "lyrics_sync": True, "maintrack_adsorb": True, "material_save_mode": 0, "subtitle_sync": True, "system_font_list": [], "video_mute": False},
        "cover": None,
        "create_time": int(time.time() * 1000),
        "duration": total_duration_us,
        "fps": 30.0,
        "id": str(uuid.uuid4()),
        "last_modified_platform": {"app_id": 359284, "app_source": "capcut", "app_version": "5.0.0", "os": "windows"},
        "materials": materials,
        "name": project_name,
        "new_version": "116.0.0",
        "platform": {"app_id": 359284, "app_source": "capcut", "app_version": "5.0.0", "os": "windows"},
        "render_index_mode": "off",
        "tracks": tracks,
        "update_time": int(time.time() * 1000),
        "version": 360000
    }

    # Xuất bản an toàn qua capcut_draft_manager
    sys.path.insert(0, os.path.dirname(__file__))
    from capcut_draft_manager import deploy_capcut_project, validate_project

    deploy_res = deploy_capcut_project(
        project_name=project_name,
        draft_content=draft_content,
        assets_map=None,
        cover_src_path=None,
        draft_id=draft_content["id"],
        auto_close_capcut=False
    )

    snapshot_file = Path("processed/snapshots") / f"{project_name}_learned_from_sample.json"
    snapshot_file.parent.mkdir(parents=True, exist_ok=True)
    with open(snapshot_file, "w", encoding="utf-8") as f:
        json.dump(draft_content, f, ensure_ascii=False, indent=2)

    validate_project(project_name)
    print(f"\n[+] ĐÃ CẬP NHẬT PROJECT CAPCUT VỚI BỘ PHONG CÁCH VIRAL MỚI!")

if __name__ == "__main__":
    build_upgraded_xanhsm_project()
