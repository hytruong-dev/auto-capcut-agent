# 🎬 Auto CapCut Agent & Portable Trained Brain

> **Hệ thống AI Dựng Video Tự Động & Bộ Não Biên Tập Tiến Hóa (Chuẩn CapCut Desktop Pro 9.6+ & FFmpeg Pipeline)**

Dự án này là bộ khung tự động hóa dựng video ngắn (TikTok/Reels/Shorts 9:16) bằng **Google Antigravity / Cursor AI Agent**, kết hợp cùng **Bộ Não Di Động (`portable_trained_brain/`)** đã được huấn luyện qua hàng chục phiên thất bại để đưa ra quy chuẩn thẩm mỹ và kỹ thuật hoàn hảo.

---

## 🚀 Hướng Dẫn Clone & Chạy Trên Máy Mới (Cross-Machine Setup)

Khi bạn clone repo này về bất kỳ máy tính Windows mới nào, hệ thống đã được thiết kế **100% Portable (Tự thích ứng)** để tái tạo chính xác video như trên máy hiện tại mà **không bị mất trí nhớ hay lỗi crash CapCut**.

### 1. Yêu cầu hệ thống
- **Hệ điều hành:** Windows 10/11 64-bit
- **Python:** 3.10 hoặc cao hơn
- **FFmpeg & FFprobe:** Đã thêm vào biến môi trường `PATH` (cài nhanh qua PowerShell: `winget install Gyan.FFmpeg`)
- **CapCut Desktop:** Khuyến nghị bản 9.6 trở lên

### 2. Cài đặt môi trường
Mở PowerShell tại thư mục dự án vừa clone:
```powershell
# 1. Cài đặt thư viện Python
pip install -r requirements.txt

# 2. Khởi chạy đồng bộ Bộ Não Di Động sang máy tính mới (1 chạm)
$env:PYTHONIOENCODING="utf-8"; python scripts/migrate_brain_to_new_pc.py
```

### 3. Cơ chế Tự Thích Ứng Di Động (Zero-Config Portability)
Khi chạy script đồng bộ (`migrate_brain_to_new_pc.py`), hệ thống tự động:
1. **Nhận diện User & Đường Dẫn CapCut:** Tự động định vị thư mục `%LOCALAPPDATA%/CapCut/User Data/Projects/com.lveditor.draft` của người dùng máy mới.
2. **Tự Động Nạp Font Oswald-Bold:** Sao chép trực tiếp file font `Oswald-Bold.ttf` từ kho tài nguyên di động vào thư mục cache hiệu ứng của CapCut (`Cache/effect/7182504807289065985/...`), đảm bảo CapCut Desktop 9.6 mở lên không bị văng.
3. **Tự Động Nhận Diện Hardware ID:** Tự quét `mac_address` và `device_id` phần cứng của máy mới để vượt qua bộ kiểm tra `DraftLoadVerifier::check_device_support` của CapCut.
4. **Đồng Bộ MCP Config:** Cập nhật lại đường dẫn tuyệt đối trong `mcp_config.json` theo thư mục clone của máy mới.
5. **Cơ Chế Tự Kích Hoạt (Self-Healing):** Ngay cả khi quên chạy bước 2, ở mọi phiên làm việc mới khi AI chạy Bước 0 (`python scripts/load_brain.py`), hệ thống sẽ phát hiện máy mới và **tự động chạy đồng bộ ngầm**!

---

## 🧠 Bộ Não Di Động (`portable_trained_brain/`)

Toàn bộ quy chuẩn thẩm mỹ và kinh nghiệm huấn luyện được bảo lưu độc lập:
- `learned_editing_style.md`: Bản quy chuẩn gu dựng, màu sắc, vị trí Safe Zone, âm lượng, nhịp cắt.
- `training_feedback_history.json`: Lịch sử các phiên train và danh sách **19 lỗi cấm lặp lại**.
- `portable_assets/`: Chứa sẵn toàn bộ Font chữ (`Oswald-Bold.ttf`, `arialbd.ttf`), hiệu ứng âm thanh SFX (`whoosh_fast`, `ding_highlight`, `cash_register`, `ting_money`, `pop_bubble`, `riser_tension`) và nhạc nền BGM LoFi loop.
- `capcut_pro_vault/`: Chứa template dự án mẫu `Template_Trend_Pro_Backup`.

