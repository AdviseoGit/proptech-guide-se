import sys

filepath = "/data/workspace/projects/proptech-guide-se/SITE_VISION.md"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("19 företag (16→19, +Accessy/Infobric/Hydda). Fortsätt växa till 20+ för att bli nischens mest kompletta.", "22 företag (19→22, +Bostadsregistraturet/Nabo/Metry). Mål: Håll den uppdaterad och lägg till 1-2 per pass för att befästa positionen som ledande katalog.")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated SITE_VISION.md")
