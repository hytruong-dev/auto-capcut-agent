---
name: adaptive-editor-memory
description: Quản lý Bộ Não Di Động (portable_trained_brain), đồng bộ hiệu ứng CapCut Pro, phân tích video mẫu bắt trend và tự học ngược từ thao tác sửa của người dùng.
---

> **⚠️ ƯU TIÊN TRONG DỰ ÁN NÀY:** Skill này chỉ là kiến thức kỹ thuật chung. Mọi quyết định về gu dựng (font, màu, vị trí phụ đề, hook, âm lượng, nhịp cắt) BẮT BUỘC lấy từ portable_trained_brain/learned_editing_style.md và 	raining_feedback_history.json (chạy python scripts/load_brain.py trước). Nếu ví dụ trong skill này mâu thuẫn (chữ trắng, Montserrat/DejaVu, phụ đề sát đáy, BGM -28dB...) thì BỎ QUA ví dụ đó. Phụ đề: dùng scripts/brain_karaoke_ass.py.


# Adaptive Video Editor Memory & Portable Brain Skill

## 1. Quy trình Nạp Trí Nhớ (Memory Initialization)
Luôn đọc `portable_trained_brain/BRAIN_INDEX.md` và `portable_trained_brain/learned_editing_style.md` trước khi xử lý video. Mọi tài nguyên (font, SFX, mẫu hiệu ứng CapCut Pro) phải tham chiếu từ `portable_trained_brain/`.

## 2. Quy trình Đọc Bối Cảnh & Lên Phương Án (Context-Aware Planning)
1. Chạy `video-understand` trên video nguyên liệu trong `raw_footage/` để tạo `processed/transcript.json` (có timestamp từng từ) và trích xuất keyframes vào `processed/keyframes/`.
2. Xem ảnh keyframes + đọc transcript để hiểu cảm xúc, nội dung, lọc bỏ đoạn nói vấp/lặp ý.
3. Đối chiếu với `learned_editing_style.md` và `trend_catalog.json` để lập file kế hoạch `processed/scene_plan.md`.
4. Gọi `capcut-mcp` (`VectCutAPI` / `pyCapCut`) để tạo bản dựng hoàn chỉnh trực tiếp vào thư mục `CapCut Drafts`, đồng thời lưu một bản snapshot `processed/snapshots/ai_initial_draft.json`.

## 3. Quy trình Học Trend Mới & Học Ngược Từ Người Dùng (Continuous Training)
- **Khi người dùng dạy bằng lời nói:** Ghi ngay quy tắc vừa dạy vào mục 4 của `portable_trained_brain/learned_editing_style.md`.
- **Khi người dùng bỏ video mẫu vào `references/`:** Phân tích nhịp cắt, kiểu chữ, vị trí phụ đề, tần suất zoom và lưu thành công thức mới trong `portable_trained_brain/viral_trends_library/trend_catalog.json`.
- **Khi người dùng tự sửa lại trên CapCut Pro:** Chạy `python scripts/diff_capcut_draft.py` để phát hiện các chỉnh sửa của người dùng trên timeline CapCut và tự động cập nhật vào `portable_trained_brain/`.
- **Khi người dùng tải hiệu ứng CapCut Pro mới vào `Template_Trend_Pro`:** Chạy `python scripts/sync_capcut_pro_effects.py` để trích xuất mã ID và sao lưu gói hiệu ứng vào `portable_trained_brain/capcut_pro_vault/`.
