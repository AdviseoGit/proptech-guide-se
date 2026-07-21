import re

with open('/data/workspace/projects/proptech-guide-se/static/smarta-byggnader-guide.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add link to sitemap manually if we can't find how it's linked
if '<loc>https://proptechguiden.se/smarta-byggnader-guide</loc>' not in open('/data/workspace/projects/proptech-guide-se/static/sitemap.xml').read():
    sitemap = open('/data/workspace/projects/proptech-guide-se/static/sitemap.xml', 'r').read()
    sitemap = sitemap.replace('</urlset>', '  <url>\n    <loc>https://proptechguiden.se/smarta-byggnader-guide</loc>\n    <lastmod>2026-07-21</lastmod>\n  </url>\n</urlset>')
    with open('/data/workspace/projects/proptech-guide-se/static/sitemap.xml', 'w') as f:
        f.write(sitemap)
else:
    sitemap = open('/data/workspace/projects/proptech-guide-se/static/sitemap.xml', 'r').read()
    sitemap = re.sub(r'(<loc>https://proptechguiden.se/smarta-byggnader-guide</loc>\s*<lastmod>)[^<]+(</lastmod>)', r'\g<1>2026-07-21\g<2>', sitemap)
    with open('/data/workspace/projects/proptech-guide-se/static/sitemap.xml', 'w') as f:
        f.write(sitemap)

# Ensure it is linked from index.html
index_content = open('/data/workspace/projects/proptech-guide-se/static/index.html').read()
if 'smarta-byggnader-guide' not in index_content:
    print("Warning: smarta-byggnader-guide not linked in index.html")
    # let's link it in the categories or main body.
    # We will just append a link in a category card if possible.
