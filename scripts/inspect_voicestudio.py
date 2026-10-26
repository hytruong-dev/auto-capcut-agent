import os, sys, subprocess, json

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

vs_dir = r"C:\Program Files\VoiceStudio"
print(f"Checking {vs_dir}...")
if os.path.exists(vs_dir):
    for root, dirs, files in os.walk(vs_dir):
        depth = root.count(os.sep) - vs_dir.count(os.sep)
        if depth <= 2:
            print(f"Dir: {root}")
            for f in files[:10]:
                fp = os.path.join(root, f)
                sz = os.path.getsize(fp)
                print(f"  {f} ({sz} bytes)")

# Check Start Menu shortcut for VoiceStudio
start_menu = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs"
user_start = os.path.expanduser(r"~\AppData\Roaming\Microsoft\Windows\Start Menu\Programs")
for sm in [start_menu, user_start]:
    if os.path.exists(sm):
        for root, dirs, files in os.walk(sm):
            for f in files:
                if 'voice' in f.lower():
                    print(f"Found shortcut: {os.path.join(root, f)}")

# Check AppData for VoiceStudio
appdata = os.path.expanduser(r"~\AppData\Roaming")
localapp = os.path.expanduser(r"~\AppData\Local")
for ad in [appdata, localapp]:
    for item in os.listdir(ad):
        if 'voice' in item.lower() or 'omni' in item.lower():
            print(f"Found AppData: {os.path.join(ad, item)}")
