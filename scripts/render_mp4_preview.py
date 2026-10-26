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

def render_preview():
    preview_dir = Path("processed/preview_clips")
    preview_dir.mkdir(parents=True, exist_ok=True)
    
    with open("processed/vlog_aligned_script.json", "r", encoding="utf-8") as f:
        items = json.load(f)
        
    print("[*] Đang cắt và xoay 90 độ các phân đoạn video...")
    clip_files = []
    for idx, item in enumerate(items):
        src_video = Path("raw_footage") / item["video_ref"]
        out_clip = preview_dir / f"clip_{item['id']}.mp4"
        
        # Cắt đúng đoạn và xoay 90 độ xuôi chiều kim đồng hồ (transpose=1), scale về 1080x1920
        cmd = [
            "ffmpeg", "-y",
            "-ss", str(item["video_start"]),
            "-i", str(src_video),
            "-t", str(item["video_duration"]),
            "-vf", "transpose=1,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "24",
            "-an",
            str(out_clip)
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        clip_files.append(out_clip)
        print(f"    [+] Xong clip {idx+1}/{len(items)}: {out_clip.name}")
        
    concat_txt = preview_dir / "concat_video.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for c in clip_files:
            f.write(f"file '{c.resolve().as_posix()}'\n")
            
    concat_video = preview_dir / "concat_raw.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_txt), "-c", "copy", str(concat_video)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Ghép âm thanh Voiceover + BGM ducked
    voice_path = Path("processed/voiceover/full_voiceover.mp3")
    bgm_path = Path("public/bgm/bgm_lofi_xanhsm.mp3")
    final_output = Path("processed/Vlog_XanhSM_Preview_60s.mp4")
    
    print(f"[*] Đang mix âm thanh và xuất video MP4 preview: {final_output}...")
    mix_cmd = [
        "ffmpeg", "-y",
        "-i", str(concat_video),
        "-i", str(voice_path),
        "-stream_loop", "-1", "-i", str(bgm_path),
        "-filter_complex",
        "[1:a]volume=1.0[v];[2:a]volume=0.15[b];[v][b]amix=inputs=2:duration=first[aout]",
        "-map", "0:v", "-map", "[aout]",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(final_output)
    ]
    subprocess.run(mix_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    if final_output.exists():
        print(f"\n[+] ĐÃ XUẤT THÀNH CÔNG VIDEO PREVIEW: {final_output.resolve()}")
        print(f"[+] Dung lượng: {final_output.stat().st_size / (1024*1024):.2f} MB")
        
if __name__ == "__main__":
    render_preview()
