---
name: record-lesson
description: Tự học và ghi nhớ bài học mới vào Bộ Não Di Động khi người dùng sửa hoặc dạy quy tắc mới
---

# Skill: Record Lesson to Brain

Mỗi khi người dùng chê, sửa hoặc dạy một quy chuẩn mới:
**BẮT BUỘC NGAY LẬP TỨC GHI VÀO BỘ NÃO DI ĐỘNG**.

## Lệnh thực thi:
```powershell
$env:PYTHONIOENCODING="utf-8"; python scripts/brain_record_lesson.py --rule "<NỘI DUNG QUY TẮC MỚI>" --mistake "<LỖI CẤM LẶP LẠI>" --project "<TÊN DỰ ÁN>"
```

## Nguyên tắc:
- Không lưu trí nhớ ở bất kỳ thư mục nào khác ngoài `portable_trained_brain/`.
- Bài học mới sẽ tự động được thêm vào `learned_editing_style.md` và `training_feedback_history.json`.
- Ở các phiên chat tiếp theo, Bước 0 `load_brain.py` sẽ tự động nạp các bài học này.
