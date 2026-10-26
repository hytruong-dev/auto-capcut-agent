import json, os, subprocess

EXPRESSIVE_SCRIPT = [
    {"id": 1, "part": "hook", "text": "Thử thách chạy xe máy điện Xanh SM cả ngày, từ sáng đến đêm... thực sự kiếm được bao nhiêu tiền nè?", "kw": "XANH SM CẢ NGÀY, KIẾM ĐƯỢC BAO NHIÊU?"},
    {"id": 2, "part": "hook", "text": "Hôm nay mình test thực tế cho anh em xem luôn nha!", "kw": "TEST THỰC TẾ LUÔN!"},
    {"id": 3, "part": "hook", "text": "Bạn nào còn thắc mắc thì xem hết video này là biết liền nè!", "kw": "XEM HẾT VIDEO NÀY NHA"},
    {"id": 4, "part": "morning", "text": "Tám giờ sáng, mình bắt đầu mở app nhận cuốc đầu tiên.", "kw": "TÁM GIỜ SÁNG, MỞ APP NHẬN CUỐC"},
    {"id": 5, "part": "morning", "text": "Phải công nhận cái chiếc xe điện VinFast này chạy êm ru luôn á, lướt trên đường phố không một tiếng động cơ!", "kw": "CHẠY ÊM RU, KHÔNG TIẾNG ĐỘNG CƠ"},
    {"id": 6, "part": "morning", "text": "Sáng sớm mát rượi, cực kỳ dễ chịu luôn!", "kw": "SÁNG SỚM MÁT RƯỢI"},
    {"id": 7, "part": "morning", "text": "Mở bát cuốc đầu tiên... được hẳn ba mươi lăm cành, quá đã!", "kw": "BA MƯƠI LĂM CÀNH!"},
    {"id": 8, "part": "afternoon", "text": "Chạy vèo một cái là đã đến chiều muộn rồi.", "kw": "ĐẾN CHIỀU MUỘN"},
    {"id": 9, "part": "afternoon", "text": "Tầm sáu giờ chiều, Sài Gòn bắt đầu lên đèn lung linh đẹp ghê luôn.", "kw": "SÁU GIỜ CHIỀU, LÊN ĐÈN LUNG LINH"},
    {"id": 10, "part": "afternoon", "text": "Giờ tan tầm kẹt xe, nhưng xe điện ga mượt, luồn lách qua ngõ nhỏ cực kỳ nhẹ nhàng!", "kw": "GA MƯỢT, LUỒN LÁCH NHẸ NHÀNG"},
    {"id": 11, "part": "afternoon", "text": "Đứng nghỉ chân có một xíu thôi, mà app lại nổ đơn liên tục luôn á!", "kw": "NỔ ĐƠN LIÊN TỤC!"},
    {"id": 12, "part": "night", "text": "Đến gần tám giờ tối rồi, phố xá cũng thưa thớt dần.", "kw": "TÁM GIỜ TỐI"},
    {"id": 13, "part": "night", "text": "Chạy đêm gió mát thật đó, nhưng mà người cũng bắt đầu thấy mỏi lưng rồi nè.", "kw": "CHẠY ĐÊM MÁT MẺ"},
    {"id": 14, "part": "night", "text": "Mỗi chuyến xe đêm là một câu chuyện, có chuyến vui, có chuyến mệt...", "kw": "MỖI CHUYẾN XE, MỘT CÂU CHUYỆN"},
    {"id": 15, "part": "night", "text": "Nhưng mà cứ nhìn đồng hồ ki-lô-mét nhảy đều là lại có động lực cày tiếp!", "kw": "ĐỘNG LỰC ĐI TIẾP!"},
    {"id": 16, "part": "outro", "text": "Và đây là kết quả sau một ngày cày cuốc: tổng kết được gần năm trăm cành, quá ấm luôn!", "kw": "GẦN NĂM TRĂM CÀNH!"},
    {"id": 17, "part": "outro", "text": "Chạy cả ngày công nhận vất vả, nhưng mà cũng rất đáng tự hào nha!", "kw": "RẤT ĐÁNG TỰ HÀO"},
    {"id": 18, "part": "outro", "text": "Còn anh em thì sao? Một ngày cày được bao nhiêu lúa? Comment cho mình biết với nha!", "kw": "BAO NHIÊU LÚA? COMMENT NHA!"},
    {"id": 19, "part": "outro", "text": "Nhớ thả cho mình một tim và follow kênh để đón xem tập tiếp theo nhé!", "kw": "THẢ TIM VÀ FOLLOW KÊNH NHÉ!"}
]

seg_dir = r"processed\voiceover\story_segments"
accum = 0.0
items = []

for seg in EXPRESSIVE_SCRIPT:
    seg_id = seg["id"]
    sf = os.path.join(seg_dir, f"seg_{seg_id:02d}.mp3")
    res = subprocess.run(["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", sf], capture_output=True, text=True)
    d = float(json.loads(res.stdout)["format"]["duration"])
    start_t = round(accum, 2)
    end_t = round(accum + d, 2)
    accum = end_t
    items.append({
        "id": seg_id,
        "part": seg["part"],
        "text": seg["text"],
        "keyword": seg["kw"],
        "audio_file": sf.replace("\\", "/"),
        "duration": d,
        "start_time": start_t,
        "end_time": end_t
    })

master_vo = r"processed\voiceover\xanhsm_story_vo.mp3"
res_m = subprocess.run(["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", master_vo], capture_output=True, text=True)
master_dur = float(json.loads(res_m.stdout)["format"]["duration"])

out_json = r"processed\story_voiceover_timeline.json"
with open(out_json, "w", encoding="utf-8") as f:
    json.dump({
        "total_duration": master_dur,
        "segment_count": len(items),
        "segments": items
    }, f, ensure_ascii=False, indent=2)

print(f"[SUCCESS] Updated {out_json} with total duration: {master_dur:.2f}s")
