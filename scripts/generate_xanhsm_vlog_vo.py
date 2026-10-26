"""
Sinh toàn bộ giọng đọc Voiceover cho Vlog XanhSM 1 Ngày Chạy Xe (Tổng thu 176k)
Thời lượng: ~2 phút 45 giây (165s)
"""
import os
import sys
import json
import subprocess
from pathlib import Path
from gtts import gTTS

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

OUTPUT_DIR = Path("processed/voiceover_xanhsm_176k")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Danh sách các câu thoại phân đoạn theo từng mốc thời gian và đơn hàng
SCRIPT_SEGMENTS = [
    # --- PHẦN 1: HOOK (0s - 12s) ---
    {
        "id": "hook_1",
        "order": 0,
        "section": "hook",
        "text": "Một ngày chạy xe máy điện Xanh SM từ sáng sớm đến đêm muộn thực sự kiếm được bao nhiêu tiền?",
        "kw": "XANH SM TỪ SÁNG ĐẾN ĐÊM"
    },
    {
        "id": "hook_2",
        "order": 0,
        "section": "hook",
        "text": "Hôm nay anh em cùng mình cày cuốc thực tế xem tổng thu được bao nhiêu nhé!",
        "kw": "CÀY THỰC TẾ XEM TỔNG THU"
    },

    # --- PHẦN 2: CA SÁNG - ĐƠN #1 (16k) ---
    {
        "id": "order1_1",
        "order": 1,
        "section": "order1",
        "text": "Tám giờ ba mươi sáng, mình bắt đầu mở app trực ca.",
        "kw": "8H30 SÁNG, MỞ APP TRỰC CA"
    },
    {
        "id": "order1_2",
        "order": 1,
        "section": "order1",
        "text": "Chiếc xe điện VinFast sạc đầy pin từ tối qua, lướt trên đường phố êm ru không một tiếng ồn.",
        "kw": "XE ĐIỆN VINFAST ÊM RU"
    },
    {
        "id": "order1_3",
        "order": 1,
        "section": "order1",
        "text": "Vừa bật app lên tầm năm phút là đã nổ đơn mở bát đón bạn sinh viên đi học rồi!",
        "kw": "NỔ ĐƠN MỞ BÁT ĐÓN KHÁCH"
    },
    {
        "id": "order1_4",
        "order": 1,
        "section": "order1",
        "text": "Cuốc đầu tiên đầu xuôi đuôi lọt, khách trả đúng mười sáu cành nha anh em!",
        "kw": "HOÀN THÀNH ĐƠN 1: +16.000Đ",
        "order_complete": {
            "order_index": 1,
            "amount": 16000,
            "amount_str": "+16.000đ",
            "total": 16000,
            "total_str": "16.000đ"
        }
    },

    # --- PHẦN 3: CA TRƯA - ĐƠN #2 (22k -> Tổng 38k) ---
    {
        "id": "order2_1",
        "order": 2,
        "section": "order2",
        "text": "Tiếp tục di chuyển qua khu văn phòng, chuông app lại reo nhận đơn giao tập hồ sơ hỏa tốc.",
        "kw": "NHẬN ĐƠN GIAO HÀNG HỎA TỐC"
    },
    {
        "id": "order2_2",
        "order": 2,
        "section": "order2",
        "text": "Giao từ Bình Thạnh sang Quận Nhất, trưa nắng bắt đầu gắt nhưng xe điện không bị phà hơi nóng vào chân.",
        "kw": "XE ĐIỆN KHÔNG PHÀ HƠI NÓNG"
    },
    {
        "id": "order2_3",
        "order": 2,
        "section": "order2",
        "text": "Giao xong đơn thứ hai, app báo cộng thêm hai mươi hai cành nữa!",
        "kw": "HOÀN THÀNH ĐƠN 2: +22.000Đ",
        "order_complete": {
            "order_index": 2,
            "amount": 22000,
            "amount_str": "+22.000đ",
            "total": 38000,
            "total_str": "38.000đ"
        }
    },

    # --- PHẦN 4: ĐẦU GIỜ CHIỀU - ĐƠN #3 (35k -> Tổng 73k) ---
    {
        "id": "order3_1",
        "order": 3,
        "section": "order3",
        "text": "Nghỉ ngơi uống vội ly trà đá thì app nổ tiếp cuốc thứ ba.",
        "kw": "APP NỔ TIẾP CUỐC THỨ 3"
    },
    {
        "id": "order3_2",
        "order": 3,
        "section": "order3",
        "text": "Cuốc này là một anh khách công sở đặt xe đi gặp đối tác ở Quận Ba, quãng đường hơn năm cây số.",
        "kw": "QUÃNG ĐƯỜNG HƠN 5 CÂY SỐ"
    },
    {
        "id": "order3_3",
        "order": 3,
        "section": "order3",
        "text": "Đường xá đông đúc nhưng xe êm nên anh khách khen quá trời luôn.",
        "kw": "XE ÊM KHÁCH KHEN QUÁ TRỜI"
    },
    {
        "id": "order3_4",
        "order": 3,
        "section": "order3",
        "text": "Trả khách xong xuôi, ví nhảy thêm ba mươi lăm nghìn, quá phấn khởi!",
        "kw": "HOÀN THÀNH ĐƠN 3: +35.000Đ",
        "order_complete": {
            "order_index": 3,
            "amount": 35000,
            "amount_str": "+35.000đ",
            "total": 73000,
            "total_str": "73.000đ"
        }
    },

    # --- PHẦN 5: GIỜ TAN TẦM - ĐƠN #4 (28k -> Tổng 101k) ---
    {
        "id": "order4_1",
        "order": 4,
        "section": "order4",
        "text": "Năm giờ chiều, Sài Gòn bước vào giờ tan tầm kẹt xe kinh hoàng.",
        "kw": "GIỜ TAN TẦM KẸT XE KINH HOÀNG"
    },
    {
        "id": "order4_2",
        "order": 4,
        "section": "order4",
        "text": "Dòng xe chen chúc từng chút một, may mà tay ga xe điện nhạy, luồn lách qua các hẻm nhỏ cực kỳ linh hoạt.",
        "kw": "TAY GA NHẠY, LUỒN LÁCH HẺM NHỎ"
    },
    {
        "id": "order4_3",
        "order": 4,
        "section": "order4",
        "text": "Đón và trả khách đúng giờ, đơn thứ tư thu về thêm hai mươi tám cành, cán mốc hơn một trăm nghìn rồi nha!",
        "kw": "HOÀN THÀNH ĐƠN 4: +28.000Đ",
        "order_complete": {
            "order_index": 4,
            "amount": 28000,
            "amount_str": "+28.000đ",
            "total": 101000,
            "total_str": "101.000đ"
        }
    },

    # --- PHẦN 6: CHẬP TỐI LÊN ĐÈN - ĐƠN #5 (42k -> Tổng 143k) ---
    {
        "id": "order5_1",
        "order": 5,
        "section": "order5",
        "text": "Bảy giờ tối, thành phố lên đèn rực rỡ, gió đêm mát rượi xua đi bao mệt mỏi.",
        "kw": "THÀNH PHỐ LÊN ĐÈN RỰC RỠ"
    },
    {
        "id": "order5_2",
        "order": 5,
        "section": "order5",
        "text": "Lúc này mình nhận một cuốc xe đường dài từ trung tâm về ngoại ô.",
        "kw": "CUỐC ĐƯỜNG DÀI VỀ NGOẠI Ô"
    },
    {
        "id": "order5_3",
        "order": 5,
        "section": "order5",
        "text": "Chạy đường đêm thoáng đãng cảm giác cực kỳ chill luôn anh em ạ.",
        "kw": "ĐƯỜNG ĐÊM THOÁNG ĐÃNG RẤT CHILL"
    },
    {
        "id": "order5_4",
        "order": 5,
        "section": "order5",
        "text": "Chuyến xe thứ năm hoàn thành xuất sắc với bốn mươi hai nghìn đồng!",
        "kw": "HOÀN THÀNH ĐƠN 5: +42.000Đ",
        "order_complete": {
            "order_index": 5,
            "amount": 42000,
            "amount_str": "+42.000đ",
            "total": 143000,
            "total_str": "143.000đ"
        }
    },

    # --- PHẦN 7: CA ĐÊM & CHỐT ĐƠN #6 (33k -> Tổng 176k) ---
    {
        "id": "order6_1",
        "order": 6,
        "section": "order6",
        "text": "Đồng hồ điểm hơn tám giờ đêm rồi, người cũng đã thấm mệt và lưng mỏi nhừ.",
        "kw": "HƠN 8H ĐÊM, NGƯỜI THẤM MỆT"
    },
    {
        "id": "order6_2",
        "order": 6,
        "section": "order6",
        "text": "Mình bật tính năng định hướng tìm cuốc về gần phòng trọ để chốt ca nghỉ ngơi.",
        "kw": "BẬT ĐỊNH HƯỚNG TÌM ĐƠN VỀ NHÀ"
    },
    {
        "id": "order6_3",
        "order": 6,
        "section": "order6",
        "text": "May mắn vừa bật lên là nổ ngay đơn tiện đường ba mươi ba nghìn!",
        "kw": "NỔ ĐƠN TIỆN ĐƯỜNG 33 CÀNH"
    },
    {
        "id": "order6_4",
        "order": 6,
        "section": "order6",
        "text": "Thế là hoàn thành trọn vẹn cuốc xe thứ sáu trong ngày hôm nay!",
        "kw": "HOÀN THÀNH ĐƠN 6 (CHỐT CA): +33.000Đ",
        "order_complete": {
            "order_index": 6,
            "amount": 33000,
            "amount_str": "+33.000đ",
            "total": 176000,
            "total_str": "176.000đ"
        }
    },

    # --- PHẦN 8: TỔNG KẾT & KÊU GỌI TƯƠNG TÁC (176k) ---
    {
        "id": "summary_1",
        "order": 0,
        "section": "summary",
        "text": "Vậy là tổng kết một ngày chạy Xanh SM của mình hôm nay được đúng một trăm bảy mươi sáu nghìn đồng sau sáu đơn xe.",
        "kw": "TỔNG THU HÔM NAY: 176.000Đ"
    },
    {
        "id": "summary_2",
        "order": 0,
        "section": "summary",
        "text": "Dù vất vả nhưng đó là những đồng tiền mồ hôi công sức chân chính và rất đáng tự hào.",
        "kw": "MỒ HÔI CÔNG SỨC CHÂN CHÍNH"
    },
    {
        "id": "summary_3",
        "order": 0,
        "section": "summary",
        "text": "Anh em chạy xe hôm nay được bao nhiêu lúa rồi? Comment giao lưu bên dưới nhé!",
        "kw": "COMMENT GIAO LƯU NHÉ!"
    },
    {
        "id": "summary_4",
        "order": 0,
        "section": "summary",
        "text": "Nhớ bấm tim và theo dõi kênh để đồng hành cùng mình trong các ca chạy tiếp theo nha!",
        "kw": "BẤM TIM VÀ THEO DÕI KÊNH NHÉ!"
    }
]

