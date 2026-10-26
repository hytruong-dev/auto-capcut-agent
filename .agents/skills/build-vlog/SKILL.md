---
name: build-vlog
description: Thực thi trọn gói Quy trình 6 bước SOP dựng video từ raw_footage/ ra CapCut Draft & processed/FINAL.mp4
---

# Skill: Build Vlog (SOP 6 Bước Chuẩn v2.0)

Khi người dùng yêu cầu dựng video mới hoặc chạy quy trình sản xuất video hoàn chỉnh:

## Bước 1: Khởi Động & Nạp Bộ Não
```powershell
$env:PYTHONIOENCODING="utf-8"; python scripts/load_brain.py
```
Xác nhận nạp đầy đủ quy chuẩn và danh sách lỗi cấm lặp lại.

## Bước 2: Bóc Tách Âm Vị & Phân Cảnh Ngữ Nghĩa
- Sử dụng Whisper/WhisperX với `word_timestamps=True` và `initial_prompt`.
- Chạy hàm loại bỏ ảo giác lặp câu (Whisper Hallucination) để tạo `cleaned_words.json`.
- Cắt thoại: đệm 180ms trước câu, 220ms sau câu, cắt khoảng lặng > 0.15s.
- Lập kế hoạch phân cảnh `processed/scene_plan.md` đổi thị giác mỗi 6-10s.

## Bước 3: Sinh Phụ Đề Karaoke Micro-Pop & Hook
```powershell
$env:PYTHONIOENCODING="utf-8"; python scripts/brain_karaoke_ass.py --words processed/cleaned_words.json --out processed/video_subtitles.ass --hook1 "<DÒNG 1>" --hook2 "<DÒNG 2>" --marginv 550
```
- Oswald-Bold IN HOA, cụm 2-4 từ (<= 26 ký tự), Vàng #F0FF00 nền, Cyan #66FFFF active + Elastic Micro-Pop.
- Safe Zone Y = -0.38 đến -0.40 (MarginV 550).

## Bước 4: Triển Khai CapCut Pro Draft
- Gọi qua `scripts/capcut_draft_manager.py` (`deploy_capcut_project`).
- Áp dụng `SUB_LEAD = 0.15s` và `GAP = 0.02s`.
- Đồng bộ `Timelines/<timeline_id>/draft_content.json` và `timeline_layout.json`.
- Tiêm Keyframes Zoom $1.0 \leftrightarrow 1.15\times$ và J-Cut $0.15\text{s}$.

## Bước 5: Render FFmpeg Master Audio & Video
- Voiceover chuẩn hóa 2-Pass Linear Loudnorm -14 LUFS (`-ar 48000`).
- BGM Ducking 0.14 - 0.16 khi có thoại; Sidechain nâng lên 0.30 khi nghỉ thoại > 0.8s.
- Ambient 0.125 lọc gió xe máy (`afftdn`).
- Trộn 4 tầng âm thanh với `amix=inputs=4:normalize=0`.
- Xoay DJI `transpose=1` (nếu cần), Night Tone Curve, ép phụ đề ASS.

## Bước 6: Kiểm Định Tự Hành (Pre-Flight QA)
```powershell
$env:PYTHONIOENCODING="utf-8"; python scripts/brain_preflight_qa.py --video processed/FINAL.mp4 --sub processed/video_subtitles.ass
```
Trích xuất 3 khung hình QA (Hook, Sub, Outro) và xác nhận đạt chuẩn 100% trước khi bàn giao.
