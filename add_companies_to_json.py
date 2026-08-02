import json
import sys

def add_companies():
    path = "/data/workspace/projects/proptech-guide-se/data/companies.json"
    with open(path, "r", encoding="utf-8") as f:
        companies = json.load(f)

    new_companies = [
        {
            "slug": "cenvigo",
            "name": "Cenvigo",
            "category": "forvaltning",
            "category_label": "Digital Förvaltning & Drift",
            "description": "Digitaliserar skötsel- och tillsynsprocesser för fastighetsbolag och kommuner med smarta sensorer och automatiska avvikelserapporter. Förbättrar trygghet och minskar manuellt arbete.",
            "url": "https://www.cenvigo.com/",
            "tier": "basic",
            "segments": ["fastighetsagare", "forvaltare"]
        },
        {
            "slug": "zyka",
            "name": "Zyka",
            "category": "energi",
            "category_label": "Energi & Hållbarhet",
            "description": "Zyka erbjuder en AI-driven plattform för att optimera energianvändning och minska koldioxidavtryck i kommersiella fastigheter genom prediktiv styrning.",
            "url": "https://www.zyka.io/",
            "tier": "basic",
            "segments": ["fastighetsagare", "forvaltare"]
        },
        {
            "slug": "navetti",
            "name": "Navetti",
            "category": "plattform",
            "category_label": "Öppna Plattformar & Integration",
            "description": "Erbjuder integrationslösningar som möjliggör sömlöst informationsflöde mellan olika proptech-system och underlättar skapandet av smarta, uppkopplade byggnader.",
            "url": "https://navetti.com/",
            "tier": "basic",
            "segments": ["fastighetsagare", "forvaltare"]
        }
    ]

    added = 0
    names = [c["name"] for c in companies]
    for c in new_companies:
        if c["name"] not in names:
            companies.append(c)
            added += 1

    with open(path, "w", encoding="utf-8") as f:
        json.dump(companies, f, indent=4, ensure_ascii=False)

    print(f"Added {added} companies. Total: {len(companies)}")

if __name__ == "__main__":
    add_companies()
