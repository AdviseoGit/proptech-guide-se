import os
import glob
import re

STATIC_DIR = "/data/workspace/projects/proptech-guide-se/static"

# Find all HTML files
html_files = glob.glob(os.path.join(STATIC_DIR, "*.html"))

# Footer regex to find the paragraph with copyright
footer_regex = re.compile(r'(<footer[^>]*>.*?)(<p[^>]*>© 2026.*?)(</footer>)', re.IGNORECASE | re.DOTALL)

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if transparency notice is already there
    if "Denna sajt skapas och drivs helt av AI" in content:
        continue
        
    # Replace footer
    ai_notice = '<p class="mt-2 text-sm text-slate-400">Denna sajt skapas och drivs helt av AI &middot; <a href="/om-oss" class="hover:text-sky-600">Om sajten</a></p>'
    
    new_content = footer_regex.sub(rf'\1{ai_notice}\2\3', content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Added transparency to {os.path.basename(filepath)}")
    else:
        print(f"Could not find footer pattern in {os.path.basename(filepath)}")

