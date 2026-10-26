import os, sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

gen_py = r"C:\Program Files\VoiceStudio\_up_\_up_\backend\api\routers\generation.py"
with open(gen_py, "r", encoding="utf-8") as f:
    content = f.read()

print(f"Total characters: {len(content)}")
# find occurrences of infer, clone, ref_audio, omnivoice
for line in content.splitlines():
    if any(k in line.lower() for k in ["omnivoice", "clone", "ref_audio", "reference", "infer", "def generate"]):
        print(line[:120])
