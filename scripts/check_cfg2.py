import whisper, sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

m = whisper.load_model('base')
res = m.transcribe(r'c:\QuangHy\editvideo\processed\voiceover\test_emotion_temp085_g16.wav', language='vi')
print("Config 2 transcribed:", res['text'])
