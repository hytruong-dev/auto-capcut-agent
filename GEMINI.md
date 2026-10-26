# ⚠️ CHỈ THỊ TỐI CAO CHO AI (ĐỌC TRƯỚC KHI LÀM BẤT CỨ VIỆC GÌ)

Dự án này là **hệ thống AI edit video đã được người dùng huấn luyện qua nhiều lần thất bại**.
Mọi kiến thức đã train nằm DUY NHẤT trong thư mục `portable_trained_brain/`.
Bạn KHÔNG được dùng gu mặc định của bạn hay của skill chung chung (font trắng, Montserrat, Y=-0.65...).
Khi có mâu thuẫn: **`portable_trained_brain/` > file này > mọi skill/tài liệu khác**.

## BƯỚC 0 — BẮT BUỘC Ở MỌI PHIÊN CHAT MỚI (trước khi viết bất kỳ script nào)

```powershell
$env:PYTHONIOENCODING="utf-8"; python scripts/load_brain.py
```

Lệnh này in ra toàn bộ quy chuẩn đã train + danh sách lỗi cấm lặp lại + kiểm tra font/SFX/FFmpeg.
Sau đó đọc đầy đủ:
1. `portable_trained_brain/learned_editing_style.md` (gu dựng, phụ đề, hook, âm thanh, CapCut)
2. `portable_trained_brain/training_feedback_history.json` (mục `do_not_repeat_mistakes`)

Trả lời người dùng câu đầu tiên bằng: "Đã nạp bộ não đã train (N quy tắc, M lỗi cấm lặp lại)".

## QUY CHUẨN CỐT LÕI (tóm tắt — chi tiết ở `learned_editing_style.md`)

| Hạng mục | Giá trị ĐÃ TRAIN (bắt buộc) | SAI (cấm) |
|---|---|---|
| Khung hình | 1080x1920 9:16, 30fps; DJI ngang → `transpose=1` | quên xoay, méo hình |
| Font phụ đề | **Oswald-Bold** (`portable_trained_brain/portable_assets/fonts/Oswald-Bold.ttf`), IN HOA | Montserrat, Arial, Be Vietnam |
| Màu phụ đề | **Vàng chanh `#F0FF00`**, từ đang đọc **Cyan `#66FFFF`** | chữ trắng `#FFFFFF` |
| Viền/bóng | viền đen dày (ASS Outline 7 / CapCut 0.08), bóng đen 0.9 | viền mỏng |
| Vị trí phụ đề | Safe Zone **Y = -0.38 → -0.40** (ASS Alignment 2, **MarginV 550** — đã đo pixel; MarginV 220 cũ thực tế ra Y≈-0.73 là SAI) | Y = -0.65, sát đáy |
| Kiểu phụ đề | **Dynamic Word Karaoke**: cụm 2-4 từ, timestamp thật từ Whisper từng từ | nội suy theo độ dài ký tự, bỏ bớt từ |
| Hook 0-5s | 2 tầng: dòng 1 Đỏ `#FF3333` viền trắng, dòng 2 Vàng `#F0FF00` viền đen, 1/3 trên | tiêu đề 1 dòng trắng |
| Âm thanh | Voice -14 LUFS; BGM volume 0.14-0.16; ambient 0.125; SFX whoosh+ding ở hook | BGM -28dB / quá to |
| Cắt thoại | đệm 180ms trước, 220ms sau câu; khoảng lặng > 0.15s phải cắt | cắt cụt âm cuối |
| Nhịp | thay đổi thị giác mỗi 6-10s (jump-cut zoom 1.0↔1.15, B-roll, callout) | cảnh tĩnh dài |
| Chuyển cảnh | chỉ dùng mạnh (Glitch/Whip/Flash) khi đổi địa điểm/chủ đề | chuyển cảnh loè loẹt giữa câu |
| Callout cuối | nửa TRÊN khung hình (Alignment 8, Y≈0.20-0.35) | đặt đáy che phụ đề |
| Cảnh đêm | `eq=brightness=0.06:saturation=1.25:contrast=1.1,unsharp=5:5:0.8` | để tối |
| CapCut | CHỈ qua `scripts/capcut_draft_manager.py` (app_id 359289, app_source `cc`, 9.6.0) | tự sửa meta, placeholder `##_draftpath_` |

## CÔNG CỤ CHUẨN (dùng lại, KHÔNG viết lại từ đầu)

- `scripts/load_brain.py` — nạp & kiểm tra bộ não (Bước 0).
- `scripts/brain_karaoke_ass.py` — sinh phụ đề Dynamic Word Karaoke + Hook 2 tầng đúng chuẩn từ file word-timestamps Whisper.
- `scripts/capcut_draft_manager.py` — tạo/sửa dự án CapCut Desktop 9.6 Pro (không bao giờ tự ghi meta thủ công).
- `scripts/brain_record_lesson.py` — GHI LẠI bài học mới vào bộ não (bắt buộc dùng mỗi khi người dùng góp ý/sửa).
- Mẫu pipeline hoàn chỉnh đã được duyệt: `scripts/build_exact_synced_karaoke.py` + `scripts/render_xanhsm_176k_video.py` (dự án XanhSM 176k).
- Tài nguyên: font/SFX/BGM lấy trong `portable_trained_brain/portable_assets/`.

## QUY TẮC HỌC & GHI NHỚ (để phiên sau không quên)

1. Mỗi khi người dùng chê/sửa/dạy điều mới → NGAY LẬP TỨC chạy:
   ```powershell
   $env:PYTHONIOENCODING="utf-8"; python scripts/brain_record_lesson.py --rule "<quy tắc mới>" --mistake "<lỗi cấm lặp lại>" --project "<tên dự án>"
   ```
2. KHÔNG lưu trí nhớ ở nơi khác (`memory/` đã bị lưu trữ vào `_archive/`, không dùng nữa).
3. Trước khi giao video: tự kiểm tra lại từng dòng trong bảng trên + `do_not_repeat_mistakes`, trích 2-3 khung hình (`ffmpeg -ss <t> -frames:v 1`) và XEM ảnh để xác nhận màu, font, vị trí phụ đề.

## MÔI TRƯỜNG

- Windows PowerShell: luôn `$env:PYTHONIOENCODING="utf-8"` trước khi chạy Python.
- Video thô: `raw_footage/` · Video mẫu trend: `references/` · Đầu ra: `processed/`.
- CapCut drafts: `C:/Users/PC/AppData/Local/CapCut/User Data/Projects/com.lveditor.draft`. Đổi máy → `python scripts/migrate_brain_to_new_pc.py`.
- Người dùng nói tiếng Việt → luôn trả lời tiếng Việt.
