import json

data = json.load(open('processed/omnivoice_176k_words.json', encoding='utf-8'))
for item in data:
    flat = [w for p in item['phrases'] for w in p]
    w_count = len(item['words'])
    dur = item['seg_end'] - item['seg_start']
    print(f"Seg {item['id']:02d}: {len(flat):2d} phrase words vs {w_count:2d} whisper words | {item['seg_start']:.2f}s -> {item['seg_end']:.2f}s ({dur:.2f}s)")
