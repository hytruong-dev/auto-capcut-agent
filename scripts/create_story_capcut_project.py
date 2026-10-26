"""
Tạo CapCut Pro Project hoàn chỉnh: Vlog_XanhSM_Storytelling_POV
- 4 Track: Video, Voiceover, BGM LoFi, Subtitles & Hook Title
- Cập nhật root_meta_info.json để CapCut Desktop nhận diện ngay lập tức
"""
import os, sys, json, shutil, uuid, time, subprocess
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

DRAFTS_DIR = r"C:\Users\PC\AppData\Local\CapCut\User Data\Projects\com.lveditor.draft"
PROJECT_NAME = "Vlog_XanhSM_Storytelling_POV"
PROJECT_DIR = os.path.join(DRAFTS_DIR, PROJECT_NAME)
TEMPLATE_DIR = os.path.join(DRAFTS_DIR, "Template_Trend_Pro")
if not os.path.exists(TEMPLATE_DIR):
    TEMPLATE_DIR = os.path.join(DRAFTS_DIR, "Du_An_CapCut_Moi")

VO_SRC = r"c:\QuangHy\editvideo\processed\voiceover\xanhsm_story_vo.mp3"
BGM_SRC = r"c:\QuangHy\editvideo\processed\bgm_nightshift_loop.mp3"
TIMELINE_JSON = r"c:\QuangHy\editvideo\processed\story_voiceover_timeline.json"

print(f"[*] Bắt đầu tạo CapCut Project: {PROJECT_NAME}")

# Xóa project cũ nếu có
if os.path.exists(PROJECT_DIR):
    shutil.rmtree(PROJECT_DIR)

# Copy cấu trúc template
shutil.copytree(TEMPLATE_DIR, PROJECT_DIR)
print(f"[+] Đã khởi tạo cấu trúc thư mục từ template: {TEMPLATE_DIR}")

# Copy assets âm thanh vào project
audio_assets_dir = os.path.join(PROJECT_DIR, "assets", "audio")
os.makedirs(audio_assets_dir, exist_ok=True)
vo_dest = os.path.join(audio_assets_dir, "xanhsm_story_vo.mp3")
bgm_dest = os.path.join(audio_assets_dir, "bgm_nightshift_loop.mp3")
shutil.copy2(VO_SRC, vo_dest)
shutil.copy2(BGM_SRC, bgm_dest)
print(f"[+] Đã đồng bộ Voiceover và BGM vào assets nội bộ CapCut")

# Đọc timeline voiceover
with open(TIMELINE_JSON, "r", encoding="utf-8") as f:
    tl_data = json.load(f)

total_duration_sec = tl_data["total_duration"]
total_duration_us = int(total_duration_sec * 1_000_000)
segments = tl_data["segments"]

# Đọc draft_content.json gốc từ template
draft_path = os.path.join(PROJECT_DIR, "draft_content.json")
with open(draft_path, "r", encoding="utf-8") as f:
    draft = json.load(f)

now_ms = int(time.time() * 1000)
project_id = str(uuid.uuid4()).upper()

# Tạo Materials
materials = draft.get("materials", {})
for key in ["videos", "audios", "texts", "material_animations", "transitions", "speeds"]:
    if key not in materials:
        materials[key] = []

# Audio materials
vo_id = str(uuid.uuid4()).upper()
bgm_id = str(uuid.uuid4()).upper()

materials["audios"] = [
    {
        "id": vo_id,
        "type": "extract_music",
        "path": vo_dest.replace("\\", "/"),
        "name": "xanhsm_story_vo.mp3",
        "duration": total_duration_us
    },
    {
        "id": bgm_id,
        "type": "music",
        "path": bgm_dest.replace("\\", "/"),
        "name": "bgm_nightshift_loop.mp3",
        "duration": total_duration_us
    }
]

# Text Materials & Subtitle Segments
text_materials = []
subtitle_segments = []

keyword_ids = {1, 2, 4, 5, 7, 9, 10, 11, 14, 15, 16, 17, 18, 19}

