"""
ĐỒNG BỘ 100% PHỤ ĐỀ DYNAMIC KARAOKE VỚI ÂM THANH THỰC TẾ:
- Sử dụng chính xác word-level timestamps từ audio/Whisper (cleaned_omnivoice_words.json)
- Nhóm thành các Short Phrases (2-4 từ/cụm) tự nhiên chuẩn Tiếng Việt
- Từng từ sáng Xanh Cyan (#66FFFF) đúng mili-giây giọng đọc phát âm
- Các từ còn lại trong cụm giữ màu Vàng Chanh (#F0FF00)
- Font Oswald-Bold, IN HOA, viền đen dày (Outline 7), Đổ bóng (Shadow 2), Safe Zone Alignment 2, MarginV 220
- 6 Thẻ tiền nhận đơn & Thẻ tổng cộng dồn (Tổng thu 176k)
"""

import sys
import os
import json
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

COLOR_CYAN = r"{\c&H00FFFF66&}"     # Active word: Cyan #66FFFF
COLOR_YELLOW = r"{\c&H0000FFF0&}"   # Inactive words: Lemon Yellow #F0FF00

def to_ass_time(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = sec % 60
    return f"{h}:{m:02d}:{s:05.2f}"

def to_srt_time(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s_int = int(sec % 60)
    ms = int((sec - int(sec)) * 1000)
    return f"{h:02d}:{m:02d}:{s_int:02d},{ms:03d}"

# Định nghĩa các cụm từ ngắn chuẩn (2 - 4 từ/cụm) cho 18 câu
PHRASE_STRUCTURES = [
    # Seg 01 (19 từ)
    [["MỘT", "NGÀY"], ["CHẠY", "XE", "MÁY", "ĐIỆN"], ["XANH", "SM"], ["TỪ", "SÁNG", "ĐẾN", "ĐÊM"], ["THỰC", "SỰ", "KIẾM", "ĐƯỢC"], ["BAO", "NHIÊU", "TIỀN?"]],
    # Seg 02 (16 từ)
    [["HÔM", "NAY"], ["ANH", "EM", "CÙNG", "MÌNH"], ["CÀY", "THỰC", "TẾ"], ["XEM", "TỔNG", "THU"], ["ĐƯỢC", "BAO", "NHIÊU", "NHÉ!"]],
    # Seg 03 (10 từ)
    [["TÁM", "GIỜ", "SÁNG"], ["MÌNH", "BẮT", "ĐẦU"], ["BẬT", "APP", "TRỰC", "CA"]],
    # Seg 04 (17 từ)
    [["XE", "VINFAST"], ["SẠC", "ĐẦY", "PIN"], ["CHẠY", "ÊM", "RU"], ["NỔ", "NGAY", "ĐƠN"], ["ĐÓN", "BẠN", "HỌC", "SINH"], ["ĐI", "HỌC"]],
    # Seg 05 (14 từ)
    [["CUỐC", "ĐẦU", "TIÊN"], ["MỞ", "BÁT"], ["KHÁCH", "TRẢ", "ĐÚNG"], ["MƯỜI", "SÁU", "CÀNH"], ["NHA", "ANH", "EM!"]],
    # Seg 06 (16 từ)
    [["TIẾP", "TỤC", "CHẠY", "TRƯA"], ["APP", "BÁO", "NHẬN", "ĐƠN"], ["GIAO", "TÀI", "LIỆU", "HỎA", "TỐC"], ["SANG", "QUẬN", "NHẤT"]],
    # Seg 07 (18 từ)
    [["TRƯA", "NẮNG", "GẮT"], ["NHƯNG", "XE", "ĐIỆN"], ["KHÔNG", "BỊ", "NÓNG", "CHÂN"], ["GIAO", "XONG", "NHẬN", "THÊM"], ["HAI", "MƯƠI", "HAI", "CÀNH!"]],
    # Seg 08 (19 từ)
    [["UỐNG", "VỘI", "LY", "TRÀ", "ĐÁ"], ["THÌ", "APP", "NỔ", "CUỐC"], ["THỨ", "BA"], ["CHỞ", "ANH", "KHÁCH", "CÔNG", "SỞ"], ["SANG", "QUẬN", "BA"]],
    # Seg 09 (18 từ)
    [["ĐƯỜNG", "XÁ", "ĐÔNG", "ĐÚC"], ["NHƯNG", "XE", "ÊM"], ["KHÁCH", "KHEN", "QUÁ", "TRỜI"], ["VÍ", "NHẢY", "THÊM"], ["BA", "MƯƠI", "LĂM", "NGHÌN!"]],
    # Seg 10 (17 từ)
    [["NĂM", "GIỜ", "CHIỀU"], ["SÀI", "GÒN", "BƯỚC", "VÀO"], ["GIỜ", "TAN", "TẦM"], ["KẸT", "XE", "CHEN", "CHÚC"], ["TỪNG", "CHÚT", "MỘT"]],
    # Seg 11 (19 từ)
    [["TAY", "GA", "NHẠY"], ["LUỒN", "LÁCH", "NGÕ", "HẺM"], ["TRẢ", "KHÁCH", "ĐÚNG", "GIỜ"], ["ĐƠN", "NÀY", "THU", "THÊM"], ["HAI", "MƯƠI", "TÁM", "CÀNH!"]],
    # Seg 12 (17 từ)
    [["BẢY", "GIỜ", "TỐI"], ["THÀNH", "PHỐ", "LÊN", "ĐÈN"], ["LUNG", "LINH"], ["MÌNH", "NHẬN", "CUỐC"], ["ĐƯỜNG", "DÀI", "VỀ", "NGOẠI", "Ô"]],
    # Seg 13 (19 từ)
    [["CHẠY", "ĐƯỜNG", "ĐÊM"], ["GIÓ", "MÁT", "CỰC", "CHILL"], ["CHUYẾN", "THỨ", "NĂM"], ["BỎ", "TÚI"], ["BỐN", "MƯƠI", "HAI", "NGHÌN!"]],
    # Seg 14 (18 từ)
    [["HƠN", "TÁM", "GIỜ", "ĐÊM"], ["NGƯỜI", "ĐÃ", "THẤM", "MỆT"], ["NÊN", "MÌNH", "BẬT", "ĐỊNH", "HƯỚNG"], ["TÌM", "ĐƠN", "VỀ", "PHÒNG", "TRỌ"]],
    # Seg 15 (20 từ)
    [["MAY", "MẮN", "NỔ", "NGAY", "ĐƠN"], ["TIỆN", "ĐƯỜNG"], ["BA", "MƯƠI", "BA", "NGHÌN!"], ["CHỐT", "TRỌN", "VẸN", "CUỐC", "XE"], ["THỨ", "SÁU", "TRONG", "NGÀY"]],
    # Seg 16 (18 từ)
    [["VẬY", "LÀ", "TỔNG", "KẾT"], ["MỘT", "NGÀY", "CHẠY", "XANH", "SM"], ["ĐƯỢC", "ĐÚNG", "MỘT", "TRĂM"], ["BẢY", "MƯƠI", "SÁU", "NGHÌN", "ĐỒNG!"]],
    # Seg 17 (18 từ)
    [["DÙ", "VẤT", "VẢ"], ["NHƯNG", "ĐÓ", "LÀ", "ĐỒNG", "TIỀN"], ["MỒ", "HÔI", "CÔNG", "SỨC"], ["CHÂN", "CHÍNH"], ["VÀ", "RẤT", "TỰ", "HÀO!"]],
    # Seg 18 (19 từ)
    [["ANH", "EM", "HÔM", "NAY"], ["ĐƯỢC", "BAO", "NHIÊU", "LÚA", "RỒI?"], ["COMMENT", "BÊN", "DƯỚI"], ["VÀ", "BẤM", "TIM"], ["ỦNG", "HỘ", "MÌNH", "NHÉ!"]]
]

def generate_exact_karaoke():
    words_data = json.load(open("processed/cleaned_omnivoice_words.json", encoding="utf-8"))
    
    all_karaoke_events = []
    all_srt_phrases = []

    for seg_idx, (phrases, s_info) in enumerate(zip(PHRASE_STRUCTURES, words_data)):
        w_words = s_info['words']
        seg_start = s_info['seg_start']
        seg_end = s_info['seg_end']
        
        flat_def_words = []
        for p in phrases:
            for w in p:
                flat_def_words.append(w)
                
        n_def = len(flat_def_words)
        n_wh = len(w_words)
        
        # Ánh xạ word timing chính xác từ whisper
        word_timings = []
        if n_def == n_wh:
            for dw, ww in zip(flat_def_words, w_words):
                word_timings.append({
                    "word": dw,
                    "start": ww['master_start'],
                    "end": ww['master_end']
                })
        else:
            # Xử lý các trường hợp lệch 1 từ (Seg 01, Seg 05, Seg 16)
            if s_info['id'] == 1: # Thiếu 'Một' ở đầu
                word_timings.append({"word": "MỘT", "start": round(seg_start, 3), "end": round(seg_start + 0.35, 3)})
                for dw, ww in zip(flat_def_words[1:], w_words):
                    word_timings.append({"word": dw, "start": ww['master_start'], "end": ww['master_end']})
            elif s_info['id'] == 5: # Thiếu 'Cuốc' ở đầu
                first_w_st = w_words[0]['master_start']
                word_timings.append({"word": "CUỐC", "start": round(max(seg_start, first_w_st - 0.25), 3), "end": first_w_st})
                for dw, ww in zip(flat_def_words[1:], w_words):
                    word_timings.append({"word": dw, "start": ww['master_start'], "end": ww['master_end']})
            elif s_info['id'] == 16: # '176 000 đồng' -> 'một trăm bảy mươi sáu nghìn đồng'
                # w_words có 14 từ, flat_def có 18 từ
                wh_start = w_words[0]['master_start']
                wh_end = w_words[-1]['master_end']
                time_span = wh_end - wh_start
                for i, dw in enumerate(flat_def_words):
                    t_s = wh_start + (i / n_def) * time_span
                    t_e = wh_start + ((i + 1) / n_def) * time_span
                    word_timings.append({"word": dw, "start": round(t_s, 3), "end": round(t_e, 3)})
            else:
                wh_start = w_words[0]['master_start']
                wh_end = w_words[-1]['master_end']
                time_span = wh_end - wh_start
                for i, dw in enumerate(flat_def_words):
                    t_s = wh_start + (i / n_def) * time_span
                    t_e = wh_start + ((i + 1) / n_def) * time_span
                    word_timings.append({"word": dw, "start": round(t_s, 3), "end": round(t_e, 3)})

        # Gom thành các Short Phrases và tạo sub-events
        cur_idx = 0
        for p in phrases:
            p_len = len(p)
            p_words = word_timings[cur_idx : cur_idx + p_len]
            cur_idx += p_len
            
            phrase_start = p_words[0]['start']
            phrase_end = p_words[-1]['end']
            
            # Cho SRT và CapCut Subtitles Track
            all_srt_phrases.append({
                "start": phrase_start,
                "end": phrase_end + 0.08,
                "text": " ".join(p)
            })
            
            # Tạo sub-events từng từ active (Dynamic Word-by-Word Highlight)
            for w_idx in range(p_len):
                w_start = p_words[w_idx]['start']
                if w_idx < p_len - 1:
                    # Kéo dài đến khi từ kế tiếp bắt đầu nói -> chuyển đổi mượt 100%
                    w_end = max(w_start + 0.1, p_words[w_idx + 1]['start'])
                else:
                    w_end = max(w_start + 0.15, phrase_end + 0.08)
                    
                if w_end <= w_start:
                    w_end = w_start + 0.15
                    
                # Xây dựng dòng text: Từ active màu Cyan, các từ khác màu Vàng
                tokens = []
                for j in range(p_len):
                    word_text = p[j]
                    if j == w_idx:
                        tokens.append(f"{COLOR_CYAN}{word_text}")
                    else:
                        tokens.append(f"{COLOR_YELLOW}{word_text}")
                        
                line_body = " ".join(tokens)
                
                # Hiệu ứng Pop-In ở từ đầu phrase, Fade-Out ở từ cuối phrase
                if p_len == 1:
                    anim_tag = r"{\fad(40,50)\t(0,40,\fscx112\fscy112)\t(40,90,\fscx100\fscy100)}"
                elif w_idx == 0:
                    anim_tag = r"{\fad(40,0)\t(0,40,\fscx112\fscy112)\t(40,90,\fscx100\fscy100)}"
                elif w_idx == p_len - 1:
                    anim_tag = r"{\fad(0,50)}"
                else:
                    anim_tag = ""
                    
                full_text = f"{anim_tag}{line_body}"
                all_karaoke_events.append({
                    "start": w_start,
                    "end": w_end,
                    "text": full_text
                })

    print(f"[+] Tạo thành công {len(all_karaoke_events)} karaoke events trên {len(all_srt_phrases)} phrases đồng bộ âm thanh!")

    # Tạo Header ASS chuẩn Oswald-Bold
    ass_header = """[Script Info]
Title: Vlog XanhSM 176k - 100% Audio Synchronized Dynamic Word Karaoke
ScriptType: v4.00+
WrapStyle: 0
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: DynamicSub,Oswald Bold,76,&H0000FFF0,&H0000FFF0,&H00000000,&H90000000,-1,0,0,0,100,100,1,0,1,7,2,2,60,60,220,1
Style: Hook1,Oswald Bold,84,&H003333FF,&H003333FF,&H00FFFFFF,&H90000000,-1,0,0,0,100,100,1,0,1,8,3,8,60,60,340,1
Style: Hook2,Oswald Bold,96,&H0000FFF0,&H0000FFF0,&H00000000,&H90000000,-1,0,0,0,100,100,1,0,1,9,3,8,60,60,460,1
Style: MoneyCard,Oswald Bold,92,&H0033FF33,&H0033FF33,&H00000000,&H90000000,-1,0,0,0,100,100,1,0,1,8,3,8,60,60,360,1
Style: TotalCard,Oswald Bold,68,&H0000FFF0,&H0000FFF0,&H00000000,&H90000000,-1,0,0,0,100,100,1,0,1,7,2,8,60,60,470,1
Style: GrandTotal,Oswald Bold,90,&H0000FFF0,&H0000FFF0,&H00000000,&H90000000,-1,0,0,0,100,100,1,0,1,9,4,8,60,60,400,1
Style: Callout,Oswald Bold,64,&H0066FF66,&H0066FF66,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,6,2,8,60,60,360,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
; --- HOOK BANNER (0.0s -> 5.5s) ---
Dialogue: 1,0:00:00.00,0:00:05.50,Hook1,,0,0,0,,{\\fad(120,120)}THỬ THÁCH 1 NGÀY
Dialogue: 1,0:00:00.00,0:00:05.50,Hook2,,0,0,0,,{\\fad(120,120)}CHẠY XE XANH SM

; --- 6 THẺ TIỀN NHẬN ĐƠN & CỘNG DỒN TỔNG THU (ĐÚNG 176K) ---
Dialogue: 2,0:00:19.20,0:00:22.50,MoneyCard,,0,0,0,,{\\fad(80,80)\\t(0,80,\\fscx120\\fscy120)\\t(80,160,\\fscx100\\fscy100)}+16.000đ (ĐƠN #1)
Dialogue: 2,0:00:19.20,0:00:22.50,TotalCard,,0,0,0,,{\\fad(80,80)}TỔNG THU: 16.000đ

Dialogue: 2,0:00:29.50,0:00:32.80,MoneyCard,,0,0,0,,{\\fad(80,80)\\t(0,80,\\fscx120\\fscy120)\\t(80,160,\\fscx100\\fscy100)}+22.000đ (ĐƠN #2)
Dialogue: 2,0:00:29.50,0:00:32.80,TotalCard,,0,0,0,,{\\fad(80,80)}TỔNG THU: 38.000đ

Dialogue: 2,0:00:39.50,0:00:43.00,MoneyCard,,0,0,0,,{\\fad(80,80)\\t(0,80,\\fscx120\\fscy120)\\t(80,160,\\fscx100\\fscy100)}+35.000đ (ĐƠN #3)
Dialogue: 2,0:00:39.50,0:00:43.00,TotalCard,,0,0,0,,{\\fad(80,80)}TỔNG THU: 73.000đ

Dialogue: 2,0:00:49.50,0:00:53.00,MoneyCard,,0,0,0,,{\\fad(80,80)\\t(0,80,\\fscx120\\fscy120)\\t(80,160,\\fscx100\\fscy100)}+28.000đ (ĐƠN #4)
Dialogue: 2,0:00:49.50,0:00:53.00,TotalCard,,0,0,0,,{\\fad(80,80)}TỔNG THU: 101.000đ

Dialogue: 2,0:00:59.80,0:01:03.20,MoneyCard,,0,0,0,,{\\fad(80,80)\\t(0,80,\\fscx120\\fscy120)\\t(80,160,\\fscx100\\fscy100)}+42.000đ (ĐƠN #5)
Dialogue: 2,0:00:59.80,0:01:03.20,TotalCard,,0,0,0,,{\\fad(80,80)}TỔNG THU: 143.000đ

Dialogue: 2,0:01:09.50,0:01:13.50,MoneyCard,,0,0,0,,{\\fad(80,80)\\t(0,80,\\fscx120\\fscy120)\\t(80,160,\\fscx100\\fscy100)}+33.000đ (ĐƠN #6)
Dialogue: 2,0:01:09.50,0:01:13.50,TotalCard,,0,0,0,,{\\fad(80,80)}TỔNG THU: 176.000đ

; --- TỔNG KẾT NGÀY (74.0s -> 78.5s) ---
Dialogue: 3,0:01:14.20,0:01:18.50,GrandTotal,,0,0,0,,{\\fad(100,100)\\t(0,100,\\fscx115\\fscy115)\\t(100,200,\\fscx100\\fscy100)}💰 TỔNG THU: 176.000đ 💰

; --- OUTRO CALLOUT (83.0s -> 88.0s) ---
Dialogue: 2,0:01:23.00,0:01:28.00,Callout,,0,0,0,,{\\fad(120,120)}💚 BẤM TIM & ĐỂ LẠI BÌNH LUẬN NHÉ! 💚

; --- DYNAMIC WORD-BY-WORD KARAOKE SUBTITLES ---
"""
    ass_lines = [ass_header]
    for ev in all_karaoke_events:
        st_str = to_ass_time(ev["start"])
        et_str = to_ass_time(ev["end"])
        ass_lines.append(f"Dialogue: 0,{st_str},{et_str},DynamicSub,,0,0,0,,{ev['text']}\n")

    out_ass = Path("processed/vlog_xanhsm_176k_master.ass")
    with open(out_ass, "w", encoding="utf-8") as f:
        f.writelines(ass_lines)
    print(f"[SUCCESS] Đã xuất ASS Master Subtitles chuẩn audio: {out_ass}")

    # Xuất file SRT
    out_srt = Path("processed/vlog_xanhsm_176k.srt")
    with open(out_srt, "w", encoding="utf-8") as f:
        for idx, s in enumerate(all_srt_phrases, 1):
            f.write(f"{idx}\n")
            f.write(f"{to_srt_time(s['start'])} --> {to_srt_time(s['end'])}\n")
            f.write(f"{s['text']}\n\n")
    print(f"[SUCCESS] Đã xuất SRT Subtitles: {out_srt}")

    # Xuất file JSON
    out_json = Path("processed/dynamic_karaoke_176k.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(all_srt_phrases, f, ensure_ascii=False, indent=2)
    print(f"[SUCCESS] Đã xuất Short Phrases JSON: {out_json}")

if __name__ == "__main__":
    generate_exact_karaoke()
