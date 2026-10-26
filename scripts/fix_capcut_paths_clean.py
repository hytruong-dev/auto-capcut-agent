import os
import sys
import json
import shutil
import time
import subprocess

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

print("[1] Đang đóng CapCut Desktop...")
subprocess.run(["taskkill", "/IM", "CapCut.exe", "/F"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)

CAPCUT_DRAFTS_DIR = r"C:\Users\PC\AppData\Local\CapCut\User Data\Projects\com.lveditor.draft"
PROJECT_NAME = "Vlog_XanhSM_Storytelling_POV"
TARGET_DIR = os.path.join(CAPCUT_DRAFTS_DIR, PROJECT_NAME)
DIR_WITH_1 = os.path.join(CAPCUT_DRAFTS_DIR, PROJECT_NAME + "(1)")

DRAFT_ID = "40F55760-F7E9-4024-91C9-DBC57CA8831F"
now_us = int(time.time() * 1_000_000)

print(f"[2] Chuẩn hóa thư mục dự án: {TARGET_DIR}")
# Xóa thư mục cũ nếu có
for d in [TARGET_DIR, DIR_WITH_1]:
    if os.path.exists(d):
        print(f"Xóa thư mục cũ: {d}")
        shutil.rmtree(d, ignore_errors=True)

# Tạo thư mục dự án sạch
os.makedirs(TARGET_DIR, exist_ok=True)
assets_audio = os.path.join(TARGET_DIR, "assets", "audio")
assets_video = os.path.join(TARGET_DIR, "assets", "video")
os.makedirs(assets_audio, exist_ok=True)
os.makedirs(assets_video, exist_ok=True)

# Copy media assets từ backup hoặc processed
VO_SRC = r"c:\QuangHy\editvideo\processed\voiceover\xanhsm_story_vo.mp3"
BGM_SRC = r"c:\QuangHy\editvideo\processed\bgm_nightshift_loop.mp3"
VIDEO_SRC = r"c:\QuangHy\editvideo\processed\xanhsm_story_raw.mp4"
COVER_SRC = r"c:\QuangHy\editvideo\processed\Vlog_XanhSM_Storytelling_POV_BACKUP\draft_cover.jpg"

shutil.copy2(VO_SRC, os.path.join(assets_audio, "xanhsm_story_vo.mp3"))
shutil.copy2(BGM_SRC, os.path.join(assets_audio, "bgm_nightshift_loop.mp3"))
shutil.copy2(VIDEO_SRC, os.path.join(assets_video, "xanhsm_story_raw.mp4"))
if os.path.exists(COVER_SRC):
    shutil.copy2(COVER_SRC, os.path.join(TARGET_DIR, "draft_cover.jpg"))

print("[3] Khôi phục draft_content.json với đường dẫn tuyệt đối chuẩn xác...")
# Lấy file draft_content.json từ backup
BACKUP_JSON = r"c:\QuangHy\editvideo\processed\Vlog_XanhSM_Storytelling_POV_BACKUP\draft_content.json"
with open(BACKUP_JSON, "r", encoding="utf-8") as f:
    content = json.load(f)

# Cập nhật ID
content["id"] = DRAFT_ID

# Đường dẫn tuyệt đối chuẩn xác dùng forward slash (chuẩn CapCut JSON)
vo_path = os.path.join(assets_audio, "xanhsm_story_vo.mp3").replace("\\", "/")
bgm_path = os.path.join(assets_audio, "bgm_nightshift_loop.mp3").replace("\\", "/")
video_path = os.path.join(assets_video, "xanhsm_story_raw.mp4").replace("\\", "/")

print("Vo path:", vo_path)
print("Bgm path:", bgm_path)
print("Video path:", video_path)

for a in content.get("materials", {}).get("audios", []):
    if "vo" in a.get("name", "").lower():
        a["path"] = vo_path
    elif "bgm" in a.get("name", "").lower():
        a["path"] = bgm_path
    else:
        # Kiểm tra placeholder
        if "placeholder" in a.get("path", ""):
            a["path"] = vo_path

for v in content.get("materials", {}).get("videos", []):
    v["path"] = video_path

content_path = os.path.join(TARGET_DIR, "draft_content.json")
with open(content_path, "w", encoding="utf-8") as f:
    json.dump(content, f, ensure_ascii=False, indent=2)

shutil.copy2(content_path, os.path.join(TARGET_DIR, "draft_content.json.bak"))

print("[4] Tạo draft_meta_info.json chuẩn local...")
norm_target_dir = TARGET_DIR.replace("\\", "/")
norm_drafts_dir = CAPCUT_DRAFTS_DIR.replace("\\", "/")

draft_meta = {
    "cloud_draft_cover": False,
    "cloud_draft_sync": False,
    "cloud_package_completed_time": "",
    "draft_cloud_capcut_purchase_info": "",
    "draft_cloud_last_action_download": False,
    "draft_cloud_package_type": "",
    "draft_cloud_purchase_info": "",
    "draft_cloud_template_id": "",
    "draft_cloud_tutorial_info": "",
    "draft_cloud_videocut_purchase_info": "",
    "draft_cover": "draft_cover.jpg",
    "draft_deeplink_url": "",
    "draft_enterprise_info": {
        "draft_enterprise_extra": "",
        "draft_enterprise_id": "",
        "draft_enterprise_name": "",
        "enterprise_material": []
    },
    "draft_fold_path": norm_target_dir,
    "draft_has_unfinished_aigc_video_effect": False,
    "draft_id": DRAFT_ID,
    "draft_is_ae_produce": False,
    "draft_is_ai_packaging_used": False,
    "draft_is_ai_shorts": False,
    "draft_is_ai_translate": False,
    "draft_is_article_video_draft": False,
    "draft_is_cloud_temp_draft": False,
    "draft_is_from_deeplink": "false",
    "draft_is_infinite_canvas_draft": False,
    "draft_is_invisible": False,
    "draft_is_pippit_draft": False,
    "draft_is_web_article_video": False,
    "draft_materials": [
        {"type": 0, "value": []},
        {"type": 1, "value": []},
        {"type": 2, "value": []},
        {"type": 3, "value": []},
        {"type": 6, "value": []},
        {"type": 7, "value": []},
        {"type": 8, "value": []}
    ],
    "draft_materials_copied_info": [],
    "draft_name": PROJECT_NAME,
    "draft_need_rename_folder": False,
    "draft_new_version": "",
    "draft_removable_storage_device": "",
    "draft_root_path": norm_drafts_dir,
    "draft_segment_extra_info": [],
    "draft_timeline_materials_size_": 2081251,
    "draft_type": "",
    "draft_web_article_video_enter_from": "",
    "pippit_avatar_url": "",
    "pippit_extra_info": "",
    "pippit_id": "",
    "pippit_user_name": "",
    "tm_draft_cloud_completed": "",
    "tm_draft_cloud_entry_id": -1,
    "tm_draft_cloud_modified": 0,
    "tm_draft_cloud_parent_entry_id": -1,
    "tm_draft_cloud_space_id": -1,
    "tm_draft_cloud_user_id": -1,
    "tm_draft_create": now_us,
    "tm_draft_modified": now_us,
    "tm_draft_removed": 0,
    "tm_duration": 78030000
}

with open(os.path.join(TARGET_DIR, "draft_meta_info.json"), "w", encoding="utf-8") as f:
    json.dump(draft_meta, f, ensure_ascii=False, indent=2)

print("[5] Cập nhật root_meta_info.json...")
root_meta_file = os.path.join(CAPCUT_DRAFTS_DIR, "root_meta_info.json")
with open(root_meta_file, "r", encoding="utf-8") as f:
    root_data = json.load(f)

# Bỏ mọi draft cũ liên quan đến Vlog_XanhSM
filtered = [
    d for d in root_data.get("all_draft_store", [])
    if PROJECT_NAME not in d.get("draft_name", "") and d.get("draft_id") != DRAFT_ID
]

root_entry = {
    "cloud_draft_cover": False,
    "cloud_draft_sync": False,
    "draft_cloud_last_action_download": False,
    "draft_cloud_purchase_info": "",
    "draft_cloud_template_id": "",
    "draft_cloud_tutorial_info": "",
    "draft_cloud_videocut_purchase_info": "",
    "draft_cover": f"{norm_target_dir}/draft_cover.jpg",
    "draft_fold_path": norm_target_dir,
    "draft_id": DRAFT_ID,
    "draft_is_ai_shorts": False,
    "draft_is_cloud_temp_draft": False,
    "draft_is_infinite_canvas_draft": False,
    "draft_is_invisible": False,
    "draft_is_pippit_draft": False,
    "draft_is_web_article_video": False,
    "draft_json_file": f"{norm_target_dir}/draft_content.json",
    "draft_name": PROJECT_NAME,
    "draft_new_version": "",
    "draft_root_path": norm_drafts_dir,
    "draft_timeline_materials_size": 2081251,
    "draft_type": "",
    "draft_web_article_video_enter_from": "",
    "pippit_avatar_url": "",
    "pippit_extra_info": "",
    "pippit_id": "",
    "pippit_user_name": "",
    "streaming_edit_draft_ready": True,
    "tm_draft_cloud_completed": "",
    "tm_draft_cloud_entry_id": -1,
    "tm_draft_cloud_modified": 0,
    "tm_draft_cloud_parent_entry_id": -1,
    "tm_draft_cloud_space_id": -1,
    "tm_draft_cloud_user_id": -1,
    "tm_draft_create": now_us,
    "tm_draft_modified": now_us,
    "tm_draft_removed": 0,
    "tm_duration": 78030000
}

filtered.insert(0, root_entry)
root_data["all_draft_store"] = filtered
root_data["root_path"] = norm_drafts_dir

with open(root_meta_file, "w", encoding="utf-8") as f:
    json.dump(root_data, f, ensure_ascii=False, indent=2)

print("[6] Cập nhật draftLayoutConfig.ini...")
config_ini = r"C:\Users\PC\AppData\Local\CapCut\User Data\Config\draftLayoutConfig.ini"
if os.path.exists(config_ini):
    with open(config_ini, "r", encoding="utf-8") as f:
        ini_content = f.read()
    if DRAFT_ID not in ini_content:
        with open(config_ini, "a", encoding="utf-8") as f:
            f.write(f"{DRAFT_ID}=0\n")

print("[7] Dọn dẹp cache locks...")
lock_patterns = [
    r"C:\Users\PC\AppData\Local\CapCut\User Data\Cache\LOCK",
    r"C:\Users\PC\AppData\Local\CapCut\User Data\Cache\CEF\LOCK"
]
for lp in lock_patterns:
    if os.path.exists(lp):
        try:
            os.remove(lp)
        except Exception:
            pass

print("[HOÀN TẤT] Đường dẫn dự án đã được đồng bộ chuẩn xác tuyệt đối!")
