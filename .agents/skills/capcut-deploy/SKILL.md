---
name: capcut-deploy
description: Đóng gói, chuẩn hóa schema text/media, tiêm keyframe và triển khai dự án CapCut Pro 9.6 Desktop không lỗi
---

# Skill: CapCut Deploy (CapCut Pro 9.6+ Draft Engine)

Dùng khi cần tạo mới, xuất bản hoặc sửa một dự án CapCut Desktop 9.6 Pro.

## Nguyên tắc cốt lõi:
1. **Duy nhất qua engine trung tâm**: Luôn gọi qua `scripts/capcut_draft_manager.py`.
2. **Platform chuẩn C++**: `app_id: 359289`, `app_source: 'cc'`, `app_version: '9.6.0'`.
3. **Triệt tiêu Placeholder**: 100% đường dẫn media là tuyệt đối với dấu gạch chéo xuôi `/`. Không bao giờ để `##_draftpath_##`.
4. **Chuẩn hóa Text Schema**:
   - `type: "text"` (CẤM `"none"`).
   - `font_path` tuyệt đối trỏ tới `Oswald-Bold.ttf`.
   - `styles[].range`: `[0, UTF-16 length]`.
   - Mảng `fonts` chứa 1 object font hợp lệ.
5. **Timing Subtitle**:
   - `SUB_LEAD = 0.15s` (bù trễ render của CapCut).
   - `GAP = 0.02s` (chống chồng lấn làm tách 2 track).
6. **Đa dòng thời gian (Multi-Timeline)**:
   - Luôn đồng bộ `draft_content.json` vào `Timelines/<timeline_id>/draft_content.json`.
   - Tạo `timeline_layout.json` khớp ID.
   - Quét dọn file `.locked` và cache locks `ParfaitServer\lock`.

## Lệnh gọi kiểm tra dự án:
```powershell
$env:PYTHONIOENCODING="utf-8"; python -c "from scripts.capcut_draft_manager import validate_project; validate_project('<TÊN_PROJECT>')"
```
