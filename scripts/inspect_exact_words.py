import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

data = json.load(open('processed/omnivoice_176k_words.json', encoding='utf-8'))
for item in data:
    print(f"\n=== SEG {item['id']:02d} ({item['seg_start']:.2f}s -> {item['seg_end']:.2f}s) ===")
    print("Script text: ", item['text'])
    print("Whisper text:", ' '.join(w['word'] for w in item['words']))
    flat_p = [w for p in item['phrases'] for w in p]
    print("Phrases text:", ' '.join(flat_p))
