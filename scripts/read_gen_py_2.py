import os, sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

gen_py = r"C:\Program Files\VoiceStudio\_up_\_up_\backend\api\routers\generation.py"
with open(gen_py, "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx, line in enumerate(lines[100:200], 101):
    print(f"{idx}: {line.rstrip()}")
