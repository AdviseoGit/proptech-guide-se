def add_to_sitemap():
    import xml.etree.ElementTree as ET
    from datetime import datetime

    sitemap_path = "/data/workspace/projects/proptech-guide-se/static/sitemap.xml"
    try:
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        ET.register_namespace('', namespace['ns'])

        exists = False
        for url in root.findall('ns:url', namespace):
            loc = url.find('ns:loc', namespace)
            if loc is not None and loc.text == 'https://proptechguiden.se/llms.txt':
                exists = True
                break

        if not exists:
            new_url = ET.Element('url')
            loc = ET.SubElement(new_url, 'loc')
            loc.text = 'https://proptechguiden.se/llms.txt'
            lastmod = ET.SubElement(new_url, 'lastmod')
            lastmod.text = datetime.now().strftime('%Y-%m-%d')
            root.append(new_url)
            tree.write(sitemap_path, encoding='utf-8', xml_declaration=True)
            print("Added /llms.txt to sitemap.xml")
        else:
            print("/llms.txt already in sitemap.xml")
    except Exception as e:
        print(f"Error modifying sitemap: {e}")

if __name__ == "__main__":
    add_to_sitemap()
