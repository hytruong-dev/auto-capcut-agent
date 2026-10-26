import os, sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

fp = r"C:\Users\PC\AppData\Local\com.debpalash.omnivoice-studio\project\omnivoice\models\omnivoice.py"
with open(fp, "r", encoding="utf-8") as f:
    cnt = f.read()

for term in ["guidance_scale", "position_temperature", "class_temperature", "temperature", "t_shift"]:
    count = cnt.count(term)
    print(f"Term '{term}': {count} occurrences")
