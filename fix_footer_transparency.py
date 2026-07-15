import os
import glob

def ensure_transparency_in_files():
    static_dir = "/data/workspace/projects/proptech-guide-se/static"
    html_files = glob.glob(os.path.join(static_dir, "*.html"))
    
    transparency_html = '<p class="text-xs text-gray-500 mt-6">Denna sajt skapas och drivs helt av AI · <a href="/om-sajten" class="hover:text-gray-300">Om sajten</a></p>'
    
    for file_path in html_files:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        if transparency_html not in content and "skapas och drivs helt av AI" not in content:
            # find footer
            footer_end = content.find("</footer>")
            if footer_end != -1:
                # find the last div before footer closes
                last_div = content.rfind("</div>", 0, footer_end)
                if last_div != -1:
                    new_content = content[:last_div] + '            ' + transparency_html + '\n        ' + content[last_div:]
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"Added transparency to {os.path.basename(file_path)}")
                else:
                    print(f"Could not find div to inject in {os.path.basename(file_path)}")
            else:
                print(f"No footer in {os.path.basename(file_path)}")

ensure_transparency_in_files()
