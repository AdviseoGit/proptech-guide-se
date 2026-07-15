import os

directory = "/data/workspace/projects/proptech-guide-se/static"

def add_link_to_nav(html_content):
    if 'href="/roi-kalkylator"' in html_content:
        return html_content
        
    # Find desktop nav
    desktop_nav_end = html_content.find('</nav>')
    if desktop_nav_end != -1:
        link = '                <a href="/roi-kalkylator" class="text-gray-600 hover:text-blue-600 transition">ROI-Kalkylator</a>\n'
        html_content = html_content[:desktop_nav_end] + link + html_content[desktop_nav_end:]
        
    # Find mobile nav
    mobile_nav_end = html_content.find('</div>\n    </header>')
    if mobile_nav_end != -1:
        link = '            <a href="/roi-kalkylator" class="block px-4 py-2 text-gray-600 hover:bg-gray-50">ROI-Kalkylator</a>\n'
        html_content = html_content[:mobile_nav_end] + link + html_content[mobile_nav_end:]
        
    return html_content

for filename in os.listdir(directory):
    if filename.endswith(".html") and filename != "roi-kalkylator.html":
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content = add_link_to_nav(content)
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Added ROI calc link to {filename}")
