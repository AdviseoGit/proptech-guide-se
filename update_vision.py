import re

vision_file = "/data/workspace/projects/proptech-guide-se/SITE_VISION.md"

with open(vision_file, "r") as f:
    content = f.read()

# Update the directory count in SITE_VISION.md
content = re.sub(r'2026-06-16: 22 företag.*', r'2026-06-16: 22 företag (19→22, +Bostadsregistraturet/Nabo/Metry).\n  - 2026-06-18: 28 företag (22→28, +Kiona/Egain/Nordomatic och bekräftat B/N/M)', content)

# Add lead capture task
if "Lead capture" not in content:
    content = content.replace("- [ ] Hela sajten håller design-nordstjärnan", "- [ ] Lead capture (PDF/Kalkylator) fungerar end-to-end och samlar in e-post via API.\n- [ ] Hela sajten håller design-nordstjärnan")

with open(vision_file, "w") as f:
    f.write(content)
