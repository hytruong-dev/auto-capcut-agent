"""
NẠP BỘ NÃO ĐÃ TRAIN — chạy ở ĐẦU MỖI PHIÊN CHAT MỚI.

    $env:PYTHONIOENCODING="utf-8"; python scripts/load_brain.py

In ra toàn bộ quy chuẩn đã train + danh sách lỗi cấm lặp lại, đồng thời kiểm tra
font / SFX / BGM / FFmpeg / Whisper để AI không phải đoán và không dùng gu mặc định.
"""
import importlib.util
import json
import shutil
import sys
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
ASSETS = BRAIN / "portable_assets"


def line(title=""):
    print("\n" + "=" * 70)
    if title:
        print(title)
        print("=" * 70)


def check(label, ok, detail=""):
    print(f"  [{'OK' if ok else 'THIẾU'}] {label}{(' - ' + detail) if detail else ''}")
    return ok


def main():
    if not STYLE.exists() or not HISTORY.exists():
        print("[LỖI] Không tìm thấy portable_trained_brain/. Không được tự bịa quy chuẩn — hãy báo người dùng.")
        sys.exit(1)

    history = json.loads(HISTORY.read_text(encoding="utf-8"))
    mistakes = history.get("do_not_repeat_mistakes", [])
    logs = history.get("session_logs", [])

    line("1) QUY CHUẨN DỰNG VIDEO ĐÃ TRAIN (learned_editing_style.md) — BẮT BUỘC TUÂN THỦ")
    print(STYLE.read_text(encoding="utf-8"))

    line(f"2) {len(mistakes)} LỖI CẤM LẶP LẠI (do_not_repeat_mistakes)")
    for i, m in enumerate(mistakes, 1):
        print(f"  {i:2d}. {m}")

    line(f"3) {min(3, len(logs))} BÀI HỌC GẦN NHẤT (trên tổng {len(logs)} phiên train)")
    for log in logs[-3:]:
        print(f"  - [{log.get('timestamp', '')}] {log.get('project', '')}: {log.get('learned_note', '')}")

    line("4) KIỂM TRA TÀI NGUYÊN & MÔI TRƯỜNG")
    all_ok = True
    all_ok &= check("Font Oswald-Bold", (ASSETS / "fonts" / "Oswald-Bold.ttf").exists(),
                    "portable_trained_brain/portable_assets/fonts/Oswald-Bold.ttf")
    for sfx in ["whoosh_fast.mp3", "ding_highlight.mp3", "cash_register.mp3", "ting_money.mp3",
                "pop_bubble.mp3", "riser_tension.mp3"]:
        all_ok &= check(f"SFX {sfx}", (ASSETS / "sfx" / sfx).exists())
    bgms = sorted(p.name for p in (ASSETS / "bgm").glob("*.mp3")) if (ASSETS / "bgm").exists() else []
    all_ok &= check("BGM", bool(bgms), ", ".join(bgms))
    all_ok &= check("ffmpeg trong PATH", shutil.which("ffmpeg") is not None)
    all_ok &= check("ffprobe trong PATH", shutil.which("ffprobe") is not None)
    has_whisper = any(importlib.util.find_spec(m) is not None for m in ("whisper", "faster_whisper"))
    all_ok &= check("Whisper (word timestamps)", has_whisper, "pip install openai-whisper nếu thiếu")
    check("CapCut draft manager", (ROOT / "scripts" / "capcut_draft_manager.py").exists())

    index = BRAIN / "BRAIN_INDEX.md"
    if index.exists() and str(ROOT).replace("\\", "/").lower() not in index.read_text(encoding="utf-8").lower():
        print("  [CẢNH BÁO] Đường dẫn dự án khác BRAIN_INDEX.md → máy mới. Chạy: python scripts/migrate_brain_to_new_pc.py")

    line("5) CÔNG CỤ CHUẨN — DÙNG LẠI, KHÔNG VIẾT LẠI TỪ ĐẦU")
    print("  - Phụ đề karaoke + Hook 2 tầng : python scripts/brain_karaoke_ass.py --words <words.json> --out processed/<ten>.ass --hook1 \"...\" --hook2 \"...\"")
    print("  - Dự án CapCut 9.6 Pro         : scripts/capcut_draft_manager.py (deploy_capcut_project / fix_and_normalize_existing_draft)")
    print("  - Ghi bài học mới vào bộ não   : python scripts/brain_record_lesson.py --rule \"...\" --mistake \"...\" --project \"...\"")
    print("  - Kiểm định tự hành Pre-flight : python scripts/brain_preflight_qa.py --video processed/<out>.mp4 --sub processed/<sub.ass>")
    print("  - Pipeline mẫu đã được duyệt   : scripts/build_exact_synced_karaoke.py + scripts/render_xanhsm_176k_video.py")

    line("TÓM TẮT")
    print(f"Đã nạp bộ não đã train: {len(mistakes)} lỗi cấm lặp lại, {len(logs)} phiên train. "
          f"Tài nguyên: {'đầy đủ' if all_ok else 'CÒN THIẾU (xem mục 4)'}.")
    print("Nhắc lại: Oswald-Bold IN HOA, Vàng #F0FF00 + Cyan #66FFFF từ đang đọc, Y=-0.38 (MarginV 550), "
          "cụm 2-4 từ (<= 26 ký tự) theo timestamp Whisper thật, Hook 2 tầng Đỏ/Vàng, BGM 0.14-0.16, voice -14 LUFS.")


if __name__ == "__main__":
    main()
