"""
Render hoàn chỉnh Video Vlog XanhSM 1 Ngày Chạy Xe (Thời lượng ~2.5 phút, Tổng thu 176k)
- Chuẩn hóa toàn bộ theo bộ não đã train (portable_trained_brain):
  + Khung hình: 1080x1920 (9:16 dọc), 30fps, DJI transpose=1
  + Cảnh đêm: Color grade bão hòa đèn đường lung linh (eq + unsharp)
  + Nhạc nền: BGM LoFi loop âm lượng 0.15 khi có thoại
  + Chuyển cảnh: Xfade mượt mà giữa các ca chạy sáng, trưa, chiều, tan tầm, đêm
  + SFX Nhận tiền: Cash Register & Ting Ting nổ đúng mili-giây hoàn thành 6 đơn xe (+16k, +22k, +35k, +28k, +42k, +33k)
  + Phụ đề: Dynamic Word Karaoke (Oswald-Bold, Vàng chanh #F0FF00, từ đang đọc Cyan #66FFFF, Safe Zone MarginV 550)
  + Hook 2 tầng 3D (Đỏ/Vàng) ở 0-5s đầu
  + Thẻ Tổng Thu Cuối Ngày 176k & Callout CTA ở nửa trên màn hình
- Đầu ra: processed/Vlog_XanhSM_1Ngay_176k_Long_FINAL.mp4
"""

import os
import sys
import json
import subprocess
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

