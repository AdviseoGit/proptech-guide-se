log_entry = "https://proptechguiden.se/roi-kalkylator | URL is unknown to Google | 2026-07-15 | Länkad i nav + sitemap tillagd"

with open("/data/workspace/projects/proptech-guide-se/INDEXING_LOG.md", "a") as f:
    f.write(log_entry + "\n")
print("Added to indexing log.")
