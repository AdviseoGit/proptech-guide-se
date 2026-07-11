import datetime
import re

log_path = "/data/workspace/projects/proptech-guide-se/INDEXING_LOG.md"

with open(log_path, "r", encoding="utf-8") as f:
    content = f.read()

# Hitta raden för directory
date_str = datetime.datetime.now().strftime("%Y-%m-%d")

if "https://proptechguiden.se/directory" in content:
    # Uppdatera befintlig
    content = re.sub(r'https://proptechguiden.se/directory \| .*', 
                     f'https://proptechguiden.se/directory | Discovered - currently not indexed | {date_str} | Fortsatt tillväxt av unikt värde (+5 bolag idag), sitemap uppdaterad', 
                     content)
else:
    content += f"\nhttps://proptechguiden.se/directory | Discovered - currently not indexed | {date_str} | Fortsatt tillväxt av unikt värde (+5 bolag idag), sitemap uppdaterad"

with open(log_path, "w", encoding="utf-8") as f:
    f.write(content)
