import os
from datetime import datetime

def generate_sitemap(directory, base_url):
    urls = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                # Skip the privacy policy from the sitemap
                if file == "privacy-policy.html":
                    continue
                path = os.path.join(root, file)
                # Create a URL path by removing the directory and the .html extension
                url_path = os.path.relpath(path, directory).replace('.html', '')
                # Handle index.html as the root
                if url_path == 'index':
                    url_path = ''
                urls.append(f"{base_url}/{url_path}")

    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in urls:
        sitemap_xml += '  <url>\n'
        sitemap_xml += f'    <loc>{url}</loc>\n'
        sitemap_xml += f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>\n'
        sitemap_xml += '  </url>\n'
    sitemap_xml += '</urlset>'
    return sitemap_xml

if __name__ == "__main__":
    sitemap = generate_sitemap("/data/workspace/projects/proptech-guide-se/static", "https://proptechguiden.se")
    with open("/data/workspace/projects/proptech-guide-se/static/sitemap.xml", "w") as f:
        f.write(sitemap)
    print("Sitemap generated successfully.")
