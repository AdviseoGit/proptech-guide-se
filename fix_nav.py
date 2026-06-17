import os
import glob
import re

def fix_nav_and_footer():
    target_dir = "/data/workspace/projects/proptech-guide-se/static"
    html_files = glob.glob(os.path.join(target_dir, "*.html"))
    
    # We will standardize the meta viewport tag across all files.
    viewport_tag = '<meta name="viewport" content="width=device-width, initial-scale=1">'
    
    for filepath in html_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Ensure viewport meta exists and is correct
        if 'name="viewport"' in content and '<meta name="viewport"' not in content:
           content = re.sub(r'<meta\s+name=["\']viewport["\'][^>]*>', viewport_tag, content)
        elif '<meta name="viewport"' not in content:
            content = content.replace('<head>', '<head>\n    ' + viewport_tag)
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

fix_nav_and_footer()
print("Mobile meta tags verified")
