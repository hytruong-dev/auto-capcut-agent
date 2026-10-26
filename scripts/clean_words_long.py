import json
import sys
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

data = json.load(open('processed/exact_words_176k_long.json', encoding='utf-8'))
cleaned_segments = []

for idx, item in enumerate(data, 1):
    script_words = [w.strip(".,?!:;\"'…") for w in item['script_text'].split() if w.strip(".,?!:;\"'…")]
    n_expected = len(script_words)
    
    raw_words = item['words']
    valid_words = []
    
    for w in raw_words:
        if len(valid_words) == n_expected:
            break
        if w['seg_end'] <= w['seg_start']:
            continue
        valid_words.append(w)
        
    print(f"SEG {idx:02d} ({item['id']}): expected {n_expected} words vs got {len(valid_words)} cleaned words")
    
    cleaned_segments.append({
        "id": item['id'],
        "script_text": item['script_text'],
        "seg_start": item['seg_start'],
        "seg_end": item['seg_end'],
        "words": valid_words
    })

out_path = "processed/cleaned_words_176k_long.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(cleaned_segments, f, ensure_ascii=False, indent=2)

print(f"\n[+] ĐÃ XUẤT FILE LÀM SẠCH HOÀN HẢO: {out_path}")
