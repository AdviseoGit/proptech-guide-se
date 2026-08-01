import json

companies_file = '/data/workspace/projects/proptech-guide-se/data/companies.json'

with open(companies_file, 'r') as f:
    companies = json.load(f)

new_companies = [
    {
        "name": "Iqnect",
        "url": "https://iqnect.se/",
        "description": "Smarta fastighetslösningar och IoT-integration för energioptimering och övervakning av inomhusklimat.",
        "category": "energi",
        "category_label": "Energi & Hållbarhet",
        "segments": ["fastighetsagare", "forvaltare"]
    },
    {
        "name": "Smartvatten",
        "url": "https://smartvatten.com/sv/",
        "description": "Tjänst för vatteneffektivisering. Följer upp vattenförbrukning i realtid via kameraavläsning av befintliga mätare och larmar vid läckage.",
        "category": "energi",
        "category_label": "Energi & Hållbarhet",
        "segments": ["fastighetsagare", "forvaltare", "brf"]
    },
    {
        "name": "HomeRun",
        "url": "https://www.homerun.net/sv/",
        "description": "Digital plattform för byggprojekt och boendekommunikation, specifikt inriktad på tillvals- och ärendehantering.",
        "category": "boende",
        "category_label": "Boendeapp & Portal",
        "segments": ["fastighetsagare", "brf"]
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
