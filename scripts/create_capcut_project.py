"""
Tạo CapCut project mới với video XanhSM NightShift v2
Dùng cấu trúc draft_content.json chuẩn của CapCut Pro
"""
import json, os, shutil, uuid, time

DRAFTS_DIR = r"C:\Users\PC\AppData\Local\CapCut\User Data\Projects\com.lveditor.draft"
TEMPLATE_PROJECT = os.path.join(DRAFTS_DIR, "Du_An_CapCut_Moi")
NEW_PROJECT_NAME = "Vlog_XanhSM_NightShift_v2"
VIDEO_PATH = r"c:\QuangHy\editvideo\processed\Vlog_XanhSM_NightShift_v2.mp4"
NEW_PROJECT_DIR = os.path.join(DRAFTS_DIR, NEW_PROJECT_NAME)

# Xóa project cũ nếu có
if os.path.exists(NEW_PROJECT_DIR):
    shutil.rmtree(NEW_PROJECT_DIR)
    print(f"Đã xóa project cũ: {NEW_PROJECT_NAME}")

# Copy cấu trúc thư mục từ template
shutil.copytree(TEMPLATE_PROJECT, NEW_PROJECT_DIR)
print(f"Đã copy cấu trúc: {NEW_PROJECT_NAME}")

# ===== Tạo draft_content.json mới =====
with open(os.path.join(TEMPLATE_PROJECT, "draft_content.json"), encoding="utf-8") as f:
    draft = json.load(f)

# Thông tin video
import subprocess
probe_cmd = [
    "ffprobe", "-v", "quiet",
    "-print_format", "json",
    "-show_streams", "-show_format",
    VIDEO_PATH
]
result = subprocess.run(probe_cmd, capture_output=True, text=True)
video_info = json.loads(result.stdout)
video_stream = next(s for s in video_info["streams"] if s["codec_type"] == "video")
duration_sec = float(video_info["format"]["duration"])
duration_us = int(duration_sec * 1_000_000)  # CapCut dùng microseconds
width = video_stream["width"]   # 1080
height = video_stream["height"] # 1920

print(f"Video: {width}x{height}, duration={duration_sec:.2f}s ({duration_us} µs)")

# === IDs ===
project_id = str(uuid.uuid4()).upper()
video_material_id = str(uuid.uuid4()).upper()
video_segment_id = str(uuid.uuid4()).upper()
track_id = str(uuid.uuid4()).upper()
canvas_id = str(uuid.uuid4()).upper()
speed_id = str(uuid.uuid4()).upper()
audio_effect_id = str(uuid.uuid4()).upper()

now_ms = int(time.time() * 1000)

