# HỒ SƠ PHONG CÁCH DỰNG VIDEO & TRÍ NHỚ TIẾN HÓA (LEARNED EDITING STYLE)

## 1. Quy chuẩn Nhịp điệu & Cắt thô (Pacing & Cutting Rules)
- **Hook (0s → 5s đầu):** Nhịp cắt nhanh, không để khoảng lặng quá $0.2\text{s}$. Luôn mở đầu bằng hiệu ứng Zoom-in từ tỷ lệ $1.0 \rightarrow 1.12$ kèm hiệu ứng chữ tiêu đề nổi bật và âm thanh `whoosh_fast` + `ding_highlight`.
- **Khoảng đệm cắt thoại (Audio Padding):** Giữ khoảng đệm $180\text{ ms}$ trước từ đầu tiên và $220\text{ ms}$ sau từ cuối cùng của mỗi câu để giọng nói tự nhiên, không bị cụt âm cuối tiếng Việt.
- **Mật độ thay đổi thị giác (Visual Change Rate):** Cứ mỗi $6\text{s} \rightarrow 10\text{s}$ phải có ít nhất $1$ thay đổi thị giác (Đổi góc khung hình Jump-cut Zoom $1.15\times$, chèn B-roll, hiện Callout Text hoặc Sticker/Meme).
- **Tốc độ thoại & Độ nén (Voice Pacing):** Tốc độ thoại chuẩn 185 – 195 WPM (khoảng $1.15\times - 1.25\times$). Bất kỳ khoảng lặng nào $> 0.15\text{s}$ giữa các câu cần được tinh gọn.

## 2. Quy chuẩn Phụ đề & Hiệu ứng Chữ (Subtitles & Typography)
- **Vị trí an toàn (Safe Zone):** Đặt phụ đề tại trục dọc $Y = -0.38$ đến $-0.40$ (khoảng $1/3$ dưới khung hình, ngang ngực/bụng nhân vật), tránh vùng giao diện mô tả và nút tương tác của TikTok/Reels/Shorts.
- **Định dạng chữ chính:** 100% IN HOA (`TT` - UPPERCASE), sử dụng phông chữ **`Oswald-Bold`** (lưu tại `portable_trained_brain/portable_assets/fonts/Oswald-Bold.ttf`, CapCut Resource ID: `7182504807289065985`), cỡ chữ 15 (trong CapCut) hoặc 64-68 (trong FFmpeg $1080\times 1920$), màu sắc Vàng chanh `#F0FF00` (`[0.941, 1.0, 0.0]`), viền đen dày (`border_color = #000000`, `border_width = 0.08`), đổ bóng đen (`shadow_color = #000000`, `shadow_alpha = 0.9`), căn giữa (Center).
- **Nhấn mạnh từ khóa (Keyword Highlight):** Các từ khóa mang tính cảm xúc, con số hoặc động từ mạnh tự động tô màu Vàng sáng `#FFFF00` hoặc Xanh Neon `#00FF88` và tăng cỡ chữ hoặc viền đậm hơn.
- **Tiêu đề Hook 2 tầng 3D (Dual-Layer Hook Title):**
  - Đặt tại $1/3$ trên màn hình ($Y \approx 0.43 \rightarrow 0.55$), dùng font `Oswald-Bold`.
  - **Dòng 1:** Chữ in hoa màu Đỏ Cam `#FF3333` viền trắng dày + đổ bóng đen ("MỘT CA ĐÊM" / "THỬ THÁCH 1 NGÀY").
  - **Dòng 2:** Chữ in hoa màu Vàng Tươi `#F0FF00` viền đen dày + bóng đổ ("CHẠY XANHSM SÀI GÒN" / "FULL TIME 11 TIẾNG...").
- **Hộp tương tác cuối video (Callout Interaction Box):**
  - Đặt tại $Y \approx 0.20 \rightarrow 0.35$ (Alignment 8 Top-Center, nửa trên khung hình), hiển thị từ giây 68 đến 82: *"TIM ❤️ NẾU BẠN CŨNG THÍCH CHẠY ĐÊM 🌙"* (Màu xanh ngọc viền đen), tuyệt đối không để ở đáy màn hình tránh che lấp phụ đề.

