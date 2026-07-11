import re

vision_path = "/data/workspace/projects/proptech-guide-se/SITE_VISION.md"

with open(vision_path, "r", encoding="utf-8") as f:
    content = f.read()

# Hitta "2026-07-10: 90 företag" och lägg till vår nya rad
new_line = "  - 2026-07-11: 95 företag (90→95, +Mestro, Sengera, Enjay, Bostadsregistraturet, Pico).\n"
content = re.sub(r'(- \[ \] Verktygssidan är TUNN.*?\n)', r'\1' + new_line, content)

with open(vision_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Vision updated.")
