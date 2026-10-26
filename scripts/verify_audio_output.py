import whisper, sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

m = whisper.load_model('base')
res = m.transcribe(r'c:\QuangHy\editvideo\processed\voiceover\test_cloned_output.wav', language='vi')
print("Transcribed audio result:", res['text'])
