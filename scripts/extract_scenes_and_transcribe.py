import os
import sys
import json
import subprocess
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

def extract_keyframes(video_path: Path, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    out_pattern = str(output_dir / "scene_%03d.jpg")
    print(f"[*] Đang trích xuất keyframes đổi cảnh bằng FFmpeg vào {output_dir}...")
    
    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-vf", "select='gt(scene,0.3)'",
        "-vsync", "vfr",
        out_pattern
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        extracted = list(output_dir.glob("*.jpg"))
        print(f"[+] Đã trích xuất {len(extracted)} keyframes.")
    except Exception as e:
        print(f"[!] Lỗi khi chạy ffmpeg scene detection: {e}")

def transcribe_audio(video_path: Path, output_json: Path, model_name: str = "base"):
    output_json.parent.mkdir(parents=True, exist_ok=True)
    print(f"[*] Bắt đầu bóc tách phụ đề với Whisper model '{model_name}'...")
    try:
        import whisper
        model = whisper.load_model(model_name)
        result = model.transcribe(str(video_path), word_timestamps=True, verbose=False)
        
        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
            
        print(f"[+] Đã lưu transcript hoàn chỉnh tại: {output_json}")
        return result
    except Exception as e:
        print(f"[!] Lỗi khi transcribe với whisper: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Cách dùng: python scripts/extract_scenes_and_transcribe.py <duong_dan_video> [model_name]")
        sys.exit(1)
        
    v_path = Path(sys.argv[1])
    m_name = sys.argv[2] if len(sys.argv) > 2 else "base"
    
    if not v_path.exists():
        print(f"[!] File không tồn tại: {v_path}")
        sys.exit(1)
        
    extract_keyframes(v_path, Path("processed/keyframes"))
    transcribe_audio(v_path, Path("processed/transcript.json"), m_name)
