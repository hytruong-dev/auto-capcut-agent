"""
Script render Vlog_XanhSM_NightShift_FINAL.mp4
- Burn-in ASS subtitles (chuẩn Typography TikTok, Keyword vàng, Normal trắng)
- Burn-in Hook Title 2 tầng (MỘT CA ĐÊM đỏ + CHẠY XANHSM SÀI GÒN vàng)
- Mix BGM Lofi (âm lượng 0.14) cùng voiceover & ambient gốc
- Xuất file hoàn chỉnh 1080x1920 30fps
"""
import subprocess, os

ASS_PATH = r"c:\QuangHy\editvideo\processed\xanhsm_nightshift_master.ass"
VIDEO_IN = r"c:\QuangHy\editvideo\processed\Vlog_XanhSM_NightShift_v2.mp4"
BGM_IN = r"c:\QuangHy\editvideo\processed\bgm_nightshift_loop.mp3"
VIDEO_OUT = r"c:\QuangHy\editvideo\processed\Vlog_XanhSM_NightShift_FINAL.mp4"

# 1. Tạo file ASS master có cả Subtitles + Hook Title + Callout
ass_content = """[Script Info]
Title: XanhSM NightShift Master Subtitles
ScriptType: v4.00+
WrapStyle: 0
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: SubtitleNormal,Arial,52,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,5,2,2,60,60,180,1
Style: SubtitleKeyword,Arial,56,&H0000E6FF,&H0000E6FF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,5,2,2,60,60,180,1
Style: Hook1,Arial,82,&H003333FF,&H003333FF,&H00FFFFFF,&H90000000,-1,0,0,0,100,100,1,0,1,6,3,8,60,60,340,1
Style: Hook2,Arial,92,&H0000E6FF,&H0000E6FF,&H00000000,&H90000000,-1,0,0,0,100,100,1,0,1,7,3,8,60,60,450,1
Style: Callout,Arial,56,&H0066FF66,&H0066FF66,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,5,2,2,60,60,260,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
; --- HOOK TITLES (0s -> 5.5s) ---
Dialogue: 1,0:00:00.00,0:00:05.50,Hook1,,0,0,0,,MỘT CA ĐÊM
Dialogue: 1,0:00:00.00,0:00:05.50,Hook2,,0,0,0,,CHẠY XANHSM SÀI GÒN

; --- SUBTITLES ---
Dialogue: 0,0:00:01.50,0:00:04.50,SubtitleNormal,,0,0,0,,HÔM NAY MÌNH BẮT ĐẦU CA
Dialogue: 0,0:00:04.50,0:00:07.50,SubtitleKeyword,,0,0,0,,TỪ SÁU GIỜ CHIỀU
Dialogue: 0,0:00:07.50,0:00:11.00,SubtitleNormal,,0,0,0,,TRỜI CÒN SÁNG
Dialogue: 0,0:00:11.00,0:00:14.50,SubtitleNormal,,0,0,0,,MÀ MÌNH ĐÃ PHÓNG RA ĐƯỜNG RỒI
Dialogue: 0,0:00:15.00,0:00:18.50,SubtitleNormal,,0,0,0,,ĐÊM NAY KHU NÀY VẮNG
Dialogue: 0,0:00:18.50,0:00:22.00,SubtitleNormal,,0,0,0,,HƠN THƯỜNG LỆ...
Dialogue: 0,0:00:22.00,0:00:26.00,SubtitleNormal,,0,0,0,,CỨ NGỒI CHỜ...
Dialogue: 0,0:00:26.00,0:00:30.00,SubtitleKeyword,,0,0,0,,RỒI ĐƠN MỚI NỔ
Dialogue: 0,0:00:31.00,0:00:35.00,SubtitleKeyword,,0,0,0,,NHƯNG ĐÂY LÀ NGHỀ MÌNH ĐÃ CHỌN
Dialogue: 0,0:00:35.00,0:00:39.00,SubtitleKeyword,,0,0,0,,MỖI CHUYẾN XE
Dialogue: 0,0:00:39.00,0:00:43.00,SubtitleNormal,,0,0,0,,LÀ MỘT CÂU CHUYỆN
Dialogue: 0,0:00:43.00,0:00:47.00,SubtitleNormal,,0,0,0,,CÓ CHUYẾN VUI, CÓ CHUYẾN MỆT...
Dialogue: 0,0:00:47.00,0:00:51.00,SubtitleKeyword,,0,0,0,,NHƯNG MÌNH VẪN CỨ ĐI
Dialogue: 0,0:00:51.00,0:00:55.00,SubtitleKeyword,,0,0,0,,VÌ ĐÓ LÀ CÁCH MÌNH KIẾM SỐNG
Dialogue: 0,0:00:55.00,0:00:59.00,SubtitleKeyword,,0,0,0,,VÀ MÌNH TỰ HÀO VỀ ĐIỀU ĐÓ
Dialogue: 0,0:01:00.00,0:01:05.00,SubtitleNormal,,0,0,0,,NẾU BẠN CŨNG ĐANG CHẠY XE CÔNG NGHỆ
Dialogue: 0,0:01:05.00,0:01:09.00,SubtitleKeyword,,0,0,0,,MÌNH HIỂU CẢM GIÁC CỦA BẠN
Dialogue: 0,0:01:10.00,0:01:14.00,SubtitleKeyword,,0,0,0,,CỨ THẾ MÀ ĐI THÔI ANH EM ƠI!
Dialogue: 0,0:01:14.00,0:01:17.00,SubtitleKeyword,,0,0,0,,ĐỪNG QUÊN BẤM TIM VÀ THEO DÕI NHÉ! ❤️

; --- OUTRO CALLOUT (68s -> 78s) ---
Dialogue: 1,0:01:08.00,0:01:18.00,Callout,,0,0,0,,TIM ❤️ NẾU BẠN CŨNG THÍCH CHẠY ĐÊM 🌙
"""

with open(ASS_PATH, "w", encoding="utf-8") as f:
    f.write(ass_content)
print(f"[+] Đã tạo {ASS_PATH}")

# 2. Render bằng FFmpeg: burn ass subtitle + mix bgm
ass_filter_path = ASS_PATH.replace("\\", "/").replace(":", "\\:")

cmd = [
    "ffmpeg", "-y",
    "-i", VIDEO_IN,
    "-i", BGM_IN,
    "-filter_complex",
    f"[0:v]ass='{ass_filter_path}'[v];[1:a]volume=0.14[bgm];[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=2[a]",
    "-map", "[v]",
    "-map", "[a]",
    "-c:v", "libx264",
    "-crf", "19",
    "-preset", "fast",
    "-c:a", "aac",
    "-b:a", "192k",
    VIDEO_OUT
]

print("[*] Đang render Master Final Video...")
res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode == 0:
    size_mb = os.path.getsize(VIDEO_OUT) / (1024 * 1024)
    print(f"[SUCCESS] Đã tạo thành công: {VIDEO_OUT} ({size_mb:.1f} MB)")
else:
    print("[ERROR] Render thất bại:")
    print(res.stderr[-500:])
