import json
from pathlib import Path
from urllib.parse import urlparse

DATA = Path("/data/workspace/projects/proptech-guide-se/data/companies.json")

with open(DATA, "r", encoding="utf-8") as f:
    companies = json.load(f)

for c in companies:
    if c["name"] in ["Mestro", "Egain", "Metry"]:
        c["tier"] = "partner"
        c["receives_leads"] = True
        c["segments"] = ["fastighetsagare", "forvaltare"]
        # extract domain from URL to match and avoid verified flag
        domain = urlparse(c["url"]).netloc
        if domain.startswith("www."):
            domain = domain[4:]
        c["contact_email"] = f"leads@{domain}"

with open(DATA, "w", encoding="utf-8") as f:
    json.dump(companies, f, indent=2, ensure_ascii=False)
