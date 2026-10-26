import os, sys, subprocess, json, time
from pathlib import Path
from gtts import gTTS

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

VOICE_DIR = r"processed\voiceover"
SEG_DIR = os.path.join(VOICE_DIR, "story_segments")
os.makedirs(SEG_DIR, exist_ok=True)

SCRIPT_SEGMENTS = [
    # --- PHẦN 1: HOOK (0s - 7s) ---
    {"id": 1, "part": "hook", "text": "Thử thách chạy xe máy điện Xanh SM cả ngày, từ sáng đến đêm thực sự kiếm được bao nhiêu?", "kw": "XANH SM CẢ NGÀY, KIẾM ĐƯỢC BAO NHIÊU?"},
    {"id": 2, "part": "hook", "text": "Hôm nay mình test thực tế luôn!", "kw": "TEST THỰC TẾ LUÔN!"},
    {"id": 3, "part": "hook", "text": "Bạn nào còn thắc mắc thì xem hết video này nha.", "kw": "XEM HẾT VIDEO NÀY NHA"},
    
    # --- PHẦN 2: CA SÁNG (7s - 22s) ---
    {"id": 4, "part": "morning", "text": "Tám giờ sáng, mình bắt đầu mở app nhận cuốc đầu tiên.", "kw": "TÁM GIỜ SÁNG, MỞ APP NHẬN CUỐC"},
    {"id": 5, "part": "morning", "text": "Phải công nhận chiếc xe điện VinFast này chạy êm ru, lướt trên đường phố không một tiếng động cơ.", "kw": "CHẠY ÊM RU, KHÔNG TIẾNG ĐỘNG CƠ"},
    {"id": 6, "part": "morning", "text": "Sáng sớm mát rượi cực kỳ dễ chịu.", "kw": "SÁNG SỚM MÁT RƯỢI"},
    {"id": 7, "part": "morning", "text": "Mở bát cuốc đầu được ba mươi lăm cành!", "kw": "BA MƯƠI LĂM CÀNH!"},
    
    # --- PHẦN 3: CHIỀU TAN TẦM (22s - 38s) ---
    {"id": 8, "part": "afternoon", "text": "Chạy vèo một cái là đến chiều muộn.", "kw": "ĐẾN CHIỀU MUỘN"},
    {"id": 9, "part": "afternoon", "text": "Tầm sáu giờ chiều, Sài Gòn bắt đầu lên đèn lung linh.", "kw": "SÁU GIỜ CHIỀU, LÊN ĐÈN LUNG LINH"},
    {"id": 10, "part": "afternoon", "text": "Giờ tan tầm kẹt xe nhưng được cái xe điện ga mượt, luồn lách qua các con phố nhỏ cực kỳ nhẹ nhàng.", "kw": "GA MƯỢT, LUỒN LÁCH NHẸ NHÀNG"},
    {"id": 11, "part": "afternoon", "text": "Đứng nghỉ chân một xíu là app lại nổ đơn liên tục!", "kw": "NỔ ĐƠN LIÊN TỤC!"},
    
    # --- PHẦN 4: CA ĐÊM (38s - 55s) ---
    {"id": 12, "part": "night", "text": "Đến gần tám giờ tối, phố xá đã thưa dần.", "kw": "TÁM GIỜ TỐI"},
    {"id": 13, "part": "night", "text": "Chạy đêm mát mẻ nhưng người cũng bắt đầu thấy mỏi lưng rồi đó.", "kw": "CHẠY ĐÊM MÁT MẺ"},
    {"id": 14, "part": "night", "text": "Mỗi chuyến xe đêm là một câu chuyện, có chuyến vui, có chuyến mệt...", "kw": "MỖI CHUYẾN XE, MỘT CÂU CHUYỆN"},
    {"id": 15, "part": "night", "text": "Nhưng cứ nhìn đồng hồ ki-lô-mét nhảy đều là lại có động lực đi tiếp!", "kw": "ĐỘNG LỰC ĐI TIẾP!"},
    
    # --- PHẦN 5: TỔNG KẾT & CALLOUT (55s - 70s) ---
    {"id": 16, "part": "outro", "text": "Và đây là kết quả sau một ngày cày cuốc: xe chạy êm, tổng kết được gần năm trăm cành!", "kw": "GẦN NĂM TRĂM CÀNH!"},
    {"id": 17, "part": "outro", "text": "Chạy cả ngày công nhận vất vả nhưng cũng rất đáng tự hào.", "kw": "RẤT ĐÁNG TỰ HÀO"},
    {"id": 18, "part": "outro", "text": "Còn anh em thì sao? Một ngày được bao nhiêu lúa? Comment cho mình biết với nha!", "kw": "BAO NHIÊU LÚA? COMMENT NHA!"},
    {"id": 19, "part": "outro", "text": "Đừng quên thả một tim và follow kênh để đón xem tập tiếp theo nhé!", "kw": "THẢ TIM VÀ FOLLOW KÊNH NHÉ!"}
]

