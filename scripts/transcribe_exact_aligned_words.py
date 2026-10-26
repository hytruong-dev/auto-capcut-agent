"""
Transcribe chính xác từng từ bằng Whisper với initial_prompt cho 18 segments của OmniVoice.
Đảm bảo 100% từ bóc tách được có timestamp thực tế từ audio, không nội suy.
Xuất file: processed/exact_omnivoice_words.json
"""

import sys
import json
import whisper
import subprocess
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("[*] Đang tải mô hình Whisper base...")
    model = whisper.load_model("base")
    print("[+] Đã tải mô hình Whisper thành công.")

    timeline_path = Path("processed/omnivoice_176k_timeline.json")
    with open(timeline_path, "r", encoding="utf-8") as f:
        timeline_data = json.load(f)
    segments = timeline_data["segments"]

    results = []

    for seg in segments:
        seg_id = seg["id"]
        seg_file = seg["file"]
        master_start = seg["start"]
        text_prompt = seg["text"]

        print(f"[{seg_id:02d}/18] Transcribe chính xác: \"{text_prompt[:40]}...\"")
        res = model.transcribe(
            seg_file,
            language="vi",
            word_timestamps=True,
            initial_prompt=text_prompt
        )

        extracted_words = []
        for s in res.get("segments", []):
            for w in s.get("words", []):
                clean_w = w["word"].strip()
                if not clean_w:
                    continue
                w_s = round(w["start"], 3)
                w_e = round(w["end"], 3)
                extracted_words.append({
                    "word": clean_w,
                    "seg_start": w_s,
                    "seg_end": w_e,
                    "master_start": round(master_start + w_s, 3),
                    "master_end": round(master_start + w_e, 3)
                })

        print(f"    -> Bóc tách được {len(extracted_words)} từ thực tế.")

        results.append({
            "id": seg_id,
            "script_text": text_prompt,
            "seg_start": master_start,
            "seg_end": seg["end"],
            "words": extracted_words
        })

    out_file = Path("processed/exact_omnivoice_words.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n[+] ĐÃ HOÀN TẤT BÓC TÁCH TỪNG TỪ CHÍNH XÁC: {out_file}")

if __name__ == "__main__":
    main()
