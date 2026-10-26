import json, sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

words = json.load(open('processed/voiceover_words.json', encoding='utf-8'))
print(f"Total whisper words: {len(words)}")

for i in range(min(40, len(words))):
    w = words[i]
    print(f"{i:3d}: [{w['start']:5.2f} - {w['end']:5.2f}] {w['word']}")