## 3. Quy chuẩn Chuyển cảnh & Âm thanh (Transitions & Audio)
- **Chuẩn hóa âm lượng:** Giọng nói chính (Voiceover/A-roll) chuẩn hóa ở mức $-14\text{ LUFS}$. Nhạc nền (BGM) tự động hạ xuống $-16\text{ dB}$ đến $-18\text{ dB}$ (hệ số `volume = 0.14 -> 0.16`) khi có người nói. Âm thanh môi trường gốc (ambient) hạ xuống `volume = 0.125` (-18dB).
- **Chuyển cảnh:** Chỉ dùng chuyển cảnh mạnh (Glitch, Whip Pan, Flash lấy từ `capcut-pro-effects.json`) khi đổi chủ đề hoặc chuyển địa điểm. Giữa các câu trong cùng một ý dùng Jump-cut kết hợp thay đổi tỷ lệ Scale ($1.0 \leftrightarrow 1.15$) để che vết cắt.

## 4. Quy tắc Kỹ thuật Khung hình & Màu sắc (Footage Processing)
- **Xử lý góc quay DJI / Camera hành trình:** Camera gắn dọc lưu file ngang 16:9 ($2688\times 1512$) → Bắt buộc dùng `transpose=1` (xoay 90° theo chiều kim đồng hồ) + scale $1080\times 1920$ để đạt tỷ lệ 9:16 dọc hoàn hảo không méo hình.
- **Color Grading cảnh đêm:** Thước phim quay đêm cần tăng nhẹ độ sáng và bão hòa màu đèn phố: `eq=brightness=0.06:saturation=1.25:contrast=1.1,unsharp=5:5:0.8`.
- **Môi trường Windows PowerShell:** Mọi script Python xử lý tiếng Việt hoặc gTTS bắt buộc set `$env:PYTHONIOENCODING="utf-8"`.

