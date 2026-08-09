import re

file_path = "static/index.html"
with open(file_path, "r") as f:
    content = f.read()

# Optimera title
content = re.sub(
    r'<title>.*?</title>',
    r'<title>Proptechguiden | Guide till digitalisering av svenska fastigheter</title>',
    content
)

# Optimera description
content = re.sub(
    r'<meta name="description" content=".*?">',
    r'<meta name="description" content="Din oberoende guide till fastighetsteknik och proptech i Sverige. Jämför leverantörer, räkna på ROI och hitta rätt digitala lösning för din fastighet eller BRF.">',
    content
)
if '<meta name="description"' not in content and '<meta content=' not in content:
   content = content.replace("</title>", "</title>\n    <meta name=\"description\" content=\"Din oberoende guide till fastighetsteknik och proptech i Sverige. Jämför leverantörer, räkna på ROI och hitta rätt digitala lösning för din fastighet eller BRF.\">")


with open(file_path, "w") as f:
    f.write(content)
print("Updated index SEO.")
