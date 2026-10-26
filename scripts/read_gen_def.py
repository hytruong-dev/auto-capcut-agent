import os

omni_py = r"C:\Users\PC\AppData\Local\com.debpalash.omnivoice-studio\project\omnivoice\models\omnivoice.py"
with open(omni_py, "r", encoding="utf-8") as f:
    content = f.read()

# search for "def generate"
pos = content.find("def generate(")
if pos != -1:
    print(content[pos:pos+1500])
