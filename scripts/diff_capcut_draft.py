import json
import sys
from datetime import datetime
from pathlib import Path

def summarize_draft(draft_json_path: Path) -> dict:
    with open(draft_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    tracks = data.get("tracks", [])
    summary = {
        "track_count": len(tracks),
        "segments_by_type": {},
        "transitions_used": [t.get("name", t.get("effect_id")) for t in data.get("materials", {}).get("transitions", [])],
        "video_effects_used": [e.get("name", e.get("effect_id")) for e in data.get("materials", {}).get("video_effects", [])]
    }
    for track in tracks:
        t_type = track.get("type", "unknown")
        segs = track.get("segments", [])
        summary["segments_by_type"].setdefault(t_type, 0)
        summary["segments_by_type"][t_type] += len(segs)
    return summary

def record_learning_to_portable_brain(before: dict, after: dict, note: str = ""):
    history_path = Path("portable_trained_brain/training_feedback_history.json")
    if history_path.exists():
        with open(history_path, "r", encoding="utf-8") as f:
            history = json.load(f)
    else:
        history = {"total_training_sessions": 0, "do_not_repeat_mistakes": [], "session_logs": []}

    history["total_training_sessions"] = history.get("total_training_sessions", 0) + 1
    history["session_logs"].append({
        "timestamp": datetime.now().isoformat(),
        "ai_initial": before,
        "user_corrected": after,
        "learned_note": note or "Người dùng đã tinh chỉnh lại cấu trúc timeline/hiệu ứng trên CapCut Pro."
    })

    history_path.parent.mkdir(parents=True, exist_ok=True)
    with open(history_path, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    print(f"[+] Đã ghi nhận bài học mới vào Bộ Não Di Động: {history_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Cách dùng: python scripts/diff_capcut_draft.py <ban_goc_ai.json> <ban_nguoi_dung_sua.json> [ghi_chu_bai_hoc]")
        sys.exit(1)
    before_summary = summarize_draft(Path(sys.argv[1]))
    after_summary = summarize_draft(Path(sys.argv[2]))
    custom_note = sys.argv[3] if len(sys.argv) >= 4 else ""
    record_learning_to_portable_brain(before_summary, after_summary, custom_note)
    print(json.dumps({"ai_generated": before_summary, "user_modified": after_summary}, ensure_ascii=False, indent=2))
