import whisper, json, sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

print("Loading whisper base...")
model = whisper.load_model("base")

audio_file = r"c:\QuangHy\editvideo\processed\voiceover\download_full.wav"
print(f"Transcribing {audio_file} (first 60s)...")

# Transcribe first 60 seconds
result = model.transcribe(audio_file, language="vi", verbose=False)

segments = []
for seg in result["segments"][:25]:
    print(f"[{seg['start']:.2f}s -> {seg['end']:.2f}s] {seg['text']}")
    segments.append({
        "start": seg["start"],
        "end": seg["end"],
        "text": seg["text"]
    })

with open(r"c:\QuangHy\editvideo\processed\voiceover\ref_transcript.json", "w", encoding="utf-8") as f:
    json.dump(segments, f, ensure_ascii=False, indent=2)
