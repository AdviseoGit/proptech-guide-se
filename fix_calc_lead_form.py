import re

calc_path = "/data/workspace/projects/proptech-guide-se/static/digital-trapphustavla-kalkylator.html"
with open(calc_path, "r") as f:
    content = f.read()

# Add script if missing
if "lead-engine.js" not in content:
    content = content.replace("</body>", '<script src="/lead-engine.js"></script>\n</body>')

with open(calc_path, "w") as f:
    f.write(content)

roi_path = "/data/workspace/projects/proptech-guide-se/static/roi-kalkylator.html"
with open(roi_path, "r") as f:
    content = f.read()

if "lead-engine.js" not in content:
    content = content.replace("</body>", '<script src="/lead-engine.js"></script>\n</body>')

with open(roi_path, "w") as f:
    f.write(content)
    
proptech_calc_path = "/data/workspace/projects/proptech-guide-se/static/proptech-kalkylator.html"
with open(proptech_calc_path, "r") as f:
    content = f.read()

if "lead-engine.js" not in content:
    content = content.replace("</body>", '<script src="/lead-engine.js"></script>\n</body>')

with open(proptech_calc_path, "w") as f:
    f.write(content)
