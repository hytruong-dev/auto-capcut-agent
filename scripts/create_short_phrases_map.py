import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

with open('processed/voiceover_words.json', 'r', encoding='utf-8') as f:
    words = json.load(f)

print(f"Total words: {len(words)}")

# Định nghĩa các cụm từ ngắn tự nhiên chuẩn tiếng Việt (2-4 từ / cụm)
CLEAN_PHRASES = [
    # Câu 1 (0.5 - 6.42s)
    "THỬ THÁCH",
    "CHẠY XE MÁY ĐIỆN",
    "XANH SM CẢ NGÀY",
    "TỪ SÁNG ĐẾN ĐÊM",
    "THỰC SỰ KIẾM ĐƯỢC",
    "BAO NHIÊU?",
    
    # Câu 2 (6.54 - 8.70s)
    "HÔM NAY",
    "MÌNH TEST THỰC TẾ",
    "LUÔN NHA!",
    
    # Câu 3 (8.82 - 12.01s)
    "BẠN NÀO",
    "CÒN THẮC MẮC",
    "THÌ XEM HẾT",
    "VIDEO NÀY NHA!",
    
    # Câu 4 (12.13 - 16.18s)
    "TÁM GIỜ SÁNG",
    "MÌNH BẮT ĐẦU",
    "MỞ APP",
    "NHẬN CUỐC ĐẦU TIÊN",
    
    # Câu 5 (16.30 - 22.42s)
    "PHẢI CÔNG NHẬN",
    "CHIẾC XE ĐIỆN VINFAST",
    "CHẠY ÊM RU",
    "LƯỚT TRÊN ĐƯỜNG PHỐ",
    "KHÔNG MỘT TIẾNG ĐỘNG CƠ",
    
    # Câu 6 (22.54 - 25.17s)
    "SÁNG SỚM",
    "MÁT RƯỢI",
    "CỰC KỲ DỄ CHỊU",
    
    # Câu 7 (25.29 - 27.88s)
    "MỞ BÁT CUỐC ĐẦU",
    "ĐƯỢC BA MƯƠI LĂM CÀNH!",
    
    # Câu 8 (28.00 - 30.36s)
    "CHẠY VÈO MỘT CÁI",
    "LÀ ĐẾN CHIỀU MUỘN",
    
    # Câu 9 (30.48 - 34.51s)
    "TẦM SÁU GIỜ CHIỀU",
    "SÀI GÒN",
    "BẮT ĐẦU",
    "LÊN ĐÈN LUNG LINH",
    
    # Câu 10 (34.63 - 41.10s)
    "GIỜ TAN TẦM",
    "KẸT XE",
    "NHƯNG XE ĐIỆN",
    "GA MƯỢT",
    "LUỒN LÁCH QUA PHỐ NHỎ",
    "CỰC KỲ NHẸ NHÀNG",
    
    # Câu 11 (41.22 - 44.95s)
    "ĐỨNG NGHỈ CHÂN",
    "MỘT XÍU LÀ",
    "APP LẠI NỔ ĐƠN",
    "LIÊN TỤC!",
    
    # Câu 12 (45.07 - 48.31s)
    "ĐẾN GẦN TÁM GIỜ TỐI",
    "PHỐ XÁ",
    "ĐÃ THƯA DẦN",
    
    # Câu 13 (48.43 - 52.56s)
    "CHẠY ĐÊM MÁT MẺ",
    "NHƯNG NGƯỜI CŨNG",
    "BẮT ĐẦU",
    "MỎI LƯNG RỒI ĐÓ",
    
    # Câu 14 (52.68 - 57.07s)
    "MỖI CHUYẾN XE ĐÊM",
    "LÀ MỘT CÂU CHUYỆN",
    "CÓ CHUYẾN VUI",
    "CÓ CHUYẾN MỆT...",
    
    # Câu 15 (57.19 - 61.55s)
    "NHƯNG CỨ NHÌN",
    "ĐỒNG HỒ KI-LÔ-MÉT",
    "NHẢY ĐỀU",
    "LÀ CÓ ĐỘNG LỰC ĐI TIẾP!",
    
    # Câu 16 (61.67 - 67.71s)
    "VÀ ĐÂY LÀ KẾT QUẢ",
    "SAU MỘT NGÀY CÀY CUỐC",
    "XE CHẠY ÊM",
    "TỔNG KẾT ĐƯỢC",
    "GẦN NĂM TRĂM CÀNH!",
    
    # Câu 17 (67.83 - 71.80s)
    "CHẠY CẢ NGÀY",
    "CÔNG NHẬN VẤT VẢ",
    "NHƯNG CŨNG",
    "RẤT ĐÁNG TỰ HÀO",
    
    # Câu 18 (71.92 - 77.23s)
    "CÒN ANH EM THÌ SAO?",
    "MỘT NGÀY ĐƯỢC",
    "BAO NHIÊU LÚA?",
    "COMMENT CHO MÌNH BIẾT NHA!",
    
    # Câu 19 (77.35 - 81.85s)
    "ĐỪNG QUÊN",
    "THẢ MỘT TIM",
    "VÀ FOLLOW KÊNH",
    "ĐÓN XEM TẬP TIẾP THEO NHÉ!"
]

print(f"Total defined short phrases: {len(CLEAN_PHRASES)}")

