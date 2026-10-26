import os

base = r"C:\Users\PC\AppData\Local\com.debpalash.omnivoice-studio\project\omnivoice"
for root, dirs, files in os.walk(base):
    for f in files:
        if f.endswith('.py'):
            print(os.path.join(root, f))
