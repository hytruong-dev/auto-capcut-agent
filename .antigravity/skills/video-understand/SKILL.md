---
name: video-understand
description: Đọc hiểu toàn diện bối cảnh video thô. Tự động bóc tách transcript có timestamp từng từ qua Whisper và dùng FFmpeg Scene Detection (gt(scene,0.3)) trích xuất ảnh keyframes tại các điểm đổi cảnh để phân tích nội dung, cảm xúc, khoảng lặng và phát hiện đoạn nói ngập ngừng.
---

> **⚠️ ƯU TIÊN TRONG DỰ ÁN NÀY:** Skill này chỉ là kiến thức kỹ thuật chung. Mọi quyết định về gu dựng (font, màu, vị trí phụ đề, hook, âm lượng, nhịp cắt) BẮT BUỘC lấy từ portable_trained_brain/learned_editing_style.md và 	raining_feedback_history.json (chạy python scripts/load_brain.py trước). Nếu ví dụ trong skill này mâu thuẫn (chữ trắng, Montserrat/DejaVu, phụ đề sát đáy, BGM -28dB...) thì BỎ QUA ví dụ đó. Phụ đề: dùng scripts/brain_karaoke_ass.py.


# Video Understanding & Scene Context Analysis

## Mục tiêu
Biến một file video thô (`raw_footage/input.mp4`) thành 2 nguồn dữ liệu phục vụ dựng phim tự động:
1. `processed/transcript.json`: Toàn bộ lời thoại kèm mốc thời gian chính xác (word-level timestamps) và nhãn phân đoạn.
2. `processed/keyframes/`: Ảnh chụp các thời điểm đổi cảnh hoặc chuyển động để Agent làm Visual QA và đánh giá bối cảnh.

## Quy trình thực hiện
Chạy script:
```bash
python scripts/extract_scenes_and_transcribe.py <duong_dan_video>
```

## Các tiêu chí phân tích kịch bản
1. **Hook (0-5s đầu):** Tìm câu nói ấn tượng nhất, nghịch lý hoặc con số gây sốc để đưa lên đầu.
2. **Lọc ngập ngừng / khoảng lặng:** Phát hiện khoảng lặng > 0.3s hoặc các từ ngập ngừng ("ờ", "à", "ừm", lặp từ) để đưa vào danh sách cắt bỏ (EDL).
3. **Pacing:** Đánh giá tốc độ nói (từ/phút), xác định các đoạn cao trào cần nhịp cắt nhanh hoặc zoom mạnh.
