import json
from pathlib import Path

DATA = Path("/data/workspace/projects/proptech-guide-se/data/guides.json")

with open(DATA, "r", encoding="utf-8") as f:
    guides = json.load(f)

for g in guides:
    if g["slug"] == "iot-energieffektivisering":
        g["sponsor"] = "Mestro"
        g["sponsor_slot_open"] = False
        g["gated"] = True
        g["pdf"] = "IoT & Energieffektivisering - Mestro Edition"

with open(DATA, "w", encoding="utf-8") as f:
    json.dump(guides, f, indent=2, ensure_ascii=False)
