"""
GHI BÀI HỌC MỚI VÀO BỘ NÃO ĐÃ TRAIN (để mọi phiên chat sau đều nhớ).

Dùng NGAY mỗi khi người dùng góp ý / chê / sửa / dạy điều mới:

    $env:PYTHONIOENCODING="utf-8"
    python scripts/brain_record_lesson.py `
        --rule "Phụ đề cỡ 70 thay vì 76 cho câu dài hơn 4 từ" `
        --mistake "Không để phụ đề tràn 2 dòng" `
        --project "Vlog_XanhSM_..." `
        --note "Người dùng chê phụ đề quá to ở video X"

--rule    : quy tắc mới (ghi vào mục 5 của learned_editing_style.md)
--mistake : lỗi cấm lặp lại (ghi vào do_not_repeat_mistakes)
--project / --note : ghi nhật ký phiên train
Có thể truyền nhiều --rule / --mistake.
"""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent
BRAIN = ROOT / "portable_trained_brain"
STYLE = BRAIN / "learned_editing_style.md"
HISTORY = BRAIN / "training_feedback_history.json"


def main():
    ap = argparse.ArgumentParser(description="Ghi bài học mới vào portable_trained_brain")
    ap.add_argument("--rule", action="append", default=[])
    ap.add_argument("--mistake", action="append", default=[])
    ap.add_argument("--project", default="")
    ap.add_argument("--note", default="")
    a = ap.parse_args()

    if not (a.rule or a.mistake or a.note):
        ap.error("Cần ít nhất một --rule, --mistake hoặc --note")

    now = datetime.now()
    today = now.strftime("%d/%m/%Y")

    # 1) Quy tắc -> learned_editing_style.md (cuối file = mục 5 Auto-Appended Rules)
    if a.rule:
        text = STYLE.read_text(encoding="utf-8").rstrip() + "\n"
        added = 0
        for r in a.rule:
            r = r.strip()
            if r and r not in text:
                text += f"- **[Train {today}{' - ' + a.project if a.project else ''}]** {r}\n"
                added += 1
        STYLE.write_text(text, encoding="utf-8")
        print(f"[+] Đã ghi {added} quy tắc mới vào {STYLE.relative_to(ROOT)}")

    # 2) Lỗi cấm lặp lại + nhật ký -> training_feedback_history.json
    hist = json.loads(HISTORY.read_text(encoding="utf-8"))
    mistakes = hist.setdefault("do_not_repeat_mistakes", [])
    new_m = [m.strip() for m in a.mistake if m.strip() and m.strip() not in mistakes]
    mistakes.extend(new_m)

    note_parts = [a.note] if a.note else []
    if a.rule:
        note_parts.append("Quy tắc: " + " | ".join(a.rule))
    if new_m:
        note_parts.append("Cấm lặp lại: " + " | ".join(new_m))
    hist.setdefault("session_logs", []).append({
        "timestamp": now.strftime("%Y-%m-%dT%H:%M:%S"),
        "project": a.project or "(không ghi tên)",
        "learned_note": ". ".join(note_parts),
    })
    hist["total_training_sessions"] = len(hist["session_logs"])
    HISTORY.write_text(json.dumps(hist, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[+] Đã ghi {len(new_m)} lỗi cấm lặp lại + 1 nhật ký vào {HISTORY.relative_to(ROOT)}")
    print("[OK] Bộ não đã được cập nhật — các phiên chat sau sẽ tự nạp bài học này.")


if __name__ == "__main__":
    main()