---

## 🎯 Quy Chuẩn Dựng Phim Bắt Buộc (Master Blueprint v2.0)

| Hạng mục | Quy chuẩn ĐÃ TRAIN (Bắt buộc $100\%$) | Lỗi cấm lặp lại |
|---|---|---|
| **Khung hình** | $1080\times 1920$ dọc ($9:16$), 30fps. DJI quay dọc lưu ngang $\rightarrow$ `transpose=1`. | Quên xoay, méo tỷ lệ hình ảnh. |
| **Font phụ đề** | **Oswald-Bold**, $100\%$ IN HOA (`TT`), tối đa **26 ký tự/dòng**. | Dùng Arial, Montserrat, chữ thường xen kẽ. |
| **Màu sắc chữ** | Nền chữ Vàng Chanh `#F0FF00`, từ đang đọc sáng Cyan `#66FFFF` (Elastic Micro-Pop). | Dùng chữ trắng đơn điệu, không bắt mắt. |
| **Vị trí phụ đề** | Safe Zone **$Y = -0.38 \rightarrow -0.40$** (ASS Alignment 2, `MarginV 550`). | Đặt $Y=-0.65$ sát đáy bị giao diện TikTok che. |
| **Độ dài cụm từ** | **Dynamic Word Karaoke (2 - 4 từ/cụm)**, chia theo word-timestamps thật từ Whisper. | Nội suy theo số chữ, làm mất chữ gốc. |
| **Hook 0 - 5s** | Tiêu đề 2 tầng 3D: Dòng 1 Đỏ `#FF3333` viền trắng, Dòng 2 Vàng `#F0FF00` viền đen. | Tiêu đề 1 dòng nhạt nhòa, không giữ chân xem. |
| **Âm thanh** | Voice 2-Pass Loudnorm **$-14\text{ LUFS}$**, BGM Ducking $0.14 - 0.16$, SFX hook. | BGM quá to lấn át giọng nói hoặc quá bé. |
| **Cắt thoại** | Đệm $180\text{ms}$ trước câu và $220\text{ms}$ sau câu; cắt khoảng lặng $> 0.15\text{s}$. | Cắt cụt âm cuối tiếng Việt. |
| **CapCut Draft** | Tạo qua `scripts/capcut_draft_manager.py` (Multi-Timeline `359289`, `cc`, `9.6.0`). | Ghi file meta thủ công, thiếu thumbnail cover. |

---

## 🛠️ Bộ Công Cụ Tiêu Chuẩn (`scripts/`)

- `scripts/load_brain.py` — **Bắt buộc ở Bước 0**: Nạp toàn bộ quy chuẩn, in 19 điều cấm, kiểm tra môi trường và tự động đồng bộ máy mới.
- `scripts/migrate_brain_to_new_pc.py` — Đồng bộ hóa dự án, nạp font cache CapCut và cấu hình MCP sang máy tính mới.
- `scripts/brain_karaoke_ass.py` — Tạo phụ đề Dynamic Word Karaoke + Elastic Micro-Pop + Hook 2 tầng từ Whisper JSON.
- `scripts/capcut_draft_manager.py` — Engine tạo và chuẩn hóa dự án CapCut Pro 9.6 Desktop đa dòng thời gian (Multi-Timeline).
- `scripts/brain_preflight_qa.py` — Công cụ Pre-flight QA tự động kiểm định 6 bước (âm lượng LUFS, độ dài dòng, visual change rate, tràn phụ đề).
- `scripts/brain_record_lesson.py` — Ghi nhận bài học và lỗi cấm mới vào Bộ Não Di Động khi có phản hồi người dùng.

---

## 💡 Cách Ra Lệnh Cho AI Edit Video

Khi bắt đầu một phiên chat mới với Antigravity / Cursor trên bất kỳ máy nào:
1. Bỏ video thô vào thư mục `raw_footage/`.
2. Ra lệnh:
   > *"Đã nạp bộ não đã train. Hãy phân tích video trong `raw_footage/`, dựng theo Master Blueprint v2.0, tạo dự án CapCut và xuất video hoàn thiện."*
3. AI sẽ tự động kích hoạt pipeline, kiểm tra QA tự hành và thông báo khi hoàn thành. Bạn chỉ cần mở CapCut Desktop lên để xem ngay timeline hoàn chỉnh!
