# HƯỚNG DẪN NHANH VẬN HÀNH HỆ THỐNG AI VIDEO EDITOR & BỘ NÃO DI ĐỘNG

Chào mừng bạn đến với hệ thống tự động edit video kết hợp giữa **CapCut Pro Automation (VectCutAPI + pyCapCut + Windows-MCP)**, **FFmpeg + Whisper** và **Bộ Não Di Động (`portable_trained_brain/`)**!

---

## 1. Cấu trúc thư mục vận hành
- `raw_footage/`: Thả video quay thô của bạn vào đây (ví dụ: các clip camera hành trình, POV xe máy, vlog...).
- `references/`: Bỏ video mẫu bạn thấy đang thịnh hành để AI phân tích và học nhịp dựng.
- `portable_trained_brain/`: **THƯ MỤC VÀNG** lưu 100% trí nhớ, gu thẩm mỹ, kho hiệu ứng CapCut Pro và tài nguyên. Khi đổi máy tính chỉ cần mang thư mục này theo.
  - `BRAIN_INDEX.md`: Bản đồ trung tâm nạp não.
  - `learned_editing_style.md`: Toàn bộ quy tắc nhịp cắt, tiêu đề Hook 2 tầng, màu sắc, âm thanh.
  - `training_feedback_history.json`: Lịch sử các lần sửa và điều cấm lặp lại.
  - `capcut_pro_vault/`: Kho lưu trữ mã ID hiệu ứng Pro và bản sao lưu project mẫu `Template_Trend_Pro_Backup`.
  - `viral_trends_library/`: Thư viện công thức trend video viral.
  - `portable_assets/`: Font chữ tiếng Việt, nhạc nền BGM, và bộ âm thanh SFX.
- `processed/`: Nơi xuất transcript phụ đề (`transcript.json`), ảnh keyframes đổi cảnh và video hoàn chỉnh.
- `tools/VectCutAPI/`: MCP Server can thiệp trực tiếp ruột `draft_content.json` của CapCut.

---

## 2. Quy trình 3 bước dựng video tự động
1. **Bước 1:** Bỏ video thô vào `raw_footage/`.
2. **Bước 2:** Nhắn cho Antigravity:
   > *"Hãy phân tích video trong `raw_footage/`, lên Scene Plan và tạo project CapCut mới cho tôi."*
   - AI sẽ tự động bóc tách transcript qua Whisper, lọc khoảng lặng, tạo keyframe zoom, gắn hiệu ứng chữ Hook 2 tầng, phụ đề dynamic chữ vàng, nhạc nền LoFi và SFX.
3. **Bước 3:** Mở CapCut Desktop lên, project dựng sẵn đã nằm ngay trên máy của bạn với 4 track riêng biệt!

---

## 3. Cách nạp thêm hiệu ứng CapCut Pro mới
1. Mở CapCut Desktop -> Mở project `Template_Trend_Pro`.
2. Kéo bất kỳ hiệu ứng chữ, chuyển cảnh, sticker Pro mới nào từ kho Cloud vào timeline.
3. Nhắn cho AI hoặc chạy:
   ```bash
   python scripts/sync_capcut_pro_effects.py
   ```
   Toàn bộ mã ID hiệu ứng Pro sẽ tự động được quét và lưu vào `portable_trained_brain/capcut_pro_vault/` để dùng cho mọi video sau này!

---

## 4. Chuyển sang máy tính mới 1 chạm (Không cần train lại)
Khi đổi sang máy tính mới:
1. Copy dự án hoặc thư mục `portable_trained_brain/` sang máy mới.
2. Chạy đúng 1 lệnh:
   ```bash
   python scripts/migrate_brain_to_new_pc.py
   ```
   Hệ thống sẽ tự nhận diện User mới, khôi phục project mẫu vào CapCut Pro máy mới và cập nhật toàn bộ đường dẫn!
