"""
Deploy project Vlog_XanhSM_Storytelling_POV vào CapCut Desktop chuẩn cấu trúc CapCut 9.6+
Sử dụng module chuẩn capcut_draft_manager để đảm bảo tuyệt đối không có lỗi đường dẫn.
"""
import os
import sys
import json
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(__file__))
from capcut_draft_manager import deploy_capcut_project, validate_project, get_capcut_drafts_dir

PROJECT_NAME = "Vlog_XanhSM_Storytelling_POV"
DRAFTS_DIR = get_capcut_drafts_dir()
PROJECT_DIR = os.path.join(DRAFTS_DIR, PROJECT_NAME)

SNAPSHOT_COVER = r"c:\QuangHy\editvideo\processed\snapshots\qa_emo_w1_thach.jpg"
VO_SRC = r"c:\QuangHy\editvideo\processed\voiceover\xanhsm_story_vo.mp3"
BGM_SRC = r"c:\QuangHy\editvideo\processed\bgm_nightshift_loop.mp3"
VIDEO_SRC = r"c:\QuangHy\editvideo\processed\xanhsm_story_raw.mp4"

# Đọc draft_content.json hiện có hoặc từ backup
CONTENT_FILE = os.path.join(PROJECT_DIR, "draft_content.json")
BACKUP_FILE = r"c:\QuangHy\editvideo\processed\Vlog_XanhSM_Storytelling_POV_BACKUP\draft_content.json"

source_json = CONTENT_FILE if os.path.exists(CONTENT_FILE) else BACKUP_FILE
if not os.path.exists(source_json):
    raise FileNotFoundError(f"Không tìm thấy file nguồn draft_content.json tại {source_json}")

with open(source_json, "r", encoding="utf-8") as f:
    content_data = json.load(f)

print(f"[*] Triển khai dự án chuẩn hóa cho CapCut Desktop: {PROJECT_NAME}")

result = deploy_capcut_project(
    project_name=PROJECT_NAME,
    draft_content=content_data,
    assets_map={
        "audio/xanhsm_story_vo.mp3": VO_SRC,
        "audio/bgm_nightshift_loop.mp3": BGM_SRC,
        "video/xanhsm_story_raw.mp4": VIDEO_SRC
    },
    cover_src_path=SNAPSHOT_COVER if os.path.exists(SNAPSHOT_COVER) else None,
    draft_id="40F55760-F7E9-4024-91C9-DBC57CA8831F",
    auto_close_capcut=True
)

if validate_project(PROJECT_NAME):
    print(f"\n✅ ĐÃ TRIỂN KHAI VÀ XÁC THỰC THÀNH CÔNG DỰ ÁN CAPCUT: {PROJECT_NAME}")
    print(f"➜ Thư mục dự án: {result['project_dir']}")
    print(f"➜ Mở CapCut Desktop để xem dự án hiển thị ngay ngoài màn hình chính!")
else:
    print(f"\n❌ Cảnh báo: Dự án chưa đạt chuẩn kiểm tra!")
