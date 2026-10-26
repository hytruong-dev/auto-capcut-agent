import json, sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Định nghĩa các cụm từ chuẩn Tiếng Việt cho từng câu (19 câu)
PHRASE_DEFS = [
    # Câu 1
    [
        ["THỬ", "THÁCH"],
        ["CHẠY", "XE", "MÁY", "ĐIỆN"],
        ["XANH", "SM", "CẢ", "NGÀY"],
        ["TỪ", "SÁNG", "ĐẾN", "ĐÊM"],
        ["THỰC", "SỰ", "KIẾM", "ĐƯỢC"],
        ["BAO", "NHIÊU", "TIỀN", "NÈ?"]
    ],
    # Câu 2
    [
        ["HÔM", "NAY", "MÌNH"],
        ["TEST", "THỰC", "TẾ"],
        ["CHO", "ANH", "EM", "XEM", "NHA!"]
    ],
    # Câu 3
    [
        ["BẠN", "NÀO"],
        ["CÒN", "THẮC", "MẮC"],
        ["THÌ", "XEM", "HẾT"],
        ["VIDEO", "LÀ", "BIẾT", "LIỀN!"]
    ],
    # Câu 4
    [
        ["TÁM", "GIỜ", "SÁNG"],
        ["MÌNH", "BẮT", "ĐẦU"],
        ["MỞ", "APP"],
        ["NHẬN", "CUỐC", "ĐẦU", "TIÊN"]
    ],
    # Câu 5
    [
        ["PHẢI", "CÔNG", "NHẬN"],
        ["XE", "ĐIỆN", "VINFAST"],
        ["CHẠY", "ÊM", "RU", "LUÔN", "Á"],
        ["LƯỚT", "TRÊN", "ĐƯỜNG", "PHỐ"],
        ["KHÔNG", "TIẾNG", "ĐỘNG", "CƠ!"]
    ],
    # Câu 6
    [
        ["SÁNG", "SỚM", "MÁT", "RƯỢI"],
        ["CỰC", "KỲ", "DỄ", "CHỊU!"]
    ],
    # Câu 7
    [
        ["MỞ", "BÁT", "CUỐC", "ĐẦU"],
        ["ĐƯỢC", "BA", "MƯƠI", "LĂM", "CÀNH"],
        ["QUÁ", "ĐÃ", "LUÔN!"]
    ],
    # Câu 8
    [
        ["CHẠY", "VÈO", "MỘT", "CÁI"],
        ["LÀ", "ĐẾN", "CHIỀU", "MUỘN", "RỒI"]
    ],
    # Câu 9
    [
        ["TẦM", "SÁU", "GIỜ", "CHIỀU"],
        ["SÀI", "GÒN", "LÊN", "ĐÈN"],
        ["LUNG", "LINH", "ĐẸP", "GHÊ!"]
    ],
    # Câu 10
    [
        ["GIỜ", "TAN", "TẦM", "KẸT", "XE"],
        ["NHƯNG", "XE", "ĐIỆN", "GA", "MƯỢT"],
        ["LUỒN", "LÁCH", "QUA", "NGÕ", "NHỎ"],
        ["CỰC", "KỲ", "NHẸ", "NHÀNG!"]
    ],
    # Câu 11
    [
        ["ĐỨNG", "NGHỈ", "CHÂN", "MỘT", "XÍU"],
        ["APP", "LẠI", "NỔ", "ĐƠN"],
        ["LIÊN", "TỤC", "LUÔN", "Á!"]
    ],
    # Câu 12
    [
        ["ĐẾN", "GẦN", "TÁM", "GIỜ", "TỐI"],
        ["PHỐ", "XÁ", "ĐÃ", "THƯA", "DẦN"]
    ],
    # Câu 13
    [
        ["CHẠY", "ĐÊM", "GIÓ", "MÁT", "THẬT"],
        ["NHƯNG", "BẮT", "ĐẦU", "MỎI", "LƯNG", "RỒI!"]
    ],
    # Câu 14
    [
        ["MỖI", "CHUYẾN", "XE", "ĐÊM"],
        ["LÀ", "MỘT", "CÂU", "CHUYỆN"],
        ["CÓ", "CHUYẾN", "VUI"],
        ["CÓ", "CHUYẾN", "MỆT..."]
    ],
    # Câu 15
    [
        ["NHƯNG", "CỨ", "NHÌN", "ĐỒNG", "HỒ"],
        ["KI-LÔ-MÉT", "NHẢY", "ĐỀU"],
        ["LÀ", "CÓ", "ĐỘNG", "LỰC", "CÀY", "TIẾP!"]
    ],
    # Câu 16
    [
        ["VÀ", "ĐÂY", "LÀ", "KẾT", "QUẢ"],
        ["SAU", "MỘT", "NGÀY", "CÀY", "CUỐC"],
        ["TỔNG", "KẾT", "ĐƯỢC"],
        ["GẦN", "NĂM", "TRĂM", "CÀNH"],
        ["QUÁ", "ẤM", "LUÔN!"]
    ],
    # Câu 17
    [
        ["CHẠY", "CẢ", "NGÀY", "VẤT", "VẢ"],
        ["NHƯNG", "RẤT", "ĐÁNG", "TỰ", "HÀO", "NHA!"]
    ],
    # Câu 18
    [
        ["CÒN", "ANH", "EM", "THÌ", "SAO?"],
        ["MỘT", "NGÀY", "ĐƯỢC", "BAO", "NHIÊU", "LÚA?"],
        ["COMMENT", "CHO", "MÌNH", "BIẾT", "NHA!"]
    ],
    # Câu 19
    [
        ["NHỚ", "THẢ", "MỘT", "TIM"],
        ["VÀ", "FOLLOW", "KÊNH"],
        ["ĐỂ", "XEM", "TẬP", "TIẾP", "THEO", "NHÉ!"]
    ]
]

if __name__ == "__main__":
    print(f"Total defined segment groups: {len(PHRASE_DEFS)}")
    total_phrases = sum(len(p) for p in PHRASE_DEFS)
    print(f"Total phrases: {total_phrases}")
