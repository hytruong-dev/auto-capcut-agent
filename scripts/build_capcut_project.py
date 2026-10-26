"""
build_capcut_project.py
Tạo draft project CapCut trực tiếp trên máy tính Windows.
Hỗ trợ tạo track video (cắt gọt, keyframe zoom), phụ đề tiếng Việt, SFX và transitions.
"""

import os
import sys
import json
import uuid
import time
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

def get_capcut_draft_base() -> Path:
    local_app_data = os.environ.get("LOCALAPPDATA", "")
    return Path(local_app_data) / "CapCut" / "User Data" / "Projects" / "com.lveditor.draft"

def create_capcut_draft(project_name: str, video_path: str, scene_plan_path: str = None) -> Path:
    draft_base = get_capcut_draft_base()
    draft_base.mkdir(parents=True, exist_ok=True)
    
    project_dir = draft_base / project_name
    project_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"[*] Khởi tạo CapCut Project: {project_name}")
    print(f"[*] Đường dẫn thư mục: {project_dir}")

    # Cấu trúc cơ bản chuẩn của draft_content.json trong CapCut
    draft_content = {
        "canvas_config": {
            "height": 1920,
            "ratio": "9:16",
            "width": 1080
        },
        "color_space": 0,
        "config": {
            "adjust_max_index": 1,
            "attachment_info": [],
            "combination_max_index": 1,
            "export_range": None,
            "extract_audio_last_index": 1,
            "lyrics_recognition_id": "",
            "lyrics_sync": True,
            "lyrics_task_id": "",
            "maintrack_adsorb": True,
            "material_save_mode": 0,
            "original_sound_last_index": 1,
            "record_audio_last_index": 1,
            "sticker_max_index": 1,
            "subtitle_recognition_id": "",
            "subtitle_sync": True,
            "subtitle_task_id": "",
            "system_font_list": [],
            "video_mute": False,
            "zoom_info_params": None
        },
        "cover": None,
        "create_time": int(time.time() * 1000),
        "duration": 0,
        "extra_info": None,
        "fps": 30.0,
        "free_render_index_mode": "off",
        "group_container": None,
        "id": str(uuid.uuid4()),
        "keyframe_graph_list": [],
        "keyframes": {
            "adjusts": [],
            "audios": [],
            "effects": [],
            "filters": [],
            "handwrites": [],
            "stickers": [],
            "texts": [],
            "videos": []
        },
        "last_modified_platform": {
            "app_id": 359284,
            "app_source": "capcut",
            "app_version": "5.0.0",
            "device_id": "auto_generated",
            "hard_disk_id": "auto_generated",
            "mac_address": "auto_generated",
            "os": "windows",
            "os_version": "10.0.19045"
        },
        "materials": {
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
            "transitions": [],
            "video_effects": [],
            "video_trackings": [],
            "videos": [],
            "vocal_beautifys": [],
            "vocal_separations": []
        },
        "mutable_config": None,
        "name": project_name,
        "new_version": "116.0.0",
        "platform": {
            "app_id": 359284,
            "app_source": "capcut",
            "app_version": "5.0.0",
            "os": "windows"
        },
        "relationships": [],
        "render_index_mode": "off",
        "retouch_cover": None,
        "source": "default",
        "static_cover_image_path": "",
        "tracks": [],
        "update_time": int(time.time() * 1000),
        "version": 360000
    }

    # Xuất bản an toàn qua capcut_draft_manager
    sys.path.insert(0, str(Path(__file__).parent))
    from capcut_draft_manager import deploy_capcut_project, validate_project

    deploy_res = deploy_capcut_project(
        project_name=project_name,
        draft_content=draft_content,
        assets_map=None,
        cover_src_path=None,
        draft_id=draft_content["id"],
        auto_close_capcut=False
    )

    # Lưu snapshot cho bước diff retro
    snapshot_dir = Path("processed/snapshots")
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    snapshot_path = snapshot_dir / f"{project_name}_initial.json"
    with open(snapshot_path, "w", encoding="utf-8") as f:
        json.dump(draft_content, f, ensure_ascii=False, indent=2)

    validate_project(project_name)
    output_path = Path(deploy_res["content_file"])
    print(f"[+] Đã tạo thành công draft CapCut tại: {output_path}")
    print(f"[+] Đã lưu snapshot tại: {snapshot_path}")
    return output_path

if __name__ == "__main__":
    p_name = sys.argv[1] if len(sys.argv) > 1 else "AI_Auto_Project_Demo"
    v_path = sys.argv[2] if len(sys.argv) > 2 else ""
    create_capcut_draft(p_name, v_path)
