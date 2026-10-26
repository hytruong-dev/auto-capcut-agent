import os, sys, sqlite3

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

db_path = r"C:\Users\PC\AppData\Roaming\OmniVoice\omnivoice.db"
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()
    print("Tables in omnivoice.db:")
    for t in tables:
        tname = t[0]
        cur.execute(f"SELECT COUNT(*) FROM {tname}")
        cnt = cur.fetchone()[0]
        print(f"  {tname}: {cnt} rows")
        if 'profile' in tname.lower() or 'voice' in tname.lower():
            cur.execute(f"SELECT * FROM {tname} LIMIT 3")
            rows = cur.fetchall()
            print(f"    Sample: {rows}")
else:
    print("DB does not exist at", db_path)
