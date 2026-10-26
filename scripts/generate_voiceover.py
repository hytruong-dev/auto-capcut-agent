import os
import sys
import subprocess
import json
from pathlib import Path
from gtts import gTTS

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

SCRIPT_PARAGRAPHS = [
    {
        "id": "seg_01",
        "text": "Nhiều anh em hỏi tôi: Chạy xe máy điện Xanh SM cả ngày từ sáng đến đêm có thực sự phê như lời đồn không? Hôm nay cùng tôi trải nghiệm nhé!",
        "video_ref": "DJI_20260908084243_0057_D.MP4",
        "video_start": 0.0,
        "highlight": "Chạy xe máy điện Xanh SM"
    },
    {
        "id": "seg_02",
        "text": "Tám giờ sáng, bật app nhận cuốc đầu tiên. Phải công nhận chiếc xe điện VinFast này chạy êm ru, lướt trên đường phố không một tiếng động cơ, sáng sớm mát rượi cực kỳ dễ chịu.",
        "video_ref": "DJI_20260908084243_0057_D.MP4",
        "video_start": 5.0,
        "highlight": "xe điện VinFast chạy êm ru"
    },
    {
        "id": "seg_03",
        "text": "Chạy vèo một cái là đến chiều muộn. Tầm sáu giờ chiều, Sài Gòn bắt đầu lên đèn lung linh. Giờ tan tầm kẹt xe nhưng được cái xe điện ga mượt, luồn lách qua các con phố nhỏ cực kỳ nhẹ nhàng.",
        "video_ref": "DJI_20260908183824_0062_D.MP4",
        "video_start": 5.0,
        "highlight": "Sài Gòn lên đèn lung linh"
    },
    {
        "id": "seg_04",
        "text": "Đến gần bảy giờ tối, dừng xe check app thì ting ting, đơn nổ liên tục! Vừa nhận cuốc mới là nổ máy chạy ngay qua mấy con phố ẩm thực, đi ngang mấy quán phở, quán hủ tiếu thơm nức mũi.",
        "video_ref": "DJI_20260908185603_0064_D.MP4",
        "video_start": 35.0,
        "highlight": "ting ting, đơn nổ liên tục!"
    },
    {
        "id": "seg_05",
        "text": "Một ngày cày cuốc gần mười một tiếng dù mỏi lưng một chút, nhưng nhìn lại thành quả ví tiền và cảm giác xe vẫn êm ái thế này thì quá xứng đáng! Anh em chạy Xanh SM hôm nay thế nào rồi? Bình luận bên dưới giao lưu nhé!",
        "video_ref": "DJI_20260908185603_0064_D.MP4",
        "video_start": 145.0,
        "highlight": "Anh em hôm nay được mấy cuốc?"
    }
]

def generate_voiceover_gtts(output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    
    current_time = 0.0
    for idx, item in enumerate(SCRIPT_PARAGRAPHS):
        raw_file = output_dir / f"raw_{item['id']}.mp3"
        out_file = output_dir / f"voice_{item['id']}.mp3"
        print(f"[*] Tạo Voiceover đoạn {idx+1}/{len(SCRIPT_PARAGRAPHS)}: '{item['text'][:45]}...'")
        
        tts = gTTS(text=item["text"], lang="vi")
        tts.save(str(raw_file))
        
        # Tăng tốc độ đọc 1.2x bằng ffmpeg filter atempo để giọng đọc năng động, cuốn hút
        cmd = [
            "ffmpeg", "-y", "-i", str(raw_file),
            "-filter:a", "atempo=1.20",
            str(out_file)
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        dur_str = subprocess.check_output([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(out_file)
        ]).decode().strip()
        duration = float(dur_str)
        
        item["voice_file"] = str(out_file.resolve()).replace("\\", "/")
        item["voice_duration"] = duration
        item["timeline_start"] = round(current_time, 2)
        item["timeline_end"] = round(current_time + duration, 2)
        item["video_duration"] = duration
        current_time += duration
        print(f"    [+] Xong: {duration:.2f}s | Timeline: {item['timeline_start']}s -> {item['timeline_end']}s")
        
    # Nối thành full voiceover
    concat_list = output_dir / "concat_list.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for item in SCRIPT_PARAGRAPHS:
            f.write(f"file '{item['voice_file']}'\n")
            
    full_voice = output_dir / "full_voiceover.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_list), "-c", "copy", str(full_voice)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    full_dur = float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(full_voice)
    ]).decode().strip())
    
    print(f"\n[+] Tổng thời lượng Voiceover Vlog: {full_dur:.2f}s tại {full_voice}")
    
    with open("processed/vlog_aligned_script.json", "w", encoding="utf-8") as f:
        json.dump(SCRIPT_PARAGRAPHS, f, ensure_ascii=False, indent=2)
        
    return SCRIPT_PARAGRAPHS, full_voice

if __name__ == "__main__":
    generate_voiceover_gtts(Path("processed/voiceover"))
