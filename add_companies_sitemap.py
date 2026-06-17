import sys

filepath = "/data/workspace/projects/proptech-guide-se/static/sitemap.xml"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Just update the directory.html lastmod
import re
content = re.sub(r'<loc>https://proptechguiden.se/directory</loc>\s*<lastmod>[^<]+</lastmod>', '<loc>https://proptechguiden.se/directory</loc>\n    <lastmod>2026-06-17</lastmod>', content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated sitemap")
