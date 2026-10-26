import os, sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

base = r"C:\Program Files\VoiceStudio\_up_\_up_"
for sub in ["backend", "omnivoice"]:
    p = os.path.join(base, sub)
    print(f"\n--- {sub} ---")
    if os.path.exists(p):
        for root, dirs, files in os.walk(p):
            rel = os.path.relpath(root, p)
            if rel == '.':
                print(f"Root files in {sub}:")
                for f in files:
                    print(f"  {f}")
                print(f"Dirs in {sub}: {dirs}")
