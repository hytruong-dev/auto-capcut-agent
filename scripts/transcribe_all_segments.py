import whisper, json, sys, os, subprocess

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

print("[*] Loading Whisper model...")
model = whisper.load_model("base")

seg_files = [f"processed/voiceover/story_segments/seg_{i:02d}.mp3" for i in range(1, 20)]

# Tính exact offset của từng segment trong master audio
accum_time = 0.0
all_segment_data = []

for idx, sf in enumerate(seg_files, 1):
    res = subprocess.run(["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", sf], capture_output=True, text=True)
    d = float(json.loads(res.stdout)["format"]["duration"])
    seg_start = accum_time
    seg_end = accum_time + d
    accum_time = seg_end
    
    print(f"[*] Transcribing Seg {idx:02d} ({seg_start:.2f}s -> {seg_end:.2f}s)...")
    trans_res = model.transcribe(sf, language="vi", word_timestamps=True)
    
    words = []
    for s in trans_res.get("segments", []):
        for w in s.get("words", []):
            words.append({
                "word": w["word"].strip(),
                "seg_start": round(w["start"], 3),
                "seg_end": round(w["end"], 3),
                "master_start": round(seg_start + w["start"], 3),
                "master_end": round(seg_start + w["end"], 3)
            })
    
    all_segment_data.append({
        "seg_id": idx,
        "seg_start": round(seg_start, 3),
        "seg_end": round(seg_end, 3),
        "seg_dur": round(d, 3),
        "text": trans_res.get("text", "").strip(),
        "words": words
    })

out_path = "processed/exact_segment_words.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(all_segment_data, f, ensure_ascii=False, indent=2)

print(f"[SUCCESS] Saved exact segment word data to: {out_path}")
for sd in all_segment_data:
    print(f"Seg {sd['seg_id']:02d}: {sd['seg_start']:5.2f}s - {sd['seg_end']:5.2f}s | {len(sd['words'])} words | {sd['text']}")
