import os, sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

vs_python = r"C:\Users\PC\AppData\Local\com.debpalash.omnivoice-studio\project\.venv\Scripts\python.exe"
infer_exe = r"C:\Users\PC\AppData\Local\com.debpalash.omnivoice-studio\project\.venv\Scripts\omnivoice-infer.exe"

import subprocess
res = subprocess.run([infer_exe, "--help"], capture_output=True, text=True)
print("omnivoice-infer --help:")
print(res.stdout[:1500])
