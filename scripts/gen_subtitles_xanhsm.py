"""
Tạo file SRT phụ đề cho video XanhSM Night Shift
Style: IN HOA, highlight từ khóa trong ASS format
"""
import os

# Timestamp voiceover (ước tính dựa theo tốc độ 190 WPM và script gTTS)
# Format: (start_sec, end_sec, text, is_keyword)
SUBTITLES = [
    (1.5,  4.5,  "HÔM NAY MÌNH BẮT ĐẦU CA", False),
    (4.5,  7.5,  "TỪ SÁU GIỜ CHIỀU", True),          # keyword: số giờ
    (7.5,  11.0, "TRỜI CÒN SÁNG", False),
    (11.0, 14.5, "MÀ MÌNH ĐÃ PHÓNG RA ĐƯỜNG RỒI", False),
    (15.0, 18.5, "ĐÊM NAY KHU NÀY VẮNG", False),
    (18.5, 22.0, "HƠN THƯỜNG LỆ...", False),
    (22.0, 26.0, "CỨ NGỒI CHỜ...", False),
    (26.0, 30.0, "RỒI ĐƠN MỚI NỔ", True),             # keyword: đơn nổ
    (31.0, 35.0, "NHƯNG ĐÂY LÀ NGHỀ MÌNH ĐÃ CHỌN", True),  # keyword: chọn
    (35.0, 39.0, "MỖI CHUYẾN XE", True),               # keyword: mỗi chuyến
    (39.0, 43.0, "LÀ MỘT CÂU CHUYỆN", False),
    (43.0, 47.0, "CÓ CHUYẾN VUI, CÓ CHUYẾN MỆT...", False),
    (47.0, 51.0, "NHƯNG MÌNH VẪN CỨ ĐI", True),        # keyword
    (51.0, 55.0, "VÌ ĐÓ LÀ CÁCH MÌNH KIẾM SỐNG", True), # keyword: kiếm sống
    (55.0, 59.0, "VÀ MÌNH TỰ HÀO VỀ ĐIỀU ĐÓ", True),
    (60.0, 65.0, "NẾU BẠN CŨNG ĐANG CHẠY XE CÔNG NGHỆ", False),
    (65.0, 69.0, "MÌNH HIỂU CẢM GIÁC CỦA BẠN", True),
    (70.0, 74.0, "CỨ THẾ MÀ ĐI THÔI ANH EM ƠI!", True),  # keyword: kêu gọi
    (74.0, 77.0, "ĐỪNG QUÊN BẤM TIM VÀ THEO DÕI NHÉ! ❤️", True),
]

def sec_to_srt(s):
    h = int(s // 3600)
    m = int((s % 3600) // 60)
    sec = s % 60
    return f"{h:02d}:{m:02d}:{sec:06.3f}".replace(".", ",")

# Tạo SRT thuần (CapCut có thể import)
out_dir = r"c:\QuangHy\editvideo\processed"
srt_path = os.path.join(out_dir, "xanhsm_nightshift.srt")

with open(srt_path, "w", encoding="utf-8") as f:
    for i, (start, end, text, is_kw) in enumerate(SUBTITLES, 1):
        f.write(f"{i}\n")
        f.write(f"{sec_to_srt(start)} --> {sec_to_srt(end)}\n")
        f.write(f"{text}\n\n")

print(f"SRT created: {srt_path} ({len(SUBTITLES)} entries)")

# Tạo ASS với màu highlight (dùng trong FFmpeg subtitles filter)
# Màu chính: Trắng #FFFFFF, viền đen #000000
# Màu keyword: Xanh Neon #66FFFF (dùng ký hiệu &H00FFFF66& trong ASS BGR)
# ASS color format: &HAABBGGRR -> Xanh Neon #66FFFF = &H00FFFF66&

ass_path = os.path.join(out_dir, "xanhsm_nightshift.ass")

ASS_HEADER = """[Script Info]
Title: XanhSM NightShift Subtitles
ScriptType: v4.00+
WrapStyle: 0
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Normal,Be Vietnam Pro,62,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,4,1,2,60,60,120,1
Style: Keyword,Be Vietnam Pro,68,&H00FFFF66,&H00FFFF66,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,4,2,2,60,60,120,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

def sec_to_ass(s):
    h = int(s // 3600)
    m = int((s % 3600) // 60)
    sec = s % 60
    return f"{h}:{m:02d}:{sec:05.2f}"

with open(ass_path, "w", encoding="utf-8") as f:
    f.write(ASS_HEADER)
    for start, end, text, is_kw in SUBTITLES:
        style = "Keyword" if is_kw else "Normal"
        f.write(f"Dialogue: 0,{sec_to_ass(start)},{sec_to_ass(end)},{style},,0,0,0,,{text}\n")

print(f"ASS created: {ass_path}")
print("\nPhụ đề sẵn sàng để burn vào video hoặc import vào CapCut!")
