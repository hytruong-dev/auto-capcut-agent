import os, sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

profiles_py = r"C:\Program Files\VoiceStudio\_up_\_up_\backend\api\routers\profiles.py"
with open(profiles_py, "r", encoding="utf-8") as f:
    text = f.read()

print("Profiles.py endpoints:")
for line in text.split('\n'):
    if line.strip().startswith('@router.'):
        print("  ", line.strip())
