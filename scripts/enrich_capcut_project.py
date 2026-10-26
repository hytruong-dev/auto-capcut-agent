"""
Script làm giàu (enrich) project CapCut Vlog_XanhSM_NightShift_v2:
- Thêm BGM Lofi (nhạc nền âm lượng 0.16)
- Thêm 19 câu Phụ đề (Subtitles) từ xanhsm_nightshift.srt
- Thêm Hook Title 2 tầng nổi bật (Đỏ + Vàng)
- Thêm Callout Box cuối video
"""
import json, os, shutil, uuid, time, re

DRAFTS_DIR = r"C:\Users\PC\AppData\Local\CapCut\User Data\Projects\com.lveditor.draft"
PROJECT_NAME = "Vlog_XanhSM_NightShift_v2"
PROJECT_DIR = os.path.join(DRAFTS_DIR, PROJECT_NAME)
SRT_PATH = r"c:\QuangHy\editvideo\processed\xanhsm_nightshift.srt"
BGM_SRC = r"c:\QuangHy\editvideo\processed\bgm_nightshift_loop.mp3"

draft_file = os.path.join(PROJECT_DIR, "draft_content.json")
if not os.path.exists(draft_file):
    print(f"Error: {draft_file} does not exist!")
    exit(1)

with open(draft_file, encoding="utf-8") as f:
    draft = json.load(f)

duration_us = draft.get("duration", 80689542)
now_ms = int(time.time() * 1000)

# --- 1. Tạo thư mục assets/audio ---
audio_dir = os.path.join(PROJECT_DIR, "assets", "audio")
os.makedirs(audio_dir, exist_ok=True)
bgm_dest = os.path.join(audio_dir, "bgm_nightshift_loop.mp3")
shutil.copy2(BGM_SRC, bgm_dest)
print(f"[+] Đã copy BGM vào project: {bgm_dest}")

# --- 2. Thêm Audio Material ---
bgm_id = str(uuid.uuid4()).upper()
bgm_material = {
    "id": bgm_id,
    "type": "music",
    "path": bgm_dest.replace("\\", "/"),
    "name": "bgm_nightshift_loop.mp3",
    "duration": duration_us
}
if "audios" not in draft["materials"]:
    draft["materials"]["audios"] = []
draft["materials"]["audios"] = [bgm_material]

# --- 3. Parse SRT và tạo Text Materials cho Subtitles ---
def parse_time_str(t_str):
    # Format: 00:00:01,500
    parts = t_str.strip().replace(",", ".").split(":")
    hours = float(parts[0])
    minutes = float(parts[1])
    seconds = float(parts[2])
    return int((hours * 3600 + minutes * 60 + seconds) * 1_000_000)

with open(SRT_PATH, encoding="utf-8") as f:
    srt_content = f.read()

srt_blocks = re.split(r'\n\s*\n', srt_content.strip())
sub_segments = []
text_materials = []

for block in srt_blocks:
    lines = [l.strip() for l in block.split("\n") if l.strip()]
    if len(lines) >= 3:
        # line 0: index
        # line 1: timing 00:00:01,500 --> 00:00:04,500
        # line 2+: text
        timing_match = re.search(r'(\d+:\d+:\d+[,\.]\d+)\s*-->\s*(\d+:\d+:\d+[,\.]\d+)', lines[1])
        if timing_match:
            start_us = parse_time_str(timing_match.group(1))
            end_us = parse_time_str(timing_match.group(2))
            text = " ".join(lines[2:])
            
            txt_id = str(uuid.uuid4()).upper()
            content_json = {
                "styles": [{
                    "fill": {
                        "alpha": 1.0,
                        "content": {
                            "render_type": "solid",
                            "solid": {"color": [1.0, 1.0, 1.0]}
                        }
                    },
                    "font": {"id": "", "path": "C:/Windows/Fonts/arialbd.ttf"},
                    "size": 8.0
                }],
                "text": text
            }
            
            txt_mat = {
                "id": txt_id,
                "type": "text",
                "content": json.dumps(content_json, ensure_ascii=False),
                "font_size": 8.0,
                "font_title": "Arial",
                "border_color": "#000000",
                "border_width": 50,
                "has_shadow": True,
                "shadow_color": "#000000",
                "shadow_alpha": 0.9
            }
            text_materials.append(txt_mat)
            
            dur_us = max(500000, end_us - start_us)
            seg = {
                "id": str(uuid.uuid4()).upper(),
                "material_id": txt_id,
                "target_timerange": {"start": start_us, "duration": dur_us},
                "source_timerange": {"start": 0, "duration": dur_us},
                "clip": {
                    "alpha": 1.0,
                    "rotation": 0.0,
                    "scale": {"x": 1.0, "y": 1.0},
                    "transform": {"x": 0.0, "y": -0.38}
                },
                "render_index": 30000
            }
            sub_segments.append(seg)

print(f"[+] Đã tạo {len(sub_segments)} subtitle segments từ SRT")

