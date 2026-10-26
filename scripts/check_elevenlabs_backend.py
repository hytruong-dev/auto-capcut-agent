import os, sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

fp = r"C:\Program Files\VoiceStudio\_up_\_up_\backend\services\tts_backend.py"
with open(fp, "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

for idx, line in enumerate(lines, 1):
    if "elevenlabs" in line.lower():
        start = max(1, idx - 5)
        end = min(len(lines), idx + 10)
        print(f"--- Around line {idx} ---")
        for i in range(start, end):
            print(f"{i}: {lines[i-1].rstrip()}")
