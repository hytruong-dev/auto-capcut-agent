import os

base = r"C:\Users\PC\AppData\Local\OmniVoice"
for root, dirs, files in os.walk(base):
    for f in files:
        fp = os.path.join(root, f)
        print(f"{fp} ({os.path.getsize(fp):,} bytes)")
