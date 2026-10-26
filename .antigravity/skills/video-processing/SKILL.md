---
name: video-processing
description: Xử lý thị giác máy tính với OpenCV. Tự động nhận diện khuôn mặt/chủ thể chuyển động để Auto-Reframe (chuyển video 16:9 sang 9:16 không bị mất mặt người) và thực hiện Visual QA kiểm tra bố cục video sau dựng.
---

> **⚠️ ƯU TIÊN TRONG DỰ ÁN NÀY:** Skill này chỉ là kiến thức kỹ thuật chung. Mọi quyết định về gu dựng (font, màu, vị trí phụ đề, hook, âm lượng, nhịp cắt) BẮT BUỘC lấy từ portable_trained_brain/learned_editing_style.md và 	raining_feedback_history.json (chạy python scripts/load_brain.py trước). Nếu ví dụ trong skill này mâu thuẫn (chữ trắng, Montserrat/DejaVu, phụ đề sát đáy, BGM -28dB...) thì BỎ QUA ví dụ đó. Phụ đề: dùng scripts/brain_karaoke_ass.py.


# Video Processing & Computer Vision QA

## Mục tiêu
1. **Auto-Reframe (16:9 -> 9:16):** Tự động theo dõi tọa độ khuôn mặt người nói (Face Detection / Haar Cascade / DNN) để xác định vị trí crop $X$ tối ưu trên từng phân cảnh, tránh trường hợp mặt người bị che hoặc lệch ra khỏi khung hình dọc.
2. **Visual QA:** Chụp các frame mẫu tại các điểm chèn text, chuyển cảnh, zoom keyframe để kiểm tra xem có bị tràn Safe Zone hoặc che mặt nhân vật không.

## Quy trình thực hiện
Chạy script:
```bash
python scripts/auto_reframe_and_qa.py <duong_dan_video>
```
