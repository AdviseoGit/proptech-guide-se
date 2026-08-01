import json

companies_file = '/data/workspace/projects/proptech-guide-se/data/companies.json'

with open(companies_file, 'r') as f:
    companies = json.load(f)

new_companies = [
    {
        "name": "Nivéus",
        "url": "https://niveus.se/",
        "description": "Digital plattform för fastighetsskötsel och drift. Förenklar felanmälan, rondering och tillsyn för fastighetstekniker.",
        "category": "forvaltning",
        "category_label": "Fastighetssystem",
        "segments": ["forvaltare", "fastighetsagare"]
    },
    {
        "name": "Hydda",
        "url": "https://hyddagroup.com/",
        "description": "Proptech-koncern som samlar flera ledande lösningar inom fastighetssystem och boendeappar för en helhetslösning.",
        "category": "plattform",
        "category_label": "Öppen Plattform",
        "segments": ["fastighetsagare", "forvaltare"]
    },
    {
        "name": "Propely",
        "url": "https://propely.com/",
        "description": "Norskt system (med stark närvaro i Sverige) för fastighetsdrift. Digitaliserar rutiner, felanmälningar och kommunikation med hyresgäster.",
        "category": "forvaltning",
        "category_label": "Fastighetssystem",
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
