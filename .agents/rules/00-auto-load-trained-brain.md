---
trigger: always_on
alwaysApply: true
description: Quy tắc tối cao - luôn nạp Bộ Não Đã Train (portable_trained_brain) ở mọi phiên chat mới trước khi edit video.
globs: ["**/*"]
---

# LUÔN NẠP BỘ NÃO ĐÃ TRAIN — KHÔNG ĐƯỢC QUÊN

Dự án này là hệ thống AI edit video đã được người dùng huấn luyện. Toàn bộ trí nhớ nằm DUY NHẤT trong `portable_trained_brain/`.
Ưu tiên: `portable_trained_brain/` > `GEMINI.md`/`AGENTS.md` > mọi skill chung (ffmpeg-video-editor, video-editing, remotion...).
Tuyệt đối không dùng gu mặc định của skill chung (chữ trắng, Montserrat, Y=-0.65, BGM -28dB).

## Bước 0 (bắt buộc ở mỗi phiên chat mới, trước khi viết/chạy bất kỳ script dựng video nào)
```powershell
$env:PYTHONIOENCODING="utf-8"; python scripts/load_brain.py
```
Sau đó đọc đầy đủ `portable_trained_brain/learned_editing_style.md` và `portable_trained_brain/training_feedback_history.json`.

## Quy chuẩn cốt lõi đã train
- 1080x1920 9:16, 30fps. DJI quay dọc lưu ngang → `transpose=1`.
- Phụ đề: **Oswald-Bold**, IN HOA, **Vàng chanh #F0FF00**, từ đang đọc **Cyan #66FFFF**, viền đen dày, bóng đen 0.9, Safe Zone **Y=-0.38→-0.40** (ASS Alignment 2, **MarginV 550** — đã đo pixel; MarginV 220 cũ thực tế ra Y≈-0.73 là SAI).
- Dynamic Word Karaoke: cụm 2-4 từ, giữ đủ 100% từ, timestamp từng từ thật từ Whisper (không nội suy theo ký tự). Dùng `scripts/brain_karaoke_ass.py`.
- Hook 0-5s: 2 tầng (Đỏ #FF3333 viền trắng / Vàng #F0FF00 viền đen) ở 1/3 trên + SFX whoosh_fast + ding_highlight, zoom 1.0→1.12.
- Âm thanh: voice -14 LUFS, BGM 0.14-0.16, ambient 0.125. Đệm cắt thoại 180ms/220ms.
- Callout cuối: nửa trên (Alignment 8). Chuyển cảnh mạnh chỉ khi đổi địa điểm.
- CapCut: chỉ qua `scripts/capcut_draft_manager.py`.

## Ghi nhớ bài học (để phiên sau không quên)
Mỗi khi người dùng góp ý/sửa/dạy → chạy ngay:
```powershell
$env:PYTHONIOENCODING="utf-8"; python scripts/brain_record_lesson.py --rule "..." --mistake "..." --project "..."
```
Không lưu trí nhớ ở nơi khác. Thư mục `memory/` cũ đã bị lưu trữ (`_archive/`) vì chứa quy chuẩn lỗi thời.

## Trước khi giao video
Trích 2-3 khung hình và XEM ảnh để xác nhận màu/font/vị trí phụ đề; đối chiếu `do_not_repeat_mistakes`.
