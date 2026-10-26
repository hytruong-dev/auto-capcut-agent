import os, sys, sqlite3

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

db_path = r"C:\Users\PC\AppData\Roaming\OmniVoice\omnivoice.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute("SELECT * FROM generation_history")
rows = cur.fetchall()
col_names = [d[0] for d in cur.description]
print("Columns in generation_history:", col_names)
for r in rows:
    print(dict(zip(col_names, r)))
