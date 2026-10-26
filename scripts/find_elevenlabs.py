import os, sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

backend_dir = r"C:\Program Files\VoiceStudio\_up_\_up_\backend"
hits = []
for root, dirs, files in os.walk(backend_dir):
    for f in files:
        if f.endswith('.py') or f.endswith('.json'):
            fp = os.path.join(root, f)
            try:
                with open(fp, 'r', encoding='utf-8', errors='ignore') as fl:
                    cnt = fl.read()
                    if 'elevenlabs' in cnt.lower():
                        hits.append(fp)
            except Exception:
                pass

print("Hits for elevenlabs in VoiceStudio:")
for h in hits:
    print(" ", h)
