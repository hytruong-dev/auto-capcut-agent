import os, sys, subprocess, json, time, shutil

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"c:\QuangHy\editvideo"
RAW_DIR = os.path.join(BASE_DIR, "raw_footage")
OUT_DIR = os.path.join(BASE_DIR, "processed")
TEMP_DIR = os.path.join(OUT_DIR, "temp_story_segments")
SNAPSHOT_DIR = os.path.join(OUT_DIR, "snapshots")
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(SNAPSHOT_DIR, exist_ok=True)

FOOTAGE = {
    "DJI_0057": os.path.join(RAW_DIR, "DJI_20260908084243_0057_D.MP4"),
    "DJI_0062": os.path.join(RAW_DIR, "DJI_20260908183824_0062_D.MP4"),
    "DJI_0064": os.path.join(RAW_DIR, "DJI_20260908185603_0064_D.MP4"),
}

VO_FILE = os.path.join(OUT_DIR, "voiceover", "xanhsm_story_vo.mp3")
BGM_FILE = os.path.join(OUT_DIR, "bgm_nightshift_loop.mp3")
ASS_FILE = os.path.join(OUT_DIR, "xanhsm_story_master.ass")
RAW_VIDEO = os.path.join(OUT_DIR, "xanhsm_story_raw.mp4")
FINAL_VIDEO = os.path.join(OUT_DIR, "Vlog_XanhSM_Story_FINAL.mp4")
FONTS_DIR = os.path.join(BASE_DIR, "portable_trained_brain", "portable_assets", "fonts")

CLIPS_SPEC = [
    # seg_id, source, ss, net_dur, is_night, trans_to_next, trans_dur
    (1, "DJI_0057", 1.0, 3.5, False, "smoothleft", 0.35),
    (2, "DJI_0062", 1.0, 3.0, True, "fadeblack", 0.40),
    (3, "DJI_0057", 5.0, 8.0, False, "dissolve", 0.40),
    (4, "DJI_0057", 13.0, 7.0, False, "smoothleft", 0.35),
    (5, "DJI_0057", 20.0, 6.4, False, "fadeblack", 0.50),
    (6, "DJI_0062", 6.0, 6.1, True, "dissolve", 0.40),
    (7, "DJI_0062", 14.0, 6.5, True, "smoothleft", 0.35),
    (8, "DJI_0062", 38.0, 4.5, True, "fadeblack", 0.50),
    (9, "DJI_0064", 25.0, 7.0, True, "dissolve", 0.40),
    (10, "DJI_0064", 75.0, 9.6, True, "dissolve", 0.40),
    (11, "DJI_0064", 135.0, 10.2, True, "dissolve", 0.40),
    (12, "DJI_0064", 150.0, 10.2, True, None, 0.0),
]

print("[*] BƯỚC 1: Cắt 12 video segments có bù trừ handle cho xfade...")
seg_files = []
for seg_id, source, ss, net_dur, is_night, trans, trans_dur in CLIPS_SPEC:
    raw_dur = net_dur + trans_dur
    out_seg = os.path.join(TEMP_DIR, f"trans_seg_{seg_id:02d}.mp4")
    seg_files.append(out_seg)
    
    if is_night:
        vf = "transpose=1,scale=1080:1920:flags=lanczos,eq=brightness=0.06:saturation=1.22:contrast=1.08,unsharp=5:5:0.7,fps=30"
    else:
        vf = "transpose=1,scale=1080:1920:flags=lanczos,eq=saturation=1.1:contrast=1.05,fps=30"
        
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(ss),
        "-i", FOOTAGE[source],
        "-t", f"{raw_dur:.3f}",
        "-vf", vf,
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "19",
        "-c:a", "aac",
        "-ar", "48000",
        "-ac", "2",
        "-b:a", "192k",
        out_seg
    ]
    print(f"  Cutting seg {seg_id:02d}: {source} dur={raw_dur:.2f}s...")
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

print("[+] Đã cắt xong 12 segments!")

print("[*] BƯỚC 2: Xây dựng filter_complex xfade 11 chuyển cảnh liên hoàn...")
# Xây dựng chuỗi xfade:
inputs_args = []
for sf in seg_files:
    inputs_args.extend(["-i", sf])

filter_chains = []
audio_chains = []

cur_offset = 0.0
last_v = "0:v"
last_a = "0:a"

