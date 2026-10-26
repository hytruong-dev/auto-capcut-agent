import json, sys, os

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

CHUNKS_FILE = r"processed\dynamic_short_subtitles.json"
SRT_FILE = r"processed\xanhsm_story.srt"
ASS_FILE = r"processed\xanhsm_story_master.ass"

with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
    chunks = json.load(f)

def sec_to_srt(s):
    h = int(s // 3600)
    m = int((s % 3600) // 60)
    sec = s % 60
    return f"{h:02d}:{m:02d}:{sec:06.3f}".replace(".", ",")

def sec_to_ass(s):
    h = int(s // 3600)
    m = int((s % 3600) // 60)
    sec = s % 60
    return f"{h}:{m:02d}:{sec:05.2f}"

# 1. Ghi file SRT với 75 phân đoạn ngắn
with open(SRT_FILE, "w", encoding="utf-8") as f:
    for idx, c in enumerate(chunks, 1):
        f.write(f"{idx}\n")
        f.write(f"{sec_to_srt(c['start'])} --> {sec_to_srt(c['end'])}\n")
        f.write(f"{c['text']}\n\n")

print(f"[+] Đã tạo file SRT ngắn gọn: {SRT_FILE} ({len(chunks)} phân đoạn)")

# 2. Ghi file ASS Master với hiệu ứng In/Out animation & Two-Tone (Cyan + Vàng) theo Hình 2
ASS_HEADER = """[Script Info]
Title: Dynamic Short Chunks Subtitles (Oswald-Bold Pop In/Out Style)
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
; --- DUAL-LAYER HOOK TITLE (0.0s -> 6.5s) ---
Dialogue: 1,0:00:00.00,0:00:06.50,Hook1,,0,0,0,,{\\fad(120,120)}THỬ THÁCH 1 NGÀY
Dialogue: 1,0:00:00.00,0:00:06.50,Hook2,,0,0,0,,{\\fad(120,120)}CHẠY XANH SM SÀI GÒN

; --- DYNAMIC SHORT SUBTITLES (2-4 TỪ / CỤM, HIỆU ỨNG IN & OUT) ---
"""

with open(ASS_FILE, "w", encoding="utf-8") as f:
    f.write(ASS_HEADER)
    
    for c in chunks:
        s_str = sec_to_ass(c['start'])
        e_str = sec_to_ass(c['end'])
        raw_text = c['text'].strip()
        words = raw_text.split()
        
        # Tạo Two-Tone Style giống Hình 2:
        # Từ đầu tiên màu Cyan xanh ngọc (&H00FFFF66&), các từ tiếp theo màu Vàng chanh (&H0000FFF0&)
        if len(words) >= 2:
            first_part = words[0]
            second_part = " ".join(words[1:])
            formatted_text = f"{{\\c&H00FFFF66&}}{first_part} {{\\c&H0000FFF0&}}{second_part}"
        else:
            formatted_text = f"{{\\c&H0000FFF0&}}{raw_text}"
            
        # Hiệu ứng In & Out:
        # - In: Phóng to nhẹ 112% trong 60ms rồi hồi về 100% trong 60ms kèm fade-in 70ms (Pop In siêu nét)
        # - Out: Mờ dần (Fade Out 70ms)
        anim_prefix = "{\\fad(70,70)\\t(0,60,\\fscx112\\fscy112)\\t(60,120,\\fscx100\\fscy100)}"
        full_line = f"{anim_prefix}{formatted_text}"
        
        f.write(f"Dialogue: 0,{s_str},{e_str},DynamicSub,,0,0,0,,{full_line}\n")
        
    # Outro Callout
    f.write("; --- OUTRO CALLOUT ---\n")
    f.write(f"Dialogue: 1,{sec_to_ass(71.92)},{sec_to_ass(81.85)},Callout,,0,0,0,,{{\\fad(150,150)}}TIM ❤️ NẾU BẠN CŨNG THÍCH CHẠY ĐÊM 🌙\n")

print(f"[+] Đã tạo file ASS Master phụ đề ngắn có hiệu ứng In & Out: {ASS_FILE}")
