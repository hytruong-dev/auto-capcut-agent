import os, sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

base = r"C:\Program Files\VoiceStudio\_up_\_up_"
print(f"Listing {base}:")
for item in os.listdir(base):
    p = os.path.join(base, item)
    is_d = os.path.isdir(p)
    print(f"  {'[DIR] ' if is_d else '      '}{item}")
