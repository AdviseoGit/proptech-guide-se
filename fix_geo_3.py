import re
import os

def fix_all_missing_geo():
    pages = ["verktyg.html", "kategorier.html", "guider.html", "directory.html", "index.html"]
    
    schema = """
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "WebPage",
      "dateModified": "2026-08-02"
    }
    </script>
    """
    
    for page in pages:
        path = f"/data/workspace/projects/proptech-guide-se/static/{page}"
        if not os.path.exists(path):
            continue
        with open(path, "r", encoding="utf-8") as f:
            html = f.read()
        
        # Add basic schema if not present (WebPage is better than nothing, but let's add FAQ for some)
        if 'application/ld+json' not in html:
            html = html.replace('</head>', schema + '\n</head>')
            
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
            
if __name__ == "__main__":
    fix_all_missing_geo()
