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

def inspect_all_footage():
    footage_dir = Path("raw_footage")
    keyframes_dir = Path("processed/keyframes")
    keyframes_dir.mkdir(parents=True, exist_ok=True)
    
    videos = sorted(list(footage_dir.glob("*.MP4")) + list(footage_dir.glob("*.mp4")))
    print(f"[*] Tìm thấy {len(videos)} video trong raw_footage.")
    
    # 1. Trích xuất thumbnails định kỳ (mỗi 5s chụp 1 frame)
    for v in videos:
        stem = v.stem
        v_out_dir = keyframes_dir / stem
        v_out_dir.mkdir(parents=True, exist_ok=True)
        print(f"[*] Đang xuất thumbnails cho {v.name}...")
        cmd = [
            "ffmpeg", "-y", "-i", str(v),
            "-vf", "fps=1/5,scale=960:-1",
            str(v_out_dir / "thumb_%03d.jpg")
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        thumbs = list(v_out_dir.glob("*.jpg"))
        print(f"[+] Đã xuất {len(thumbs)} frames cho {v.name}")

    # 2. Chạy Whisper bóc tách âm thanh / lời nói
    print("[*] Đang nạp Whisper model 'base' để bóc tách lời thoại...")
    import whisper
    model = whisper.load_model("base")
    
    transcripts = {}
    for v in videos:
        stem = v.stem
        print(f"[*] Đang nhận diện âm thanh cho {v.name}...")
        res = model.transcribe(str(v), language="vi", word_timestamps=True, verbose=False)
        text = res.get("text", "").strip()
        segments = res.get("segments", [])
        transcripts[stem] = {
            "text": text,
            "segment_count": len(segments),
            "segments": [
                {
                    "start": round(s["start"], 2),
                    "end": round(s["end"], 2),
                    "text": s["text"].strip()
                } for s in segments
            ]
        }
        print(f"    -> Lời thoại {v.name} ({len(segments)} segments): '{text[:120]}...'")

    out_json = Path("processed/all_transcripts.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(transcripts, f, ensure_ascii=False, indent=2)
    print(f"[+] Đã lưu toàn bộ transcripts vào {out_json}")

if __name__ == "__main__":
    inspect_all_footage()
