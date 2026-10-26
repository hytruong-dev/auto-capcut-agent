import whisper, sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

m = whisper.load_model('base')
for s in [8, 12]:
    p = f"c:\\QuangHy\\editvideo\\processed\\voiceover\\test_steps_{s}.wav"
    res = m.transcribe(p, language='vi')
    print(f"Steps={s} transcribed: {res['text']}")