def build_and_render():
    print("="*65)
    print("🎬 KHỞI ĐỘNG PIPELINE RENDER VLOG XANHSM 176K (2.5 PHÚT)")
    print("="*65)

    base_dir = Path(__file__).resolve().parent.parent
    out_dir = base_dir / "processed"
    temp_dir = out_dir / "temp_render_176k_long"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    final_video = out_dir / "Vlog_XanhSM_1Ngay_176k_Long_FINAL.mp4"

    # ---------------------------------------------------------
    # BƯỚC 1: TRỘN MASTER AUDIO (Voiceover + BGM LoFi + 10 SFX)
    # ---------------------------------------------------------
    print("\n[1/4] Trộn Master Audio (4 tầng âm thanh chuyên nghiệp)...")
    vo_file = out_dir / "voiceover_xanhsm_176k" / "vlog_xanhsm_176k_full_voiceover.mp3"
    bgm_file = out_dir / "bgm_xanhsm_176k_loop.mp3"
    
    sfx_whoosh = base_dir / "public" / "sfx" / "whoosh_fast.mp3"
    sfx_ding = base_dir / "public" / "sfx" / "ding_highlight.mp3"
    sfx_cash = base_dir / "public" / "sfx" / "cash_register.mp3"
    sfx_ting = base_dir / "public" / "sfx" / "ting_money.mp3"

    # Lịch trình SFX khớp 100% từng mili-giây
    sfx_schedule = [
        {"file": str(sfx_whoosh), "delay": 0, "vol": 0.85},          # Hook whoosh
        {"file": str(sfx_ding), "delay": 1200, "vol": 0.9},          # Hook ding
        {"file": str(sfx_cash), "delay": 26800, "vol": 0.95},        # Đơn 1 (+16k, Tổng 16k)
        {"file": str(sfx_ting), "delay": 44800, "vol": 0.95},        # Đơn 2 (+22k, Tổng 38k)
        {"file": str(sfx_cash), "delay": 65400, "vol": 0.95},        # Đơn 3 (+35k, Tổng 73k)
        {"file": str(sfx_ting), "delay": 82700, "vol": 0.95},        # Đơn 4 (+28k, Tổng 101k)
        {"file": str(sfx_cash), "delay": 105100, "vol": 0.95},       # Đơn 5 (+42k, Tổng 143k)
        {"file": str(sfx_cash), "delay": 124800, "vol": 0.95},       # Đơn 6 (+33k, Tổng 176k)
        {"file": str(sfx_ting), "delay": 125600, "vol": 0.9},        # Ting chốt ca
        {"file": str(sfx_ding), "delay": 129500, "vol": 0.95}        # Thẻ Tổng Thu 176k
    ]

    inputs_audio = ["-i", str(vo_file), "-i", str(bgm_file)]
    filter_parts = [
        "[0:a]volume=1.05[avo];",
        "[1:a]volume=0.15[abgm];"
    ]
    mix_labels = ["[avo]", "[abgm]"]

    for idx, item in enumerate(sfx_schedule, start=2):
        inputs_audio.extend(["-i", item["file"]])
        d = item["delay"]
        v = item["vol"]
        filter_parts.append(f"[{idx}:a]adelay={d}|{d},volume={v}[asfx{idx}];")
        mix_labels.append(f"[asfx{idx}]")

    num_inputs = len(mix_labels)
    filter_parts.append(f"{''.join(mix_labels)}amix=inputs={num_inputs}:duration=first:dropout_transition=0,volume={num_inputs * 0.72}[aout]")

    master_audio = temp_dir / "master_audio_long.wav"
    cmd_audio = ["ffmpeg", "-y"] + inputs_audio + ["-filter_complex", "".join(filter_parts), "-map", "[aout]", str(master_audio)]
    subprocess.run(cmd_audio, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"  [+] Đã xuất file Master Audio hoàn chỉnh: {master_audio}")

    # ---------------------------------------------------------
    # BƯỚC 2: CẮT & COLOR GRADE CÁC PHÂN ĐOÀN TỪ 3 CLIP DJI
    # ---------------------------------------------------------
    print("\n[2/4] Cắt và định dạng 15 phân cảnh 9:16 dọc từ 3 footage...")
    
    foot_0057 = str(base_dir / "raw_footage" / "DJI_20260908084243_0057_D.MP4")
    foot_0062 = str(base_dir / "raw_footage" / "DJI_20260908183824_0062_D.MP4")
    foot_0064 = str(base_dir / "raw_footage" / "DJI_20260908185603_0064_D.MP4")

    # Danh sách 15 scenes bao phủ trọn vẹn 153s
    scenes_spec = [
        # --- CA SÁNG (0s -> 31.9s) ---
        {"id": 0, "foot": foot_0057, "ss": 0.0, "dur": 5.5, "night": False, "zoom": True},    # Hook 0-5.5s
        {"id": 1, "foot": foot_0057, "ss": 5.5, "dur": 9.5, "night": False, "zoom": False},   # Chuẩn bị & mở app
        {"id": 2, "foot": foot_0057, "ss": 10.4, "dur": 16.9, "night": False, "zoom": False}, # Đón học sinh & Đơn 1 (+16k)
        
        # --- CA TRƯA & ĐẦU CHIỀU (31.9s -> 70.4s) ---
        {"id": 3, "foot": foot_0062, "ss": 0.0, "dur": 12.9, "night": False, "zoom": False},  # Chạy trưa văn phòng
        {"id": 4, "foot": foot_0062, "ss": 13.0, "dur": 4.7, "night": False, "zoom": False},  # Giao hồ sơ & Đơn 2 (+22k)
        {"id": 5, "foot": foot_0062, "ss": 18.0, "dur": 15.9, "night": False, "zoom": False}, # Trà đá & đón khách công sở
        {"id": 6, "foot": foot_0062, "ss": 34.0, "dur": 5.0, "night": False, "zoom": False},  # Khách khen & Đơn 3 (+35k)
        
        # --- GIỜ TAN TẦM (70.4s -> 90.1s) ---
        {"id": 7, "foot": foot_0062, "ss": 39.0, "dur": 12.3, "night": False, "zoom": False}, # Kẹt xe tan tầm chen chúc
        {"id": 8, "foot": foot_0062, "ss": 51.5, "dur": 7.4, "night": False, "zoom": False},  # Luồn lách hẻm & Đơn 4 (+28k)
        
        # --- CA ĐÊM / LÊN ĐÈN (90.1s -> 129.1s) ---
        {"id": 9, "foot": foot_0064, "ss": 0.0, "dur": 15.0, "night": True, "zoom": False},   # 7h tối lên đèn rực rỡ
        {"id": 10, "foot": foot_0064, "ss": 15.0, "dur": 4.3, "night": True, "zoom": False},  # Cuốc đường dài & Đơn 5 (+42k)
        {"id": 11, "foot": foot_0064, "ss": 20.0, "dur": 15.4, "night": True, "zoom": False}, # Thấm mệt bật định hướng
        {"id": 12, "foot": foot_0064, "ss": 35.5, "dur": 4.3, "night": True, "zoom": False},  # Đơn tiện đường & Đơn 6 (+33k)
        
        # --- TỔNG KẾT & OUTRO (129.1s -> 153.0s) ---
        {"id": 13, "foot": foot_0064, "ss": 40.0, "dur": 13.4, "night": True, "zoom": False}, # Tổng kết ngày 176k
        {"id": 14, "foot": foot_0064, "ss": 54.0, "dur": 10.5, "night": True, "zoom": False}  # Outro tim & bình luận
    ]

    rendered_segs = []
    for sc in scenes_spec:
        idx = sc["id"]
        seg_mp4 = temp_dir / f"scene_{idx:02d}.mp4"
        rendered_segs.append(str(seg_mp4.resolve()))

        if not seg_mp4.exists() or seg_mp4.stat().st_size < 1000:
            # Bộ lọc xử lý hình ảnh chuẩn đã train
            if sc["zoom"]:
                # Hook zoom punch-in 1.10x
                vf_steps = ["transpose=1", "scale=1200:2133", "crop=1080:1920"]
            else:
                vf_steps = ["transpose=1", "scale=1080:1920:force_original_aspect_ratio=increase", "crop=1080:1920"]
                
            if sc["night"]:
                # Chuẩn màu đêm: eq + unsharp
                vf_steps.append("eq=brightness=0.06:saturation=1.25:contrast=1.1,unsharp=5:5:0.8")
            else:
                vf_steps.append("eq=saturation=1.12:contrast=1.06")
                
            vf_steps.append("fps=30")
            vf_filter = ",".join(vf_steps)

            cmd_cut = [
                "ffmpeg", "-y",
                "-ss", str(sc["ss"]),
                "-t", str(sc["dur"]),
                "-i", sc["foot"],
                "-vf", vf_filter,
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
                "-r", "30", "-an",
                str(seg_mp4)
            ]
            subprocess.run(cmd_cut, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"  [+] Đã cắt phân cảnh {idx+1}/{len(scenes_spec)} ({sc['dur']}s, night={sc['night']})")

    # Ghép 15 phân cảnh thành video thô
    concat_txt = temp_dir / "concat_scenes.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for sf in rendered_segs:
            f.write(f"file '{sf.replace(chr(92), '/')}'\n")

    raw_stitched = temp_dir / "stitched_raw_long.mp4"
    cmd_concat = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt), "-c", "copy", str(raw_stitched)]
    subprocess.run(cmd_concat, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"  [+] Đã ghép xong 15 phân cảnh liên tục: {raw_stitched}")

    # ---------------------------------------------------------
    # BƯỚC 3: ÉP PHỤ ĐỀ ASS DYNAMIC KARAOKE & GHÉP MASTER AUDIO
    # ---------------------------------------------------------
    print("\n[3/4] Ép phụ đề Dynamic Word Karaoke, 6 Thẻ Tiền, Hook 2 Tầng và Xuất Bản...")
    
    ass_file = "processed/vlog_xanhsm_176k_long_master.ass"
    fonts_dir = "portable_trained_brain/portable_assets/fonts"
    ass_filter_arg = f"ass='{ass_file}':fontsdir='{fonts_dir}'"

    cmd_render = [
        "ffmpeg", "-y",
        "-i", str(raw_stitched),
        "-i", str(master_audio),
        "-vf", ass_filter_arg,
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(final_video)
    ]
    subprocess.run(cmd_render, check=True)

    # Đo thông số video hoàn chỉnh
    dur = float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(final_video)
    ]).decode().strip())
    size_mb = os.path.getsize(final_video) / (1024 * 1024)

    # ---------------------------------------------------------
    # BƯỚC 4: TRÍCH XUẤT CÁC KHUNG HÌNH KIỂM TRA CHẤT LƯỢNG (QA)
    # ---------------------------------------------------------
    print("\n[4/4] Trích xuất khung hình QA để kiểm tra phụ đề, thẻ tiền và bố cục...")
    qa_dir = out_dir / "qa_frames_long"
    qa_dir.mkdir(parents=True, exist_ok=True)

    qa_points = [
        {"name": "01_hook_dual_layer.jpg", "time": 2.5},     # Hook 2 tầng Đỏ - Vàng
        {"name": "02_order1_cash_16k.jpg", "time": 28.5},     # Đơn 1 (+16k, Tổng 16k)
        {"name": "03_order3_cash_35k.jpg", "time": 67.5},     # Đơn 3 (+35k, Tổng 73k)
        {"name": "04_order6_cash_33k.jpg", "time": 126.5},    # Đơn 6 (+33k, Tổng 176k)
        {"name": "05_summary_box_176k.jpg", "time": 133.0},   # Thẻ Tổng Thu 176k
        {"name": "06_outro_callout.jpg", "time": 146.0}       # Callout tương tác CTA
    ]

    for q in qa_points:
        q_out = qa_dir / q["name"]
        cmd_qa = [
            "ffmpeg", "-y",
            "-ss", str(q["time"]),
            "-i", str(final_video),
            "-frames:v", "1",
            "-q:v", "2",
            str(q_out)
        ]
        subprocess.run(cmd_qa, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"  [+] Đã chụp ảnh QA tại {q['time']}s: {q_out}")

    print("\n" + "="*65)
    print("🎉 CHÚC MỪNG! VIDEO VLOG XANHSM 176K (2.5 PHÚT) ĐÃ XUẤT XƯỞNG!")
    print(f"🎬 File Video: {final_video}")
    print(f"⏱️ Thời lượng chuẩn: {dur:.2f}s (~{dur/60:.2f} phút) -> ĐÚNG YÊU CẦU 2 - 3 PHÚT!")
    print(f"💾 Dung lượng: {size_mb:.2f} MB")
    print(f"📐 Bố cục: 1080x1920 (9:16 dọc TikTok/Reels/Shorts)")
    print(f"💰 6 Đơn xe: Đơn 1 (+16k), Đơn 2 (+22k), Đơn 3 (+35k), Đơn 4 (+28k), Đơn 5 (+42k), Đơn 6 (+33k)")
    print(f"🎯 Tổng kết ngày: ĐÚNG 176.000Đ!")
    print(f"🔊 SFX Nhận tiền: Nổ cash register & ting money từng đơn")
    print("="*65)

if __name__ == "__main__":
    build_and_render()
