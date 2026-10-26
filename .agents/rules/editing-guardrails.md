---
trigger: always_on
alwaysApply: true
description: Quy chuẩn sống còn đã train của hệ thống tự động dựng video Antigravity v2.0
globs: ["**/*"]
---

# QUY CHUẨN SỐNG CÒN ĐÃ TRAIN (EDITING GUARDRAILS v2.0)

1. **BƯỚC 0 BẮT BUỘC**: Luôn chạy `$env:PYTHONIOENCODING="utf-8"; python scripts/load_brain.py` trước khi xử lý bất kỳ yêu cầu dựng video nào.
2. **PHỤ ĐỀ**: Bắt buộc dùng font `Oswald-Bold` 100% IN HOA, chữ thường Vàng Chanh `#F0FF00`, từ đang đọc Xanh Cyan `#66FFFF` kèm hiệu ứng Elastic Micro-Pop, cụm 2-4 từ (<= 26 ký tự), giữ đủ 100% từ thoại, đặt tại Safe Zone Y = -0.38 đến -0.40 (`MarginV 550`).
3. **CAPCUT TIMELINE**: Chỉ xuất dự án qua `scripts/capcut_draft_manager.py` (app_id 359289, cc, 9.6.0). Áp dụng `SUB_LEAD = 0.15s` và `GAP = 0.02s`. Đồng bộ `Timelines/<id>/draft_content.json`. Tiêm Keyframes Zoom $1.0 \leftrightarrow 1.15\times$ và J-Cut $0.15\text{s}$.
4. **AUDIO & VISUAL**: Voice chuẩn hóa 2-pass `-14 LUFS` (`-ar 48000`), BGM `0.14 - 0.16` (Ducking), Ambient `0.125`, `amix normalize=0`. Đệm cắt thoại 180ms đầu / 220ms cuối.
5. **PRE-FLIGHT QA TRƯỚC BÀN GIAO**: Chạy `python scripts/brain_preflight_qa.py` kiểm tra 0 điểm chồng lấn sub, -14 LUFS, MarginV 550, độ dài cụm <= 26 ký tự và trích xuất 3 khung hình Visual QA trước khi bàn giao.
