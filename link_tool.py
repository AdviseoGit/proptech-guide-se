import re
import os

files_to_update = ['index.html', 'smarta-byggnader-guide.html', 'brf-digitalisering.html', 'kategorier.html', 'om-sajten.html', 'directory.html', 'ai-i-fastigheter.html']

for filename in files_to_update:
    filepath = f'/data/workspace/projects/proptech-guide-se/static/{filename}'
    if not os.path.exists(filepath):
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Link in navbar
    # Look for <a href="/roi-kalkylator" class="hover:text-sky-600">ROI-Kalkylator</a>
    # and insert <a href="/digital-trapphustavla-kalkylator" class="hover:text-sky-600">Trapphustavla-kalkylator</a>
    if '/digital-trapphustavla-kalkylator' not in content:
        content = content.replace(
            '<a href="/roi-kalkylator" class="hover:text-sky-600">ROI-Kalkylator</a>',
            '<a href="/roi-kalkylator" class="hover:text-sky-600">ROI-Kalkylator</a>\n            <a href="/digital-trapphustavla-kalkylator" class="hover:text-sky-600">Trapphustavla-kalkylator</a>'
        )
        content = content.replace(
            '<a href="/roi-kalkylator" class="hover:text-sky-600 block">ROI-Kalkylator</a>',
            '<a href="/roi-kalkylator" class="hover:text-sky-600 block">ROI-Kalkylator</a>\n            <a href="/digital-trapphustavla-kalkylator" class="hover:text-sky-600 block">Trapphustavla-kalkylator</a>'
        )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")

# Add to sitemap
sitemap_path = '/data/workspace/projects/proptech-guide-se/static/sitemap.xml'
with open(sitemap_path, 'r', encoding='utf-8') as f:
    sitemap = f.read()

if '/digital-trapphustavla-kalkylator' not in sitemap:
    sitemap = sitemap.replace('</urlset>', '  <url>\n    <loc>https://proptechguiden.se/digital-trapphustavla-kalkylator</loc>\n    <lastmod>2026-07-21</lastmod>\n  </url>\n</urlset>')
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(sitemap)
    print("Updated sitemap.xml")