def generate_voiceovers():
    print(f"[*] Bắt đầu sinh giọng đọc tiếng Việt cho {len(SCRIPT_SEGMENTS)} phân đoạn...")
    timeline = []
    current_time = 0.0

    raw_seg_files = []
    
    for idx, seg in enumerate(SCRIPT_SEGMENTS):
        seg_id = seg["id"]
        raw_mp3 = OUTPUT_DIR / f"{idx:02d}_{seg_id}_raw.mp3"
        fast_mp3 = OUTPUT_DIR / f"{idx:02d}_{seg_id}.mp3"
        
        # Sinh audio bằng gTTS
        tts = gTTS(text=seg["text"], lang="vi", slow=False)
        tts.save(str(raw_mp3))
        
        # Tăng tốc độ lên 1.18x theo chuẩn ASL viral của kịch bản
        # filter atempo=1.18
        cmd_speed = [
            "ffmpeg", "-y", "-i", str(raw_mp3),
            "-filter:a", "atempo=1.18",
            "-b:a", "192k",
            str(fast_mp3)
        ]
        subprocess.run(cmd_speed, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        
        dur = float(subprocess.check_output([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(fast_mp3)
        ]).decode().strip())
        
        # Khoảng đệm giữa các câu: 0.18s
        padding = 0.18
        
        seg_info = {
            "id": seg_id,
            "order": seg["order"],
            "section": seg["section"],
            "text": seg["text"],
            "kw": seg["kw"],
            "file": str(fast_mp3.resolve()).replace("\\", "/"),
            "start": round(current_time, 3),
            "duration": round(dur, 3),
            "end": round(current_time + dur, 3)
        }
        if "order_complete" in seg:
            seg_info["order_complete"] = seg["order_complete"]
            
        timeline.append(seg_info)
        raw_seg_files.append(str(fast_mp3.resolve()))
        print(f"  [{idx+1}/{len(SCRIPT_SEGMENTS)}] {seg_info['start']:.2f}s -> {seg_info['end']:.2f}s ({dur:.2f}s): {seg['text'][:40]}...")
        
        current_time += dur + padding

    total_duration = round(current_time, 3)
    print(f"\n[+] Tổng thời lượng Voiceover: {total_duration:.2f}s (~{total_duration/60:.2f} phút)")

    # Nối tất cả các segment thành 1 file full_voiceover.mp3 duy nhất
    concat_list_file = OUTPUT_DIR / "concat_list.txt"
    with open(concat_list_file, "w", encoding="utf-8") as f:
        for seg in timeline:
            f.write(f"file '{seg['file']}'\n")
            # Chèn im lặng 0.18s giữa các câu
    
    full_vo_file = OUTPUT_DIR / "vlog_xanhsm_176k_full_voiceover.mp3"
    
    # Ghép chuẩn qua ffmpeg amix hoặc concat demuxer
    # Để căn chuẩn chính xác timeline, ta tạo file audio ghép theo đúng thời gian timeline
    inputs = []
    filter_complex = []
    for i, seg in enumerate(timeline):
        inputs.extend(["-i", seg["file"]])
        delay_ms = int(seg["start"] * 1000)
        filter_complex.append(f"[{i}:a]adelay={delay_ms}|{delay_ms}[a{i}];")
    
    mix_inputs = "".join(f"[a{i}]" for i in range(len(timeline)))
    filter_complex.append(f"{mix_inputs}amix=inputs={len(timeline)}:duration=longest:dropout_transition=0,volume={len(timeline)}[outa]")
    
    cmd_mix = ["ffmpeg", "-y"] + inputs + ["-filter_complex", "".join(filter_complex), "-map", "[outa]", "-b:a", "192k", str(full_vo_file)]
    subprocess.run(cmd_mix, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    final_dur = float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(full_vo_file)
    ]).decode().strip())
    
    print(f"[+] Đã tạo file Voiceover tổng hoàn chỉnh: {full_vo_file} (Thời lượng: {final_dur:.2f}s)")

    timeline_data = {
        "title": "Vlog 1 Ngày Chạy Xe XanhSM - Tổng Thu 176k",
        "total_duration": final_dur,
        "segments": timeline
    }
    
    timeline_json = Path("processed/xanhsm_176k_timeline.json")
    with open(timeline_json, "w", encoding="utf-8") as f:
        json.dump(timeline_data, f, ensure_ascii=False, indent=2)
    print(f"[+] Đã lưu timeline metadata: {timeline_json}")

if __name__ == "__main__":
    generate_voiceovers()
