import os, sys, time, json, subprocess
import torch
import torchaudio

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

os.environ["HF_HOME"] = r"C:\Users\PC\AppData\Local\OmniVoice\hf_cache"

from omnivoice.models.omnivoice import OmniVoice

VOICE_DIR = r"processed\voiceover"
SEG_DIR = os.path.join(VOICE_DIR, "story_segments")
os.makedirs(SEG_DIR, exist_ok=True)

model_path = r"C:\Users\PC\AppData\Local\OmniVoice\hf_cache\models--k2-fsa--OmniVoice\snapshots\c5fdb5ccb189668d56333f77ba2629f4cd7535f4"
ref_audio = r"c:\QuangHy\editvideo\processed\voiceover\ref_sample_hook.wav"
ref_text = "Thử thách chạy GrabFood 11 tiếng thực sự kiếm được bao nhiêu. Hôm nay anh test thực tế luôn."

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

print(f"[*] Đang tải mô hình OmniVoice từ {model_path}...")
t_load = time.time()
model = OmniVoice.from_pretrained(model_path, device_map="cpu", dtype=torch.float32)
print(f"[*] Đã tải xong mô hình trong {time.time() - t_load:.2f}s")

print(f"[*] Đang mã hoá mẫu giọng nói từ video Download.mp4...")
clone_prompt = model.create_voice_clone_prompt(
    ref_audio=ref_audio,
    ref_text=ref_text,
    preprocess_prompt=True
)
print(f"[+] Đã tạo voice clone prompt thành công!")

total_segs = len(SCRIPT_SEGMENTS)
start_all = time.time()

for idx, seg in enumerate(SCRIPT_SEGMENTS, 1):
    seg_id = seg["id"]
    text = seg["text"]
    raw_wav = os.path.join(SEG_DIR, f"vs_raw_{seg_id:02d}.wav")
    final_mp3 = os.path.join(SEG_DIR, f"seg_{seg_id:02d}.mp3")
    
    print(f"[{idx}/{total_segs}] Sinh giọng câu {seg_id:02d}: \"{text}\"...")
    t_start = time.time()
    
    # Sinh giọng bằng VoiceStudio
    audios = model.generate(
        text=text,
        language="Vietnamese",
        voice_clone_prompt=clone_prompt,
        num_step=14,
        guidance_scale=2.0,
        speed=1.05,
    )
    torchaudio.save(raw_wav, audios[0], model.sampling_rate)
    gen_time = time.time() - t_start
    
    # Chuẩn hoá Loudnorm (-14 LUFS, TP -1.5, LRA 11) và xuất file seg_XX.mp3
    speed_cmd = [
        "ffmpeg", "-y",
        "-i", raw_wav,
        "-filter_complex", "loudnorm=I=-14:TP=-1.5:LRA=11",
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        final_mp3
    ]
    subprocess.run(speed_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    probe_cmd = [
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        final_mp3
    ]
    res = subprocess.run(probe_cmd, capture_output=True, text=True)
    dur = float(json.loads(res.stdout)["format"]["duration"])
    
    print(f"    -> Xong trong {gen_time:.1f}s | Độ dài audio: {dur:.2f}s | File: {final_mp3}")

print(f"\n[+] ĐÃ HOÀN TẤT SINH 19 CÂU THOẠI TRONG {time.time() - start_all:.1f}s!")

# Ghép toàn bộ 19 file thành master voiceover
concat_list_path = os.path.join(SEG_DIR, "concat_list.txt")
with open(concat_list_path, "w", encoding="utf-8") as f:
    for seg in SCRIPT_SEGMENTS:
        seg_id = seg["id"]
        final_mp3 = os.path.join(SEG_DIR, f"seg_{seg_id:02d}.mp3")
        f.write(f"file '{os.path.abspath(final_mp3)}'\n")

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

probe_master = subprocess.run([
    "ffprobe", "-v", "quiet",
    "-print_format", "json",
    "-show_format",
    master_vo
], capture_output=True, text=True)
master_dur = float(json.loads(probe_master.stdout)["format"]["duration"])
print(f"[SUCCESS] Master Voiceover mới: {master_vo} ({master_dur:.2f}s)")
