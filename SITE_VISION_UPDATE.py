import re

with open('/data/workspace/projects/proptech-guide-se/SITE_VISION.md', 'r') as f:
    content = f.read()

new_list_item = "  - 2026-07-18: 125 företag (115→125, +Nivika, Hyresvärd.se, Smartvatten, HomeRun, Paligo, Iqnect, InviSense, Sally R, Noda, RCO, Hydda, Infobric, Flowbird, Amido, Propely).\n"
content = re.sub(r'(  - 2026-07-17: 115 företag.*?\n)', r'\1' + new_list_item, content)

with open('/data/workspace/projects/proptech-guide-se/SITE_VISION.md', 'w') as f:
    f.write(content)
