import re

with open('/data/workspace/projects/proptech-guide-se/static/proptech-kalkylator.html', 'r') as f:
    content = f.read()

content = content.replace('<title>ROI Kalkylator för PropTech | Proptech Guide Sverige</title>', '<title>PropTech ROI-kalkylator | Räkna ut din avkastning & spara pengar</title>')

with open('/data/workspace/projects/proptech-guide-se/static/proptech-kalkylator.html', 'w') as f:
    f.write(content)

