import psutil, os, sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

print("Checking running processes:")
for proc in psutil.process_iter(['pid', 'name', 'exe']):
    try:
        pname = proc.info['name'].lower()
        if 'omni' in pname or 'voice' in pname or 'studio' in pname:
            print(f"  PID {proc.info['pid']}: {proc.info['name']} -> {proc.info['exe']}")
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass
