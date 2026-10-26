import os
import sys
import json
import shutil
import getpass
from pathlib import Path

def get_capcut_draft_dir() -> Path:
    local_app_data = os.environ.get("LOCALAPPDATA", "")
    if local_app_data:
        return Path(local_app_data) / "CapCut" / "User Data" / "Projects" / "com.lveditor.draft"
    return Path.home() / "Movies" / "CapCut" / "User Data" / "Projects" / "com.lveditor.draft"

def migrate_to_current_pc(silent: bool = False):
    project_root = Path(__file__).resolve().parent.parent
    current_user = getpass.getuser()
    capcut_draft_dir = get_capcut_draft_dir()
    brain_dir = project_root / "portable_trained_brain"

    if not silent:
        print("=================================================================")
        print(" KHỞI ĐỘNG ĐỒNG BỘ BỘ NÃO DI ĐỘNG (PORTABLE BRAIN MIGRATION) ")
        print("=================================================================")
        print(f"[*] Người dùng máy tính hiện tại : {current_user}")
        print(f"[*] Thư mục gốc dự án            : {project_root.as_posix()}")
        print(f"[*] Thư mục CapCut Drafts        : {capcut_draft_dir.as_posix()}")

    # 1. Tự động tạo thư mục CapCut Drafts nếu chưa có
    try:
        capcut_draft_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        if not silent:
            print(f"[!] Không thể tạo thư mục CapCut Drafts: {e}")

    # 2. Tự động nạp font Oswald-Bold.ttf vào CapCut Effect Cache để ngăn CapCut crash
    local_app_data = os.environ.get("LOCALAPPDATA", "")
    if local_app_data:
        effect_font_dir = Path(local_app_data) / "CapCut" / "User Data" / "Cache" / "effect" / "7182504807289065985" / "0a5333de6f4d592cb2d2390d68b31efb"
        source_font = brain_dir / "portable_assets" / "fonts" / "Oswald-Bold.ttf"
        if source_font.exists():
            try:
                effect_font_dir.mkdir(parents=True, exist_ok=True)
                dest_font = effect_font_dir / "Oswald-Bold.ttf"
                if not dest_font.exists():
                    shutil.copy2(source_font, dest_font)
                    if not silent:
                        print(f"[+] Đã tự động cài font Oswald-Bold vào CapCut Cache: {dest_font.as_posix()}")
            except Exception as e:
                if not silent:
                    print(f"[!] Lỗi khi cài font vào cache CapCut: {e}")

    # 3. Khôi phục Template_Trend_Pro từ Bộ Não Di Động vào CapCut Pro của máy mới
    backup_template = brain_dir / "capcut_pro_vault" / "Template_Trend_Pro_Backup"
    target_template = capcut_draft_dir / "Template_Trend_Pro"
    if backup_template.exists() and capcut_draft_dir.exists():
        if not target_template.exists():
            try:
                shutil.copytree(backup_template, target_template)
                if not silent:
                    print(f"[+] Đã khôi phục project mẫu 'Template_Trend_Pro' vào CapCut Pro của máy mới!")
            except Exception as e:
                if not silent:
                    print(f"[!] Lỗi khôi phục Template_Trend_Pro: {e}")
        else:
            if not silent:
                print(f"[*] Project mẫu 'Template_Trend_Pro' đã tồn tại sẵn trên máy này.")

    # 4. Tự động cập nhật đường dẫn tuyệt đối trong mcp_config.json cho máy mới
    vectcut_dir = (project_root / "tools" / "VectCutAPI").as_posix()
    mcp_config = {
        "mcpServers": {
            "capcut-mcp": {
                "command": "python",
                "args": ["mcp_server.py"],
                "cwd": vectcut_dir,
                "env": {
                    "PYTHONPATH": vectcut_dir
                }
            },
            "windows-mcp": {
                "command": "uvx",
                "args": ["windows-mcp", "serve"]
            }
        }
    }
    mcp_config_path = project_root / "mcp_config.json"
    try:
        with open(mcp_config_path, "w", encoding="utf-8") as f:
            json.dump(mcp_config, f, ensure_ascii=False, indent=2)
        if not silent:
            print(f"[+] Đã tự động cập nhật đường dẫn máy mới vào: {mcp_config_path.name}")
    except Exception as e:
        if not silent:
            print(f"[!] Lỗi cập nhật mcp_config.json: {e}")

    # 5. Cập nhật trạng thái máy tính hiện tại vào BRAIN_INDEX.md
    brain_index_path = brain_dir / "BRAIN_INDEX.md"
    if brain_index_path.exists():
        try:
            content = brain_index_path.read_text(encoding="utf-8")
            lines = content.splitlines()
            new_lines = []
            for line in lines:
                if line.startswith("- **Last Active OS User:**"):
                    new_lines.append(f"- **Last Active OS User:** `{current_user}`")
                elif line.startswith("- **CapCut Drafts Directory:**"):
                    new_lines.append(f"- **CapCut Drafts Directory:** `{capcut_draft_dir.as_posix()}`")
                elif line.startswith("- **Project Root Directory:**"):
                    new_lines.append(f"- **Project Root Directory:** `{project_root.as_posix()}`")
                else:
                    new_lines.append(line)
            brain_index_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
            if not silent:
                print(f"[+] Đã đồng bộ thông tin máy tính mới vào: portable_trained_brain/BRAIN_INDEX.md")
        except Exception as e:
            if not silent:
                print(f"[!] Lỗi cập nhật BRAIN_INDEX.md: {e}")

    # 6. Kiểm tra phụ thuộc môi trường
    if not silent:
        print("\n--- KIỂM TRA MÔI TRƯỜNG MÁY MỚI ---")
        ffmpeg_ok = shutil.which("ffmpeg") is not None
        ffprobe_ok = shutil.which("ffprobe") is not None
        print(f"  [{'✓' if ffmpeg_ok else '✗'}] FFmpeg: {'Sẵn sàng' if ffmpeg_ok else 'THIẾU (Cài qua: winget install Gyan.FFmpeg)'}")
        print(f"  [{'✓' if ffprobe_ok else '✗'}] FFprobe: {'Sẵn sàng' if ffprobe_ok else 'THIẾU (Đi kèm FFmpeg)'}")
        try:
            import whisper
            print("  [✓] OpenAI Whisper: Sẵn sàng")
        except ImportError:
            try:
                import faster_whisper
                print("  [✓] Faster Whisper: Sẵn sàng")
            except ImportError:
                print("  [!] Whisper: Chưa cài đặt (Chạy: pip install -r requirements.txt)")

        print("=================================================================")
        print(" HOÀN TẤT! ANTIGRAVITY ĐÃ NẠP 100% DỮ LIỆU ĐÃ TRAIN TRƯỚC ĐÓ. ")
        print("=================================================================")

if __name__ == "__main__":
    migrate_to_current_pc()
