import json

def add_companies():
    new_companies = [
        {
            "slug": "celsius-view",
            "name": "Celsius View",
            "category": "energi",
            "category_label": "Energi & Hållbarhet",
            "description": "System för mätvärdesinsamling och visualisering av energidata för fastighetsägare och förvaltare.",
            "url": "https://celsiusview.se/",
            "tier": "free",
            "contact_email": "",
            "receives_leads": False
        },
        {
            "slug": "nordic-climate-group",
            "name": "Nordic Climate Group",
            "category": "energi",
            "category_label": "Energi & Hållbarhet",
            "description": "Helhetsleverantör av kyl-, värme- och energieffektiva lösningar för kommersiella fastigheter.",
            "url": "https://www.nordicclimategroup.se/",
            "tier": "free",
            "contact_email": "",
            "receives_leads": False
        },
        {
            "slug": "energy-machines",
            "name": "Energy Machines",
            "category": "energi",
            "category_label": "Energi & Hållbarhet",
            "description": "Utvecklar mjuk- och hårdvara för integrerade energisystem som minskar koldioxidavtryck och driftkostnader för fastigheter.",
            "url": "https://www.energymachines.com/",
            "tier": "free",
            "contact_email": "",
            "receives_leads": False
        }
    ]

    with open("/data/workspace/projects/proptech-guide-se/data/companies.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    existing_slugs = {c.get("slug") for c in data}
    added = 0

    for c in new_companies:
        if c["slug"] not in existing_slugs:
            data.append(c)
            added += 1

    with open("/data/workspace/projects/proptech-guide-se/data/companies.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Added {added} new companies.")

if __name__ == "__main__":
    add_companies()
