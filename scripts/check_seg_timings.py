import json, sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

whisper_words = json.load(open('processed/voiceover_words.json', encoding='utf-8'))

# Let's inspect the 19 audio segments directly!
# Remember each sentence was generated as seg_01.mp3 ... seg_19.mp3!
# We can run ffprobe on each seg_01 ... seg_19 to get their exact duration in the concatenated master!
import subprocess
from pathlib import Path

seg_files = [f"processed/voiceover/story_segments/seg_{i:02d}.mp3" for i in range(1, 20)]
accum_time = 0.0
seg_timings = []

for idx, sf in enumerate(seg_files, 1):
    res = subprocess.run(["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", sf], capture_output=True, text=True)
    d = float(json.loads(res.stdout)["format"]["duration"])
    start = accum_time
    end = accum_time + d
    accum_time = end
    seg_timings.append({
        "id": idx,
        "start": start,
        "end": end,
        "dur": d,
        "file": sf
    })
    print(f"Seg {idx:02d}: {start:5.2f}s -> {end:5.2f}s (dur: {d:4.2f}s)")

print(f"Total concatenated duration: {accum_time:5.2f}s")
