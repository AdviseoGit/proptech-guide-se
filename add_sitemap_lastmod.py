import re

with open('/data/workspace/projects/proptech-guide-se/static/sitemap.xml', 'r') as f:
    sitemap = f.read()

sitemap = re.sub(r'(<loc>https://proptechguiden.se/ai-i-fastigheter</loc>\s*<lastmod>)[^<]+(</lastmod>)', r'\g<1>2026-07-21\g<2>', sitemap)
sitemap = re.sub(r'(<loc>https://proptechguiden.se/kategorier</loc>\s*<lastmod>)[^<]+(</lastmod>)', r'\g<1>2026-07-21\g<2>', sitemap)
sitemap = re.sub(r'(<loc>https://proptechguiden.se/brf-digitalisering</loc>\s*<lastmod>)[^<]+(</lastmod>)', r'\g<1>2026-07-21\g<2>', sitemap)

with open('/data/workspace/projects/proptech-guide-se/static/sitemap.xml', 'w') as f:
    f.write(sitemap)
