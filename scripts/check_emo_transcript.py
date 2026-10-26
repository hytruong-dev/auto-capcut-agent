import whisper, sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

m = whisper.load_model('base')
res = m.transcribe(r'c:\QuangHy\editvideo\processed\voiceover\test_emotion_temp07_g17.wav', language='vi')
print("Transcribed result:", res['text'])
