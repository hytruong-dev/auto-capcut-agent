import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

data = json.load(open('processed/exact_omnivoice_words.json', encoding='utf-8'))
for seg_id in [4, 6, 7, 9]:
    seg = [d for d in data if d['id'] == seg_id][0]
    print(f"\n=== SEG {seg_id} ===")
    print("Script:", seg['script_text'])
    print("Words:", [(w['word'], w['seg_start'], w['seg_end']) for w in seg['words']])
