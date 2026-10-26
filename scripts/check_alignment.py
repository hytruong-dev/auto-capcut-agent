import json, sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

whisper_words = json.load(open('processed/voiceover_words.json', encoding='utf-8'))

clean_script = [
    # Câu 1
    "Thử thách chạy xe máy điện Xanh SM cả ngày từ sáng đến đêm thực sự kiếm được bao nhiêu",
    # Câu 2
    "Hôm nay mình test thực tế luôn",
    # Câu 3
    "Bạn nào còn thắc mắc thì xem hết video này nha",
    # Câu 4
    "Tám giờ sáng mình bắt đầu mở app nhận cuốc đầu tiên",
    # Câu 5
    "Phải công nhận chiếc xe điện VinFast này chạy êm ru lướt trên đường phố không một tiếng động cơ",
    # Câu 6
    "Sáng sớm mát rượi cực kỳ dễ chịu",
    # Câu 7
    "Mở bát cuốc đầu được ba mươi lăm cành",
    # Câu 8
    "Chạy vèo một cái là đến chiều muộn",
    # Câu 9
    "Tầm sáu giờ chiều Sài Gòn bắt đầu lên đèn lung linh",
    # Câu 10
    "Giờ tan tầm kẹt xe nhưng được cái xe điện ga mượt luồn lách qua các con phố nhỏ cực kỳ nhẹ nhàng",
    # Câu 11
    "Đứng nghỉ chân một xíu là app lại nổ đơn liên tục",
    # Câu 12
    "Đến gần tám giờ tối phố xá đã thưa dần",
    # Câu 13
    "Chạy đêm mát mẻ nhưng người cũng bắt đầu thấy mỏi lưng rồi đó",
    # Câu 14
    "Mỗi chuyến xe đêm là một câu chuyện có chuyến vui có chuyến mệt",
    # Câu 15
    "Nhưng cứ nhìn đồng hồ ki lô mét nhảy đều là lại có động lực đi tiếp",
    # Câu 16
    "Và đây là kết quả sau một ngày cày cuốc xe chạy êm tổng kết được gần năm trăm cành",
    # Câu 17
    "Chạy cả ngày công nhận vất vả nhưng cũng rất đáng tự hào",
    # Câu 18
    "Còn anh em thì sao Một ngày được bao nhiêu lúa Comment cho mình biết với nha",
    # Câu 19
    "Đừng quên thả một tim và follow kênh để đón xem tập tiếp theo nhé"
]

all_script_words = []
for s in clean_script:
    all_script_words.extend(s.split())

print(f"Total script words: {len(all_script_words)}")
print(f"Total whisper words: {len(whisper_words)}")

for i in range(min(len(all_script_words), len(whisper_words))):
    sw = all_script_words[i]
    ww = whisper_words[i]['word'].strip('.,?!')
    if sw.lower() != ww.lower():
        print(f"Mismatch at {i}: script='{sw}' vs whisper='{ww}' [{whisper_words[i]['start']:.2f}s]")
        if i > 50:
            break
