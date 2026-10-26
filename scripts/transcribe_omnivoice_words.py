"""
Bóc tách word-level timestamps bằng Whisper cho 18 audio segments của OmniVoice.
Xuất file: processed/omnivoice_176k_words.json
"""

import sys
import json
import whisper
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

def transcribe_words():
    print("[*] Đang tải mô hình Whisper base...")
    model = whisper.load_model("base")
    print("[+] Đã tải mô hình Whisper.")

    timeline_path = Path("processed/omnivoice_176k_timeline.json")
    with open(timeline_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    segments = data["segments"]

    result_data = []

    for seg in segments:
        seg_id = seg["id"]
        seg_file = seg["file"]
        master_start = seg["start"]
        phrases = seg["phrases"]

        print(f"[{seg_id:02d}/18] Transcribe {Path(seg_file).name}...")
        res = model.transcribe(seg_file, language="vi", word_timestamps=True)
        
        words = []
        for s in res.get("segments", []):
            for w in s.get("words", []):
                words.append({
                    "word": w["word"].strip(),
                    "start": round(w["start"], 3),
                    "end": round(w["end"], 3),
                    "master_start": round(master_start + w["start"], 3),
                    "master_end": round(master_start + w["end"], 3)
                })

        result_data.append({
            "id": seg_id,
            "text": seg["text"],
            "phrases": phrases,
            "seg_start": master_start,
            "seg_end": seg["end"],
            "words": words
        })

    out_file = Path("processed/omnivoice_176k_words.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(result_data, f, ensure_ascii=False, indent=2)

    print(f"\n[+] ĐÃ HOÀN TẤT TRANSCRIBE WORD TIMESTAMPS: {out_file}")

if __name__ == "__main__":
    transcribe_words()
