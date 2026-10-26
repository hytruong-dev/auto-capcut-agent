"""
SINH PHỤ ĐỀ DYNAMIC WORD KARAOKE ĐÚNG CHUẨN ĐÃ TRAIN (dùng cho MỌI video mới).

Chuẩn (lấy từ portable_trained_brain/learned_editing_style.md):
- Oswald-Bold, IN HOA, Vàng chanh #F0FF00; từ đang đọc Cyan #66FFFF
- Viền đen dày (Outline 7), bóng đen, Alignment 2, MarginV 550 → tâm chữ ở Safe Zone Y≈-0.38
  (đã đo bằng pixel: MarginV 220 cũ cho Y≈-0.73, thấp hơn giới hạn cấm Y=-0.65)
- Cụm ngắn 2-4 từ, GIỮ ĐỦ 100% từ, timing lấy từ word-timestamps Whisper thật
- Hook 2 tầng: dòng 1 Đỏ #FF3333 viền trắng, dòng 2 Vàng #F0FF00 viền đen (1/3 trên)
- Callout cuối: nửa trên khung hình (Alignment 8)

Đầu vào --words chấp nhận 2 dạng JSON:
  a) [{"word": "...", "start": 1.2, "end": 1.5}, ...]                (danh sách phẳng)
  b) [{"words": [{"word": "...", "master_start": .., "master_end": ..}]}, ...]  (theo câu,
     ví dụ processed/exact_omnivoice_words.json) — mỗi câu được tách cụm riêng.

Ví dụ:
  $env:PYTHONIOENCODING="utf-8"
  python scripts/brain_karaoke_ass.py --words processed/exact_omnivoice_words.json `
      --out processed/my_video.ass --hook1 "THỬ THÁCH 1 NGÀY" --hook2 "CHẠY XE XANH SM" `
      --callout "BẤM TIM & BÌNH LUẬN NHÉ!" --callout-start 83 --callout-end 88

Ép phụ đề bằng FFmpeg (fontsdir để chắc chắn dùng Oswald-Bold):
  ffmpeg -i in.mp4 -vf "ass=processed/my_video.ass:fontsdir=portable_trained_brain/portable_assets/fonts" ...
"""
import argparse
import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

CYAN = r"{\c&H00FFFF66&}"    # #66FFFF (ASS dùng BGR)
YELLOW = r"{\c&H0000FFF0&}"  # #F0FF00
MIN_WORDS, MAX_WORDS = 2, 4
BREAK_PUNCT = re.compile(r"[,.!?;:…]$")