from capcut_draft_manager import OSWALD_CAPCUT_FONT, _resolve_font_abs
OSWALD_FONT_PATH = _resolve_font_abs(OSWALD_CAPCUT_FONT)
OSWALD_RESOURCE_ID = "7182504807289065985"

DYNAMIC_SUB_JSON = str(Path(__file__).resolve().parent.parent / "processed" / "dynamic_short_subtitles.json")
with open(DYNAMIC_SUB_JSON, "r", encoding="utf-8") as f:
    short_chunks = json.load(f)

for idx, chunk in enumerate(short_chunks, 1):
    txt_mat_id = str(uuid.uuid4()).upper()
    txt_seg_id = str(uuid.uuid4()).upper()
    start_us = int(chunk["start"] * 1_000_000)
    dur_us = max(300_000, int((chunk["end"] - chunk["start"]) * 1_000_000))
    
    # Chuẩn style theo hình mẫu CapCut người dùng gửi:
    # Font Oswald-Bold, Cỡ 16, Viết hoa TT, Màu vàng #f0ff00, Viền đen nét dày, Đổ bóng
    text_color = [0.9411764740943909, 1.0, 0.0]
    font_size = 16.0
    text_upper = chunk["text"].upper()
    
    content_payload = {
        "styles": [{
            "fill": {
                "alpha": 1.0,
                "content": {"render_type": "solid", "solid": {"alpha": 1.0, "color": text_color}}
            },
            "font": {"id": OSWALD_RESOURCE_ID, "path": OSWALD_FONT_PATH},
            "size": font_size,
            "range": [0, len(text_upper)],
            "strokes": [{
                "alpha": 1.0,
                "content": {"render_type": "solid", "solid": {"alpha": 1.0, "color": [0.0, 0.0, 0.0]}},
                "width": 0.06
            }],
            "useLetterColor": True
        }],
        "text": text_upper
    }
    
    text_materials.append({
        "id": txt_mat_id,
        "type": "text",
        "name": "",
        "content": json.dumps(content_payload, ensure_ascii=False),
        "typesetting": 0,
        "alignment": 1,
        "border_color": "#000000",
        "border_width": 0.08,
        "border_alpha": 1.0,
        "shadow_color": "#000000",
        "shadow_alpha": 0.9,
        "shadow_smoothing": 0.45,
        "shadow_distance": 5.0,
        "text_color": "#f0ff00",
        "font_size": 16.0,
        "font_path": OSWALD_FONT_PATH,
        "font_title": "Oswald-Bold",
        "font_resource_id": OSWALD_RESOURCE_ID,
        "fonts": [{
            "id": str(uuid.uuid4()).upper(),
            "resource_id": OSWALD_RESOURCE_ID,
            "category_id": "preset",
            "category_name": "Cài đặt sẵn",
            "source_platform": 1,
            "path": OSWALD_FONT_PATH,
            "effect_id": OSWALD_RESOURCE_ID,
            "title": "Oswald-Bold"
        }]
    })
    
    subtitle_segments.append({
        "id": txt_seg_id,
        "material_id": txt_mat_id,
        "target_timerange": {"start": start_us, "duration": dur_us},
        "source_timerange": {"start": 0, "duration": dur_us},
        "speed": 1.0,
        "volume": 1.0,
        "visible": True,
        "clip": {
            "alpha": 1.0,
            "rotation": 0.0,
            "scale": {"x": 1.0, "y": 1.0},
            "transform": {"x": 0.0, "y": -0.38},
            "flip": {"horizontal": False, "vertical": False}
        },
        "render_index": 17000 + idx,
        "extra_material_refs": []
    })

