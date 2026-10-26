"""
Sinh Voiceover 1 Ngày Chạy Xe XanhSM (Tổng thu 176k) bằng VoiceStudio / OmniVoice Voice Clone
- Model: OmniVoice from VoiceStudio
- Reference audio: ref_sample_hook.wav (mẫu giọng tài xế vlog từ Download.mp4)
- Output: processed/voiceover_omnivoice_176k/
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
import torch
import torchaudio

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

os.environ["HF_HOME"] = r"C:\Users\PC\AppData\Local\OmniVoice\hf_cache"
from omnivoice.models.omnivoice import OmniVoice

OUT_DIR = Path("processed/voiceover_omnivoice_176k")
OUT_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH = r"C:\Users\PC\AppData\Local\OmniVoice\hf_cache\models--k2-fsa--OmniVoice\snapshots\c5fdb5ccb189668d56333f77ba2629f4cd7535f4"
REF_AUDIO = r"c:\QuangHy\editvideo\processed\voiceover\ref_sample_hook.wav"
REF_TEXT = "Thử thách chạy GrabFood 11 tiếng thực sự kiếm được bao nhiêu. Hôm nay anh test thực tế luôn."

SCRIPT_ITEMS = [
    # --- PHẦN 1: HOOK (0s - 12s) ---
    {
        "id": 1,
        "text": "Một ngày chạy xe máy điện Xanh SM từ sáng đến đêm thực sự kiếm được bao nhiêu tiền?",
        "phrases": [
            ["MỘT", "NGÀY", "CHẠY", "XE"],
            ["MÁY", "ĐIỆN", "XANH", "SM"],
            ["TỪ", "SÁNG", "ĐẾN", "ĐÊM"],
            ["THỰC", "SỰ", "KIẾM", "ĐƯỢC"],
            ["BAO", "NHIÊU", "TIỀN?"]
        ]
    },
    {
        "id": 2,
        "text": "Hôm nay anh em cùng mình cày thực tế xem tổng thu được bao nhiêu nhé!",
        "phrases": [
            ["HÔM", "NAY", "CÙNG", "MÌNH"],
            ["CÀY", "THỰC", "TẾ"],
            ["XEM", "TỔNG", "THU"],
            ["ĐƯỢC", "BAO", "NHIÊU", "NHÉ!"]
        ]
    },

    # --- PHẦN 2: CA SÁNG - ĐƠN #1 (16k) ---
    {
        "id": 3,
        "text": "Tám giờ sáng, mình bắt đầu bật app trực ca.",
        "phrases": [
            ["TÁM", "GIỜ", "SÁNG"],
            ["MÌNH", "BẮT", "ĐẦU"],
            ["BẬT", "APP", "TRỰC", "CA"]
        ]
    },
    {
        "id": 4,
        "text": "Xe VinFast sạc đầy pin chạy êm ru, nổ ngay đơn đón bạn học sinh đi học.",
        "phrases": [
            ["XE", "VINFAST", "ÊM", "RU"],
            ["NỔ", "NGAY", "ĐƠN"],
            ["ĐÓN", "BẠN", "HỌC", "SINH"]
        ]
    },
    {
        "id": 5,
        "text": "Cuốc đầu tiên mở bát, khách trả đúng mười sáu cành nha anh em!",
        "phrases": [
            ["CUỐC", "ĐẦU", "TIÊN"],
            ["MỞ", "BÁT"],
            ["ĐƯỢC", "MƯỜI", "SÁU", "CÀNH!"]
        ],
        "cash_event": {"order": 1, "amt": "+16.000đ", "total": "TỔNG THU: 16.000đ"}
    },

    # --- PHẦN 3: CA TRƯA - ĐƠN #2 (22k -> 38k) ---
    {
        "id": 6,
        "text": "Tiếp tục chạy trưa, app báo nhận đơn giao tài liệu hỏa tốc sang Quận Nhất.",
        "phrases": [
            ["TIẾP", "TỤC", "CHẠY", "TRƯA"],
            ["NHẬN", "ĐƠN", "HỎA", "TỐC"],
            ["SANG", "QUẬN", "NHẤT"]
        ]
    },
    {
        "id": 7,
        "text": "Trưa nắng gắt nhưng xe điện không bị nóng chân, giao xong nhận thêm hai mươi hai cành.",
        "phrases": [
            ["XE", "ĐIỆN", "MÁT", "MẺ"],
            ["GIAO", "XONG", "NHẬN"],
            ["HAI", "MƯƠI", "HAI", "CÀNH!"]
        ],
        "cash_event": {"order": 2, "amt": "+22.000đ", "total": "TỔNG THU: 38.000đ"}
    },

    # --- PHẦN 4: ĐẦU GIỜ CHIỀU - ĐƠN #3 (35k -> 73k) ---
    {
        "id": 8,
        "text": "Uống vội ly trà đá thì app nổ cuốc thứ ba chở anh khách công sở sang Quận Ba.",
        "phrases": [
            ["UỐNG", "VỘI", "LY", "TRÀ"],
            ["NỔ", "CUỐC", "THỨ", "BA"],
            ["SANG", "QUẬN", "BA"]
        ]
    },
    {
        "id": 9,
        "text": "Đường xá đông đúc nhưng xe êm khách khen quá trời, ví nhảy thêm ba mươi lăm nghìn.",
        "phrases": [
            ["XE", "ÊM", "KHÁCH", "KHEN"],
            ["VÍ", "NHẢY", "THÊM"],
            ["BA", "MƯƠI", "LĂM", "NGHÌN!"]
        ],
        "cash_event": {"order": 3, "amt": "+35.000đ", "total": "TỔNG THU: 73.000đ"}
    },

    # --- PHẦN 5: GIỜ TAN TẦM - ĐƠN #4 (28k -> 101k) ---
    {
        "id": 10,
        "text": "Năm giờ chiều, Sài Gòn bước vào giờ tan tầm kẹt xe chen chúc từng chút một.",
        "phrases": [
            ["NĂM", "GIỜ", "CHIỀU"],
            ["GIỜ", "TAN", "TẦM"],
            ["KẸT", "XE", "CHEN", "CHÚC"]
        ]
    },
    {
        "id": 11,
        "text": "Tay ga nhạy luồn lách ngõ hẻm trả khách đúng giờ, đơn này thu thêm hai mươi tám cành.",
        "phrases": [
            ["LUỒN", "LÁCH", "HẺM", "NHỎ"],
            ["THU", "VỀ", "THÊM"],
            ["HAI", "MƯƠI", "TÁM", "CÀNH!"]
        ],
        "cash_event": {"order": 4, "amt": "+28.000đ", "total": "TỔNG THU: 101.000đ"}
    },

    # --- PHẦN 6: CHẬP TỐI LÊN ĐÈN - ĐƠN #5 (42k -> 143k) ---
    {
        "id": 12,
        "text": "Bảy giờ tối, thành phố lên đèn lung linh, mình nhận cuốc đường dài về ngoại ô.",
        "phrases": [
            ["BẢY", "GIỜ", "TỐI"],
            ["LÊN", "ĐÈN", "LUNG", "LINH"],
            ["CUỐC", "ĐƯỜNG", "DÀI"]
        ]
    },
    {
        "id": 13,
        "text": "Chạy đường đêm gió mát cảm giác cực kỳ chill, chuyến thứ năm bỏ túi bốn mươi hai nghìn.",
        "phrases": [
            ["GIÓ", "MÁT", "RẤT", "CHILL"],
            ["BỎ", "TÚI", "THÊM"],
            ["BỐN", "MƯƠI", "HAI", "NGHÌN!"]
        ],
        "cash_event": {"order": 5, "amt": "+42.000đ", "total": "TỔNG THU: 143.000đ"}
    },

    # --- PHẦN 7: CA ĐÊM & CHỐT ĐƠN #6 (33k -> 176k) ---
    {
        "id": 14,
        "text": "Hơn tám giờ đêm, người đã thấm mệt nên mình bật định hướng tìm đơn về phòng trọ.",
        "phrases": [
            ["HƠN", "TÁM", "GIỜ", "ĐÊM"],
            ["NGƯỜI", "ĐÃ", "THẤM", "MỆT"],
            ["TÌM", "ĐƠN", "VỀ", "NHÀ"]
        ]
    },
    {
        "id": 15,
        "text": "May mắn nổ ngay đơn tiện đường ba mươi ba nghìn, chốt trọn vẹn cuốc xe thứ sáu trong ngày.",
        "phrases": [
            ["NỔ", "ĐƠN", "TIỆN", "ĐƯỜNG"],
            ["BA", "MƯƠI", "BA", "NGHÌN!"],
            ["CHỐT", "CA", "THÀNH", "CÔNG"]
        ],
        "cash_event": {"order": 6, "amt": "+33.000đ", "total": "TỔNG THU: 176.000đ"}
    },

    # --- PHẦN 8: TỔNG KẾT & KÊU GỌI TƯƠNG TÁC (176k) ---
    {
        "id": 16,
        "text": "Vậy là tổng kết một ngày chạy Xanh SM được đúng một trăm bảy mươi sáu nghìn đồng.",
        "phrases": [
            ["TỔNG", "KẾT", "MỘT", "NGÀY"],
            ["ĐÚNG", "MỘT", "TRĂM"],
            ["BẢY", "MƯƠI", "SÁU", "NGHÌN!"]
        ]
    },
    {
        "id": 17,
        "text": "Dù vất vả nhưng đó là đồng tiền mồ hôi công sức chân chính và rất tự hào.",
        "phrases": [
            ["ĐỒNG", "TIỀN", "MỒ", "HÔI"],
            ["CÔNG", "SỨC", "CHÂN", "CHÍNH"],
            ["RẤT", "TỰ", "HÀO!"]
        ]
    },
    {
        "id": 18,
        "text": "Anh em hôm nay được bao nhiêu lúa rồi? Comment bên dưới và bấm tim ủng hộ mình nhé!",
        "phrases": [
            ["ANH", "EM", "HÔM", "NAY"],
            ["ĐƯỢC", "BAO", "NHIÊU?"],
            ["COMMENT", "BÊN", "DƯỚI"],
            ["BẤM", "TIM", "ỦNG", "HỘ", "NHÉ!"]
        ]
    }
]

def main():
    print(f"[*] Đang tải mô hình OmniVoice từ {MODEL_PATH}...")
    t0 = time.time()
    model = OmniVoice.from_pretrained(MODEL_PATH, device_map="cpu", dtype=torch.float32)
    print(f"[*] Đã tải xong mô hình trong {time.time() - t0:.2f}s")

    print(f"[*] Mã hóa giọng nói tham chiếu từ: {REF_AUDIO}...")
    clone_prompt = model.create_voice_clone_prompt(
        ref_audio=REF_AUDIO,
        ref_text=REF_TEXT,
        preprocess_prompt=True
    )
    print(f"[+] Đã tạo voice clone prompt thành công!")

    timeline = []
    current_time = 0.5  # Khoảng đệm đầu video 0.5s

    for item in SCRIPT_ITEMS:
        item_id = item["id"]
        text = item["text"]
        raw_wav = OUT_DIR / f"raw_{item_id:02d}.wav"
        final_mp3 = OUT_DIR / f"seg_{item_id:02d}.mp3"

        if not final_mp3.exists():
            print(f"[{item_id:02d}/{len(SCRIPT_ITEMS)}] Đang sinh giọng: \"{text[:35]}...\"")
            t_gen = time.time()
            audios = model.generate(
                text=text,
                language="Vietnamese",
                voice_clone_prompt=clone_prompt,
                num_step=10,             # 10 steps: nhanh và giữ độ tự nhiên cao
                guidance_scale=1.8,
                speed=1.05
            )
            torchaudio.save(str(raw_wav), audios[0], model.sampling_rate)
            
            # Chuẩn hóa loudnorm -14 LUFS theo chuẩn learned_editing_style
            cmd_norm = [
                "ffmpeg", "-y",
                "-i", str(raw_wav),
                "-filter_complex", "loudnorm=I=-14:TP=-1.5:LRA=11",
                "-c:a", "libmp3lame", "-b:a", "192k",
                str(final_mp3)
            ]
            subprocess.run(cmd_norm, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"    -> Xong trong {time.time() - t_gen:.1f}s")

        dur = float(subprocess.check_output([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(final_mp3)
        ]).decode().strip())

        seg_entry = {
            "id": item_id,
            "text": text,
            "phrases": item["phrases"],
            "file": str(final_mp3.resolve()).replace("\\", "/"),
            "start": round(current_time, 3),
            "duration": round(dur, 3),
            "end": round(current_time + dur, 3)
        }
        if "cash_event" in item:
            seg_entry["cash_event"] = item["cash_event"]

        timeline.append(seg_entry)
        current_time += dur + 0.18 # Đệm 180ms giữa các câu

    total_dur = round(current_time, 3)
    print(f"\n[+] Tổng thời lượng Voiceover OmniVoice: {total_dur:.2f}s (~{total_dur/60:.2f} phút)")

    # Ghép master voiceover
    concat_txt = OUT_DIR / "concat_list.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for t in timeline:
            f.write(f"file '{t['file']}'\n")

    master_vo = OUT_DIR / "vlog_xanhsm_176k_omnivoice_master.mp3"
    inputs = []
    filter_complex = []
    for i, t in enumerate(timeline):
        inputs.extend(["-i", t["file"]])
        delay_ms = int(t["start"] * 1000)
        filter_complex.append(f"[{i}:a]adelay={delay_ms}|{delay_ms}[a{i}];")
    mix_ins = "".join(f"[a{i}]" for i in range(len(timeline)))
    filter_complex.append(f"{mix_ins}amix=inputs={len(timeline)}:duration=longest:dropout_transition=0,volume={len(timeline)}[outa]")
    
    cmd_mix = ["ffmpeg", "-y"] + inputs + ["-filter_complex", "".join(filter_complex), "-map", "[outa]", "-b:a", "192k", str(master_vo)]
    subprocess.run(cmd_mix, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Lưu metadata
    meta_path = Path("processed/omnivoice_176k_timeline.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump({
            "total_duration": total_dur,
            "segments": timeline
        }, f, ensure_ascii=False, indent=2)

    print(f"[+] Master voiceover đã xuất xưởng: {master_vo}")
    print(f"[+] Metadata lưu tại: {meta_path}")

if __name__ == "__main__":
    main()