# --- 4. Tạo Hook Title (2 tầng) & Outro Callout ---
# Dòng 1: MỘT CA ĐÊM (Đỏ)
hook1_id = str(uuid.uuid4()).upper()
hook1_content = {
    "styles": [{
        "fill": {
            "alpha": 1.0,
            "content": {
                "render_type": "solid",
                "solid": {"color": [1.0, 0.2, 0.2]}
            }
        },
        "font": {"id": "", "path": "C:/Windows/Fonts/arialbd.ttf"},
        "size": 10.5
    }],
    "text": "MỘT CA ĐÊM"
}
hook1_mat = {
    "id": hook1_id,
    "type": "text",
    "content": json.dumps(hook1_content, ensure_ascii=False),
    "font_size": 10.5,
    "border_color": "#FFFFFF",
    "border_width": 60,
    "has_shadow": True
}
text_materials.append(hook1_mat)

# Dòng 2: CHẠY XANHSM SÀI GÒN (Vàng)
hook2_id = str(uuid.uuid4()).upper()
hook2_content = {
    "styles": [{
        "fill": {
            "alpha": 1.0,
            "content": {
                "render_type": "solid",
                "solid": {"color": [1.0, 0.95, 0.0]}
            }
        },
        "font": {"id": "", "path": "C:/Windows/Fonts/arialbd.ttf"},
        "size": 11.5
    }],
    "text": "CHẠY XANHSM SÀI GÒN"
}
hook2_mat = {
    "id": hook2_id,
    "type": "text",
    "content": json.dumps(hook2_content, ensure_ascii=False),
    "font_size": 11.5,
    "border_color": "#000000",
    "border_width": 70,
    "has_shadow": True
}
text_materials.append(hook2_mat)

# Outro Callout: TIM ❤️ VÀ COMMENT GIAO LƯU NHÉ 👍 (Xanh ngọc)
callout_id = str(uuid.uuid4()).upper()
callout_content = {
    "styles": [{
        "fill": {
            "alpha": 1.0,
            "content": {
                "render_type": "solid",
                "solid": {"color": [0.0, 1.0, 0.6]}
            }
        },
        "font": {"id": "", "path": "C:/Windows/Fonts/arialbd.ttf"},
        "size": 8.5
    }],
    "text": "TIM ❤️ NẾU BẠN CŨNG THÍCH CHẠY ĐÊM 🌙"
}
callout_mat = {
    "id": callout_id,
    "type": "text",
    "content": json.dumps(callout_content, ensure_ascii=False),
    "font_size": 8.5,
    "border_color": "#000000",
    "border_width": 50,
    "has_shadow": True
}
text_materials.append(callout_mat)

# Segments cho Hook & Callout Track
hook_segments = [
    {
        "id": str(uuid.uuid4()).upper(),
        "material_id": hook1_id,
        "target_timerange": {"start": 0, "duration": 5500000},
        "source_timerange": {"start": 0, "duration": 5500000},
        "clip": {
            "alpha": 1.0,
            "rotation": 0.0,
            "scale": {"x": 1.0, "y": 1.0},
            "transform": {"x": 0.0, "y": 0.55}
        },
        "render_index": 40000
    },
    {
        "id": str(uuid.uuid4()).upper(),
        "material_id": hook2_id,
        "target_timerange": {"start": 0, "duration": 5500000},
        "source_timerange": {"start": 0, "duration": 5500000},
        "clip": {
            "alpha": 1.0,
            "rotation": 0.0,
            "scale": {"x": 1.0, "y": 1.0},
            "transform": {"x": 0.0, "y": 0.43}
        },
        "render_index": 40001
    },
    {
        "id": str(uuid.uuid4()).upper(),
        "material_id": callout_id,
        "target_timerange": {"start": 68000000, "duration": 10000000},
        "source_timerange": {"start": 0, "duration": 10000000},
        "clip": {
            "alpha": 1.0,
            "rotation": 0.0,
            "scale": {"x": 1.0, "y": 1.0},
            "transform": {"x": 0.0, "y": 0.20}
        },
        "render_index": 40002
    }
]

# Gán text materials vào draft
draft["materials"]["texts"] = text_materials

# --- 5. Build Tracks ---
# Giữ video track gốc
video_track = draft["tracks"][0]

# Audio track (BGM)
bgm_track = {
    "id": str(uuid.uuid4()).upper(),
    "type": "audio",
    "segments": [{
        "id": str(uuid.uuid4()).upper(),
        "material_id": bgm_id,
        "target_timerange": {"start": 0, "duration": duration_us},
        "source_timerange": {"start": 0, "duration": duration_us},
        "speed": 1.0,
        "volume": 0.16,
        "visible": True,
        "render_index": 20000
    }]
}

# Text track (Subtitles)
sub_track = {
    "id": str(uuid.uuid4()).upper(),
    "type": "text",
    "segments": sub_segments
}

# Text track (Hook Titles & Callout)
hook_track = {
    "id": str(uuid.uuid4()).upper(),
    "type": "text",
    "segments": hook_segments
}

draft["tracks"] = [video_track, bgm_track, sub_track, hook_track]
draft["update_time"] = now_ms

# --- 6. Lưu draft_content.json ---
with open(draft_file, "w", encoding="utf-8") as f:
    json.dump(draft, f, ensure_ascii=False, indent=2)
print(f"[+] Đã cập nhật {draft_file} thành công!")
print(f"    - Tracks: {len(draft['tracks'])}")
print(f"    - Subtitle segments: {len(sub_segments)}")
print(f"    - Hook & Callout segments: {len(hook_segments)}")
print(f"    - BGM: volume=0.16")
