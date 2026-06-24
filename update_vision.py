import re
with open("/data/workspace/projects/proptech-guide-se/SITE_VISION.md", "r") as f:
    content = f.read()

new_log = "  - 2026-06-24: 49 företag (43→49, +Avtal24/Lexly, Boappa, Bemsiq, +3 previous).\n"
target = "  - 2026-06-23: 43 företag"

content = content.replace(target, new_log + target)

with open("/data/workspace/projects/proptech-guide-se/SITE_VISION.md", "w") as f:
    f.write(content)
