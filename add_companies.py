import json

companies_file = '/data/workspace/projects/proptech-guide-se/data/companies.json'

with open(companies_file, 'r') as f:
    companies = json.load(f)

new_companies = [
    {
        "name": "EcoGuard",
        "url": "https://www.ecoguard.se/",
        "description": "Ledande inom IMD (Individuell mätning och debitering) och temperaturmätning. Hjälper bostadsbolag att visualisera och optimera energiförbrukningen med trådlösa sensorer.",
        "category": "energi",
        "category_label": "Energi & Hållbarhet"
    },
    {
        "name": "Infracontrol",
        "url": "https://www.infracontrol.com/",
        "description": "Oberoende plattform (Infracontrol Online) för driftövervakning, felanmälan och IoT i den smarta staden. Integrerar fastighetssystem, infrastruktur och sensorer i en vy.",
        "category": "plattform",
        "category_label": "Öppen Plattform"
    },
    {
        "name": "Fastout",
        "url": "https://www.fastout.com/",
        "description": "Skapar interaktiva 360°-drönarvyer och digitala tvillingar av områden och fastigheter. Används flitigt av mäklare och fastighetsbolag för uthyrning och marknadsföring.",
        "category": "uthyrning",
        "category_label": "Uthyrning & Marknad"
    }
]

companies.extend(new_companies)

with open(companies_file, 'w') as f:
    json.dump(companies, f, indent=4, ensure_ascii=False)

print(f"Added {len(new_companies)} companies. Total: {len(companies)}")
