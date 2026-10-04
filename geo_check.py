"""GEO-check for /digital-trapphustavla.

Scores the page against five criteria (20 pts each) → max 100.
Run with:  python geo_check.py
"""
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

PAGE_FILE = "static/digital-trapphustavla.html"
SITEMAP_FILE = "static/sitemap.xml"
INDEXED_PAGES = [
    "static/verktyg.html",
    "static/brf.html",
    "static/index.html",
]
TARGET_URL = "https://proptechguiden.se/digital-trapphustavla"


def check_file_exists() -> tuple[bool, str]:
    ok = os.path.isfile(PAGE_FILE)
    return ok, f"File {PAGE_FILE} {'exists (200)' if ok else 'MISSING (404)'}"


def check_in_sitemap() -> tuple[bool, str]:
    try:
        tree = ET.parse(SITEMAP_FILE)
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls = [loc.text.strip() for loc in tree.findall(".//sm:loc", ns)]
        ok = TARGET_URL in urls
        return ok, f"Sitemap {'contains' if ok else 'MISSING'} {TARGET_URL}"
    except Exception as e:
        return False, f"Sitemap parse error: {e}"


def check_internal_link() -> tuple[bool, str]:
    for path in INDEXED_PAGES:
        try:
            with open(path, encoding="utf-8") as fh:
                content = fh.read()
            if "/digital-trapphustavla" in content:
                return True, f"Internal link found in {path}"
        except FileNotFoundError:
            pass
    return False, f"No internal link to /digital-trapphustavla in {INDEXED_PAGES}"


def check_faqpage_schema() -> tuple[bool, str]:
    try:
        with open(PAGE_FILE, encoding="utf-8") as fh:
            content = fh.read()
        scripts = re.findall(
            r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            content, re.DOTALL
        )
        for raw in scripts:
            try:
                data = json.loads(raw)
                if data.get("@type") == "FAQPage":
                    entities = data.get("mainEntity", [])
                    if len(entities) >= 2:
                        return True, f"FAQPage JSON-LD schema found with {len(entities)} questions"
            except json.JSONDecodeError:
                pass
        return False, "No valid FAQPage JSON-LD schema found"
    except Exception as e:
        return False, f"Error reading page: {e}"


def check_comparison_table() -> tuple[bool, str]:
    try:
        with open(PAGE_FILE, encoding="utf-8") as fh:
            content = fh.read()
        has_table = "<table" in content
        has_thead = "<thead" in content
        if has_table and has_thead:
            return True, "Comparison table (thead+tbody) found"
        return False, "No comparison table found"
    except Exception as e:
        return False, f"Error reading page: {e}"


CHECKS = [
    ("Fil returnerar 200", check_file_exists),
    ("URL finns i sitemap", check_in_sitemap),
    ("Intern länk från indexerad sida", check_internal_link),
    ("FAQPage JSON-LD schema", check_faqpage_schema),
    ("Jämförelsetabell", check_comparison_table),
]


def main():
    score = 0
    print("GEO-check: /digital-trapphustavla\n" + "=" * 40)
    for label, fn in CHECKS:
        ok, msg = fn()
        pts = 20 if ok else 0
        score += pts
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] +{pts:>2}/20  {label}")
        print(f"          {msg}")
    print("=" * 40)
    print(f"TOTAL: {score}/100")
    if score < 100:
        sys.exit(1)


if __name__ == "__main__":
    main()
