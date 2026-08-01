import os

with open('/data/workspace/projects/proptech-guide-se/INDEXING_LOG.md', 'r') as f:
    content = f.read()

lines = [
    "https://proptechguiden.se/kategorier | Discovered - currently not indexed | 2026-08-01 | Starka interna länkar tillagda via nav & hem-CTA",
    "https://proptechguiden.se/leverantor/bravida | URL is unknown to Google | 2026-08-01 | Partnerprofil tillagd i sitemap + internt länkad från directory",
    "https://proptechguiden.se/leverantor/chargenode | URL is unknown to Google | 2026-08-01 | Partnerprofil tillagd i sitemap + internt länkad från directory",
    "https://proptechguiden.se/leverantor/ecocloud | URL is unknown to Google | 2026-08-01 | Partnerprofil tillagd i sitemap + internt länkad från directory",
    "https://proptechguiden.se/leverantor/egain | URL is unknown to Google | 2026-08-01 | Partnerprofil tillagd i sitemap + internt länkad från directory",
    "https://proptechguiden.se/leverantor/mestro | URL is unknown to Google | 2026-08-01 | Partnerprofil tillagd i sitemap + internt länkad från directory",
    "https://proptechguiden.se/leverantor/metry | URL is unknown to Google | 2026-08-01 | Partnerprofil tillagd i sitemap + internt länkad från directory"
]

with open('/data/workspace/projects/proptech-guide-se/INDEXING_LOG.md', 'w') as f:
    f.write("# INDEXING_LOG.md - URL:er som Google har svårt med\n\n" + "\n".join(lines))
