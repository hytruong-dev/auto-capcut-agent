"""
Tạo file phụ đề Advanced SubStation Alpha (.ass) chất lượng cao cho Vlog XanhSM 176k:
- Font Oswald-Bold, Viết hoa toàn bộ TT
- Màu vàng chanh #F0FF00, viền đen dày, bóng mờ
- Hook 2 Tầng (Đỏ cam + Vàng tươi)
- 6 Thẻ tiền Hoàn Thành Đơn + Hiệu ứng đếm tiền cộng dồn
- Thẻ Tổng Thu Cuối Ngày 176k
- Callout tương tác CTA
"""

import sys
import json
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

def sec_to_ass_time(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int(round((seconds - int(seconds)) * 100))
    if cs >= 100:
        cs = 99
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def generate_ass():
    with open("processed/xanhsm_176k_timeline.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    segments = data["segments"]
    total_dur = data["total_duration"]

    # Header chuẩn ASS cho video dọc 1080x1920
    # Màu trong ASS là BGR:
    # &H0000FFFF& -> Vàng (#FFFF00)
    # &H0000FF66& -> Xanh Neon (#66FF00)
    # &H0000E6FF& -> Vàng Chanh (#FFE600)
    # &H003333FF& -> Đỏ Cam (#FF3333)
    # &H00FFFFFF& -> Trắng (#FFFFFF)
    # &H00000000& -> Đen (#000000)
    
    ass_lines = [
        "[Script Info]",
        "Title: Vlog 1 Ngay Chay Xe XanhSM - Tong Thu 176k",
        "ScriptType: v4.00+",
        "WrapStyle: 0",
        "PlayResX: 1080",
        "PlayResY: 1920",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        # Phụ đề chính: Alignment 2 (Bottom-Center), MarginV 360 (ngang ngực/bụng, Safe Zone)
        "Style: SubNormal,Oswald,64,&H0000E6FF,&H0000E6FF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,6,3,2,60,60,360,1",
        "Style: SubKeyword,Oswald,68,&H0000FFFF,&H0000FFFF,&H00000000,&H90000000,-1,0,0,0,100,100,1,0,1,7,3,2,60,60,360,1",
        # Hook 2 tầng: Alignment 8 (Top-Center)
        "Style: Hook1,Oswald,88,&H003333FF,&H003333FF,&H00FFFFFF,&H90000000,-1,0,0,0,100,100,2,0,1,7,4,8,60,60,360,1",
        "Style: Hook2,Oswald,98,&H0000E6FF,&H0000E6FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,8,4,8,60,60,480,1",
        # Thẻ tiền Hoàn Thành Đơn: Alignment 8 (Top-Center, Y vừa phải)
        "Style: CashBadgeHeader,Oswald,62,&H0000FF66,&H0000FF66,&H00000000,&H90000000,-1,0,0,0,100,100,1,0,1,7,3,8,60,60,780,1",
        "Style: CashBadgeAmount,Oswald,96,&H0000FFFF,&H0000FFFF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,9,4,8,60,60,860,1",
        "Style: CashBadgeTotal,Oswald,58,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,1,0,1,6,3,8,60,60,980,1",
        # Thẻ Tổng Kết Cuối Ngày
        "Style: SummaryBox,Oswald,76,&H0000FFFF,&H0000FFFF,&H00000000,&HB0000000,-1,0,0,0,100,100,1,0,1,8,4,8,60,60,720,1",
        # Callout CTA
        "Style: CalloutCTA,Oswald,64,&H0066FF66,&H0066FF66,&H00000000,&H90000000,-1,0,0,0,100,100,1,0,1,6,3,8,60,60,1100,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"
    ]

    # 1. Hook Titles (0s -> 6.0s)
    ass_lines.append("; --- HOOK TITLES ---")
    ass_lines.append(f"Dialogue: 1,0:00:00.00,0:00:06.00,Hook1,,0,0,0,,THỬ THÁCH 1 NGÀY")
    ass_lines.append(f"Dialogue: 1,0:00:00.00,0:00:06.00,Hook2,,0,0,0,,CHẠY XE XANH SM")

    # 2. Subtitles từ các câu thoại
    ass_lines.append("\n; --- PHỤ ĐỀ TIẾNG VIỆT ---")
    for seg in segments:
        st_str = sec_to_ass_time(seg["start"])
        et_str = sec_to_ass_time(seg["end"])
        text = seg["text"].upper()
        style = "SubKeyword" if any(k in seg["kw"] for k in ["HOÀN THÀNH", "16.000", "22.000", "35.000", "28.000", "42.000", "33.000", "176.000"]) else "SubNormal"
        ass_lines.append(f"Dialogue: 0,{st_str},{et_str},{style},,0,0,0,,{text}")

    # 3. 6 Thẻ Tiền Hoàn Thành Đơn Nhận Tiền
    ass_lines.append("\n; --- HIỆU ỨNG THẺ TIỀN NHẬN ĐƠN ---")
    orders_info = [
        {"order": 1, "st": 29.5, "et": 34.0, "amt": "+16.000đ", "total": "TỔNG THU: 16.000đ"},
        {"order": 2, "st": 47.0, "et": 51.5, "amt": "+22.000đ", "total": "TỔNG THU: 38.000đ"},
        {"order": 3, "st": 67.5, "et": 72.0, "amt": "+35.000đ", "total": "TỔNG THU: 73.000đ"},
        {"order": 4, "st": 86.5, "et": 91.0, "amt": "+28.000đ", "total": "TỔNG THU: 101.000đ"},
        {"order": 5, "st": 105.5, "et": 110.0, "amt": "+42.000đ", "total": "TỔNG THU: 143.000đ"},
        {"order": 6, "st": 125.0, "et": 129.5, "amt": "+33.000đ", "total": "TỔNG THU: 176.000đ"}
    ]

    for o in orders_info:
        st_s = sec_to_ass_time(o["st"])
        et_s = sec_to_ass_time(o["et"])
        title = f"✓ HOÀN THÀNH ĐƠN #{o['order']}"
        amt = o['amt']
        tot = o['total']
        
        ass_lines.append(f"Dialogue: 2,{st_s},{et_s},CashBadgeHeader,,0,0,0,,{title}")
        ass_lines.append(f"Dialogue: 2,{st_s},{et_s},CashBadgeAmount,,0,0,0,,{amt}")
        ass_lines.append(f"Dialogue: 2,{st_s},{et_s},CashBadgeTotal,,0,0,0,,{tot}")

    # 4. Thẻ Tổng Kết Cuối Ngày 176k
    ass_lines.append("\n; --- TỔNG KẾT CUỐI NGÀY 176K ---")
    st_sum = sec_to_ass_time(128.0)
    et_sum = sec_to_ass_time(total_dur)
    ass_lines.append(f"Dialogue: 2,{st_sum},{et_sum},SummaryBox,,0,0,0,,★ TỔNG THU HÔM NAY: 176.000đ ★\\N(6 ĐƠN XE XANHSM)")

    # 5. Callout CTA
    ass_lines.append("\n; --- CALLOUT TƯƠNG TÁC ---")
    st_cta = sec_to_ass_time(140.0)
    et_cta = sec_to_ass_time(total_dur)
    ass_lines.append(f"Dialogue: 2,{st_cta},{et_cta},CalloutCTA,,0,0,0,,TIM ❤️ VÀ COMMENT GIAO LƯU NHÉ 👍")

    out_file = Path("processed/vlog_xanhsm_176k_master.ass")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("\n".join(ass_lines))
    print(f"[+] Đã tạo file phụ đề ASS: {out_file}")

if __name__ == "__main__":
    generate_ass()
