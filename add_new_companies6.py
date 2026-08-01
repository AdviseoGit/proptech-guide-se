import json

companies_file = '/data/workspace/projects/proptech-guide-se/data/companies.json'

with open(companies_file, 'r') as f:
    companies = json.load(f)

new_companies = [
    {
        "name": "Hyresvärd.se",
        "url": "https://hyresvard.se/",
        "description": "Ett komplett, molnbaserat fastighetssystem designat för att hantera hyreskontrakt, avisering och ekonomi för både mindre och större hyresvärdar.",
        "category": "forvaltning",
        "category_label": "Fastighetssystem",
        "segments": ["fastighetsagare", "forvaltare"]
    },
    {
        "name": "Paligo",
        "url": "https://paligo.net/",
        "description": "CCMS-system som används inom proptech och fastighetssektorn för att hantera, strukturera och publicera teknisk dokumentation för smarta byggnader.",
        "category": "forvaltning",
        "category_label": "Fastighetssystem",
        "segments": ["fastighetsagare", "forvaltare"]
    },
    {
        "name": "InviSense",
        "url": "https://invisense.se/",
        "description": "Utvecklar supertunna, passiva fuktsensorer som byggs in i fastigheter för kontinuerlig fuktmätning utan att behöva bryta ytskikt.",
        "category": "energi",
        "category_label": "Energi & Hållbarhet",
        "segments": ["fastighetsagare", "forvaltare", "brf"]
    },
    {
        "name": "Noda",
        "url": "https://noda.se/",
        "description": "Intelligent plattform för energioptimering och styrning av fjärrvärme och kylsystem, driven av AI och data från smarta mätare.",
        "category": "energi",
        "category_label": "Energi & Hållbarhet",
        "segments": ["fastighetsagare", "forvaltare", "brf"]
    },
    {
        "name": "Amido",
        "url": "https://amido.se/",
        "description": "Öppen plattform (Alliera) för administration av passersystem. Möjliggör central hantering av digitala nycklar oberoende av underliggande hårdvara.",
        "category": "passer",
        "category_label": "Passersystem",
        "segments": ["fastighetsagare", "forvaltare"]
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
