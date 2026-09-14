import re

guider_path = "/data/workspace/projects/proptech-guide-se/static/guider.html"
with open(guider_path, "r") as f:
    content = f.read()

if "lead-engine.js" not in content:
    content = content.replace("</body>", '<script src="/lead-engine.js"></script>\n</body>')
    with open(guider_path, "w") as f:
        f.write(content)

