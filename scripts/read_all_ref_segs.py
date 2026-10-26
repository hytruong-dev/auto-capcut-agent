import json, sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open(r"c:\QuangHy\editvideo\processed\voiceover\ref_transcript.json", "r", encoding="utf-8") as f:
    segs = json.load(f)

print("All segments from ref_transcript.json:")
for idx, s in enumerate(segs):
    print(f"[{s['start']:5.1f}s -> {s['end']:5.1f}s] {s['text']}")
