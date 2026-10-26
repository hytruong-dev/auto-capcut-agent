---
name: remotion-captions
description: Transcribing, displaying and animating captions
version: 4.0.537
---

> **⚠️ ƯU TIÊN TRONG DỰ ÁN NÀY:** Skill này chỉ là kiến thức kỹ thuật chung. Mọi quyết định về gu dựng (font, màu, vị trí phụ đề, hook, âm lượng, nhịp cắt) BẮT BUỘC lấy từ portable_trained_brain/learned_editing_style.md và 	raining_feedback_history.json (chạy python scripts/load_brain.py trước). Nếu ví dụ trong skill này mâu thuẫn (chữ trắng, Montserrat/DejaVu, phụ đề sát đáy, BGM -28dB...) thì BỎ QUA ví dụ đó. Phụ đề: dùng scripts/brain_karaoke_ass.py.


All captions must be processed in JSON. The captions must use the [`Caption`](https://www.remotion.dev/docs/captions/caption.md) type which is the following:

```ts
import type { Caption } from "@remotion/captions";
```

This is the definition:

```ts
type Caption = {
  text: string;
  startMs: number;
  endMs: number;
  timestampMs: number | null;
  confidence: number | null;
  pageBreakAfter?: boolean;
};
```

## Generating captions

To transcribe video and audio files to generate captions, load the [transcribe-captions.md](transcribe-captions.md) file for more instructions.

## Displaying captions

To display captions in your video, load the [display-captions.md](display-captions.md) file for more instructions.

## Importing captions

To import captions from a .srt file, load the [import-srt-captions.md](import-srt-captions.md) file for more instructions.

## Post-creation

After you're done, load this skill: Remotion Best Practices

If not alreay done, open the Remotion Studio, unless instructed otherwise.
