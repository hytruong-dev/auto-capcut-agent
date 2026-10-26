import os, sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

paths_to_check = [
    r"C:\Program Files\VoiceStudio",
    r"C:\Users\PC\AppData\Local\OmniVoice",
    r"C:\Users\PC\AppData\Local\com.debpalash.omnivoice-studio",
    r"C:\Users\PC\AppData\Roaming\OmniVoice",
    r"C:\Users\PC\AppData\Roaming\com.debpalash.omnivoice-studio",
]

for p in paths_to_check:
    print(f"\nChecking {p}:")
    if os.path.exists(p):
        for root, dirs, files in os.walk(p):
            for d in dirs:
                if 'venv' in d.lower() or 'python' in d.lower() or 'env' in d.lower() or 'model' in d.lower():
                    print(f"  [DIR] {os.path.join(root, d)}")
            for f in files:
                if f.endswith('.exe') or f.endswith('.sqlite') or f.endswith('.db') or f.endswith('.pt') or f.endswith('.onnx') or f.endswith('.safetensors') or f.endswith('.bin'):
                    fp = os.path.join(root, f)
                    print(f"  [FILE] {fp} ({os.path.getsize(fp)} bytes)")
    else:
        print("  Does not exist.")