# Hook Title (2 tầng: Đỏ Cam + Vàng)
hook1_mat_id = str(uuid.uuid4()).upper()
hook1_seg_id = str(uuid.uuid4()).upper()
hook1_content = {
    "styles": [{
        "fill": {"alpha": 1.0, "content": {"render_type": "solid", "solid": {"alpha": 1.0, "color": [1.0, 0.2, 0.2]}}},
        "font": {"id": OSWALD_RESOURCE_ID, "path": OSWALD_FONT_PATH},
        "size": 18.0,
        "range": [0, 14],
        "strokes": [{
            "alpha": 1.0,
            "content": {"render_type": "solid", "solid": {"alpha": 1.0, "color": [1.0, 1.0, 1.0]}},
            "width": 0.08
        }]
    }],
    "text": "THỬ THÁCH 1 NGÀY"
}
text_materials.append({
    "id": hook1_mat_id,
    "type": "text",
    "name": "",
    "content": json.dumps(hook1_content, ensure_ascii=False),
    "border_color": "#FFFFFF",
    "border_width": 0.08,
    "shadow_color": "#000000",
    "shadow_alpha": 0.9,
    "font_size": 18.0,
    "font_path": OSWALD_FONT_PATH,
    "font_title": "Oswald-Bold",
    "font_resource_id": OSWALD_RESOURCE_ID,
    "fonts": [{
        "id": str(uuid.uuid4()).upper(),
        "resource_id": OSWALD_RESOURCE_ID,
        "category_id": "preset",
        "category_name": "Cài đặt sẵn",
        "source_platform": 1,
        "path": OSWALD_FONT_PATH,
        "effect_id": OSWALD_RESOURCE_ID,
        "title": "Oswald-Bold"
    }]
})
hook_dur_us = int(6.5 * 1_000_000)
subtitle_segments.append({
    "id": hook1_seg_id,
    "material_id": hook1_mat_id,
    "target_timerange": {"start": 0, "duration": hook_dur_us},
    "source_timerange": {"start": 0, "duration": hook_dur_us},
    "clip": {"alpha": 1.0, "rotation": 0.0, "scale": {"x": 1.0, "y": 1.0}, "transform": {"x": 0.0, "y": 0.52}},
    "render_index": 18001,
    "extra_material_refs": []
})

hook2_mat_id = str(uuid.uuid4()).upper()
hook2_seg_id = str(uuid.uuid4()).upper()
hook2_content = {
    "styles": [{
        "fill": {"alpha": 1.0, "content": {"render_type": "solid", "solid": {"alpha": 1.0, "color": [0.941, 1.0, 0.0]}}},
        "font": {"id": OSWALD_RESOURCE_ID, "path": OSWALD_FONT_PATH},
        "size": 20.0,
        "range": [0, 20],
        "strokes": [{
            "alpha": 1.0,
            "content": {"render_type": "solid", "solid": {"alpha": 1.0, "color": [0.0, 0.0, 0.0]}},
            "width": 0.08
        }]
    }],
    "text": "CHẠY XANH SM SÀI GÒN"
}
text_materials.append({
    "id": hook2_mat_id,
    "type": "text",
    "name": "",
    "content": json.dumps(hook2_content, ensure_ascii=False),
    "border_color": "#000000",
    "border_width": 0.08,
    "shadow_color": "#000000",
    "shadow_alpha": 0.9,
    "font_size": 20.0,
    "font_path": OSWALD_FONT_PATH,
    "font_title": "Oswald-Bold",
    "font_resource_id": OSWALD_RESOURCE_ID,
    "fonts": [{
        "id": str(uuid.uuid4()).upper(),
        "resource_id": OSWALD_RESOURCE_ID,
        "category_id": "preset",
        "category_name": "Cài đặt sẵn",
        "source_platform": 1,
        "path": OSWALD_FONT_PATH,
        "effect_id": OSWALD_RESOURCE_ID,
        "title": "Oswald-Bold"
    }]
})
subtitle_segments.append({
    "id": hook2_seg_id,
    "material_id": hook2_mat_id,
    "target_timerange": {"start": 0, "duration": hook_dur_us},
    "source_timerange": {"start": 0, "duration": hook_dur_us},
    "clip": {"alpha": 1.0, "rotation": 0.0, "scale": {"x": 1.0, "y": 1.0}, "transform": {"x": 0.0, "y": 0.38}},
    "render_index": 18002,
    "extra_material_refs": []
})

