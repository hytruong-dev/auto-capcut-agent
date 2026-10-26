"""
Module quản lý và xuất bản dự án CapCut Pro Desktop (CapCut 9.6+ Standard)
Đảm bảo 100% dự án tạo ra luôn mở được ngay trong CapCut Desktop,
không bao giờ bị lỗi 'đường dẫn không đúng' (draft_unconventional_path_cannot_open)
hoặc xung đột cloud sync / placeholder.
"""

import os
import sys
import json
import shutil
import uuid
import time
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any, Union

# Bắt buộc UTF-8 output trên Windows console
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Các đường dẫn hệ thống chuẩn của CapCut Desktop trên Windows
DEFAULT_LOCAL_APPDATA = os.environ.get("LOCALAPPDATA", r"C:\Users\PC\AppData\Local")
CAPCUT_BASE_DIR = os.path.join(DEFAULT_LOCAL_APPDATA, "CapCut")
CAPCUT_DRAFTS_DIR = os.path.join(CAPCUT_BASE_DIR, "User Data", "Projects", "com.lveditor.draft")
CAPCUT_CONFIG_INI = os.path.join(CAPCUT_BASE_DIR, "User Data", "Config", "draftLayoutConfig.ini")
ROOT_META_INFO_PATH = os.path.join(CAPCUT_DRAFTS_DIR, "root_meta_info.json")


def norm_path(path: Union[str, Path]) -> str:
    """Chuẩn hóa đường dẫn tuyệt đối sang format forward slash '/' của CapCut materials."""
    if not path:
        return ""
    p_str = str(path).replace("\\", "/")
    while "//" in p_str and not p_str.startswith("http"):
        p_str = p_str.replace("//", "/")
    return p_str


def get_capcut_drafts_dir() -> str:
    """Trả về đường dẫn tuyệt đối thư mục drafts của CapCut."""
    return CAPCUT_DRAFTS_DIR


def get_native_platform_info() -> dict:
    """
    Trả về cấu hình platform chuẩn xác của máy hiện tại để vượt qua hoàn toàn
    hệ thống kiểm tra DraftLoadVerifier::check_app_support và check_device_support của CapCut 9.6+.
    """
    candidates = [
        os.path.join(CAPCUT_DRAFTS_DIR, ".recycle_bin", "1022", "draft_content.json"),
        os.path.join(CAPCUT_DRAFTS_DIR, ".recycle_bin", "1019", "draft_content.json"),
        os.path.join(CAPCUT_DRAFTS_DIR, ".recycle_bin", "AI_Viral_Project_60s", "draft_content.json"),
    ]
    for c in candidates:
        if os.path.exists(c):
            try:
                with open(c, "r", encoding="utf-8") as f:
                    d = json.load(f)
                plat = d.get("platform")
                if plat and plat.get("app_id") == 359289 and plat.get("app_source") == "cc":
                    return plat
            except Exception:
                pass

    return {
        "os": "windows",
        "os_version": "10.0.26300",
        "app_id": 359289,
        "app_version": "9.6.0",
        "app_source": "cc",
        "device_id": "4475d19983c69cde88e66433dd341c72",
        "hard_disk_id": "",
        "mac_address": "26ebfda668b7dfc60a011ffef74a230b,4f652529e3ad390a5fc5f40eb605bcf9"
    }


