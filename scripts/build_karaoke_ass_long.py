"""
Sinh file phụ đề ASS Dynamic Word-by-Word Karaoke + Hook 2 tầng + 6 Thẻ tiền nhận đơn + Thẻ Tổng Thu 176k
Chuẩn huấn luyện:
- Oswald-Bold, IN HOA, Vàng chanh #F0FF00, Active word Cyan #66FFFF
- Alignment 2, MarginV 550 (Safe Zone Y ≈ -0.38)
- 6 Thẻ tiền nhận đơn với SFX âm thanh nhận tiền
"""

import os
import sys
import json
import re
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

CYAN = r"{\c&H00FFFF66&}"    # Active word: #66FFFF (ASS BGR)
YELLOW = r"{\c&H0000FFF0&}"  # Inactive word: #F0FF00
BREAK_PUNCT = re.compile(r"[,.!?;:…]$")

HEADER = """[Script Info]
Title: Vlog 1 Ngay Chay Xe XanhSM 176k Long (2.5 Phut)
ScriptType: v4.00+
WrapStyle: 0
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: DynamicSub,Oswald,74,&H0000FFF0,&H0000FFF0,&H00000000,&H1A000000,-1,0,0,0,100,100,1,0,1,7,2,2,60,60,550,1
Style: Hook1,Oswald,84,&H003333FF,&H003333FF,&H00FFFFFF,&H1A000000,-1,0,0,0,100,100,1,0,1,8,3,8,60,60,340,1
Style: Hook2,Oswald,96,&H0000FFF0,&H0000FFF0,&H00000000,&H1A000000,-1,0,0,0,100,100,1,0,1,9,3,8,60,60,460,1
Style: CashHeader,Oswald,62,&H0066FF00,&H0066FF00,&H00000000,&H1A000000,-1,0,0,0,100,100,1,0,1,7,3,8,60,60,780,1
Style: CashAmount,Oswald,98,&H0000FFFF,&H0000FFFF,&H00000000,&H1A000000,-1,0,0,0,100,100,2,0,1,9,4,8,60,60,860,1
Style: CashTotal,Oswald,60,&H00FFFFFF,&H00FFFFFF,&H00000000,&H1A000000,-1,0,0,0,100,100,1,0,1,6,3,8,60,60,980,1
Style: SummaryBox,Oswald,76,&H0000FFFF,&H0000FFFF,&H00000000,&H2A000000,-1,0,0,0,100,100,1,0,1,8,4,8,60,60,720,1
Style: CalloutCTA,Oswald,66,&H0066FF66,&H0066FF66,&H00000000,&H1A000000,-1,0,0,0,100,100,0,0,1,7,2,8,60,60,360,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

def ass_time(sec):
    sec = max(0.0, sec)
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = sec % 60
    return f"{h}:{m:02d}:{s:05.2f}"

def split_phrases(words, min_words=2, max_words=4):
    phrases, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) >= max_words or (len(cur) >= min_words and BREAK_PUNCT.search(w["word"])):
            phrases.append(cur)
            cur = []
    if cur:
        if len(cur) < min_words and phrases and len(phrases[-1]) + len(cur) <= max_words + 1:
            phrases[-1].extend(cur)
        else:
            phrases.append(cur)
    return phrases

def build_events(segments):
    events = []
    total_words = 0
    for seg in segments:
        words = seg["words"]
        total_words += len(words)
        
        # Chuẩn hóa từ
        norm_words = []
        for w in words:
            wt = w["word"].strip().upper()
            st = float(w["master_start"])
            en = float(w["master_end"])
            norm_words.append({"word": wt, "start": st, "end": en})
            
        phrases = split_phrases(norm_words)
        for p in phrases:
            p_end = p[-1]["end"] + 0.08
            for i, w in enumerate(p):
                st = w["start"]
                en = max(st + 0.1, p[i + 1]["start"]) if i < len(p) - 1 else max(st + 0.15, p_end)
                toks = [(CYAN if j == i else YELLOW) + x["word"] for j, x in enumerate(p)]
                
                # Hiệu ứng nảy nhẹ khi chuyển cụm
                if len(p) == 1:
                    anim = r"{\fad(40,50)\t(0,40,\fscx112\fscy112)\t(40,90,\fscx100\fscy100)}"
                elif i == 0:
                    anim = r"{\fad(40,0)\t(0,40,\fscx112\fscy112)\t(40,90,\fscx100\fscy100)}"
                elif i == len(p) - 1:
                    anim = r"{\fad(0,50)}"
                else:
                    anim = ""
                events.append((st, en, anim + " ".join(toks)))
    return events, total_words

def main():
    cleaned_path = Path("processed/cleaned_words_176k_long.json")
    with open(cleaned_path, "r", encoding="utf-8") as f:
        segments = json.load(f)

    events, total_words = build_events(segments)

    lines = [HEADER]

    # 1. Hook Titles (0s -> 5.5s)
    lines.append("; --- HOOK TITLES ---\n")
    lines.append(f"Dialogue: 1,{ass_time(0.0)},{ass_time(5.5)},Hook1,,0,0,0,,{{\\fad(100,100)}}THỬ THÁCH 1 NGÀY\n")
    lines.append(f"Dialogue: 1,{ass_time(0.0)},{ass_time(5.5)},Hook2,,0,0,0,,{{\\fad(100,100)}}CHẠY XE XANH SM\n")

    # 2. 6 Thẻ tiền Hoàn Thành Đơn
    orders_info = [
        {"order": 1, "st": 26.8, "et": 31.8, "amt": "+16.000đ", "total": "TỔNG THU: 16.000đ"},
        {"order": 2, "st": 44.8, "et": 49.5, "amt": "+22.000đ", "total": "TỔNG THU: 38.000đ"},
        {"order": 3, "st": 65.4, "et": 70.4, "amt": "+35.000đ", "total": "TỔNG THU: 73.000đ"},
        {"order": 4, "st": 82.7, "et": 90.0, "amt": "+28.000đ", "total": "TỔNG THU: 101.000đ"},
        {"order": 5, "st": 105.1, "et": 109.4, "amt": "+42.000đ", "total": "TỔNG THU: 143.000đ"},
        {"order": 6, "st": 124.8, "et": 129.1, "amt": "+33.000đ", "total": "TỔNG THU: 176.000đ"}
    ]

    lines.append("\n; --- 6 THẺ TIỀN NHẬN ĐƠN ---\n")
    for o in orders_info:
        st_s = ass_time(o["st"])
        et_s = ass_time(o["et"])
        title = f"✓ HOÀN THÀNH ĐƠN #{o['order']}"
        amt = o['amt']
        tot = o['total']
        
        # Animation pop in
        anim_hdr = r"{\fad(80,80)\t(0,60,\fscx110\fscy110)\t(60,120,\fscx100\fscy100)}"
        anim_amt = r"{\fad(80,80)\t(0,80,\fscx115\fscy115)\t(80,140,\fscx100\fscy100)}"
        anim_tot = r"{\fad(80,80)}"
        
        lines.append(f"Dialogue: 2,{st_s},{et_s},CashHeader,,0,0,0,,{anim_hdr}{title}\n")
        lines.append(f"Dialogue: 2,{st_s},{et_s},CashAmount,,0,0,0,,{anim_amt}{amt}\n")
        lines.append(f"Dialogue: 2,{st_s},{et_s},CashTotal,,0,0,0,,{anim_tot}{tot}\n")

    # 3. Thẻ Tổng Thu Cuối Ngày 176k (129.5s -> 142.5s)
    lines.append("\n; --- THẺ TỔNG THU CUỐI NGÀY 176K ---\n")
    st_sum = ass_time(129.5)
    et_sum = ass_time(142.5)
    anim_sum = r"{\fad(100,100)\t(0,80,\fscx112\fscy112)\t(80,150,\fscx100\fscy100)}"
    lines.append(f"Dialogue: 2,{st_sum},{et_sum},SummaryBox,,0,0,0,,{anim_sum}★ TỔNG THU HÔM NAY: 176.000đ ★\\N(6 ĐƠN XE XANHSM)\n")

    # 4. Callout CTA (143.0s -> 153.0s, nửa trên khung hình)
    lines.append("\n; --- CALLOUT TƯƠNG TÁC ---\n")
    st_cta = ass_time(143.0)
    et_cta = ass_time(153.0)
    anim_cta = r"{\fad(100,100)}"
    lines.append(f"Dialogue: 2,{st_cta},{et_cta},CalloutCTA,,0,0,0,,{anim_cta}TIM ❤️ VÀ COMMENT GIAO LƯU NHÉ 👍\n")

    # 5. Phụ đề Dynamic Karaoke
    lines.append("\n; --- DYNAMIC WORD KARAOKE EVENTS ---\n")
    for st, en, text in events:
        lines.append(f"Dialogue: 0,{ass_time(st)},{ass_time(en)},DynamicSub,,0,0,0,,{text}\n")

    out_file = Path("processed/vlog_xanhsm_176k_long_master.ass")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("".join(lines))

    print(f"[+] ĐÃ TẠO THÀNH CÔNG: {out_file}")
    print(f"    - Tổng số từ: {total_words}")
    print(f"    - Tổng số events karaoke: {len(events)}")
    print(f"    - Vị trí phụ đề: Alignment 2, MarginV 550 (Safe Zone Y ≈ -0.38)")
    print(f"    - 6 Thẻ tiền nổ theo SFX: Đơn 1 (+16k), Đơn 2 (+22k), Đơn 3 (+35k), Đơn 4 (+28k), Đơn 5 (+42k), Đơn 6 (+33k)")
    print(f"    - Thẻ tổng kết: 176.000đ")

if __name__ == "__main__":
    main()
