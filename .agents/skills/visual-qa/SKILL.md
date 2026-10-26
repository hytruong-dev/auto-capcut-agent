---
name: visual-qa
description: Kiểm định tự động chất lượng video trước bàn giao (đo âm lượng -14 LUFS, 0 overlap sub, MarginV 550, trích xuất 3 keyframe)
---

# Skill: Visual & Audio Pre-Flight QA

Chạy kiểm định tự hành theo Bước 6 của Master Blueprint v2.0 trước khi bàn giao video cho người dùng.

## 1. Chạy Pre-Flight QA Script
```powershell
$env:PYTHONIOENCODING="utf-8"; python scripts/brain_preflight_qa.py --video processed/FINAL.mp4 --sub processed/video_subtitles.ass
```

## 2. Các tiêu chí kiểm tra tự động:
1. **Âm thanh tích hợp**: `ebur128` đạt `-14.0 LUFS` (sai số cho phép $\pm 0.8\text{ LUFS}$), True Peak $\le -1.0\text{ dBTP}$.
2. **Phụ đề overlap**: 0 điểm chồng lấn giữa các cụm sub liền kề.
3. **Độ dài dòng sub**: Tối đa 26 ký tự/dòng (chống tràn viền ngang 1080px).
4. **Safe Zone**: `MarginV == 550` (tương đương $Y \approx -0.38 \rightarrow -0.40$).
5. **Bảo toàn từ vựng**: Đối chiếu $100\%$ từ của câu thoại gốc có mặt trong phụ đề.

## 3. Trích xuất & Soi 3 Khung Hình Thị Giác:
- **Frame 1 (Hook ~2.5s)**: Tiêu đề Hook 2 tầng Đỏ `#FF3333` viền trắng + Vàng `#F0FF00` viền đen ở 1/3 trên.
- **Frame 2 (Giữa video ~30s)**: Phụ đề `Oswald-Bold` Vàng/Cyan ở $Y \approx -0.38$ + Badge nhận tiền (nếu có).
- **Frame 3 (Outro ~cuối -5s)**: Callout Box ở nửa TRÊN khung hình ($Y \approx 0.20 \rightarrow 0.35$).
