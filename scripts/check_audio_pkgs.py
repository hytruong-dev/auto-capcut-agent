import sys
print("Python:", sys.executable)
for mod in ["whisper", "faster_whisper", "whisperx", "torchaudio", "soundfile"]:
    try:
        __import__(mod)
        print(f"  [OK] {mod}")
    except Exception as e:
        print(f"  [NO] {mod}: {e}")
