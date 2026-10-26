import os, sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

fp = r"C:\Users\PC\AppData\Local\com.debpalash.omnivoice-studio\project\omnivoice\utils\voice_design.py"
with open(fp, "r", encoding="utf-8") as f:
    print(f.read())