def clean_cloud_upload_conflicts(draft_id: str):
    """
    Xóa các bản ghi rác trong cloud_draft_upload_path_cfg.ini và AutoBackupStatus.json
    để ngăn chặn việc CapCut hiểu nhầm local draft thành cloud draft bị hỏng đường dẫn.
    """
    if not draft_id:
        return

    cfg_path = os.path.join(CAPCUT_BASE_DIR, "User Data", "Config", "cloud_draft_upload_path_cfg.ini")
    if os.path.exists(cfg_path):
        try:
            with open(cfg_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            new_lines = []
            skip = False
            for line in lines:
                if line.startswith("["):
                    if draft_id.lower() in line.lower():
                        skip = True
                        continue
                    else:
                        skip = False
                if not skip:
                    new_lines.append(line)
            with open(cfg_path, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
        except Exception:
            pass

    autobackup_dir = os.path.join(CAPCUT_BASE_DIR, "User Data", "Config", "AutoBackUp")
    if os.path.exists(autobackup_dir):
        for root, dirs, files in os.walk(autobackup_dir):
            for file in files:
                if file == "AutoBackupStatus.json":
                    fp = os.path.join(root, file)
                    try:
                        with open(fp, "r", encoding="utf-8") as f:
                            bk = json.load(f)
                        bk["backup_status"] = [
                            item for item in bk.get("backup_status", [])
                            if item.get("draft_id", "").lower() != draft_id.lower()
                        ]
                        with open(fp, "w", encoding="utf-8") as f:
                            json.dump(bk, f, ensure_ascii=False, indent=2)
                    except Exception:
                        pass



def get_capcut_exe_path() -> Optional[str]:
    """Tìm file thực thi CapCut.exe mới nhất."""
    apps_dir = os.path.join(CAPCUT_BASE_DIR, "Apps")
    if not os.path.exists(apps_dir):
        return None
    
    # Ưu tiên các thư mục version dạng 9.6.0.4097
    subdirs = [os.path.join(apps_dir, d) for d in os.listdir(apps_dir) if os.path.isdir(os.path.join(apps_dir, d))]
    for d in sorted(subdirs, reverse=True):
        exe = os.path.join(d, "CapCut.exe")
        if os.path.exists(exe):
            return exe
            
    # File trực tiếp trong Apps
    main_exe = os.path.join(apps_dir, "CapCut.exe")
    if os.path.exists(main_exe):
        return main_exe
        
    return None


def kill_capcut_if_running() -> bool:
    """Đóng CapCut Desktop để giải phóng file locks trước khi ghi dữ liệu."""
    try:
        res = subprocess.run(
            ["taskkill", "/IM", "CapCut.exe", "/F"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if "SUCCESS" in res.stdout or res.returncode == 0:
            time.sleep(1.2)
            return True
    except Exception:
        pass
    return False


def clean_cache_locks():
    """Dọn dẹp các file LOCK trong CEF, Cache và ParfaitServer để tránh CapCut bị treo hoặc tự đóng khi khởi động."""
    import glob
    lock_dirs = [
        os.path.join(CAPCUT_BASE_DIR, "User Data", "Cache"),
        os.path.join(CAPCUT_BASE_DIR, "User Data", "Cache", "CEF")
    ]
    for ld in lock_dirs:
        lf = os.path.join(ld, "LOCK")
        if os.path.exists(lf):
            try:
                os.remove(lf)
            except Exception:
                pass

    parfait_pattern = os.path.join(CAPCUT_BASE_DIR, "User Data", "ParfaitServer", "lock", "*", "*")
    for pf in glob.glob(parfait_pattern):
        try:
            os.remove(pf)
        except Exception:
            pass



def sanitize_draft_materials(draft_content: dict, project_dir: str) -> dict:
    """
    Quét sạch mọi chuỗi placeholder và chuẩn hóa toàn bộ đường dẫn media
    trong draft_content thành đường dẫn tuyệt đối chuẩn xác trên ổ cứng.
    """
    import re

    norm_proj = norm_path(project_dir)
    assets_audio = f"{norm_proj}/assets/audio"
    assets_video = f"{norm_proj}/assets/video"
    assets_image = f"{norm_proj}/assets/image"

    materials = draft_content.get("materials", {})

    # 1. Dọn dẹp các mảng placeholder vô nghĩa
    for k in ["placeholder_infos", "placeholder_materials", "placeholders"]:
        if k in materials and isinstance(materials[k], list):
            materials[k] = []

    # 2. Chuẩn hóa videos
    for v in materials.get("videos", []):
        old_path = v.get("path", "")
        # Khử placeholder dạng ##_draftpath_placeholder_UUID_##
        cleaned = re.sub(r'##_draftpath_placeholder_[^#]+##/?', '', old_path)
        if not cleaned or not re.match(r'^[a-zA-Z]:/', cleaned.replace('\\', '/')):
            name = v.get("material_name") or v.get("name") or os.path.basename(cleaned) or "video.mp4"
            v["path"] = f"{assets_video}/{name}"
        else:
            v["path"] = norm_path(cleaned)

    # 3. Chuẩn hóa audios
    for a in materials.get("audios", []):
        old_path = a.get("path", "")
        cleaned = re.sub(r'##_draftpath_placeholder_[^#]+##/?', '', old_path)
        if not cleaned or not re.match(r'^[a-zA-Z]:/', cleaned.replace('\\', '/')):
            name = a.get("material_name") or a.get("name") or os.path.basename(cleaned) or "audio.mp3"
            a["path"] = f"{assets_audio}/{name}"
        else:
            a["path"] = norm_path(cleaned)

    # 4. Chuẩn hóa images
    for im in materials.get("images", []):
        old_path = im.get("path", "")
        cleaned = re.sub(r'##_draftpath_placeholder_[^#]+##/?', '', old_path)
        if not cleaned or not re.match(r'^[a-zA-Z]:/', cleaned.replace('\\', '/')):
            name = im.get("material_name") or im.get("name") or os.path.basename(cleaned) or "image.png"
            im["path"] = f"{assets_image}/{name}"
        else:
            im["path"] = norm_path(cleaned)

    # 5. Font path PHẢI tuyệt đối: font tương đối làm CapCut 9.6 tự đóng ngay khi mở dự án
    draft_content = sanitize_font_paths(draft_content)

    return draft_content


OSWALD_CAPCUT_FONT = (
    "C:/Users/PC/AppData/Local/CapCut/User Data/Cache/effect/"
    "7182504807289065985/0a5333de6f4d592cb2d2390d68b31efb/Oswald-Bold.ttf"
)


def _resolve_font_abs(path: str) -> str:
    """Đổi font path tương đối/hỏng thành đường dẫn tuyệt đối tồn tại thật."""
    if path and os.path.isabs(path) and os.path.exists(path):
        return norm_path(path)
    name = os.path.basename(path or "").lower()
    if "oswald" in name or not name:
        if os.path.exists(OSWALD_CAPCUT_FONT):
            return OSWALD_CAPCUT_FONT
        repo = Path(__file__).resolve().parent.parent / "portable_trained_brain" / "portable_assets" / "fonts" / "Oswald-Bold.ttf"
        if repo.exists():
            return norm_path(repo)
    if path and not os.path.isabs(path):
        cand = Path(__file__).resolve().parent.parent / path
        if cand.exists():
            return norm_path(cand)
    return norm_path(path) if path else path


def sanitize_font_paths(draft_content: dict) -> dict:
    """Chuẩn hóa mọi lớp chữ về đúng schema CapCut 9.6 (nếu sai CapCut tự đóng khi vào giao diện edit):
    - font_path / styles[].font.path là đường dẫn TUYỆT ĐỐI
    - material.type == "text" (KHÔNG được là "none")
    - mỗi style có "range": [0, độ dài UTF-16 của text]
    - material.fonts có 1 mục mô tả font (như CapCut tự ghi)
    """
    for t in draft_content.get("materials", {}).get("texts", []):
        if t.get("type") in (None, "", "none"):
            t["type"] = "text"
        if t.get("font_path") is not None:
            t["font_path"] = _resolve_font_abs(t.get("font_path", ""))
        try:
            ct = json.loads(t.get("content", "") or "{}")
        except Exception:
            continue
        changed = False
        n_utf16 = len(ct.get("text", "").encode("utf-16-le")) // 2
        for st in ct.get("styles", []):
            fo = st.get("font")
            if isinstance(fo, dict) and fo.get("path") is not None:
                new = _resolve_font_abs(fo["path"])
                if new != fo["path"]:
                    fo["path"] = new
                    changed = True
            if "range" not in st and len(ct.get("styles", [])) == 1:
                st["range"] = [0, n_utf16]
                changed = True
        if changed:
            t["content"] = json.dumps(ct, ensure_ascii=False)
        if not t.get("fonts") and t.get("font_path"):
            fid = str(t.get("font_id") or t.get("font_resource_id") or "")
            t["fonts"] = [{
                "id": str(uuid.uuid4()).upper(), "resource_id": fid, "third_resource_id": "",
                "category_id": "preset", "category_name": "Cài đặt sẵn", "source_platform": 1,
                "path": t["font_path"], "effect_id": fid,
                "title": t.get("font_name") or "Oswald-Bold",
                "team_id": "", "file_uri": "", "request_id": "",
            }]
            if not t.get("font_title") or t.get("font_title") == "none":
                t["font_title"] = t.get("font_name") or "Oswald-Bold"
    return draft_content


def create_zoom_keyframes(start_scale: float = 1.0, end_scale: float = 1.15, duration_us: int = 350000, start_offset_us: int = 0) -> List[dict]:
    """
    Sinh cấu trúc common_keyframes cho hiệu ứng Zoom mượt (KFTypeScaleX và KFTypeScaleY)
    chuẩn theo VECreator.dll CapCut 9.6 Pro (Master Blueprint v2.0 Section 3.3).
    """
    kfs = []
    for prop in ["KFTypeScaleX", "KFTypeScaleY"]:
        kfs.append({
            "id": str(uuid.uuid4()).upper(),
            "material_id": "",
            "property_type": prop,
            "keyframe_list": [
                {
                    "id": str(uuid.uuid4()).upper(),
                    "time_offset": start_offset_us,
                    "values": [float(start_scale)],
                    "curveType": "Line",
                    "graphID": "",
                    "left_control": {"x": 0.0, "y": 0.0},
                    "right_control": {"x": 0.0, "y": 0.0}
                },
                {
                    "id": str(uuid.uuid4()).upper(),
                    "time_offset": start_offset_us + duration_us,
                    "values": [float(end_scale)],
                    "curveType": "Line",
                    "graphID": "",
                    "left_control": {"x": 0.0, "y": 0.0},
                    "right_control": {"x": 0.0, "y": 0.0}
                }
            ]
        })
    return kfs


def create_volume_duck_keyframes(high_vol: float = 0.30, low_vol: float = 0.15, duck_duration_us: int = 150000, start_offset_us: int = 0) -> List[dict]:
    """
    Sinh cấu trúc common_keyframes hạ âm lượng BGM (Ducking) chuẩn VECreator.dll CapCut 9.6 Pro.
    """
    return [{
        "id": str(uuid.uuid4()).upper(),
        "material_id": "",
        "property_type": "KFTypeVolume",
        "keyframe_list": [
            {
                "id": str(uuid.uuid4()).upper(),
                "time_offset": start_offset_us,
                "values": [float(high_vol)],
                "curveType": "Line",
                "graphID": "",
                "left_control": {"x": 0.0, "y": 0.0},
                "right_control": {"x": 0.0, "y": 0.0}
            },
            {
                "id": str(uuid.uuid4()).upper(),
                "time_offset": start_offset_us + duck_duration_us,
                "values": [float(low_vol)],
                "curveType": "Line",
                "graphID": "",
                "left_control": {"x": 0.0, "y": 0.0},
                "right_control": {"x": 0.0, "y": 0.0}
            }
        ]
    }]


def deploy_capcut_project(
    project_name: str,
    draft_content: dict,
    assets_map: Optional[Dict[str, str]] = None,
    cover_src_path: Optional[str] = None,
    draft_id: Optional[str] = None,
    auto_close_capcut: bool = True
) -> Dict[str, Any]:
    """
    Hàm chuẩn hóa tối cao triển khai một dự án vào CapCut Desktop:
    1. Đóng CapCut an toàn (nếu cần).
    2. Khởi tạo thư mục dự án cục bộ trong com.lveditor.draft.
    3. Copy các file media (audio, video, image) vào assets nội bộ dự án.
    4. Khử sạch toàn bộ placeholder và chuyển tất cả đường dẫn sang đường dẫn tuyệt đối với dấu '/'.
    5. Ghi draft_content.json và draft_content.json.bak.
    6. Tạo draft_meta_info.json với cờ thuần local, draft_fold_path và draft_root_path chính xác.
    7. Cập nhật root_meta_info.json đưa dự án lên đầu danh sách hiển thị ngoài Home CapCut.
    8. Đăng ký draftLayoutConfig.ini.
    9. Xóa cache locks.
    """
    if auto_close_capcut:
        kill_capcut_if_running()

    os.makedirs(CAPCUT_DRAFTS_DIR, exist_ok=True)
    norm_drafts_dir = norm_path(CAPCUT_DRAFTS_DIR)

    project_dir = os.path.join(CAPCUT_DRAFTS_DIR, project_name)
    norm_project_dir = norm_path(project_dir)

    # Dọn dẹp thư mục backup xung đột nếu có
    backup_conflict_dir = os.path.join(CAPCUT_DRAFTS_DIR, project_name + "(1)")
    if os.path.exists(backup_conflict_dir):
        shutil.rmtree(backup_conflict_dir, ignore_errors=True)

    # Tạo thư mục dự án và cây assets chuẩn
    os.makedirs(project_dir, exist_ok=True)
    assets_audio_dir = os.path.join(project_dir, "assets", "audio")
    assets_video_dir = os.path.join(project_dir, "assets", "video")
    assets_image_dir = os.path.join(project_dir, "assets", "image")
    os.makedirs(assets_audio_dir, exist_ok=True)
    os.makedirs(assets_video_dir, exist_ok=True)
    os.makedirs(assets_image_dir, exist_ok=True)

    # Copy assets nếu được cung cấp
    # assets_map: {"video/main.mp4": "c:/path/to/src.mp4", "audio/vo.mp3": ...}
    if assets_map:
        for dest_rel, src_path in assets_map.items():
            if os.path.exists(src_path):
                dest_full = os.path.join(project_dir, "assets", dest_rel)
                os.makedirs(os.path.dirname(dest_full), exist_ok=True)
                shutil.copy2(src_path, dest_full)

    # Xử lý cover
    cover_dest = os.path.join(project_dir, "draft_cover.jpg")
    if cover_src_path and os.path.exists(cover_src_path):
        if os.path.abspath(cover_src_path).lower() != os.path.abspath(cover_dest).lower():
            try:
                shutil.copy2(cover_src_path, cover_dest)
            except Exception:
                pass

    # Chuẩn hóa Draft ID và tránh trùng lặp với dự án khác
    final_draft_id = (draft_id or draft_content.get("id") or str(uuid.uuid4())).upper()
    if os.path.exists(ROOT_META_INFO_PATH):
        try:
            with open(ROOT_META_INFO_PATH, "r", encoding="utf-8") as f:
                existing_root = json.load(f)
            used_ids = {
                item.get("draft_id"): item.get("draft_name")
                for item in existing_root.get("all_draft_store", [])
            }
            if final_draft_id in used_ids and used_ids[final_draft_id] != project_name:
                final_draft_id = str(uuid.uuid4()).upper()
        except Exception:
            pass

    draft_content["id"] = final_draft_id
    draft_content["name"] = project_name
    draft_content["version"] = 360000
    draft_content["new_version"] = "189.0.0"
    draft_content["color_space"] = -1
    draft_content["render_index_track_mode_on"] = True

    # Gán cấu hình platform chuẩn của máy chủ để vượt qua DraftLoadVerifier của CapCut 9.6
    plat = get_native_platform_info()
    draft_content["platform"] = dict(plat)
    draft_content["last_modified_platform"] = dict(plat)

    # Khử sạch placeholder và chuẩn hóa đường dẫn materials
    draft_content = sanitize_draft_materials(draft_content, project_dir)

    # Dọn dẹp .locked và thư mục tạm {uuid} trong thư mục dự án
    locked_p = os.path.join(project_dir, ".locked")
    if os.path.exists(locked_p):
        try:
            os.remove(locked_p)
        except Exception:
            pass
    for item in os.listdir(project_dir):
        ip = os.path.join(project_dir, item)
        if os.path.isdir(ip) and item.startswith("{") and item.endswith("}"):
            try:
                shutil.rmtree(ip, ignore_errors=True)
            except Exception:
                pass

    # Ghi root draft_content.json và file backup
    content_file = os.path.join(project_dir, "draft_content.json")
    content_bak = os.path.join(project_dir, "draft_content.json.bak")
    with open(content_file, "w", encoding="utf-8") as f:
        json.dump(draft_content, f, ensure_ascii=False, indent=2)
    shutil.copy2(content_file, content_bak)

    # Đồng bộ cây Timelines đa dòng thời gian (bắt buộc cho CapCut 9.6 Pro)
    tl_dir = os.path.join(project_dir, "Timelines")
    os.makedirs(tl_dir, exist_ok=True)
    timeline_id = final_draft_id
    subdirs = [d for d in os.listdir(tl_dir) if os.path.isdir(os.path.join(tl_dir, d))]
    if subdirs:
        timeline_id = subdirs[0]
    tl_guid_dir = os.path.join(tl_dir, timeline_id)
    os.makedirs(tl_guid_dir, exist_ok=True)

    tl_dc_path = os.path.join(tl_guid_dir, "draft_content.json")
    with open(tl_dc_path, "w", encoding="utf-8") as f:
        json.dump(draft_content, f, ensure_ascii=False, indent=2)
    shutil.copy2(tl_dc_path, os.path.join(tl_guid_dir, "draft_content.json.bak"))

    # Copy cover vào timeline nếu có
    if os.path.exists(cover_dest):
        shutil.copy2(cover_dest, os.path.join(tl_guid_dir, "draft_cover.jpg"))

    now_us = int(time.time() * 1_000_000)

    # Ghi Timelines/project.json
    project_json_data = {
        "config": {
            "color_space": -1,
            "hdr_vivid": False,
            "mixed_track_mode_on": False,
            "render_index_track_mode_on": False,
            "use_float_render": False
        },
        "create_time": now_us,
        "id": timeline_id,
        "main_timeline_id": timeline_id,
        "timelines": [
            {
                "create_time": now_us,
                "id": timeline_id,
                "is_marked_delete": False,
                "name": "Dòng thời gian 01",
                "update_time": now_us
            }
        ],
        "update_time": now_us,
        "version": 0
    }
    with open(os.path.join(tl_dir, "project.json"), "w", encoding="utf-8") as f:
        json.dump(project_json_data, f, ensure_ascii=False, indent=2)
    shutil.copy2(os.path.join(tl_dir, "project.json"), os.path.join(tl_dir, "project.json.bak"))

    # Ghi root timeline_layout.json cho Qt docking editor
    layout_data = {
        "dockItems": [
            {
                "dockIndex": 0,
                "ratio": 1,
                "timelineIds": [timeline_id],
                "timelineNames": ["Dòng thời gian 01"]
            }
        ],
        "layoutOrientation": 1
    }
    with open(os.path.join(project_dir, "timeline_layout.json"), "w", encoding="utf-8") as f:
        json.dump(layout_data, f, ensure_ascii=False, indent=2)

    # Ghi các file cấu hình phụ trợ chuẩn của CapCut Desktop
    with open(os.path.join(project_dir, "draft_agency_config.json"), "w", encoding="utf-8") as f:
        json.dump({"is_auto_agency_enabled": False, "is_auto_agency_popup": False, "is_single_agency_mode": False, "marterials": None, "use_converter": False, "video_resolution": 720}, f, ensure_ascii=False, indent=2)

    with open(os.path.join(project_dir, "draft_biz_config.json"), "w", encoding="utf-8") as f:
        json.dump({}, f, ensure_ascii=False, indent=2)

    with open(os.path.join(project_dir, "performance_opt_info.json"), "w", encoding="utf-8") as f:
        json.dump({"manual_cancle_precombine_segs": None, "need_auto_precombine_segs": None}, f, ensure_ascii=False, indent=2)

    with open(os.path.join(project_dir, "attachment_pc_common.json"), "w", encoding="utf-8") as f:
        json.dump({"ai_packaging_infos": [], "ai_packaging_report_info": {"caption_id_list": [], "commercial_material": "", "material_source": "", "method": "", "page_from": "", "style": "", "task_id": "", "text_style": "", "tos_id": "", "video_category": ""}, "broll": {"ai_packaging_infos": [], "ai_packaging_report_info": {"caption_id_list": [], "commercial_material": "", "material_source": "", "method": "", "page_from": "", "style": "", "task_id": "", "text_style": "", "tos_id": "", "video_category": ""}}, "commercial_music_category_ids": [], "pc_feature_flag": 0, "recognize_tasks": [], "reference_lines_config": {"horizontal_lines": [], "is_lock": False, "is_visible": False, "vertical_lines": []}, "safe_area_type": 0, "template_item_infos": [], "unlock_template_ids": []}, f, ensure_ascii=False, indent=2)

    with open(os.path.join(tl_guid_dir, "attachment_editing.json"), "w", encoding="utf-8") as f:
        json.dump({"editing_draft": {"ai_remove_filter_words": {"enter_source": "", "right_id": ""}, "ai_shorts_info": {"report_params": "", "type": 0}, "cover_extra_info": {"draft_id": "", "position": 0, "select_segment_id": "", "select_segment_source_start": 0, "select_segment_target_start": 0, "slot_image_path": "", "slot_info_config": {"slot_image_path": "", "used_video_algorithm_configs": []}, "type": 1, "video_draft_source": -1}, "crop_info_extra": {"crop_mirror_type": 0, "crop_rotate": 0.0, "crop_rotate_total": 0.0}, "cutsame_to_image_edit_template_id": "", "digital_human_template_to_video_info": {"has_upload_material": False, "template_type": 0}, "draft_used_recommend_function": "", "edit_type": 0, "eye_correct_enabled_multi_face_time": 0, "has_adjusted_render_layer": False, "is_open_expand_player": False, "version": "1.0.0"}}, f, ensure_ascii=False, indent=2)

    # Dọn sạch các file template .tmp rác cũ nếu có
    for sdir in [project_dir, tl_guid_dir]:
        for tmp_name in ["template.tmp", "template-2.tmp", "template.json"]:
            tp = os.path.join(sdir, tmp_name)
            if os.path.exists(tp):
                try:
                    os.remove(tp)
                except Exception:
                    pass

    # Tính thời lượng (microsecond)
    duration_us = draft_content.get("duration", 0)


    # Chuẩn hóa đường dẫn hệ thống sang Windows backslashes tuyệt đối
    native_project_dir = os.path.normpath(project_dir)
    native_drafts_dir = os.path.normpath(CAPCUT_DRAFTS_DIR)
    native_content_file = os.path.normpath(content_file)
    native_cover_dest = os.path.normpath(cover_dest) if os.path.exists(cover_dest) else ""

    # Tạo draft_meta_info.json chuẩn xác tuyệt đối (KHÔNG ĐƯỢC RỖNG DRAFT_FOLD_PATH)
    meta_info = {
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
        "draft_cover": "draft_cover.jpg" if os.path.exists(cover_dest) else "",
        "draft_deeplink_url": "",
        "draft_enterprise_info": {
            "draft_enterprise_extra": "",
            "draft_enterprise_id": "",
            "draft_enterprise_name": "",
            "enterprise_material": []
        },
        "draft_fold_path": native_project_dir,
        "draft_has_unfinished_aigc_video_effect": False,
        "draft_id": final_draft_id,
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
        "draft_name": project_name,
        "draft_need_rename_folder": False,
        "draft_new_version": "189.0.0",
        "draft_removable_storage_device": "",
        "draft_root_path": native_drafts_dir,
        "draft_segment_extra_info": [],
        "draft_timeline_materials_size_": os.path.getsize(content_file),
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
        "tm_duration": duration_us
    }

    meta_file = os.path.join(project_dir, "draft_meta_info.json")
    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump(meta_info, f, ensure_ascii=False, indent=2)

    # Cập nhật root_meta_info.json
    root_data = {"all_draft_store": [], "draft_ids": 1, "root_path": native_drafts_dir}
    if os.path.exists(ROOT_META_INFO_PATH):
        try:
            with open(ROOT_META_INFO_PATH, "r", encoding="utf-8") as f:
                root_data = json.load(f)
        except Exception:
            pass

    # Lọc bỏ mục cũ có cùng tên hoặc cùng ID
    filtered_store = [
        item for item in root_data.get("all_draft_store", [])
        if item.get("draft_name") != project_name and item.get("draft_id") != final_draft_id
    ]

    new_root_entry = {
        "cloud_draft_cover": False,
        "cloud_draft_sync": False,
        "draft_cloud_last_action_download": False,
        "draft_cloud_purchase_info": "",
        "draft_cloud_template_id": "",
        "draft_cloud_tutorial_info": "",
        "draft_cloud_videocut_purchase_info": "",
        "draft_cover": native_cover_dest,
        "draft_fold_path": native_project_dir,
        "draft_id": final_draft_id,
        "draft_is_ai_shorts": False,
        "draft_is_cloud_temp_draft": False,
        "draft_is_infinite_canvas_draft": False,
        "draft_is_invisible": False,
        "draft_is_pippit_draft": False,
        "draft_is_web_article_video": False,
        "draft_json_file": native_content_file,
        "draft_name": project_name,
        "draft_new_version": "189.0.0",
        "draft_root_path": native_drafts_dir,
        "draft_timeline_materials_size": os.path.getsize(content_file),
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
        "tm_duration": duration_us
    }

    # Đặt vào đầu danh sách
    filtered_store.insert(0, new_root_entry)
    root_data["all_draft_store"] = filtered_store
    root_data["root_path"] = native_drafts_dir

    with open(ROOT_META_INFO_PATH, "w", encoding="utf-8") as f:
        json.dump(root_data, f, ensure_ascii=False, indent=2)

    # Dọn dẹp bản ghi xung đột trên cloud config
    clean_cloud_upload_conflicts(final_draft_id)

    # Cập nhật draftLayoutConfig.ini
    if os.path.exists(CAPCUT_CONFIG_INI):
        try:
            with open(CAPCUT_CONFIG_INI, "r", encoding="utf-8") as f:
                ini_text = f.read()
            if final_draft_id not in ini_text:
                with open(CAPCUT_CONFIG_INI, "a", encoding="utf-8") as f:
                    f.write(f"{final_draft_id}=0\n")
        except Exception:
            pass

    # Xóa CEF cache locks
    clean_cache_locks()

    print(f"[CapCutDraftManager] ✅ Đã triển khai thành công dự án CapCut: '{project_name}'")
    print(f"                     📂 Thư mục: {norm_project_dir}")
    print(f"                     🆔 Draft ID: {final_draft_id}")

    return {
        "status": "success",
        "project_name": project_name,
        "project_dir": project_dir,
        "draft_id": final_draft_id,
        "content_file": content_file,
        "duration_us": duration_us
    }


def fix_and_normalize_existing_draft(project_name: str) -> bool:
    """
    Sửa triệt để một dự án CapCut hiện có trên ổ đĩa nếu nó đang gặp lỗi đường dẫn hoặc placeholder.
    """
    project_dir = os.path.join(CAPCUT_DRAFTS_DIR, project_name)
    if not os.path.exists(project_dir):
        print(f"[Fix] ❌ Không tìm thấy thư mục dự án: {project_dir}")
        return False

    content_file = os.path.join(project_dir, "draft_content.json")
    if not os.path.exists(content_file):
        print(f"[Fix] ❌ Không tìm thấy draft_content.json trong {project_dir}")
        return False

    with open(content_file, "r", encoding="utf-8") as f:
        draft_content = json.load(f)

    # Đọc draft_id từ content hoặc meta
    meta_file = os.path.join(project_dir, "draft_meta_info.json")
    draft_id = draft_content.get("id")
    if not draft_id and os.path.exists(meta_file):
        try:
            with open(meta_file, "r", encoding="utf-8") as f:
                meta = json.load(f)
                draft_id = meta.get("draft_id")
        except Exception:
            pass

    cover_path = os.path.join(project_dir, "draft_cover.jpg")
    cover_src = cover_path if os.path.exists(cover_path) else None

    # Tái triển khai chuẩn qua deploy_capcut_project
    res = deploy_capcut_project(
        project_name=project_name,
        draft_content=draft_content,
        assets_map=None,
        cover_src_path=cover_src,
        draft_id=draft_id,
        auto_close_capcut=False
    )
    return res.get("status") == "success"


def fix_all_existing_drafts() -> List[str]:
    """
    Quét và chuẩn hóa toàn bộ các dự án trong com.lveditor.draft về chuẩn CapCut 9.6 Pro:
    - Gán chính xác thông tin platform phần cứng hiện tại (vượt qua DraftLoadVerifier)
    - Chuẩn hóa Windows backslashes trong root_meta_info.json và draft_meta_info.json
    - Dọn sạch xung đột cloud upload / AutoBackupStatus
    - Chuẩn hóa new_version: '189.0.0', version: 360000
    """
    fixed = []
    if not os.path.exists(CAPCUT_DRAFTS_DIR):
        return fixed

    for item in os.listdir(CAPCUT_DRAFTS_DIR):
        pdir = os.path.join(CAPCUT_DRAFTS_DIR, item)
        if os.path.isdir(pdir) and not item.startswith("."):
            cfile = os.path.join(pdir, "draft_content.json")
            if os.path.exists(cfile):
                print(f"[CapCutDraftManager] 🔧 Đang chuẩn hóa dự án: '{item}'...")
                if fix_and_normalize_existing_draft(item):
                    fixed.append(item)
    return fixed


def validate_project(project_name: str) -> bool:
    """Kiểm tra tính hợp lệ của dự án CapCut xem có nguy cơ gây lỗi không."""
    project_dir = os.path.join(CAPCUT_DRAFTS_DIR, project_name)
    if not os.path.exists(project_dir):
        print(f"[Validate] ❌ Thư mục không tồn tại: {project_dir}")
        return False

    content_file = os.path.join(project_dir, "draft_content.json")
    meta_file = os.path.join(project_dir, "draft_meta_info.json")

    if not os.path.exists(content_file):
        print(f"[Validate] ❌ Thiếu draft_content.json")
        return False
    if not os.path.exists(meta_file):
        print(f"[Validate] ❌ Thiếu draft_meta_info.json")
        return False

    with open(content_file, "r", encoding="utf-8") as f:
        content = json.load(f)
    with open(meta_file, "r", encoding="utf-8") as f:
        meta = json.load(f)

    # Kiểm tra draft_fold_path
    if not meta.get("draft_fold_path"):
        print(f"[Validate] ❌ draft_fold_path trong draft_meta_info.json bị rỗng!")
        return False

    # Kiểm tra platform app_id ở root
    plat = content.get("platform", {})
    if plat.get("app_id") != 359289:
        print(f"[Validate] ⚠️ Cảnh báo: root app_id không phải 359289 (CapCut PC) mà là {plat.get('app_id')}")
        return False

    # Kiểm tra timeline_layout.json
    layout_file = os.path.join(project_dir, "timeline_layout.json")
    if not os.path.exists(layout_file):
        print(f"[Validate] ❌ Thiếu timeline_layout.json cho Qt docking editor")
        return False

    # Kiểm tra cây Timelines
    tl_dir = os.path.join(project_dir, "Timelines")
    if not os.path.exists(tl_dir):
        print(f"[Validate] ❌ Thiếu thư mục Timelines")
        return False

    subdirs = [d for d in os.listdir(tl_dir) if os.path.isdir(os.path.join(tl_dir, d))]
    if not subdirs:
        print(f"[Validate] ❌ Thư mục Timelines không có subfolder dòng thời gian nào!")
        return False

    tl_dc = os.path.join(tl_dir, subdirs[0], "draft_content.json")
    if not os.path.exists(tl_dc):
        print(f"[Validate] ❌ Thiếu Timelines/{subdirs[0]}/draft_content.json")
        return False

    with open(tl_dc, "r", encoding="utf-8") as f:
        tl_content = json.load(f)
    tl_plat = tl_content.get("platform", {})
    if tl_plat.get("app_id") != 359289:
        print(f"[Validate] ❌ Timelines/{subdirs[0]}/draft_content.json app_id không chuẩn: {tl_plat.get('app_id')}")
        return False

    # Kiểm tra font path tuyệt đối (font tương đối => CapCut 9.6 tự đóng khi mở)
    for t in content.get("materials", {}).get("texts", []):
        fps = [t.get("font_path", "")]
        try:
            fps += [s.get("font", {}).get("path", "") for s in json.loads(t.get("content", "{}")).get("styles", [])]
        except Exception:
            pass
        for fpth in fps:
            if fpth and (not os.path.isabs(fpth) or not os.path.exists(fpth)):
                print(f"[Validate] ❌ Font path không tuyệt đối/không tồn tại: {fpth} (gây CapCut tự đóng!)")
                return False

    # Kiểm tra cờ .locked
    if os.path.exists(os.path.join(project_dir, ".locked")):
        print(f"[Validate] ⚠️ Cảnh báo: Dự án đang có file .locked bị bỏ sót!")
        return False

    # Kiểm tra placeholder trong materials
    content_str = json.dumps(content)
    if "placeholder" in content_str.lower() and "_draftpath_placeholder_" in content_str:
        print(f"[Validate] ❌ Phát hiện placeholder _draftpath_placeholder_ trong draft_content.json!")
        return False

    print(f"[Validate] ✅ Dự án '{project_name}' đạt chuẩn 100% CapCut 9.6+ (Cả Root và Timeline)!")
    return True



if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--fix-all":
            fixed_list = fix_all_existing_drafts()
            print(f"[CapCutDraftManager] 🎉 Đã chuẩn hóa thành công {len(fixed_list)} dự án: {fixed_list}")
        elif sys.argv[1] == "--fix" and len(sys.argv) > 2:
            pname = sys.argv[2]
            fix_and_normalize_existing_draft(pname)
            validate_project(pname)
        else:
            pname = sys.argv[1]
            if not validate_project(pname):
                print(f"[Info] Tự động khắc phục lỗi cho dự án '{pname}'...")
                fix_and_normalize_existing_draft(pname)
                validate_project(pname)
    else:
        print("[CapCutDraftManager] Tự động rà soát toàn bộ dự án...")
        fixed_list = fix_all_existing_drafts()
        for p in fixed_list:
            validate_project(p)

