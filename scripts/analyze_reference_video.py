import os
import sys
import subprocess
import json
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

def analyze_reference(video_path: Path):
    out_dir = Path("processed/reference_analysis")
    out_dir.mkdir(parents=True, exist_ok=True)
    frames_dir = out_dir / "keyframes"
    frames_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"[*] Bắt đầu giải mã video mẫu: {video_path}")
    
    # 1. Đo Scene Cuts bằng FFmpeg (bắt điểm chuyển cảnh)
    print("[*] Đang phát hiện các điểm chuyển cảnh (Scene Detection)...")
    scene_filter_cmd = [
        "ffmpeg", "-i", str(video_path),
        "-filter_complex", "select='gt(scene,0.25)',metadata=print:file=" + str(out_dir / "scenes.txt").replace("\\", "/"),
        "-f", "null", "-"
    ]
    subprocess.run(scene_filter_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # 2. Xuất frames mẫu tại các giây quan trọng (mỗi 3s trong 60s đầu, và mỗi 10s về sau)
    print("[*] Đang xuất keyframes mẫu để phân tích thị giác...")
    frame_cmd = [
        "ffmpeg", "-y", "-i", str(video_path),
        "-vf", "fps=1/4,scale=576:1024",
        str(frames_dir / "frame_%03d.jpg")
    ]
    subprocess.run(frame_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    extracted_frames = sorted(list(frames_dir.glob("*.jpg")))
    print(f"[+] Đã xuất {len(extracted_frames)} frames phân tích.")
    
    # 3. Phân tích lời thoại / kịch bản bằng Whisper
    print("[*] Đang nhận diện lời thoại / âm thanh bằng Whisper...")
    import whisper
    model = whisper.load_model("base")
    res = model.transcribe(str(video_path), language="vi", word_timestamps=True, verbose=False)
    
    transcript_file = out_dir / "transcript.json"
    with open(transcript_file, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
        
    print(f"[+] Đã trích xuất transcript ({len(res.get('segments', []))} segments)")
    print(f"    Lời thoại mở đầu: {res.get('text', '')[:180]}...")
    
    return len(extracted_frames), res.get('text', '')

if __name__ == "__main__":
    analyze_reference(Path("references/Download.mp4"))
