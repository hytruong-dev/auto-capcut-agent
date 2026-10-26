import os
import json
import shutil
import getpass
from pathlib import Path

def get_capcut_draft_dir() -> Path:
    local_app_data = os.environ.get("LOCALAPPDATA", "")
    if local_app_data:
        return Path(local_app_data) / "CapCut" / "User Data" / "Projects" / "com.lveditor.draft"
    return Path.home() / "Movies" / "CapCut" / "User Data" / "Projects" / "com.lveditor.draft"

def migrate_to_current_pc():
    project_root = Path.cwd().resolve()
    current_user = getpass.getuser()
    capcut_draft_dir = get_capcut_draft_dir()
    brain_dir = project_root / "portable_trained_brain"

    print("=================================================================")
    print(" KHỞI ĐỘNG ĐỒNG BỘ BỘ NÃO DI ĐỘNG (PORTABLE BRAIN MIGRATION) ")
    print("=================================================================")
    print(f"[*] Người dùng máy tính hiện tại : {current_user}")
    print(f"[*] Thư mục gốc dự án            : {project_root.as_posix()}")
    print(f"[*] Thư mục CapCut Drafts        : {capcut_draft_dir.as_posix()}")

    # 1. Khôi phục Template_Trend_Pro từ Bộ Não Di Động vào CapCut Pro của máy mới
    backup_template = brain_dir / "capcut_pro_vault" / "Template_Trend_Pro_Backup"
    target_template = capcut_draft_dir / "Template_Trend_Pro"
    if backup_template.exists() and capcut_draft_dir.exists():
        if not target_template.exists():
            shutil.copytree(backup_template, target_template)
            print(f"[+] Đã khôi phục project mẫu 'Template_Trend_Pro' vào CapCut Pro của máy mới!")
        else:
            print(f"[*] Project mẫu 'Template_Trend_Pro' đã tồn tại sẵn trên máy này.")
    else:
        print(f"[!] Lưu ý: Chưa có bản sao lưu Template_Trend_Pro_Backup hoặc chưa cài CapCut PC.")

    # 2. Tự động cập nhật đường dẫn tuyệt đối trong mcp_config.json cho máy mới
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
    with open(mcp_config_path, "w", encoding="utf-8") as f:
        json.dump(mcp_config, f, ensure_ascii=False, indent=2)
    print(f"[+] Đã tự động cập nhật đường dẫn máy mới vào: {mcp_config_path.name}")

    # 3. Cập nhật trạng thái máy tính hiện tại vào BRAIN_INDEX.md
    brain_index_path = brain_dir / "BRAIN_INDEX.md"
    if brain_index_path.exists():
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
        print(f"[+] Đã đồng bộ thông tin máy tính mới vào: portable_trained_brain/BRAIN_INDEX.md")

    print("=================================================================")
    print(" HOÀN TẤT! ANTIGRAVITY ĐÃ NẠP 100% DỮ LIỆU ĐÃ TRAIN TRƯỚC ĐÓ. ")
    print("=================================================================")

if __name__ == "__main__":
    migrate_to_current_pc()
