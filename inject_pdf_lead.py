import json
import re
from pathlib import Path

ROOT = Path("/data/workspace/projects/proptech-guide-se")
DATA = ROOT / "data"
STATIC = ROOT / "static"

with open(DATA / "guides.json", "r", encoding="utf-8") as f:
    guides = json.load(f)

for g in guides:
    if g.get("gated"):
        slug = g["slug"]
        filepath = STATIC / f"{slug}.html"
        if not filepath.exists():
            print(f"File not found: {filepath}")
            continue
            
        with open(filepath, "r", encoding="utf-8") as f:
            html = f.read()
            
        if 'id="lead-form-guide"' in html:
            # Need to update the JS payload to include guide_slug
            if "body: JSON.stringify({ email: email })" in html:
                html = html.replace(
                    "body: JSON.stringify({ email: email })",
                    f"body: JSON.stringify({{ email: email, guide_slug: '{slug}' }})"
                )
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(html)
                print(f"Updated JS in {slug}.html")
            else:
                print(f"JS already updated or not found in {slug}.html")
            continue