print(f"[*] Bắt đầu xử lý {len(SCRIPT_SEGMENTS)} phân đoạn voiceover...")

timeline_items = []
current_time = 0.5  # Bắt đầu sau 0.5s để có khoảng đệm mở đầu
concat_list_path = os.path.join(SEG_DIR, "concat_list.txt")
file_list = []

for seg in SCRIPT_SEGMENTS:
    seg_id = seg["id"]
    text = seg["text"]
    raw_seg_file = os.path.join(SEG_DIR, f"raw_{seg_id:02d}.mp3")
    final_seg_file = os.path.join(SEG_DIR, f"seg_{seg_id:02d}.mp3")
    
    # Tạo TTS nếu chưa có
    if not os.path.exists(raw_seg_file):
        tts = gTTS(text=text, lang="vi", slow=False)
        tts.save(raw_seg_file)
    
    # Tăng tốc 1.18x và normalize loudnorm (-14 LUFS)
    if not os.path.exists(final_seg_file):
        speed_cmd = [
            "ffmpeg", "-y",
            "-i", raw_seg_file,
            "-filter_complex", "atempo=1.18,loudnorm=I=-14:TP=-1.5:LRA=11",
            "-c:a", "libmp3lame",
            "-b:a", "192k",
            final_seg_file
        ]
        subprocess.run(speed_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Đo duration bằng ffprobe
    probe_cmd = [
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        final_seg_file
    ]
    res = subprocess.run(probe_cmd, capture_output=True, text=True)
    info = json.loads(res.stdout)
    dur = float(info["format"]["duration"])
    
    start_t = round(current_time, 2)
    end_t = round(current_time + dur, 2)
    
    timeline_items.append({
        "id": seg_id,
        "part": seg["part"],
        "text": text,
        "keyword": seg["kw"],
        "audio_file": final_seg_file.replace("\\", "/"),
        "duration": dur,
        "start_time": start_t,
        "end_time": end_t
    })
    
    file_list.append(final_seg_file)
    # Khoảng nghỉ nhẹ 0.12s giữa các câu
    current_time = end_t + 0.12

print(f"[+] Đã hoàn thành xử lý {len(timeline_items)} câu thoại. Tổng độ dài dự kiến: {current_time:.2f}s")

# Ghi file concat_list.txt
with open(concat_list_path, "w", encoding="utf-8") as f:
    for fp in file_list:
        f.write(f"file '{os.path.abspath(fp)}'\n")

# Ghép toàn bộ thành master voiceover
master_vo = os.path.join(VOICE_DIR, "xanhsm_story_vo.mp3")
concat_cmd = [
    "ffmpeg", "-y",
    "-f", "concat",
    "-safe", "0",
    "-i", concat_list_path,
    "-c:a", "libmp3lame",
    "-b:a", "192k",
    master_vo
]
subprocess.run(concat_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Đo lại master voiceover
probe_master = subprocess.run([
    "ffprobe", "-v", "quiet",
    "-print_format", "json",
    "-show_format",
    master_vo
], capture_output=True, text=True)
master_info = json.loads(probe_master.stdout)
master_dur = float(master_info["format"]["duration"])
print(f"[SUCCESS] Master Voiceover: {master_vo} ({master_dur:.2f}s)")

# Xuất timeline JSON chi tiết
timeline_json_path = os.path.join(r"processed", "story_voiceover_timeline.json")
with open(timeline_json_path, "w", encoding="utf-8") as f:
    json.dump({
        "total_duration": master_dur,
        "segment_count": len(timeline_items),
        "segments": timeline_items
    }, f, ensure_ascii=False, indent=2)

print(f"[SUCCESS] Đã lưu bản đồ thời gian phụ đề & voiceover vào: {timeline_json_path}")
