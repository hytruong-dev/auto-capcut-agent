import os, sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

fp = r"C:\Users\PC\AppData\Local\com.debpalash.omnivoice-studio\project\omnivoice\models\omnivoice.py"
with open(fp, "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx, line in enumerate(lines, 1):
    if "temperature" in line.lower() or "guidance_scale" in line.lower():
        print(f"{idx}: {line.strip()}")
