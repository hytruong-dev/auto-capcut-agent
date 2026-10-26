import os
import sys
import subprocess
import json
from pathlib import Path
import cv2
import numpy as np

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

def inspect_transitions_and_sfx(video_path: Path):
    out_dir = Path("processed/deep_effect_analysis")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"[*] Đang mổ xẻ chi tiết Hiệu ứng Chuyển cảnh & SFX từ: {video_path}")
    
    # 1. Trích xuất âm thanh ra WAV để phân tích các đợt đỉnh âm lượng (SFX Peaks & BGM)
    audio_wav = out_dir / "audio_track.wav"
    subprocess.run([
        "ffmpeg", "-y", "-i", str(video_path),
        "-vn", "-ac", "1", "-ar", "22050",
        str(audio_wav)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # 2. Trích xuất chuỗi frame tại các mốc thời gian chuyển cảnh tiêu biểu
    # Thử lấy các mốc: 3.5s (sau câu hook), 8.5s (sau câu mở đầu), 15.0s, 22.0s
    transition_times = [3.6, 5.6, 8.4, 11.5, 20.0, 35.0, 50.0]
    
    cap = cv2.VideoCapture(str(video_path))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    
    transition_findings = []
    
    for t in transition_times:
        center_frame = int(t * fps)
        t_folder = out_dir / f"trans_{int(t*10)}s"
        t_folder.mkdir(parents=True, exist_ok=True)
        
        # Chụp 5 frame trước và 5 frame sau điểm chuyển cảnh
        frames = []
        for f_offset in range(-4, 5):
            f_idx = max(0, center_frame + f_offset)
            cap.set(cv2.CAP_PROP_POS_FRAMES, f_idx)
            ret, frame = cap.read()
            if ret:
                f_name = t_folder / f"f_{f_offset:+03d}.jpg"
                cv2.imwrite(str(f_name), frame)
                frames.append(frame)
                
        # Phân tích độ biến thiên giữa các frame để nhận diện kiểu chuyển cảnh
        if len(frames) >= 2:
            diffs = []
            for i in range(len(frames)-1):
                diff = cv2.absdiff(frames[i], frames[i+1])
                diff_score = np.mean(diff)
                diffs.append(diff_score)
            max_diff = max(diffs)
            
            # Nhận diện: nếu max_diff rất lớn -> Jump Cut hoặc Flash; nếu tăng dần đều -> Zoom/Wipe/Dissolve
            t_type = "Hard Jump-Cut + Sound Effect"
            if max_diff > 45:
                t_type = "High-energy Whip/Flash/Jump Cut"
            elif max_diff > 25:
                t_type = "Dynamic Motion Transition"
            else:
                t_type = "Subtle Pacing Cut"
                
            transition_findings.append({
                "timestamp_sec": t,
                "type": t_type,
                "motion_energy_score": round(float(max_diff), 2),
                "frame_folder": str(t_folder.resolve()).replace("\\", "/")
            })
            
    cap.release()
    
    summary_file = out_dir / "transitions_summary.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(transition_findings, f, ensure_ascii=False, indent=2)
        
    print(f"[+] Đã hoàn tất phân tích {len(transition_findings)} điểm chuyển cảnh!")
    return transition_findings

if __name__ == "__main__":
    inspect_transitions_and_sfx(Path("references/Download.mp4"))
