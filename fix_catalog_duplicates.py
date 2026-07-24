"""Engångsstädning av katalogen: slå ihop dubbletter och karantänsätt overifierade poster.

Namnbaserad deduplicering fångar inte samma bolag under olika namn, och den fångar
inte poster som aldrig borde ha lagts in. Underlaget nedan är kontrollerat mot
publika källor i juli 2026.

Kör:  python fix_catalog_duplicates.py
"""
import json
from pathlib import Path

DATA = Path(__file__).parent / "data"

# Samma bolag under flera namn. Nyckeln är slugen som behålls, resten tas bort.
# Den behållna posten skrivs över med de kontrollerade uppgifterna.
MERGES = {
    # Avy och Tmpl gick ihop i februari 2022 och driver en gemensam plattform.
    "avy": {
        "absorb": ["tmpl-avy"],
        "name": "Avy-Tmpl",
        "category": "boende",
        "url": "https://www.avy.se",
        "description": (
            "Boendeapp och plattform för hyresvärdar och BRF:er. Samlar felanmälan, "
            "digital boendepärm, bokning av gemensamma resurser och kommunikation med "
            "de boende. Bildades när Avy och Tmpl gick ihop 2022."
        ),
    },
    # Mestro är ett energiuppföljningsbolag. Posten "Mestro" beskrev arbetsorder
    # och underhåll, vilket är fel bolag, och "Mestro Energy" låg på en domän som
    # inte går att belägga.
    "mestro": {
        "absorb": ["mestro-energy"],
        "name": "Mestro",
        "category": "energi",
        "url": "https://mestro.com",
        "description": (
            "Molnbaserad plattform för automatiserad energiuppföljning. Samlar in och "
            "visualiserar energidata från el, värme och vatten i realtid, med moduler "
            "för hållbarhetsrapportering och kostnadskontroll."
        ),
    },
}

# Poster där webbadressen saknades och nu är kontrollerad.
URL_FIXES = {
    "enjay": "https://www.enjaysystems.com",
}

# Poster som inte gått att belägga i någon publik källa. De tas ur den publicerade
# katalogen men sparas i companies_unverified.json så inget går förlorat.
# En oberoende leverantörsguide kan inte lista bolag som inte går att verifiera.
QUARANTINE = ["pico", "sengera"]


def main():
    path = DATA / "companies.json"
    companies = json.loads(path.read_text(encoding="utf-8"))
    by_slug = {c["slug"]: c for c in companies}

    removed = set()

    for keep_slug, spec in MERGES.items():
        target = by_slug.get(keep_slug)
        if not target:
            print(f"  hoppar över {keep_slug} — finns inte i katalogen")
            continue
        for absorbed in spec["absorb"]:
            if absorbed in by_slug:
                removed.add(absorbed)
                print(f"  slår ihop {by_slug[absorbed]['name']} -> {spec['name']}")
        target["name"] = spec["name"]
        target["category"] = spec["category"]
        target["url"] = spec["url"]
        target["description"] = spec["description"]

    for slug, url in URL_FIXES.items():
        if slug in by_slug:
            by_slug[slug]["url"] = url
            print(f"  webbadress för {by_slug[slug]['name']}: {url}")

    quarantined = [by_slug[s] for s in QUARANTINE if s in by_slug]
    removed.update(s for s in QUARANTINE if s in by_slug)
    for c in quarantined:
        print(f"  karantän: {c['name']} (kunde inte verifieras)")

    kept = [c for c in companies if c["slug"] not in removed]
    kept.sort(key=lambda c: c["name"].lower())
    path.write_text(json.dumps(kept, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if quarantined:
        qpath = DATA / "companies_unverified.json"
        existing = json.loads(qpath.read_text(encoding="utf-8")) if qpath.exists() else []
        known = {c["slug"] for c in existing}
        existing += [c for c in quarantined if c["slug"] not in known]
        qpath.write_text(json.dumps(existing, ensure_ascii=False, indent=2) + "\n",
                         encoding="utf-8")

    print(f"\n{len(companies)} -> {len(kept)} bolag i den publicerade katalogen")


if __name__ == "__main__":
    main()
