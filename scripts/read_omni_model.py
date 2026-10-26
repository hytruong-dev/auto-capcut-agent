import os

omni_py = r"C:\Users\PC\AppData\Local\com.debpalash.omnivoice-studio\project\omnivoice\models\omnivoice.py"
with open(omni_py, "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx, line in enumerate(lines[:120], 1):
    print(f"{idx}: {line.rstrip()}")
