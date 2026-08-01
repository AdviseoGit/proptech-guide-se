import json

companies_file = '/data/workspace/projects/proptech-guide-se/data/companies.json'

with open(companies_file, 'r') as f:
    companies = json.load(f)

new_companies = [
    {
        "name": "Iqnite",
        "url": "https://www.iqnite.se/",
        "description": "Molnbaserad plattform för fastighetsautomation och energioptimering. Integrerar och styr olika fastighetssystem för ökad effektivitet.",
        "category": "energi",
        "category_label": "Energi & Hållbarhet",
        "segments": ["fastighetsagare", "forvaltare"]
    },
    {
        "name": "Zesec",
        "url": "https://zesec.com/",
        "description": "Mobila passersystem som ersätter nycklar och taggar med mobilen. Fokuserar på enkel hantering av behörigheter och digitala nycklar.",
        "category": "passer",
        "category_label": "Passersystem",
        "segments": ["fastighetsagare", "forvaltare", "brf"]
    },
    {
        "name": "Bemsiq",
        "url": "https://www.bemsiq.se/",
        "description": "Koncern inom byggnadsautomation och smarta fastigheter. Består av flera bolag som fokuserar på energieffektivisering och inneklimat.",
        "category": "energi",
        "category_label": "Energi & Hållbarhet",
        "segments": ["fastighetsagare"]
    }
]

# Check for duplicates before adding
existing_names = {c['name'].lower() for c in companies}
added_count = 0

for c in new_companies:
    if c['name'].lower() not in existing_names:
        companies.append(c)
        added_count += 1
    else:
        print(f"Skipping duplicate: {c['name']}")

with open(companies_file, 'w') as f:
    json.dump(companies, f, indent=4, ensure_ascii=False)

print(f"Added {added_count} companies. Total: {len(companies)}")