# === Build draft_content ===
new_draft = {
    "id": project_id,
    "version": draft["version"],
    "new_version": draft.get("new_version", "110.0.0"),
    "name": NEW_PROJECT_NAME,
    "duration": duration_us,
    "create_time": now_ms,
    "update_time": now_ms,
    "fps": 30.0,
    "is_drop_frame_timecode": False,
    "color_space": 0,
    "config": draft.get("config", {}),
    "canvas_config": {
        "width": 1080,
        "height": 1920,
        "ratio": "9:16"
    },
    "group_container": None,
    "keyframes": {"adjusts": []},
    "keyframe_graph_list": [],
    "platform": draft.get("platform", {}),
    "last_modified_platform": draft.get("last_modified_platform", {}),
    "mutable_config": None,
    "cover": "",
    "retouch_cover": "",
    "extra_info": None,
    "relationships": [],
    "mixed_track_mode_on": False,
    "render_index_track_mode_on": False,
    "free_render_index_mode_on": False,
    "static_cover_image_path": "",
    "source": "default",
    "time_marks": None,
    "path": NEW_PROJECT_DIR,
    "lyrics_effects": [],
    "uneven_animation_template_info": None,
    "draft_type": 0,
    "smart_ads_info": None,
    "function_assistant_info": None,

    # === Materials ===
    "materials": {
        "videos": [{
            "id": video_material_id,
            "type": "video",
            "path": VIDEO_PATH,
            "duration": duration_us,
            "width": width,
            "height": height,
            "fps": 30.0,
            "has_audio": True,
            "audio_fade": None,
            "audio_channel": 2,
            "sample_rate": 48000,
            "create_time": 0,
            "extra_type_option": 0,
            "import_time": now_ms,
            "import_time_ms": now_ms,
            "is_unified_beauty_mode": False,
            "local_task_id": "",
            "material_id": "",
            "material_url": "",
            "md5": "",
            "metetype": "normal",
            "roughcut_time_range": {"duration": duration_us, "start": 0},
            "segment_id": "",
            "source_platform": 0,
            "status": "online",
            "sub_type": "",
            "team_id": "",
            "text_alpha": -1,
            "timeclip_duration": 0,
            "total_segment_duration": duration_us,
            "uniq_id": "",
            "update_time": 0,
            "video_algorithm": {
                "algorithms": [],
                "deflicker": None,
                "motion_blur_config": None,
                "noise_reduction": None,
                "path": "",
                "quality_enhance": None,
                "time_range": None
            }
        }],
        "audios": [],
        "images": [],
        "texts": [],
        "effects": [],
        "stickers": [],
        "canvases": [{
            "id": canvas_id,
            "type": "canvas_color",
            "color": "",
            "image": "",
            "image_id": "",
            "image_name": "",
            "source_platform": 0,
            "team_id": "",
            "album_image_request_id": ""
        }],
        "transitions": [],
        "audio_effects": [],
        "audio_fades": [],
        "beats": [],
        "material_animations": [],
        "placeholders": [],
        "placeholder_infos": [],
        "speeds": [{
            "id": speed_id,
            "type": "speed",
            "mode": 0,
            "speed": 1.0,
            "curve_speed": None
        }],
        "common_mask": [],
        "chromas": [],
        "text_templates": [],
        "realtime_denoises": [],
        "audio_pannings": [],
        "audio_pitch_shifts": [],
        "video_trackings": [],
        "hsl": [],
        "drafts": [],
        "color_curves": [],
        "hsl_curves": [],
        "primary_color_wheels": [],
        "log_color_wheels": [],
        "video_effects": [],
        "ai_text_effects": [],
        "ai_generate_holders": [],
        "audio_balances": [],
        "handwrites": [],
        "manual_deformations": [],
        "manual_beautys": [],
        "plugin_effects": [],
        "sound_channel_mappings": [],
        "green_screens": [],
        "shapes": [],
        "material_colors": [],
        "digital_humans": [],
        "digital_human_model_dressing": [],
        "smart_crops": [],
        "ai_translates": [],
        "audio_track_indexes": [],
        "loudnesses": [],
        "vocal_beautifys": [],
        "vocal_separations": [],
        "smart_relights": [],
        "time_marks": [],
        "multi_language_refs": [],
        "video_shadows": [],
        "video_strokes": [],
        "video_radius": [],
        "flowers": [],
        "tail_leaders": [],
    },

    # === Tracks ===
    "tracks": [
        {
            "id": track_id,
            "type": "video",
            "attribute": 0,
            "flag": 0,
            "is_default_name": True,
            "name": "",
            "segments": [{
                "id": video_segment_id,
                "type": "video",
                "material_id": video_material_id,
                "target_timerange": {"start": 0, "duration": duration_us},
                "source_timerange": {"start": 0, "duration": duration_us},
                "speed": 1.0,
                "volume": 1.0,
                "visible": True,
                "clip": {
                    "alpha": 1.0,
                    "flip": {"horizontal": False, "vertical": False},
                    "rotation": 0.0,
                    "scale": {"x": 1.0, "y": 1.0},
                    "transform": {"x": 0.0, "y": 0.0}
                },
                "extra_material_refs": [canvas_id, speed_id],
                "hdr_settings": None,
                "intensifies_audio": False,
                "intensifies_audio_id": "",
                "is_placeholder": False,
                "is_tone_modify": False,
                "last_nonzero_volume": 1.0,
                "render_index": 0,
                "responsive_layout": {
                    "enable": False,
                    "horizontal_pos_layout": 0,
                    "size_layout": 0,
                    "vertical_pos_layout": 0,
                    "target_follow": ""
                },
                "template_id": "",
                "template_scene": "default",
                "track_attribute": 0,
                "track_render_index": 0,
                "uniform_scale": None,
                "caption_info": None
            }],
            "main_track_relationship": {
                "id": "",
                "type": "none"
            }
        }
    ]
}

# Lưu draft_content.json
# Xuất bản an toàn qua capcut_draft_manager
sys.path.insert(0, os.path.dirname(__file__))
from capcut_draft_manager import deploy_capcut_project, validate_project

deploy_result = deploy_capcut_project(
    project_name=NEW_PROJECT_NAME,
    draft_content=new_draft,
    assets_map={
        f"video/{os.path.basename(VIDEO_PATH)}": VIDEO_PATH
    } if os.path.exists(VIDEO_PATH) else None,
    cover_src_path=None,
    draft_id=project_id,
    auto_close_capcut=False
)

validate_project(NEW_PROJECT_NAME)

print(f"\n✅ CapCut project đã tạo xong!")
print(f"   Tên: {NEW_PROJECT_NAME}")
print(f"   Thư mục: {NEW_PROJECT_DIR}")
print(f"   Video: {VIDEO_PATH}")
print(f"\n➜ Mở CapCut và nhấn 'Đồng bộ dự án' hoặc restart CapCut để thấy project mới!")
