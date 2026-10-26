import os, sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

main_py = r"C:\Program Files\VoiceStudio\_up_\_up_\backend\main.py"
with open(main_py, "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx, line in enumerate(lines[:60], 1):
    print(f"{idx}: {line.rstrip()}")
