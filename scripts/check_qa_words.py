import json, sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

data = json.load(open('processed/exact_segment_words.json', encoding='utf-8'))
for w in data[0]['words'][:10]:
    print(f"Seg 1 word: {w['word']:15} [{w['master_start']:.2f}s -> {w['master_end']:.2f}s]")

for w in data[1]['words'][:6]:
    print(f"Seg 2 word: {w['word']:15} [{w['master_start']:.2f}s -> {w['master_end']:.2f}s]")
