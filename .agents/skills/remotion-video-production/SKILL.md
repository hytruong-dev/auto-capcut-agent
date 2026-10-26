---
name: remotion-video-production
description: Điều phối bố cục và quy chuẩn sản xuất video ngắn chuyên nghiệp (Shorts/Reels/TikTok). Kiểm soát Safe Zones, nhịp dựng Hook 5 giây đầu, nhịp chuyển động và chuẩn hóa QA trước khi xuất bản.
---

> **⚠️ ƯU TIÊN TRONG DỰ ÁN NÀY:** Skill này chỉ là kiến thức kỹ thuật chung. Mọi quyết định về gu dựng (font, màu, vị trí phụ đề, hook, âm lượng, nhịp cắt) BẮT BUỘC lấy từ portable_trained_brain/learned_editing_style.md và 	raining_feedback_history.json (chạy python scripts/load_brain.py trước). Nếu ví dụ trong skill này mâu thuẫn (chữ trắng, Montserrat/DejaVu, phụ đề sát đáy, BGM -28dB...) thì BỎ QUA ví dụ đó. Phụ đề: dùng scripts/brain_karaoke_ass.py.


# Remotion Video Production Guidelines

## 1. Safe Zones (TikTok, Instagram Reels, YouTube Shorts)
- **Top Safe Margin:** Tránh đặt text/logo ở $15\%$ trên cùng màn hình (nơi chứa thanh tìm kiếm, tab Following/For You).
- **Bottom Safe Margin:** Tránh đặt text/phụ đề quan trọng ở $20\%$ dưới cùng màn hình (nơi chứa username, caption, âm thanh).
- **Right Safe Margin:** Chừa $100\text{px}$ bên phải màn hình (khu vực nút Like, Comment, Share, Bookmark).
- **Vị trí vàng đặt phụ đề:** Tọa độ $Y = 65\% - 75\%$ chiều cao màn hình, căn giữa trục $X$.

## 2. Công thức Pacing Video Viral
- **0s - 3s (The Hook):** Hiển thị ngay vấn đề / tiêu đề giật tóm tắt cốt lõi, kèm chuyển động (Zoom in $1.1\times$) + SFX Whoosh/Ding.
- **3s - 15s (The Retain):** Nhịp nói dứt khoát, cắt bỏ toàn bộ khoảng lặng $> 0.2\text{s}$, chèn B-roll hoặc hình minh họa.
- **15s - Kết thúc (Value & CTA):** Giữ nhịp độ ổn định, kết bài gãy gọn, kêu gọi tương tác.

## 3. Checklist QA xuất bản
- [ ] Phụ đề không bị cắt chữ do sai tỉ lệ khung hình.
- [ ] Font chữ hỗ trợ 100% tiếng Việt có dấu.
- [ ] Âm lượng giọng nói đạt chuẩn $-14\text{ LUFS}$.
- [ ] Nhạc nền tự động ducking khi có giọng nói.
