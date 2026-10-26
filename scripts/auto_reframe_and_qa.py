import os
import sys
import json
import cv2
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

def analyze_auto_reframe(video_path: Path, output_json: Path):
    output_json.parent.mkdir(parents=True, exist_ok=True)
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        print(f"[!] Không thể mở video: {video_path}")
        return

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    print(f"[*] Phân tích video: {width}x{height}, {fps} fps, {total_frames} frames")
    
    # Load Haar cascade mặt có sẵn trong opencv
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(cascade_path)
    
    target_aspect = 9 / 16
    target_crop_w = int(height * target_aspect)
    
    frame_step = max(1, int(fps / 2)) # Quét 2 lần mỗi giây để tối ưu tốc độ
    results = []
    
    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        if frame_idx % frame_step == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=4, minSize=(60, 60))
            
            center_x = width // 2
            if len(faces) > 0:
                # Lấy mặt lớn nhất
                largest_face = max(faces, key=lambda f: f[2] * f[3])
                fx, fy, fw, fh = largest_face
                center_x = fx + fw // 2
                
            crop_x1 = max(0, min(width - target_crop_w, center_x - target_crop_w // 2))
            crop_x2 = crop_x1 + target_crop_w
            
            timestamp = round(frame_idx / fps, 2)
            results.append({
                "timestamp_sec": timestamp,
                "frame": frame_idx,
                "face_detected": len(faces) > 0,
                "center_x": int(center_x),
                "crop_x1": int(crop_x1),
                "crop_x2": int(crop_x2)
            })
            
        frame_idx += 1
        
    cap.release()
    
    reframe_data = {
        "source_resolution": {"width": width, "height": height},
        "target_resolution": {"width": target_crop_w, "height": height},
        "target_ratio": "9:16",
        "key_frames_crop": results
    }
    
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(reframe_data, f, ensure_ascii=False, indent=2)
        
    print(f"[+] Hoàn tất phân tích Auto-Reframe. Đã lưu tọa độ vào: {output_json}")
    return reframe_data

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Cách dùng: python scripts/auto_reframe_and_qa.py <duong_dan_video>")
        sys.exit(1)
        
    v_path = Path(sys.argv[1])
    if not v_path.exists():
        print(f"[!] File không tồn tại: {v_path}")
        sys.exit(1)
        
    analyze_auto_reframe(v_path, Path("processed/reframe_plan.json"))
