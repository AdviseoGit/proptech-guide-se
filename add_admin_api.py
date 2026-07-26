with open("/data/workspace/projects/proptech-guide-se/main.py", "r") as f:
    content = f.read()

import re

admin_endpoint = """
@app.get("/api/admin/leads")
async def get_admin_leads():
    # Enkelt mockat API för admin-vyn tills db-koppling finns
    import os
    import json
    
    leads = []
    leads_file = "data/leads.jsonl"
    
    if os.path.exists(leads_file):
        with open(leads_file, "r") as f:
            for line in f:
                try:
                    leads.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    
    # Sortera nyaste först
    leads.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    
    # Byt namn på fält för att matcha frontenden
    for lead in leads:
        if "timestamp" in lead and "created_at" not in lead:
            lead["created_at"] = lead["timestamp"]
    
    return {"leads": leads}
"""

if "@app.get(\"/api/admin/leads\")" not in content:
    content = content + "\n\n" + admin_endpoint
    with open("/data/workspace/projects/proptech-guide-se/main.py", "w") as f:
        f.write(content)
    print("Added admin endpoint")
else:
    print("Admin endpoint already exists")
