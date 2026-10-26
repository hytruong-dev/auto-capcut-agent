import os, sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

readme_path = r"C:\Program Files\VoiceStudio\_up_\_up_\README.md"
with open(readme_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx, line in enumerate(lines[250:400], 251):
    print(f"{idx}: {line.rstrip()}")
