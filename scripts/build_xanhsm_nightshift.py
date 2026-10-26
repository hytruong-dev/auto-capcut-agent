"""
Script FFmpeg cắt ghép video XanhSM Night Shift
Output: 9:16 dọc (1080x1920), ghép theo EDL, crop thông minh từ 2688x1512 DJI footage
"""
import subprocess
import os
import json

# =============================================
# CẤU HÌNH
# =============================================
BASE_DIR = r"c:\QuangHy\editvideo"
RAW_DIR = os.path.join(BASE_DIR, "raw_footage")
OUT_DIR = os.path.join(BASE_DIR, "processed")
TEMP_DIR = os.path.join(OUT_DIR, "temp_segments")
VO_FILE = os.path.join(OUT_DIR, "voiceover", "xanhsm_nightshift_vo.mp3")

os.makedirs(TEMP_DIR, exist_ok=True)

# =============================================
# EDIT DECISION LIST (EDL)
# Footage DJI: 2688x1512, cần rotate 90° CW và crop thành 1080x1920
# rotate=1 trong ffmpeg = 90° CW (transpose=1)
# Sau rotate 90°: ảnh trở thành 1512x2688 -> scale & crop thành 1080x1920
# =============================================
FOOTAGE = {
    "DJI_0057": os.path.join(RAW_DIR, "DJI_20260908084243_0057_D.MP4"),
    "DJI_0062": os.path.join(RAW_DIR, "DJI_20260908183824_0062_D.MP4"),
    "DJI_0064": os.path.join(RAW_DIR, "DJI_20260908185603_0064_D.MP4"),
}

# EDL: (segment_id, source, ss, t) - ss=start in source, t=duration
# Thêm padding 0.18s đầu, 0.22s cuối theo quy chuẩn bộ nhớ
PADDING_IN  = 0.18
PADDING_OUT = 0.22

EDL = [
    # id,  source,     ss,      duration
    (1,  "DJI_0057",  2.0,     5.0),   # Hook ban ngày
    (2,  "DJI_0057",  7.0,     10.0),  # Giới thiệu ban ngày
    (3,  "DJI_0062",  0.5,     10.0),  # Đêm hẻm - chờ đơn
    (4,  "DJI_0062",  12.0,    10.0),  # Đêm - điện thoại app
    (5,  "DJI_0062",  40.0,    7.5),   # Đêm - cao trào 1
    (6,  "DJI_0064",  30.0,    7.5),   # Đêm chạy hẻm - cao trào 2
    (7,  "DJI_0064",  80.0,    7.5),   # Đêm tiếp - outro 1
    (8,  "DJI_0064",  140.0,   7.5),   # Đêm sâu - outro 2
    (9,  "DJI_0064",  160.0,   12.0),  # Fade out cuối
]

# =============================================
# BƯỚC 1: Cắt từng segment, rotate + crop 9:16
# =============================================
# DJI: 2688x1512 (16:9 landscape)
# Sau transpose=1: 1512x2688 (9:16 portrait)
# Scale để fill 1080x1920: scale=1080:1920 (aspect ratio gần đúng: 1512/2688 = 0.5625 = 9:16 PERFECT!)
# Tỷ lệ 2688/1512 = 1.777... = 16:9 → sau rotate = 1512/2688 = 9:16 → ĐÚNG 9:16!
# Chỉ cần scale lên từ 1512x2688 → 1080x1920

VFILTER_9_16 = "transpose=1,scale=1080:1920:flags=lanczos"

segment_files = []

for seg_id, source, ss, dur in EDL:
    src_path = FOOTAGE[source]
    out_path = os.path.join(TEMP_DIR, f"seg_{seg_id:02d}.mp4")
    segment_files.append(out_path)
    
    # Áp dụng padding
    ss_padded = max(0, ss - PADDING_IN)
    dur_padded = dur + PADDING_IN + PADDING_OUT
    
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(ss_padded),
        "-i", src_path,
        "-t", str(dur_padded),
        "-vf", VFILTER_9_16,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "20",
        "-c:a", "aac",
        "-ar", "48000",
        "-ac", "2",
        "-b:a", "192k",
        out_path
    ]
    
    print(f"Cắt segment {seg_id}: {source} @ {ss:.1f}s, dur={dur:.1f}s ...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  LỖI: {result.stderr[-300:]}")
    else:
        size = os.path.getsize(out_path) / 1024 / 1024
        print(f"  OK - {size:.1f} MB")

print(f"\nHoàn thành {len(segment_files)} segments!")

# =============================================
# BƯỚC 2: Tạo file list để concat
# =============================================
list_file = os.path.join(TEMP_DIR, "concat_list.txt")
with open(list_file, "w", encoding="utf-8") as f:
    for seg_path in segment_files:
        f.write(f"file '{seg_path}'\n")

# =============================================
# BƯỚC 3: Ghép tất cả segments
# =============================================
raw_concat = os.path.join(OUT_DIR, "xanhsm_nightshift_raw.mp4")
cmd_concat = [
    "ffmpeg", "-y",
    "-f", "concat",
    "-safe", "0",
    "-i", list_file,
    "-c", "copy",
    raw_concat
]
print("\nGhép tất cả segments...")
r = subprocess.run(cmd_concat, capture_output=True, text=True)
if r.returncode != 0:
    print(f"LỖI concat: {r.stderr[-400:]}")
else:
    size = os.path.getsize(raw_concat) / 1024 / 1024
    print(f"OK - Raw video: {size:.1f} MB → {raw_concat}")

# =============================================
# BƯỚC 4: Mix voiceover vào video
# Voiceover: -14 LUFS target, BGM nếu có thì -28dB
# =============================================
final_output = os.path.join(OUT_DIR, "Vlog_XanhSM_NightShift_v1.mp4")

if os.path.exists(VO_FILE):
    print(f"\nMix voiceover: {VO_FILE}")
    cmd_mix = [
        "ffmpeg", "-y",
        "-i", raw_concat,
        "-i", VO_FILE,
        "-filter_complex",
        # Chuẩn hóa voiceover -14 LUFS, giảm audio gốc xuống -18dB
        "[0:a]volume=0.125[orig];[1:a]loudnorm=I=-14:TP=-2:LRA=11[vo];[orig][vo]amix=inputs=2:duration=first:weights=1 4[aout]",
        "-map", "0:v",
        "-map", "[aout]",
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "48000",
        "-shortest",
        final_output
    ]
    r2 = subprocess.run(cmd_mix, capture_output=True, text=True)
    if r2.returncode != 0:
        print(f"LỖI mix: {r2.stderr[-400:]}")
        # Fallback: chỉ dùng video thô
        import shutil
        shutil.copy(raw_concat, final_output)
        print("Fallback: Dùng video thô không voiceover")
    else:
        size = os.path.getsize(final_output) / 1024 / 1024
        print(f"OK - Final video: {size:.1f} MB → {final_output}")
else:
    print(f"Không tìm thấy voiceover tại {VO_FILE}, dùng video thô")
    import shutil
    shutil.copy(raw_concat, final_output)

print("\n✅ HOÀN THÀNH! Video đã xuất tại:")
print(f"   {final_output}")