HEADER = """[Script Info]
Title: {title}
ScriptType: v4.00+
WrapStyle: 0
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: DynamicSub,Oswald,{size},&H0000FFF0,&H0000FFF0,&H00000000,&H1A000000,-1,0,0,0,100,100,1,0,1,7,2,2,60,60,{marginv},1
Style: Hook1,Oswald,84,&H003333FF,&H003333FF,&H00FFFFFF,&H1A000000,-1,0,0,0,100,100,1,0,1,8,3,8,60,60,340,1
Style: Hook2,Oswald,96,&H0000FFF0,&H0000FFF0,&H00000000,&H1A000000,-1,0,0,0,100,100,1,0,1,9,3,8,60,60,460,1
Style: Callout,Oswald,64,&H0066FF66,&H0066FF66,&H00000000,&H1A000000,-1,0,0,0,100,100,0,0,1,6,2,8,60,60,360,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def ass_time(sec):
    sec = max(0.0, sec)
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = sec % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def load_sentences(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = data.get("segments") or data.get("words") or []
    sentences = []
    if data and isinstance(data[0], dict) and "words" in data[0]:
        for seg in data:
            ws = [norm_word(w) for w in seg["words"]]
            sentences.append([w for w in ws if w])
    else:
        ws = [norm_word(w) for w in data]
        sentences.append([w for w in ws if w])
    return [dedupe_whisper_repeat(s, i) for i, s in enumerate(sentences, 1) if s]


def dedupe_whisper_repeat(words, idx):
    """Whisper hay 'ảo giác' lặp lại nguyên câu 2 lần. Phát hiện và bỏ phần lặp."""
    key = [re.sub(r"[^\w]", "", w["word"]) for w in words]
    n = len(key)
    for size in range(n // 2, 2, -1):
        if key[n - 2 * size:n - size] == key[n - size:]:
            print(f"[CẢNH BÁO] Câu {idx}: Whisper lặp lại {size} từ cuối → đã bỏ phần lặp. "
                  "Nên dùng file *cleaned* hoặc chạy lại Whisper với initial_prompt.")
            return words[:n - size]
    return words


def norm_word(w):
    text = str(w.get("word", w.get("text", ""))).strip()
    st = w.get("master_start", w.get("start"))
    en = w.get("master_end", w.get("end"))
    if not text or st is None or en is None:
        return None
    return {"word": text.upper(), "start": float(st), "end": float(en)}


def split_phrases(words):
    """Chia câu thành cụm 2-4 từ (tối đa 26 ký tự), ưu tiên ngắt sau dấu câu, không bỏ từ nào."""
    phrases, cur = [], []
    for w in words:
        trial = cur + [w]
        trial_len = len(" ".join(x["word"] for x in trial))
        # Nếu đã đủ từ hoặc có dấu câu hoặc nếu thêm vào vượt quá 26 ký tự
        if cur and (trial_len > 26 or len(cur) >= MAX_WORDS or (len(cur) >= MIN_WORDS and BREAK_PUNCT.search(cur[-1]["word"]))):
            phrases.append(cur)
            cur = [w]
        else:
            cur.append(w)
    if cur:
        if len(cur) < MIN_WORDS and phrases:
            merged = phrases[-1] + cur
            if len(" ".join(x["word"] for x in merged)) <= 26 and len(merged) <= MAX_WORDS + 1:
                phrases[-1] = merged
            else:
                phrases.append(cur)
        else:
            phrases.append(cur)
    return phrases


def build_events(sentences):
    """Xây dựng chuỗi sự kiện Dynamic Karaoke với hiệu ứng Elastic Micro-Pop và 0 overlap."""
    all_phrases = []
    n_words = 0
    for words in sentences:
        n_words += len(words)
        all_phrases.extend(split_phrases(words))

    events = []
    for p_idx, p in enumerate(all_phrases):
        next_p_st = all_phrases[p_idx + 1][0]["start"] if p_idx + 1 < len(all_phrases) else 999999.0
        p_end = p[-1]["end"] + 0.08
        if p_end > next_p_st - 0.01:
            p_end = max(p[-1]["start"] + 0.15, next_p_st - 0.02)

        for i, w in enumerate(p):
            st = w["start"]
            if i < len(p) - 1:
                en = max(st + 0.10, p[i + 1]["start"])
            else:
                en = max(st + 0.15, p_end)
            if en > next_p_st - 0.01 and i == len(p) - 1:
                en = max(st + 0.08, next_p_st - 0.01)

            # Cụm từ với từ active được tô màu Cyan + hiệu ứng Elastic Micro-Pop
            toks = [(CYAN if j == i else YELLOW) + x["word"] for j, x in enumerate(p)]
            # Hiệu ứng Elastic Micro-Pop nảy nhẹ 106% -> 100% trong 90ms
            pop_anim = r"{\fscx106\fscy106\t(0,90,\fscx100\fscy100)}"
            events.append((st, en, pop_anim + " ".join(toks)))

    # Đảm bảo tuyệt đối 0 overlap giữa 2 sự kiện liên tiếp
    cleaned_events = []
    for idx, (st, en, txt) in enumerate(events):
        if idx + 1 < len(events):
            next_st = events[idx + 1][0]
            if en > next_st:
                en = max(st + 0.05, next_st)
        if en > st:
            cleaned_events.append((st, en, txt))

    return cleaned_events, n_words


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--words", required=True, help="JSON word timestamps từ Whisper")
    ap.add_argument("--out", required=True, help="File .ass đầu ra")
    ap.add_argument("--hook1", default="", help="Dòng 1 hook (Đỏ)")
    ap.add_argument("--hook2", default="", help="Dòng 2 hook (Vàng)")
    ap.add_argument("--hook-end", type=float, default=5.5)
    ap.add_argument("--callout", default="")
    ap.add_argument("--callout-start", type=float, default=0)
    ap.add_argument("--callout-end", type=float, default=0)
    ap.add_argument("--marginv", type=int, default=550, help="Khoảng cách đáy. 550 = tâm chữ ở Y≈-0.38 (69%% chiều cao). KHÔNG dùng 220 (=86%%, thấp hơn giới hạn Y=-0.65)")
    ap.add_argument("--size", type=int, default=76, help="Cỡ chữ phụ đề (chuẩn 76 ở 1080x1920)")
    ap.add_argument("--title", default="Dynamic Word Karaoke (trained brain)")
    a = ap.parse_args()

    sentences = load_sentences(a.words)
    if not sentences:
        sys.exit("[LỖI] Không đọc được word timestamps. Hãy chạy Whisper word_timestamps=True trước.")
    events, n_words = build_events(sentences)

    lines = [HEADER.format(title=a.title, size=a.size, marginv=a.marginv)]
    if a.hook1:
        lines.append(f"Dialogue: 1,{ass_time(0)},{ass_time(a.hook_end)},Hook1,,0,0,0,,{{\\fad(120,120)}}{a.hook1.upper()}\n")
    if a.hook2:
        lines.append(f"Dialogue: 1,{ass_time(0)},{ass_time(a.hook_end)},Hook2,,0,0,0,,{{\\fad(120,120)}}{a.hook2.upper()}\n")
    if a.callout and a.callout_end > a.callout_start:
        lines.append(f"Dialogue: 2,{ass_time(a.callout_start)},{ass_time(a.callout_end)},Callout,,0,0,0,,{{\\fad(120,120)}}{a.callout.upper()}\n")
    for st, en, text in events:
        lines.append(f"Dialogue: 0,{ass_time(st)},{ass_time(en)},DynamicSub,,0,0,0,,{text}\n")

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("".join(lines), encoding="utf-8")
    print(f"[OK] {out}: {n_words} từ (giữ đủ 100%), {len(events)} karaoke events, {len(sentences)} câu.")
    print('[i] Ép phụ đề: -vf "ass=' + out.as_posix() + ':fontsdir=portable_trained_brain/portable_assets/fonts"')


if __name__ == "__main__":
    main()
