import os, sys, json

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

TIMELINE_FILE = r"processed\story_voiceover_timeline.json"
SRT_FILE = r"processed\xanhsm_story.srt"
ASS_FILE = r"processed\xanhsm_story_master.ass"

with open(TIMELINE_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

segments = data["segments"]

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

# 1. Ghi SRT
with open(SRT_FILE, "w", encoding="utf-8") as f:
    for idx, seg in enumerate(segments, 1):
        f.write(f"{idx}\n")
        f.write(f"{sec_to_srt(seg['start_time'])} --> {sec_to_srt(seg['end_time'])}\n")
        f.write(f"{seg['text'].upper()}\n\n")

print(f"[+] Đã tạo file SRT: {SRT_FILE} ({len(segments)} phụ đề)")

# 2. Ghi ASS Master với Styles:
# - SubtitleNormal: Chữ trắng viền đen
# - SubtitleKeyword: Chữ vàng tươi #FFEE00 (&H0000EEFF) viền đen
# - Hook1: Chữ đỏ cam viền trắng (#FF3333 -> &H003333FF)
# - Hook2: Chữ vàng tươi viền đen (#FFEE00 -> &H0000EEFF)
# - Callout: Chữ xanh ngọc neon (#66FF66 -> &H0066FF66)

ASS_HEADER = """[Script Info]
Title: XanhSM Story Master Subtitles (Oswald-Bold Style)
ScriptType: v4.00+
WrapStyle: 0
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: SubtitleNormal,Oswald Bold,64,&H0000FFF0,&H0000FFF0,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,6,2,2,60,60,180,1
Style: SubtitleKeyword,Oswald Bold,68,&H0000FFF0,&H0000FFF0,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,7,2,2,60,60,180,1
Style: Hook1,Oswald Bold,88,&H003333FF,&H003333FF,&H00FFFFFF,&H90000000,-1,0,0,0,100,100,1,0,1,8,3,8,60,60,340,1
Style: Hook2,Oswald Bold,98,&H0000FFF0,&H0000FFF0,&H00000000,&H90000000,-1,0,0,0,100,100,1,0,1,9,3,8,60,60,460,1
Style: Callout,Oswald Bold,60,&H0066FF66,&H0066FF66,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,6,2,8,60,60,380,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
; --- DUAL-LAYER HOOK TITLE (0.0s -> 6.5s) ---
Dialogue: 1,0:00:00.00,0:00:06.50,Hook1,,0,0,0,,THỬ THÁCH 1 NGÀY
Dialogue: 1,0:00:00.00,0:00:06.50,Hook2,,0,0,0,,CHẠY XANH SM SÀI GÒN

; --- SUBTITLES ---
"""

with open(ASS_FILE, "w", encoding="utf-8") as f:
    f.write(ASS_HEADER)
    
    # Keyword segments IDs: 1, 2, 4, 5, 7, 9, 10, 11, 14, 15, 16, 17, 18, 19
    keyword_ids = {1, 2, 4, 5, 7, 9, 10, 11, 14, 15, 16, 17, 18, 19}
    
    for seg in segments:
        s_id = seg["id"]
        start_str = sec_to_ass(seg["start_time"])
        end_str = sec_to_ass(seg["end_time"])
        style = "SubtitleKeyword" if s_id in keyword_ids else "SubtitleNormal"
        text = seg["text"].upper()
        f.write(f"Dialogue: 0,{start_str},{end_str},{style},,0,0,0,,{text}\n")
        
    # --- OUTRO CALLOUT (71.9s -> 81.8s) ---
    f.write("; --- OUTRO CALLOUT ---\n")
    f.write(f"Dialogue: 1,{sec_to_ass(71.92)},{sec_to_ass(81.85)},Callout,,0,0,0,,TIM ❤️ NẾU BẠN CŨNG THÍCH CHẠY ĐÊM 🌙\n")

print(f"[+] Đã tạo file ASS Master: {ASS_FILE}")
