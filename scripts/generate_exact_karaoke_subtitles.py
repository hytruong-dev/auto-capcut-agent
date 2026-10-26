import sys, os, json, re
sys.path.append('.')
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from scripts.build_dynamic_karaoke_subtitles import PHRASE_DEFS

seg_data = json.load(open('processed/exact_segment_words.json', encoding='utf-8'))

# Colors:
# Cyan: &H00FFFF66& (#66FFFF in BGR)
# Lemon Yellow: &H0000FFF0& (#F0FF00 in BGR)
COLOR_CYAN = r"{\c&H00FFFF66&}"
COLOR_YELLOW = r"{\c&H0000FFF0&}"

def to_ass_time(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = sec % 60
    return f"{h}:{m:02d}:{s:05.2f}"

# Map phrases to exact whisper words
all_karaoke_events = []
all_srt_segments = []
srt_counter = 1

for seg_idx, (phrases, s_info) in enumerate(zip(PHRASE_DEFS, seg_data)):
    w_words = s_info['words']
    seg_start = s_info['seg_start']
    seg_end = s_info['seg_end']
    
    flat_def_words = []
    for p in phrases:
        for w in p:
            flat_def_words.append(w)
            
    n_def = len(flat_def_words)
    n_wh = len(w_words)
    
    word_timings = []
    if n_def == n_wh:
        for dw, ww in zip(flat_def_words, w_words):
            word_timings.append({
                "word": dw,
                "start": ww['master_start'],
                "end": ww['master_end']
            })
    else:
        wh_start = w_words[0]['master_start']
        wh_end = w_words[-1]['master_end']
        time_span = wh_end - wh_start
        for i, dw in enumerate(flat_def_words):
            t_s = wh_start + (i / n_def) * time_span
            t_e = wh_start + ((i + 1) / n_def) * time_span
            word_timings.append({
                "word": dw,
                "start": round(t_s, 3),
                "end": round(t_e, 3)
            })

    # Bây giờ gom thành phrases và tạo karaoke sub-events
    cur_idx = 0
    for p in phrases:
        p_len = len(p)
        p_words = word_timings[cur_idx : cur_idx + p_len]
        cur_idx += p_len
        
        phrase_start = p_words[0]['start']
        phrase_end = p_words[-1]['end']
        
        # Cho SRT
        all_srt_segments.append({
            "start": phrase_start,
            "end": phrase_end,
            "text": " ".join(p)
        })
        
        # Tạo karaoke sub-events cho từng từ
        for w_idx in range(p_len):
            w_start = p_words[w_idx]['start']
            # End time của word active
            if w_idx < p_len - 1:
                w_end = max(w_start + 0.1, p_words[w_idx + 1]['start'])
            else:
                w_end = max(w_start + 0.15, phrase_end)
                
            # Đảm bảo không chồng chéo vô lý
            if w_end <= w_start:
                w_end = w_start + 0.2
                
            # Xây dựng chuỗi text: Từ w_idx đổi sang CYAN, các từ khác YELLOW
            tokens = []
            for j in range(p_len):
                word_text = p[j]
                if j == w_idx:
                    tokens.append(f"{COLOR_CYAN}{word_text}")
                else:
                    tokens.append(f"{COLOR_YELLOW}{word_text}")
            
            # Ghép text
            line_body = " ".join(tokens)
            
            # Hiệu ứng In & Out:
            # - Từ đầu tiên của phrase: có Pop In và Fade In
            # - Từ cuối cùng của phrase: có Fade Out
            # - Nếu phrase chỉ có 1 từ: có cả Pop In, Fade In và Fade Out
            if p_len == 1:
                anim_tag = r"{\fad(50,60)\t(0,50,\fscx112\fscy112)\t(50,110,\fscx100\fscy100)}"
            elif w_idx == 0:
                anim_tag = r"{\fad(50,0)\t(0,50,\fscx112\fscy112)\t(50,110,\fscx100\fscy100)}"
            elif w_idx == p_len - 1:
                anim_tag = r"{\fad(0,60)}"
            else:
                anim_tag = ""
                
            full_line_text = f"{anim_tag}{line_body}"
            
            all_karaoke_events.append({
                "start": w_start,
                "end": w_end,
                "text": full_line_text
            })

print(f"Generated {len(all_karaoke_events)} karaoke sub-events across {len(all_srt_segments)} phrases.")

# Tạo file ASS
ass_header = """[Script Info]
Title: Dynamic Word Karaoke Subtitles (Oswald-Bold CapCut Style)
ScriptType: v4.00+
WrapStyle: 0
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: DynamicSub,Oswald Bold,74,&H0000FFF0,&H0000FFF0,&H00000000,&H90000000,-1,0,0,0,100,100,1,0,1,7,2,2,60,60,220,1
Style: Hook1,Oswald Bold,88,&H003333FF,&H003333FF,&H00FFFFFF,&H90000000,-1,0,0,0,100,100,1,0,1,8,3,8,60,60,340,1
Style: Hook2,Oswald Bold,98,&H0000FFF0,&H0000FFF0,&H00000000,&H90000000,-1,0,0,0,100,100,1,0,1,9,3,8,60,60,460,1
Style: Callout,Oswald Bold,60,&H0066FF66,&H0066FF66,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,6,2,8,60,60,380,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
; --- DUAL-LAYER HOOK TITLE (0.0s -> 5.5s) ---
Dialogue: 1,0:00:00.00,0:00:05.50,Hook1,,0,0,0,,{\\fad(120,120)}THỬ THÁCH 1 NGÀY
Dialogue: 1,0:00:00.00,0:00:05.50,Hook2,,0,0,0,,{\\fad(120,120)}CHẠY XANH SM SÀI GÒN

; --- DYNAMIC WORD-BY-WORD KARAOKE HIGHLIGHT ---
"""

ass_lines = [ass_header]
for ev in all_karaoke_events:
    st_str = to_ass_time(ev['start'])
    et_str = to_ass_time(ev['end'])
    ass_lines.append(f"Dialogue: 0,{st_str},{et_str},DynamicSub,,0,0,0,,{ev['text']}\n")

# Callout ở cuối
ass_lines.append("; --- OUTRO CALLOUT BOX (74.68s -> 79.18s) ---\n")
ass_lines.append("Dialogue: 1,0:01:14.68,0:01:19.18,Callout,,0,0,0,,{\\fad(150,150)}TIM 💚 NẾU BẠN CŨNG THÍCH CHẠY ĐÊM 🌛\n")

ass_path = "processed/xanhsm_story_master.ass"
with open(ass_path, "w", encoding="utf-8") as f:
    f.writelines(ass_lines)
print(f"[SUCCESS] Saved ASS master subtitles to: {ass_path}")

# Tạo file SRT đồng bộ
srt_path = "processed/xanhsm_story.srt"
with open(srt_path, "w", encoding="utf-8") as f:
    for idx, s in enumerate(all_srt_segments, 1):
        def to_srt_time(sec):
            h = int(sec // 3600)
            m = int((sec % 3600) // 60)
            s_int = int(sec % 60)
            ms = int((sec - int(sec)) * 1000)
            return f"{h:02d}:{m:02d}:{s_int:02d},{ms:03d}"
        f.write(f"{idx}\n")
        f.write(f"{to_srt_time(s['start'])} --> {to_srt_time(s['end'])}\n")
        f.write(f"{s['text']}\n\n")
print(f"[SUCCESS] Saved SRT subtitles to: {srt_path}")

# Lưu JSON dữ liệu phrases hoàn chỉnh
json_path = "processed/dynamic_short_subtitles.json"
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(all_srt_segments, f, ensure_ascii=False, indent=2)
print(f"[SUCCESS] Saved phrases map to: {json_path}")
