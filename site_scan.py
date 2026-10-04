"""Scan all sitemap URLs and verify that the corresponding static file exists.

Prints OK / 404 per URL and exits non-zero if any 404s are found.
Bug that was fixed: empty path (root URL https://…/) previously mapped to
static/.html which doesn't exist.  Now explicitly handled as index.html.
"""
import sys
import xml.etree.ElementTree as ET

SITEMAP = "static/sitemap.xml"
STATIC_DIR = "static"
BASE_URL = "https://proptechguiden.se"


def url_to_file(url: str) -> str:
    path = url.removeprefix(BASE_URL)
    # Strip trailing slash
    path = path.rstrip("/")
    if path == "" or path == "/":
        return f"{STATIC_DIR}/index.html"
    # Strip leading slash and append .html
    rel = path.lstrip("/")
    return f"{STATIC_DIR}/{rel}.html"


def main():
    import os

    tree = ET.parse(SITEMAP)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [loc.text.strip() for loc in tree.findall(".//sm:loc", ns)]

    failures = []
    for url in urls:
        fp = url_to_file(url)
        status = "OK  " if os.path.isfile(fp) else "404 "
        print(f"{status} {url}  →  {fp}")
        if status.strip() == "404":
            failures.append(url)

    print(f"\n{len(urls) - len(failures)}/{len(urls)} OK", end="")
    if failures:
        print(f"  |  {len(failures)} FAILED:")
        for f in failures:
            print(f"     {f}")
        sys.exit(1)
    else:
        print("  — all clear")


if __name__ == "__main__":
    main()