# Đọc timeline 19 câu thoại để nội suy thời gian chính xác cho từng cụm
with open('processed/story_voiceover_timeline.json', 'r', encoding='utf-8') as f:
    tl_data = json.load(f)

segments = tl_data['segments']

# Nhóm các cụm theo từng câu tương ứng
phrase_groups = [
    # Câu 1
    ["THỬ THÁCH", "CHẠY XE MÁY ĐIỆN", "XANH SM CẢ NGÀY", "TỪ SÁNG ĐẾN ĐÊM", "THỰC SỰ KIẾM ĐƯỢC", "BAO NHIÊU?"],
    # Câu 2
    ["HÔM NAY", "MÌNH TEST THỰC TẾ", "LUÔN NHA!"],
    # Câu 3
    ["BẠN NÀO", "CÒN THẮC MẮC", "THÌ XEM HẾT", "VIDEO NÀY NHA!"],
    # Câu 4
    ["TÁM GIỜ SÁNG", "MÌNH BẮT ĐẦU", "MỞ APP", "NHẬN CUỐC ĐẦU TIÊN"],
    # Câu 5
    ["PHẢI CÔNG NHẬN", "CHIẾC XE ĐIỆN VINFAST", "CHẠY ÊM RU", "LƯỚT TRÊN ĐƯỜNG PHỐ", "KHÔNG MỘT TIẾNG ĐỘNG CƠ"],
    # Câu 6
    ["SÁNG SỚM", "MÁT RƯỢI", "CỰC KỲ DỄ CHỊU"],
    # Câu 7
    ["MỞ BÁT CUỐC ĐẦU", "ĐƯỢC BA MƯƠI LĂM CÀNH!"],
    # Câu 8
    ["CHẠY VÈO MỘT CÁI", "LÀ ĐẾN CHIỀU MUỘN"],
    # Câu 9
    ["TẦM SÁU GIỜ CHIỀU", "SÀI GÒN", "BẮT ĐẦU", "LÊN ĐÈN LUNG LINH"],
    # Câu 10
    ["GIỜ TAN TẦM", "KẸT XE", "NHƯNG XE ĐIỆN", "GA MƯỢT", "LUỒN LÁCH QUA PHỐ NHỎ", "CỰC KỲ NHẸ NHÀNG"],
    # Câu 11
    ["ĐỨNG NGHỈ CHÂN", "MỘT XÍU LÀ", "APP LẠI NỔ ĐƠN", "LIÊN TỤC!"],
    # Câu 12
    ["ĐẾN GẦN TÁM GIỜ TỐI", "PHỐ XÁ", "ĐÃ THƯA DẦN"],
    # Câu 13
    ["CHẠY ĐÊM MÁT MẺ", "NHƯNG NGƯỜI CŨNG", "BẮT ĐẦU", "MỎI LƯNG RỒI ĐÓ"],
    # Câu 14
    ["MỖI CHUYẾN XE ĐÊM", "LÀ MỘT CÂU CHUYỆN", "CÓ CHUYẾN VUI", "CÓ CHUYẾN MỆT..."],
    # Câu 15
    ["NHƯNG CỨ NHÌN", "ĐỒNG HỒ KI-LÔ-MÉT", "NHẢY ĐỀU", "LÀ CÓ ĐỘNG LỰC ĐI TIẾP!"],
    # Câu 16
    ["VÀ ĐÂY LÀ KẾT QUẢ", "SAU MỘT NGÀY CÀY CUỐC", "XE CHẠY ÊM", "TỔNG KẾT ĐƯỢC", "GẦN NĂM TRĂM CÀNH!"],
    # Câu 17
    ["CHẠY CẢ NGÀY", "CÔNG NHẬN VẤT VẢ", "NHƯNG CŨNG", "RẤT ĐÁNG TỰ HÀO"],
    # Câu 18
    ["CÒN ANH EM THÌ SAO?", "MỘT NGÀY ĐƯỢC", "BAO NHIÊU LÚA?", "COMMENT CHO MÌNH BIẾT NHA!"],
    # Câu 19
    ["ĐỪNG QUÊN", "THẢ MỘT TIM", "VÀ FOLLOW KÊNH", "ĐÓN XEM TẬP TIẾP THEO NHÉ!"]
]

final_chunks = []
for idx, (seg, p_list) in enumerate(zip(segments, phrase_groups)):
    s_start = seg['start_time']
    s_end = seg['end_time']
    s_dur = s_end - s_start
    
    # Tính số ký tự của từng phrase để phân bổ thời gian tỷ lệ chính xác
    char_lens = [len(p.replace(' ', '')) for p in p_list]
    total_chars = sum(char_lens)
    
    cur_t = s_start
    for p, c_len in zip(p_list, char_lens):
        p_dur = round(s_dur * (c_len / total_chars), 2)
        p_end = round(cur_t + p_dur, 2)
        if p_end > s_end:
            p_end = s_end
        
        final_chunks.append({
            "text": p,
            "start": round(cur_t, 2),
            "end": p_end,
            "sentence_id": seg['id'],
            "part": seg['part']
        })
        cur_t = p_end

print(f"Generated {len(final_chunks)} timed short phrases.")
with open('processed/dynamic_short_subtitles.json', 'w', encoding='utf-8') as f:
    json.dump(final_chunks, f, ensure_ascii=False, indent=2)

for fc in final_chunks[:10]:
    print(f"[{fc['start']:5.2f}s -> {fc['end']:5.2f}s] {fc['text']}")
