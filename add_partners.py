import json

with open("data/companies.json", "r") as f:
    companies = json.load(f)

# Update some energi companies to partners
updates = {
    "Mestro": {
        "tier": "partner",
        "usp": ["Sveriges ledande plattform för energiuppföljning.", "Över 10 000 anslutna fastigheter.", "Helt automatiserad datainsamling."],
        "cases": [{"name": "Akelius", "url": "#"}, {"name": "Hufvudstaden", "url": "#"}],
        "contact_email": "partner@mestro.se",
        "receives_leads": True
    },
    "Egain": {
        "tier": "partner",
        "usp": ["AI-styrning av värmesystem för flerbostadshus.", "Sänker energiförbrukningen med upp till 20%.", "Kräver inga stora ingrepp i fastigheten."],
        "cases": [{"name": "Riksbyggen", "url": "#"}, {"name": "HSB", "url": "#"}],
        "contact_email": "sales@egain.io",
        "receives_leads": True
    },
    "Metry": {
        "tier": "partner",
        "usp": ["Samlar in miljö- och energidata från alla dina mätare.", "Används för ESG-rapportering av ledande fastighetsbolag.", "Enkel integration mot andra system."],
        "cases": [{"name": "Vasakronan", "url": "#"}, {"name": "Castellum", "url": "#"}],
        "contact_email": "hello@metry.io",
        "receives_leads": True
    }
}

for c in companies:
    if c["name"] in updates:
        c.update(updates[c["name"]])

with open("data/companies.json", "w") as f:
    json.dump(companies, f, indent=2, ensure_ascii=False)
