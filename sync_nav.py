"""Synka global navigering och footer på de handskrivna sidorna.

Nav och footer har klistrats in för hand i varje HTML-fil, vilket gjort att
menyerna glidit isär — vissa sidor saknar länkar som andra har. Det här skriptet
byter ut <nav> och <footer> mot den delade markupen från site_template, så att
målgruppsindelningen finns överallt.

Sidor som genereras av build.py hoppas över — de får redan rätt markup därifrån.

Kör:  python sync_nav.py
"""
from pathlib import Path

from bs4 import BeautifulSoup

import site_template as T

STATIC = Path(__file__).parent / "static"

# Genereras av build.py, ska inte röras här.
GENERATED = {
    "index.html", "directory.html", "fastighetsagare.html", "forvaltare.html",
    "brf.html", "verktyg.html", "guider.html", "for-leverantorer.html",
}

# Vilken menypost som ska markeras aktiv per sida.
ACTIVE = {
    "roi-kalkylator.html": "verktyg",
    "digital-trapphustavla-kalkylator.html": "verktyg",
    "proptech-kalkylator.html": "verktyg",
    "kategorier.html": "directory",
}


def sync(path):
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    active = ACTIVE.get(path.name, "guider" if path.name.endswith("-guide.html") else "")
    changed = False

    nav_el = soup.find("nav")
    if nav_el:
        # Den gamla mobilmenyn låg som en separat div efter <nav> och ingår nu
        # i den delade markupen — ta bort den så den inte dubbleras.
        old_mobile = soup.find(id="mobile-menu")
        if old_mobile and old_mobile is not nav_el and not nav_el.find(id="mobile-menu"):
            old_mobile.decompose()

        # På vissa sidor ligger navigeringen inbäddad i en <header> med egen
        # hamburgerknapp runt omkring. Byts bara <nav> ut blir resten kvar som
        # föräldralös markup, så hela headern ersätts i de fallen.
        target = nav_el.find_parent("header") or nav_el
        target.replace_with(BeautifulSoup(T.nav(active), "html.parser"))
        changed = True

    # Knappen som togglade den gamla menyn finns inte i den delade markupen.
    # Ligger den kvar syns en död hamburgare, och sidans JS kraschar på den.
    for stale in soup.find_all(id="mobile-menu-btn"):
        stale.decompose()

    footer_el = soup.find("footer")
    if footer_el:
        new_footer = BeautifulSoup(T.footer(), "html.parser").find("footer")
        footer_el.replace_with(new_footer)
        changed = True

    if changed:
        path.write_text(str(soup), encoding="utf-8")
    return changed


def main():
    updated = 0
    for path in sorted(STATIC.glob("*.html")):
        if path.name in GENERATED:
            continue
        if sync(path):
            updated += 1
            print(f"  {path.name}")
    print(f"Synkade nav/footer på {updated} sidor.")


if __name__ == "__main__":
    main()