materials["texts"] = text_materials

# Video Track: Sử dụng video thô đã ghép hoặc multi-cuts
raw_video_path = os.path.abspath(r"processed\xanhsm_story_raw.mp4").replace("\\", "/")
v_mat_id = str(uuid.uuid4()).upper()
v_seg_id = str(uuid.uuid4()).upper()
materials["videos"] = [{
    "id": v_mat_id,
    "type": "video",
    "path": raw_video_path,
    "material_name": "xanhsm_story_raw.mp4",
    "width": 1080,
    "height": 1920,
    "duration": total_duration_us
}]

video_segments = [{
    "id": v_seg_id,
    "material_id": v_mat_id,
    "target_timerange": {"start": 0, "duration": total_duration_us},
    "source_timerange": {"start": 0, "duration": total_duration_us},
    "speed": 1.0,
    "volume": 0.12,
    "visible": True,
    "clip": {
        "alpha": 1.0,
        "rotation": 0.0,
        "scale": {"x": 1.0, "y": 1.0},
        "transform": {"x": 0.0, "y": 0.0},
        "flip": {"horizontal": False, "vertical": False}
    },
    "render_index": 14000,
    "extra_material_refs": []
}]

# Voiceover segment
vo_seg_id = str(uuid.uuid4()).upper()
vo_segment = [{
    "id": vo_seg_id,
    "material_id": vo_id,
    "target_timerange": {"start": 0, "duration": total_duration_us},
    "source_timerange": {"start": 0, "duration": total_duration_us},
    "speed": 1.0,
    "volume": 1.0,
    "visible": True,
    "render_index": 15000,
    "extra_material_refs": []
}]

# BGM segment
bgm_seg_id = str(uuid.uuid4()).upper()
bgm_segment = [{
    "id": bgm_seg_id,
    "material_id": bgm_id,
    "target_timerange": {"start": 0, "duration": total_duration_us},
    "source_timerange": {"start": 0, "duration": total_duration_us},
    "speed": 1.0,
    "volume": 0.14,
    "visible": True,
    "render_index": 16000,
    "extra_material_refs": []
}]

# 4 Tracks hoàn chỉnh
tracks = [
    {"id": str(uuid.uuid4()).upper(), "type": "video", "segments": video_segments, "attribute": 0, "flag": 0},
    {"id": str(uuid.uuid4()).upper(), "type": "audio", "segments": vo_segment, "attribute": 0, "flag": 0},
    {"id": str(uuid.uuid4()).upper(), "type": "audio", "segments": bgm_segment, "attribute": 0, "flag": 0},
    {"id": str(uuid.uuid4()).upper(), "type": "text", "segments": subtitle_segments, "attribute": 0, "flag": 0}
]

draft["id"] = project_id
draft["name"] = PROJECT_NAME
draft["duration"] = total_duration_us
draft["create_time"] = now_ms
draft["update_time"] = now_ms
draft["canvas_config"] = {"width": 1080, "height": 1920, "ratio": "9:16"}
draft["materials"] = materials
draft["tracks"] = tracks

# Xuất bản an toàn qua capcut_draft_manager
sys.path.insert(0, os.path.dirname(__file__))
from capcut_draft_manager import deploy_capcut_project, validate_project

deploy_result = deploy_capcut_project(
    project_name=PROJECT_NAME,
    draft_content=draft,
    assets_map={
        "audio/xanhsm_story_vo.mp3": VO_SRC,
        "audio/bgm_nightshift_loop.mp3": BGM_SRC,
        "video/xanhsm_story_raw.mp4": r"c:\QuangHy\editvideo\processed\xanhsm_story_raw.mp4"
    },
    cover_src_path=r"c:\QuangHy\editvideo\processed\snapshots\qa_emo_w1_thach.jpg",
    draft_id=project_id,
    auto_close_capcut=False
)

validate_project(PROJECT_NAME)
print(f"[SUCCESS] Dự án CapCut Pro Desktop đã sẵn sàng: {PROJECT_NAME}")
