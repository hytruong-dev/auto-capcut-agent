import os, sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

api_dir = r"C:\Program Files\VoiceStudio\_up_\_up_\backend\api"
print(f"Files in {api_dir}:")
for root, dirs, files in os.walk(api_dir):
    for f in files:
        rel = os.path.relpath(os.path.join(root, f), api_dir)
        print(f"  {rel}")
