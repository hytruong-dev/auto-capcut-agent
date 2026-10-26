import os
import json
import shutil
from pathlib import Path
try:
    import pycapcut as cc
except ImportError:
    cc = None

def get_default_capcut_draft_dir() -> Path:
    local_app_data = os.environ.get("LOCALAPPDATA", "")
    if local_app_data:
        return Path(local_app_data) / "CapCut" / "User Data" / "Projects" / "com.lveditor.draft"
    # Hỗ trợ thêm macOS nếu chuyển sang máy Mac
    return Path.home() / "Movies" / "CapCut" / "User Data" / "Projects" / "com.lveditor.draft"

def sync_and_backup_capcut_pro_effects(
    template_name: str = "Template_Trend_Pro",
    vault_dir: str = "portable_trained_brain/capcut_pro_vault"
):
    draft_dir = get_default_capcut_draft_dir()
    template_path = draft_dir / template_name
    vault_path = Path(vault_dir)
    vault_path.mkdir(parents=True, exist_ok=True)

    if not template_path.exists():
        print(f"[!] Chưa tìm thấy project mẫu '{template_name}' tại: {draft_dir}")
        print("[*] Hướng dẫn: Hãy mở CapCut Pro, tạo 1 project đặt tên 'Template_Trend_Pro' và kéo các hiệu ứng Pro yêu thích vào đó.")
        return

    print(f"[*] Đang quét mã hiệu ứng CapCut Pro từ: {template_path}...")
    if cc:
        try:
            draft_folder = cc.DraftFolder(str(draft_dir))
            draft_folder.inspect_material(template_name)
        except Exception as e:
            print(f"[!] Cảnh báo khi gọi inspect_material: {e}")

    draft_content_path = template_path / "draft_content.json"
    if draft_content_path.exists():
        with open(draft_content_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        materials = data.get("materials", {})
        extracted_catalog = {
            "video_effects": materials.get("video_effects", []),
            "transitions": materials.get("transitions", []),
            "text_animations": materials.get("material_animations", []),
            "stickers": materials.get("stickers", []),
            "filters": materials.get("effects", []),
            "audio_effects": materials.get("audio_effects", [])
        }

        output_json = vault_path / "capcut-pro-effects.json"
        with open(output_json, "w", encoding="utf-8") as out_f:
            json.dump(extracted_catalog, out_f, ensure_ascii=False, indent=2)
        print(f"[+] Đã lưu từ điển mã hiệu ứng CapCut Pro vào: {output_json}")

    # Sao lưu toàn bộ thư mục Template_Trend_Pro vào portable_trained_brain để mang sang máy tính khác
    backup_target = vault_path / "Template_Trend_Pro_Backup"
    if backup_target.exists():
        shutil.rmtree(backup_target)
    shutil.copytree(template_path, backup_target)
    print(f"[+] Đã sao lưu toàn bộ gói project mẫu vào Bộ Não Di Động: {backup_target}")

if __name__ == "__main__":
    sync_and_backup_capcut_pro_effects()
