import json, re

p = r"C:\Users\PC\AppData\Local\CapCut\User Data\Projects\com.lveditor.draft\Vlog_XanhSM_Storytelling_POV\draft_content.json"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

matches = re.findall(r'[^"\s]*placeholder[^"\s]*', text)
print("Total placeholder matches:", len(matches))
for m in set(matches):
    print("Match:", m)

data = json.load(open(p, "r", encoding="utf-8"))
for mtype, mlist in data.get("materials", {}).items():
    if isinstance(mlist, list):
        for item in mlist:
            if isinstance(item, dict):
                for k, v in item.items():
                    if isinstance(v, str) and "placeholder" in v:
                        print(f"Found in materials.{mtype}[].{k} = {v}")
