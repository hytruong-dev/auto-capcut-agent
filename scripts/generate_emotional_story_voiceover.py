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

EXPRESSIVE_SCRIPT = [
    # --- PHẦN 1: HOOK (0s - 7s) ---
    {"id": 1, "text": "Thử thách chạy xe máy điện Xanh SM cả ngày, từ sáng đến đêm... thực sự kiếm được bao nhiêu tiền nè?", "kw": "XANH SM CẢ NGÀY, KIẾM ĐƯỢC BAO NHIÊU?"},
    {"id": 2, "text": "Hôm nay mình test thực tế cho anh em xem luôn nha!", "kw": "TEST THỰC TẾ LUÔN!"},
    {"id": 3, "text": "Bạn nào còn thắc mắc thì xem hết video này là biết liền nè!", "kw": "XEM HẾT VIDEO NÀY NHA"},
    
    # --- PHẦN 2: CA SÁNG (7s - 22s) ---
    {"id": 4, "text": "Tám giờ sáng, mình bắt đầu mở app nhận cuốc đầu tiên.", "kw": "TÁM GIỜ SÁNG, MỞ APP NHẬN CUỐC"},
    {"id": 5, "text": "Phải công nhận cái chiếc xe điện VinFast này chạy êm ru luôn á, lướt trên đường phố không một tiếng động cơ!", "kw": "CHẠY ÊM RU, KHÔNG TIẾNG ĐỘNG CƠ"},
    {"id": 6, "text": "Sáng sớm mát rượi, cực kỳ dễ chịu luôn!", "kw": "SÁNG SỚM MÁT RƯỢI"},
    {"id": 7, "text": "Mở bát cuốc đầu tiên... được hẳn ba mươi lăm cành, quá đã!", "kw": "BA MƯƠI LĂM CÀNH!"},
    
    # --- PHẦN 3: CHIỀU TAN TẦM (22s - 38s) ---
    {"id": 8, "text": "Chạy vèo một cái là đã đến chiều muộn rồi.", "kw": "ĐẾN CHIỀU MUỘN"},
    {"id": 9, "text": "Tầm sáu giờ chiều, Sài Gòn bắt đầu lên đèn lung linh đẹp ghê luôn.", "kw": "SÁU GIỜ CHIỀU, LÊN ĐÈN LUNG LINH"},
    {"id": 10, "text": "Giờ tan tầm kẹt xe, nhưng xe điện ga mượt, luồn lách qua ngõ nhỏ cực kỳ nhẹ nhàng!", "kw": "GA MƯỢT, LUỒN LÁCH NHẸ NHÀNG"},
    {"id": 11, "text": "Đứng nghỉ chân có một xíu thôi, mà app lại nổ đơn liên tục luôn á!", "kw": "NỔ ĐƠN LIÊN TỤC!"},
    
    # --- PHẦN 4: CA ĐÊM (38s - 55s) ---
    {"id": 12, "text": "Đến gần tám giờ tối rồi, phố xá cũng thưa thớt dần.", "kw": "TÁM GIỜ TỐI"},
    {"id": 13, "text": "Chạy đêm gió mát thật đó, nhưng mà người cũng bắt đầu thấy mỏi lưng rồi nè.", "kw": "CHẠY ĐÊM MÁT MẺ"},
    {"id": 14, "text": "Mỗi chuyến xe đêm là một câu chuyện, có chuyến vui, có chuyến mệt...", "kw": "MỖI CHUYẾN XE, MỘT CÂU CHUYỆN"},
    {"id": 15, "text": "Nhưng mà cứ nhìn đồng hồ ki-lô-mét nhảy đều là lại có động lực cày tiếp!", "kw": "ĐỘNG LỰC ĐI TIẾP!"},
    
    # --- PHẦN 5: TỔNG KẾT & CALLOUT (55s - 70s) ---
    {"id": 16, "text": "Và đây là kết quả sau một ngày cày cuốc: tổng kết được gần năm trăm cành, quá ấm luôn!", "kw": "GẦN NĂM TRĂM CÀNH!"},
    {"id": 17, "text": "Chạy cả ngày công nhận vất vả, nhưng mà cũng rất đáng tự hào nha!", "kw": "RẤT ĐÁNG TỰ HÀO"},
    {"id": 18, "text": "Còn anh em thì sao? Một ngày cày được bao nhiêu lúa? Comment cho mình biết với nha!", "kw": "BAO NHIÊU LÚA? COMMENT NHA!"},
    {"id": 19, "text": "Nhớ thả cho mình một tim và follow kênh để đón xem tập tiếp theo nhé!", "kw": "THẢ TIM VÀ FOLLOW KÊNH NHÉ!"}
]

print(f"[*] Đang tải mô hình OmniVoice để sinh giọng cảm xúc biểu cảm...")
t_load = time.time()
model = OmniVoice.from_pretrained(model_path, device_map="cpu", dtype=torch.float32)
print(f"[*] Đã tải xong mô hình trong {time.time() - t_load:.2f}s")

print(f"[*] Tạo Voice Clone Prompt từ Download.mp4...")
clone_prompt = model.create_voice_clone_prompt(
    ref_audio=ref_audio,
    ref_text=ref_text,
    preprocess_prompt=True
)

total_segs = len(EXPRESSIVE_SCRIPT)
start_all = time.time()

for idx, seg in enumerate(EXPRESSIVE_SCRIPT, 1):
    seg_id = seg["id"]
    text = seg["text"]
    raw_wav = os.path.join(SEG_DIR, f"vs_raw_{seg_id:02d}.wav")
    final_mp3 = os.path.join(SEG_DIR, f"seg_{seg_id:02d}.mp3")
    
    print(f"[{idx}/{total_segs}] Sinh giọng câu {seg_id:02d}: \"{text}\"...")
    t_start = time.time()
    
    # Sinh giọng với class_temperature=0.7 (bật sampling biểu cảm ngắt nhịp) và guidance_scale=1.7
    audios = model.generate(
        text=text,
        language="Vietnamese",
        voice_clone_prompt=clone_prompt,
        num_step=14,
        guidance_scale=1.7,
        class_temperature=0.7,
        speed=1.06,
    )
    torchaudio.save(raw_wav, audios[0], model.sampling_rate)
    gen_time = time.time() - t_start
    
    # Chuẩn hoá Loudnorm (-14 LUFS) và xuất file MP3
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

print(f"\n[+] ĐÃ HOÀN TẤT SINH 19 CÂU THOẠI CẢM XÚC TRONG {time.time() - start_all:.1f}s!")

# Ghép toàn bộ 19 file thành master voiceover
concat_list_path = os.path.join(SEG_DIR, "concat_list.txt")
with open(concat_list_path, "w", encoding="utf-8") as f:
    for seg in EXPRESSIVE_SCRIPT:
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
print(f"[SUCCESS] Master Voiceover biểu cảm: {master_vo} ({master_dur:.2f}s)")
