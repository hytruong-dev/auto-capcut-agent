import os
import sys
import json
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

def extract_rules():
    transcript_path = Path("processed/reference_analysis/transcript.json")
    with open(transcript_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    segments = data.get("segments", [])
    total_duration = data.get("duration", 227.6)
    total_words = sum(len(s.get("text", "").split()) for s in segments)
    wpm = round((total_words / (total_duration / 60)), 1)
    avg_seg_dur = round(total_duration / max(1, len(segments)), 2)
    
    print("=== KẾT QUẢ GIẢI MÃ PHONG CÁCH TỪ VIDEO MẪU (TREND DECONSTRUCTION) ===")
    print(f"- Thời lượng tổng: {total_duration:.1f}s")
    print(f"- Tổng số phân đoạn thoại: {len(segments)}")
    print(f"- Tốc độ nói trung bình (WPM): {wpm} từ/phút (Nhịp nói rất nhanh, dứt khoát, liên tục không ngắt quãng)")
    print(f"- Thời lượng trung bình mỗi câu/phân cảnh (ASL): {avg_seg_dur}s (Nhịp cắt cực kỳ dồn dập, cứ mỗi 2.7s đổi 1 câu hoặc 1 góc máy)")
    
    # 5 câu đầu tiên (Hook Strategy)
    print("\n--- CHIẾN LƯỢC HOOK 5S ĐẦU TIÊN ---")
    for s in segments[:4]:
        print(f"[{s['start']:.1f}s - {s['end']:.1f}s] {s['text']}")
        
    rules_summary = {
        "source": "references/Download.mp4",
        "title": "Thử thách chạy GrabFood 11 tiếng thực tế",
        "pacing": {
            "wpm": wpm,
            "avg_shot_length_sec": avg_seg_dur,
            "rule": "Cắt bỏ toàn bộ khoảng lặng > 0.15s, nhịp nói dồn dập, không để video có 1 giây 'chết'"
        },
        "hook_formula": {
            "title_layout": "Tiêu đề 2 dòng đặt tại 1/3 trên màn hình: Dòng 1 Đỏ Cam viền trắng, Dòng 2 Vàng viền đen 3D nổi khối",
            "hook_script_template": "Thử thách [Hành động] [Thời gian] thực sự kiếm được bao nhiêu? Hôm nay mình test thực tế luôn! Ai thắc mắc xem hết video này nha!"
        },
        "subtitle_styling": {
            "position_y": -0.4,
            "font_casing": "IN HOA TOÀN BỘ (UPPERCASE)",
            "base_color": "#FFFFFF",
            "border_color": "#000000",
            "border_width_px": 8,
            "highlight_color": "#66FFFF",
            "highlight_usage": "Đổi màu Xanh Dương Neon hoặc Vàng cho từ khóa hành động/con số ngay khi đọc đến từ đó (Word-level pop animation)"
        },
        "b_roll_and_visual_retention": {
            "cut_in_face": "Cứ 3-5s chèn 1 shot quay cận mặt tài xế uống nước, nói chuyện hoặc biểu cảm mệt/vui",
            "cut_in_phone": "Chèn shot cận cảnh màn hình điện thoại (app nổ đơn, bản đồ chỉ đường, số tiền cộng vào ví)",
            "callout_box": "Khung chat trắng bo góc kèm icon Trái tim, Hoa, Like ở góc phải/giữa màn hình để kêu gọi tương tác"
        }
    }
    
    out_file = Path("processed/reference_analysis/extracted_rules.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(rules_summary, f, ensure_ascii=False, indent=2)
        
    print(f"\n[+] Đã lưu cấu trúc quy tắc vào {out_file}")
    return rules_summary

if __name__ == "__main__":
    extract_rules()
