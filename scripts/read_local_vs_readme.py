import os, sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

readme_path = r"C:\Program Files\VoiceStudio\_up_\_up_\README.md"
with open(readme_path, "r", encoding="utf-8") as f:
    text = f.read()

print(f"README length: {len(text)} chars")
# Print sections containing 'cli', 'api', 'clone', 'run'
for line in text.split('\n')[:80]:
    print(line)
