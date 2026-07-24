"""One-off migration: lyft ut bolagen ur static/directory.html till data/companies.json.

Katalogen har hittills varit hårdkodad HTML. Datat behöver vara strukturerat för att
kunna bära tier (fri/verifierad/partner), segment och sponsorplaceringar.
"""
import json
import re
import unicodedata
from pathlib import Path

from bs4 import BeautifulSoup

# Kategori -> vilka målgrupper som normalt köper i kategorin.
CATEGORY_SEGMENTS = {
    "forvaltning": ["fastighetsagare", "forvaltare", "brf"],
    "energi": ["fastighetsagare", "forvaltare", "brf"],
    "iot": ["fastighetsagare", "forvaltare"],
    "access": ["fastighetsagare", "forvaltare", "brf"],
    "uthyrning": ["fastighetsagare", "forvaltare"],
    "boende": ["forvaltare", "brf"],
    "analys": ["fastighetsagare", "forvaltare"],
    "plattform": ["fastighetsagare", "forvaltare"],
}

# Kategorier som smugit in utanför filtrets värdelista och därför blivit osynliga
# i katalogens filtrering. Mappas till närmaste giltiga kategori.
CATEGORY_ALIASES = {
    "smarta-byggnader-passersystem": "access",
    "sakerhet": "access",
    "drönare": "iot",
    "kundresa-uthyrning": "uthyrning",
    "fastighetssystem": "forvaltning",
    # En äldre korttyp använde en helt egen taxonomi.
    "energi-miljo": "energi",
    "smart-hem-boende": "boende",
    "drift-underhall": "forvaltning",
    "bygg-anlaggning": "forvaltning",
    "plattform-integration": "plattform",
}

CATEGORY_LABELS = {
    "forvaltning": "Digital Förvaltning & Drift",
    "energi": "Energi & Hållbarhet",
    "iot": "IoT & Hårdvara",
    "access": "Lås & Passagesystem",
    "uthyrning": "Uthyrning & Marknad",
    "boende": "Boendeapp & Hyresgäst",
    "analys": "Analys & AI",
    "plattform": "Öppen Plattform",
}


def slugify(name):
    text = unicodedata.normalize("NFKD", name.lower())
    text = text.replace("ä", "a").replace("å", "a").replace("ö", "o")
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def main():
    root = Path(__file__).parent
    html = (root / "static" / "directory.html").read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    companies = []
    seen = set()
    skipped = []
    duplicates = []
    # Katalogen innehåller två korttyper: en nyare med <h3> och en äldre med <h2>.
    # Letas bara efter h3 försvinner den äldre typen tyst ur katalogen. Krockar
    # namnen vinner det nyare kortet, som är det mer aktuellt kurerade.
    cards = soup.select(".company-card")
    ordered = [c for c in cards if c.find("h3")] + [c for c in cards if not c.find("h3")]

    for card in ordered:
        name_el = card.find(["h3", "h2"])
        if not name_el:
            skipped.append(card.get_text(" ", strip=True)[:60])
            continue
        name = name_el.get_text(strip=True)
        slug = slugify(name)
        if not slug:
            skipped.append(name)
            continue
        if slug in seen:
            duplicates.append(name)
            continue
        seen.add(slug)

        category = card.get("data-category", "forvaltning")
        category = CATEGORY_ALIASES.get(category, category)
        paragraphs = card.find_all("p")
        description = paragraphs[-1].get_text(strip=True) if paragraphs else ""
        link = card.find("a", href=True)
        url = link["href"] if link else ""

        companies.append({
            "slug": slug,
            "name": name,
            "category": category,
            "category_label": CATEGORY_LABELS.get(category, category),
            "description": description,
            "url": url,
            # Monetiseringsfält — allt startar på gratisnivå.
            "tier": "free",
            "segments": CATEGORY_SEGMENTS.get(category, ["fastighetsagare"]),
            "usp": [],
            "cases": [],
            "logo": "",
            "contact_email": "",
            "receives_leads": False,
        })

    companies.sort(key=lambda c: c["name"].lower())
    out = root / "data" / "companies.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(companies, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Skrev {len(companies)} bolag till {out}")
    print(f"Dubbletter som slogs ihop: {len(duplicates)}")
    if skipped:
        # Ska aldrig hända tyst — ett kort utan läsbart namn är data vi tappar.
        print(f"VARNING: {len(skipped)} kort kunde inte tolkas: {skipped}")


if __name__ == "__main__":
    main()