## 5. Các Quy Tắc Đã Được Người Dùng Train Bổ Sung (Auto-Appended Rules)
- **Quy chuẩn Font & Phụ đề CapCut (Cập nhật 22/10/2026):** Toàn bộ phụ đề tự động và phụ đề CapCut bắt buộc dùng Font **`Oswald-Bold`**, cỡ chữ **15**, kiểu viết hoa **`TT`**, màu chữ **Vàng chanh `#F0FF00`**, viền đen dày nét nét **0.08**, bóng mờ đen **0.9**, căn giữa (`Center`). Chuẩn hóa preset thứ 5 ở hàng 1 trong CapCut.
- **Quy chuẩn Đường Dẫn & Xuất Bản CapCut Desktop (Cập nhật 23/10/2026 - Bắt buộc vĩnh viễn):**
  - **Triệt tiêu Lỗi 'Không thể dùng dự án do đường dẫn không đúng' (`draft_unconventional_path_cannot_open`):**
    - **Nguyên nhân gốc (Reverse Engineered từ `VECreator.dll` -> `DraftLoadVerifier::verify_draft`):**
      1. CapCut 9.6+ có module `DraftLoadVerifier::check_app_support` kiểm tra trường `platform` trong `draft_content.json`. Nếu `app_id` là `359284` (của app Jianying TQ), `app_source` là `capcut` (thay vì `cc`), `app_version` là `5.0.0` (thay vì `9.6.0`), hoặc thiếu `device_id` và `mac_address` thực tế của máy, CapCut sẽ gán cờ `from_unusual_path` / `draft_from_jianyingmac` và bung popup lỗi "Không dùng được dự án hiện tại do đường dẫn của dự án không đúng".
      2. Đường dẫn trong `root_meta_info.json` và `draft_meta_info.json` (`draft_fold_path`, `draft_root_path`, `draft_json_file`, `draft_cover`) BẮT BUỘC dùng định dạng chuẩn Windows backslashes (`C:\Users\PC\...`), không dùng dấu `/` để tránh lỗi so khớp chuỗi `currentCustomDraftPath` trong C++.
      3. Khi AutoBackup của CapCut Pro chạy ngầm, nếu thấy dự án mới có `tm_draft_cloud_entry_id > 0`, nó sẽ ghi bản ghi vào `cloud_draft_upload_path_cfg.ini` với `upload_path=` rỗng, khiến CapCut hiểu nhầm đây là dự án đám mây bị đứt link. Do đó BẮT BUỘC set toàn bộ `tm_draft_cloud_entry_id: -1`, `tm_draft_cloud_space_id: -1`, `tm_draft_cloud_user_id: -1` và tự động dọn sạch các entry rác trong `cloud_draft_upload_path_cfg.ini` và `AutoBackupStatus.json`.
  - **Triệt tiêu Placeholder:** Tuyệt đối KHÔNG bao giờ dùng chuỗi placeholder dạng `##_draftpath_placeholder_...##` trong `draft_content.json`. Mọi đường dẫn file media (`materials.videos`, `materials.audios`, `materials.images`) BẮT BUỘC là đường dẫn tuyệt đối chuẩn xác với dấu gạch chéo xuôi (`/`), ví dụ: `C:/Users/PC/AppData/Local/CapCut/User Data/Projects/com.lveditor.draft/<PROJECT_NAME>/assets/...`.
  - **Dọn dẹp mảng rác:** `placeholder_infos`, `placeholder_materials`, `placeholders` trong `materials` phải để mảng rỗng `[]`.
  - **Quy chuẩn `draft_meta_info.json`:**
    - `draft_fold_path` bắt buộc là đường dẫn tuyệt đối đến thư mục dự án (tuyệt đối KHÔNG được để rỗng `""`).
    - `draft_root_path` bắt buộc là đường dẫn đến thư mục cha `com.lveditor.draft` (KHÔNG được trỏ vào thư mục con của dự án).
    - Tắt cờ cloud sync để tránh CapCut tự động rename thành `(1)`: `cloud_draft_sync: False`, `cloud_draft_cover: False`, `tm_draft_cloud_entry_id: -1`, `tm_draft_cloud_space_id: -1`, `tm_draft_cloud_user_id: -1`.
  - **Đăng ký `root_meta_info.json` & `draftLayoutConfig.ini`:**
    - Luôn cập nhật dự án vào đầu danh sách `all_draft_store` của `root_meta_info.json` với `streaming_edit_draft_ready: True`.
    - Luôn ghi ID dự án vào `draftLayoutConfig.ini` dưới dạng `<DRAFT_ID>=0`.
  - **Engine Tập Trung:** Mọi script tạo mới hoặc sửa dự án CapCut BẮT BUỘC gọi qua `scripts/capcut_draft_manager.py` (`deploy_capcut_project` hoặc `fix_and_normalize_existing_draft`). Tuyệt đối không tự viết code thao tác file meta thủ công rải rác.
- **Quy chuẩn Triệt tiêu Lỗi Tự Đóng/Thoát CapCut Sau Khi Mở Dự Án (CapCut 9.6 Pro Auto-Close Fix - Cập nhật 23/10/2026):**
  - **Hiện tượng:** Người dùng click vào dự án, giao diện editor mở lên hiển thị timeline nhưng ngay sau đó CapCut tự động đóng/thoát hẳn.
  - **4 Nguyên nhân kỹ thuật gốc rễ:**
    1. **Lệch cấu trúc Đa Dòng Thời Gian (`Timelines/<timeline_id>/draft_content.json`):** CapCut 9.6 Pro quản lý dự án theo kiến trúc multi-timeline. Trang chủ chỉ đọc root `draft_content.json`, nhưng khi click vào dự án để vào Editor, trình biên tập sẽ đọc timeline active từ `Timelines/<timeline_id>/draft_content.json`. Nếu file này còn chứa platform cũ (`app_id: 359284`, `app_version: 5.0.0`, `new_version: 164.0.0`, thiếu `mac_address`/`device_id`), `DraftLoadVerifier` bên trong editor player sẽ kích hoạt cơ chế tự thoát an toàn (graceful termination).
    2. **Thiếu file bố cục Qt Docking (`timeline_layout.json`):** Giao diện CapCut Desktop 9.6 dựa trên Qt QML docking layout. Khi mở editor, nếu thiếu `timeline_layout.json` (chứa `timelineIds` khớp với ID timeline đang mở), bộ điều phối cửa sổ của Qt gặp lỗi ngoại lệ phân luồng và đóng cửa sổ editor.
    3. **Không khớp cờ Render Index & Color Space:** Dự án tạo ra phải có `render_index_track_mode_on: True` và `color_space: -1` để đồng nhất với pipeline render timeline của CapCut 9.6 PC bản địa.
    4. **File khóa tồn dư (`.locked`) & Tiến trình mồ côi (`ParfaitServer\\lock`):** Các lần thoát trước để lại file `.locked` trong thư mục dự án hoặc tiến trình CEF/ParfaitServer ngầm giữ file khóa tại `C:\Users\PC\AppData\Local\CapCut\User Data\ParfaitServer\lock\359289\*`. Khi mở dự án, cơ chế Single-Instance Guard kiểm tra thấy xung đột và tự đóng app.
  - **Giải pháp chuẩn hóa vĩnh viễn (Đã tích hợp trong `scripts/capcut_draft_manager.py`):**
    - Luôn sao chép và đồng bộ 100% `draft_content.json` từ Root vào thư mục `Timelines/<timeline_id>/draft_content.json`.
    - Tự động sinh `timeline_layout.json` chuẩn trỏ đúng ID timeline.
    - Tự động sinh `Timelines/project.json`, `draft_agency_config.json`, `draft_biz_config.json`, `performance_opt_info.json`, `attachment_pc_common.json` và `Timelines/<guid>/attachment_editing.json`.
    - Tự động quét sạch mọi file `.locked` và thư mục rác `{uuid}` trong toàn bộ thư mục dự án.
    - Hàm `clean_cache_locks()` tự động dọn sạch thư mục `ParfaitServer\lock`.
