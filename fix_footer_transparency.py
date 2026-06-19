import os
import glob

STATIC_DIR = "/data/workspace/projects/proptech-guide-se/static"

# Find all HTML files
html_files = glob.glob(os.path.join(STATIC_DIR, "*.html"))

ai_notice = '<p class="mt-2 text-sm text-slate-400">Denna sajt skapas och drivs helt av AI &middot; <a href="/om-oss" class="hover:text-sky-600">Om sajten</a></p>'

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "Denna sajt skapas och drivs helt av AI" not in content:
        # Try replacing the specific end of footer paragraph
        if "© 2026 Proptech Guide Sverige | Utvecklad av Adviseo</p>" in content:
            new_content = content.replace("© 2026 Proptech Guide Sverige | Utvecklad av Adviseo</p>", f"{ai_notice}<p class=\"mt-4\">© 2026 Proptech Guide Sverige | Utvecklad av Adviseo</p>")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Fixed {os.path.basename(filepath)}")
        else:
             print(f"Still failing on {os.path.basename(filepath)}")

