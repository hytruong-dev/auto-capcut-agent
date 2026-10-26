import json
import sys
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

data = json.load(open('processed/exact_omnivoice_words.json', encoding='utf-8'))

cleaned_segments = []

for item in data:
    script_words = [w.strip(".,?!:;\"'") for w in item['script_text'].split() if w.strip(".,?!:;\"'")]
    n_expected = len(script_words)
    
    # Lọc các từ hợp lệ (dur > 0 và lấy tối đa n_expected từ đầu tiên)
    raw_words = item['words']
    valid_words = []
    for w in raw_words:
        # Nếu đã đủ số từ thì dừng
        if len(valid_words) == n_expected:
            break
        # Bỏ qua từ bị lặp thời lượng 0
        if w['seg_end'] <= w['seg_start']:
            continue
        valid_words.append(w)
        
    print(f"\nSEG {item['id']:02d}: expected {n_expected} words vs got {len(valid_words)} valid whisper words")
    print("Script: ", " ".join(script_words))
    print("Whisper:", " ".join(w['word'].strip(".,?!:;\"'") for w in valid_words))
    
    cleaned_segments.append({
        "id": item['id'],
        "script_text": item['script_text'],
        "seg_start": item['seg_start'],
        "seg_end": item['seg_end'],
        "words": valid_words
    })

with open("processed/cleaned_omnivoice_words.json", "w", encoding="utf-8") as f:
    json.dump(cleaned_segments, f, ensure_ascii=False, indent=2)

print("\n[+] ĐÃ XUẤT FILE LÀM SẠCH: processed/cleaned_omnivoice_words.json")