- **[Train 23/10/2026 - Hệ thống Bộ Não (sửa lỗi quên trí nhớ)]** Phụ đề ASS 1080x1920 Alignment 2: dùng MarginV 550 để tâm chữ nằm đúng Safe Zone Y≈-0.38 (đã đo pixel). MarginV 220 trong các script cũ thực tế ra Y≈-0.73 (quá thấp). Sinh phụ đề mới bằng scripts/brain_karaoke_ass.py.
- **[Train 23/10/2026 - Vlog_XanhSM_1Ngay_176k_Long]** CapCut draft: font.path trong styles[] của materials.texts và font_path PHẢI là đường dẫn TUYỆT ĐỐI tồn tại (C:/Users/PC/AppData/Local/CapCut/User Data/Cache/effect/7182504807289065985/0a5333de6f4d592cb2d2390d68b31efb/Oswald-Bold.ttf). capcut_draft_manager.sanitize_font_paths tự chuẩn hóa; validate_project kiểm tra.
- **[Train 23/10/2026 - Vlog_XanhSM_1Ngay_176k_Long]** CapCut 9.6: moi material text phai co type='text', fonts=[{resource_id,path,title...}], font_title ten font, va styles[].range=[0,len UTF-16]. sanitize_font_paths() trong capcut_draft_manager.py tu dong chuan hoa. Khi nghi crash: bisect video/audio/text bang TEST_A/B/C.
- **[Train 23/10/2026 - Vlog_XanhSM_1Ngay_176k_Long]** Phu de karaoke: cuoi moi cum phai bi cat tai (start cum ke tiep - 20ms); khong dung +0.1s dem cung. Sau khi deploy phai kiem tra 0 overlap giua cac segment sub.
- **[Train 23/10/2026 - Vlog_XanhSM_1Ngay_176k_Long]** Sub CapCut phai hien SOM hon voice 0.15s (SUB_LEAD trong deploy_capcut_176k_long.py). Nguoi dung do thuc te sub tre 0.1-0.2s so voi voice.
- **[Train 26/10/2026 - Master_Blueprint_v2.0]** Master Blueprint v2.0: Pre-flight QA tu dong (brain_preflight_qa.py), sub Elastic Micro-Pop <=26 ky tu, khoa ar 48000 am thanh, CapCut Keyframes Zoom va J-Cut 0.15s
- **[Train 26/10/2026 - vlog_demo]** CapCut 9.6 Pro Multi-Timeline: Tat ca cac file root_meta_info, draft_meta_info, draft_content (id), Timelines/<guid>, project.json (id, main_timeline_id) va timeline_layout.json (timelineIds) BAT BUOC dong nhat 100% ID timeline. Luon copy draft_cover.jpg va khai bao draft_timeline_materials_size > 0.
