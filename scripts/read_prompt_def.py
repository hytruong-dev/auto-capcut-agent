import os

omni_py = r"C:\Users\PC\AppData\Local\com.debpalash.omnivoice-studio\project\omnivoice\models\omnivoice.py"
with open(omni_py, "r", encoding="utf-8") as f:
    content = f.read()

pos = content.find("def create_voice_clone_prompt")
if pos != -1:
    print(content[pos:pos+800])
