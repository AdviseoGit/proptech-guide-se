import json

companies_file = '/data/workspace/projects/proptech-guide-se/data/companies.json'

with open(companies_file, 'r') as f:
    companies = json.load(f)

new_companies = [
    {
        "name": "Nivika",
        "url": "https://nivika.se/",
        "description": "Fastighetsbolag med starkt fokus på proptech-integration och hållbarhet i sina bestånd. Visar på praktisk användning av digitala tvillingar.",
        "category": "plattform",
        "category_label": "Öppen Plattform",
        "segments": ["fastighetsagare"]
    },
    {
        "name": "Infobric",
        "url": "https://infobric.se/",
        "description": "Digitala lösningar för bygg- och fastighetsbranschen, inklusive passersystem, fordonsuppföljning och maskinstyrning.",
        "category": "passer",
        "category_label": "Passersystem",
        "segments": ["fastighetsagare", "forvaltare"]
    },
    {
        "name": "Flowbird",
        "url": "https://flowbird.se/",
        "description": "Smarta mobilitets- och parkeringslösningar för fastighetsägare och städer, med integrationer mot digitala betalplattformar.",
        "category": "parkering",
        "category_label": "Parkering & Mobilitet",
        "segments": ["fastighetsagare", "forvaltare", "brf"]
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
