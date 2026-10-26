"""
Build Dynamic Word-by-Word Karaoke Subtitles & Money Counters cho Vlog XanhSM 176k:
- Font: Oswald Bold
- Từ active: Cyan (#66FFFF / &H00FFFF66&)
- Từ còn lại trong cụm: Lemon Yellow (#F0FF00 / &H0000FFF0&)
- Viền đen dày (Outline 7), Đổ bóng (Shadow 2), Safe Zone Alignment 2, MarginV 220
- Hiệu ứng Pop-In đầu cụm, Fade-Out cuối cụm
- 6 Thẻ tiền nhận đơn (+16k, +22k, +35k, +28k, +42k, +33k) & Thẻ tổng cộng dồn (Tổng thu: 176.000đ)
"""

import os
import sys
import json
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Colors (ASS format &HAABBGGRR)
COLOR_CYAN = r"{\c&H00FFFF66&}"     # Active word: Cyan #66FFFF
COLOR_YELLOW = r"{\c&H0000FFF0&}"   # Inactive words: Lemon Yellow #F0FF00
COLOR_GREEN = r"{\c&H0033FF33&}"    # Money add: Bright Green #33FF33
COLOR_WHITE = r"{\c&H00FFFFFF&}"    # White text

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

def generate_karaoke_ass():
    words_data_path = Path("processed/omnivoice_176k_words.json")
    with open(words_data_path, "r", encoding="utf-8") as f:
        segments = json.load(f)

    all_karaoke_events = []
    all_srt_segments = []
    
    # 1. Xử lý từng segment & phrase
    for seg in segments:
        seg_id = seg["id"]
        phrases = seg["phrases"]
        seg_start = seg["seg_start"]
        seg_end = seg["seg_end"]
        whisper_words = seg.get("words", [])
        
        # Gom tất cả các từ trong phrase
        flat_phrase_words = []
        for p in phrases:
            for w in p:
                flat_phrase_words.append(w)
                
        n_phrase_words = len(flat_phrase_words)
        n_whisper_words = len(whisper_words)
        
        # Căn chỉnh thời gian cho từng từ trong phrase
        word_timings = []
        if n_whisper_words > 0 and abs(n_phrase_words - n_whisper_words) <= 2:
            # Nếu số từ xấp xỉ bằng nhau, dùng thời gian từ whisper
            wh_start = whisper_words[0]["master_start"]
            wh_end = whisper_words[-1]["master_end"]
            span = max(0.5, wh_end - wh_start)
            for i, pw in enumerate(flat_phrase_words):
                t_s = wh_start + (i / n_phrase_words) * span
                t_e = wh_start + ((i + 1) / n_phrase_words) * span
                word_timings.append({
                    "word": pw,
                    "start": round(t_s, 3),
                    "end": round(t_e, 3)
                })
        else:
            # Dùng trực tiếp thời gian của segment
            span = max(0.5, seg_end - seg_start)
            for i, pw in enumerate(flat_phrase_words):
                t_s = seg_start + (i / n_phrase_words) * span
                t_e = seg_start + ((i + 1) / n_phrase_words) * span
                word_timings.append({
                    "word": pw,
                    "start": round(t_s, 3),
                    "end": round(t_e, 3)
                })
                
        # Gom thành từng phrase cụm ngắn
        cur_w_idx = 0
        for p in phrases:
            p_len = len(p)
            p_words = word_timings[cur_w_idx : cur_w_idx + p_len]
            cur_w_idx += p_len
            
            p_start = p_words[0]["start"]
            p_end = p_words[-1]["end"]
            
            # Lưu vào danh sách SRT
            all_srt_segments.append({
                "start": p_start,
                "end": p_end,
                "text": " ".join(p)
            })
            
            # Tạo karaoke sub-events cho từng từ active
            for w_idx in range(p_len):
                w_start = p_words[w_idx]["start"]
                if w_idx < p_len - 1:
                    w_end = max(w_start + 0.08, p_words[w_idx + 1]["start"])
                else:
                    w_end = max(w_start + 0.12, p_end)
                    
                if w_end <= w_start:
                    w_end = w_start + 0.15
                    
                # Xây dựng chuỗi: Từ w_idx đổi CYAN, các từ khác YELLOW
                tokens = []
                for j in range(p_len):
                    w_text = p[j]
                    if j == w_idx:
                        tokens.append(f"{COLOR_CYAN}{w_text}")
                    else:
                        tokens.append(f"{COLOR_YELLOW}{w_text}")
                        
                line_body = " ".join(tokens)
                
                # Hiệu ứng Pop-In ở từ đầu phrase, Fade-Out ở từ cuối phrase
                if p_len == 1:
                    anim_tag = r"{\fad(40,50)\t(0,40,\fscx110\fscy110)\t(40,90,\fscx100\fscy100)}"
                elif w_idx == 0:
                    anim_tag = r"{\fad(40,0)\t(0,40,\fscx110\fscy110)\t(40,90,\fscx100\fscy100)}"
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

    print(f"[+] Đã tạo {len(all_karaoke_events)} karaoke events trên {len(all_srt_segments)} short phrases!")

    # 2. Xây dựng Header ASS hoàn chỉnh
    ass_header = """[Script Info]
Title: Vlog XanhSM 176k - Dynamic Word Karaoke & Money Cards
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

Dialogue: 2,0:01:69.50,0:01:74.00,MoneyCard,,0,0,0,,{\\fad(80,80)\\t(0,80,\\fscx120\\fscy120)\\t(80,160,\\fscx100\\fscy100)}+33.000đ (ĐƠN #6)
Dialogue: 2,0:01:69.50,0:01:74.00,TotalCard,,0,0,0,,{\\fad(80,80)}TỔNG THU: 176.000đ

; --- TỔNG KẾT NGÀY (74.0s -> 78.5s) ---
Dialogue: 3,0:01:14.20,0:01:18.50,GrandTotal,,0,0,0,,{\\fad(100,100)\\t(0,100,\\fscx115\\fscy115)\\t(100,200,\\fscx100\\fscy100)}💰 TỔNG THU: 176.000đ 💰

; --- OUTRO CALLOUT (83.0s -> 88.0s) ---
Dialogue: 2,0:01:23.00,0:01:28.00,Callout,,0,0,0,,{\\fad(120,120)}💚 BẤM TIM & ĐỂ LẠI BÌNH LUẬN NHÉ! 💚

; --- DYNAMIC WORD-BY-WORD KARAOKE SUBTITLES ---
"""
    # Lưu ý: sửa lại thời gian của Đơn 6 (phút 1 giây 09 là 0:01:09.50 chứ không phải 0:01:69.50)
    ass_header = ass_header.replace("0:01:69.50", "0:01:09.50").replace("0:01:74.00", "0:01:13.50")

    ass_lines = [ass_header]
    for ev in all_karaoke_events:
        st_str = to_ass_time(ev["start"])
        et_str = to_ass_time(ev["end"])
        ass_lines.append(f"Dialogue: 0,{st_str},{et_str},DynamicSub,,0,0,0,,{ev['text']}\n")

    out_ass = Path("processed/vlog_xanhsm_176k_master.ass")
    with open(out_ass, "w", encoding="utf-8") as f:
        f.writelines(ass_lines)
    print(f"[SUCCESS] Đã lưu ASS Master Subtitles: {out_ass}")

    # Xuất file SRT
    out_srt = Path("processed/vlog_xanhsm_176k.srt")
    with open(out_srt, "w", encoding="utf-8") as f:
        for idx, s in enumerate(all_srt_segments, 1):
            f.write(f"{idx}\n")
            f.write(f"{to_srt_time(s['start'])} --> {to_srt_time(s['end'])}\n")
            f.write(f"{s['text']}\n\n")
    print(f"[SUCCESS] Đã lưu SRT Subtitles: {out_srt}")

    # Xuất JSON
    out_json = Path("processed/dynamic_karaoke_176k.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(all_srt_segments, f, ensure_ascii=False, indent=2)
    print(f"[SUCCESS] Đã lưu Phrases JSON: {out_json}")

if __name__ == "__main__":
    generate_karaoke_ass()
