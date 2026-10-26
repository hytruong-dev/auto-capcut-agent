"""
Script tạo voiceover tiếng Việt bằng gTTS cho video XanhSM Night Shift
"""
from gtts import gTTS
import os

# Script tiếng Việt đầy đủ - style cảm xúc/lao động
SCRIPT_FULL = """Hôm nay mình bắt đầu ca từ sáu giờ chiều.
Trời còn sáng mà mình đã phóng ra đường rồi.
Đêm nay khu này vắng hơn thường lệ.
Cứ ngồi chờ... rồi đơn mới nổ.
Nhưng đây là nghề mình đã chọn.
Mỗi chuyến xe là một câu chuyện.
Có chuyến vui, có chuyến mệt.
Nhưng mình vẫn cứ đi.
Vì đó là cách mình kiếm sống.
Và mình tự hào về điều đó.
Nếu bạn cũng đang chạy xe công nghệ, mình hiểu cảm giác của bạn.
Cứ thế mà đi thôi anh em ơi!
Đừng quên bấm tim và theo dõi kênh mình nhé!"""

output_dir = os.path.join(os.path.dirname(__file__), "..", "processed", "voiceover")
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "xanhsm_nightshift_vo.mp3")

print("Đang tạo voiceover tiếng Việt...")
tts = gTTS(text=SCRIPT_FULL, lang='vi', slow=False)
tts.save(output_path)
print(f"Đã lưu: {output_path}")

# Kiểm tra file size
size = os.path.getsize(output_path)
print(f"File size: {size/1024:.1f} KB")
