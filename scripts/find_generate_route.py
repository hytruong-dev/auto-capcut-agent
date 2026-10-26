import os, sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

gen_py = r"C:\Program Files\VoiceStudio\_up_\_up_\backend\api\routers\generation.py"
with open(gen_py, "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx, line in enumerate(lines, 1):
    if '@router.post("/generate"' in line:
        print(f"Found on line {idx}:")
        for j in range(idx - 1, min(len(lines), idx + 40)):
            print(f"{j+1}: {lines[j].rstrip()}")
        break