for i in range(len(CLIPS_SPEC) - 1):
    c = CLIPS_SPEC[i]
    cur_offset += c[3] # net_dur
    trans_name = c[5]
    trans_dur = c[6]
    
    next_v = f"{i+1}:v"
    out_v = f"v_xfade_{i+1}"
    
    filter_chains.append(
        f"[{last_v}][{next_v}]xfade=transition={trans_name}:duration={trans_dur:.2f}:offset={cur_offset:.2f}[{out_v}]"
    )
    last_v = out_v

# Ghép ambient audio bằng acrossfade hoặc amix
for i in range(len(CLIPS_SPEC) - 1):
    c = CLIPS_SPEC[i]
    trans_dur = c[6]
    next_a = f"{i+1}:a"
    out_a = f"a_xfade_{i+1}"
    audio_chains.append(
        f"[{last_a}][{next_a}]acrossfade=d={trans_dur:.2f}[{out_a}]"
    )
    last_a = out_a

full_v_filter = ";".join(filter_chains)
full_a_filter = ";".join(audio_chains)
full_filter = f"{full_v_filter};{full_a_filter}"

xfade_cmd = [
    "ffmpeg", "-y"
] + inputs_args + [
    "-filter_complex", full_filter,
    "-map", f"[{last_v}]",
    "-map", f"[{last_a}]",
    "-c:v", "libx264",
    "-preset", "fast",
    "-crf", "19",
    "-c:a", "aac",
    "-b:a", "192k",
    RAW_VIDEO
]

print("[*] Đang render RAW_VIDEO với xfade...")
subprocess.run(xfade_cmd, check=True)

# Đo lại thời lượng video thô sau xfade
probe_raw = subprocess.run([
    "ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", RAW_VIDEO
], capture_output=True, text=True)
raw_dur = float(json.loads(probe_raw.stdout)["format"]["duration"])
print(f"[SUCCESS] RAW_VIDEO đã xuất xưởng: {RAW_VIDEO} (Thời lượng: {raw_dur:.2f}s)")

# BƯỚC 3: Burn-in Subtitles & Mix Audio 3 lớp
print("[*] BƯỚC 3: Burn-in Karaoke Subtitles & Mix Audio...")
ass_filter = ASS_FILE.replace('\\', '/').replace(':', r'\:')
fonts_filter = FONTS_DIR.replace('\\', '/').replace(':', r'\:')

mix_cmd = [
    'ffmpeg', '-y',
    '-i', RAW_VIDEO,
    '-i', VO_FILE,
    '-i', BGM_FILE,
    '-filter_complex',
    f"[0:v]ass='{ass_filter}':fontsdir='{fonts_filter}'[v];[0:a]volume=0.12[amb];[1:a]volume=1.0[vo];[2:a]volume=0.14[bgm];[amb][vo][bgm]amix=inputs=3:duration=first:dropout_transition=2[a]",
    '-map', '[v]',
    '-map', '[a]',
    '-c:v', 'libx264',
    '-crf', '19',
    '-preset', 'fast',
    '-c:a', 'aac',
    '-b:a', '256k',
    FINAL_VIDEO
]
subprocess.run(mix_cmd, check=True)

print("[*] BƯỚC 4: Trích xuất ảnh QA chuyển cảnh...")
# Chụp tại điểm giao giữa các đoạn chuyển cảnh để kiểm định:
qa_points = [
    ("qa_trans_01_hook_night.jpg", 3.48),    # Đang lướt sang đêm
    ("qa_trans_02_morning_fade.jpg", 6.48),   # Mờ đen sang sáng
    ("qa_trans_05_sunset_fade.jpg", 27.88),   # Mờ đen sang chiều lên đèn
    ("qa_trans_08_night_fade.jpg", 44.95),    # Mờ đen sang ca đêm
    ("qa_trans_10_story_dissolve.jpg", 61.58) # Mờ chồng sang tổng kết
]

for fname, ts in qa_points:
    out_p = os.path.join(SNAPSHOT_DIR, fname)
    subprocess.run([
        'ffmpeg', '-y', '-ss', str(ts), '-i', FINAL_VIDEO,
        '-vframes', '1', '-q:v', '2', out_p
    ], check=True)
    print(f"  [QA Transition Snapshot] {fname} @ {ts:.2f}s -> OK")

print("\n[SUCCESS] Hoàn tất toàn bộ quy trình chuyển cảnh Cinematic!")
