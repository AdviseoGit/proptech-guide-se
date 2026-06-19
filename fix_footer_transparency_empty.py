import os

files = [
    "/data/workspace/projects/proptech-guide-se/static/vad-ar-proptech.html",
    "/data/workspace/projects/proptech-guide-se/static/proptech-losningar.html",
    "/data/workspace/projects/proptech-guide-se/static/ai-i-fastigheter-artikel.html"
]

standard_footer = """<footer class="py-12 border-t border-slate-200 text-center text-slate-500 mt-auto w-full"><div class="space-x-4"><a href="/om-oss" class="hover:text-sky-600">Om oss</a><a href="/privacy-policy" class="hover:text-sky-600">Integritetspolicy</a></div><p class="mt-2 text-sm text-slate-400">Denna sajt skapas och drivs helt av AI &middot; <a href="/om-oss" class="hover:text-sky-600">Om sajten</a></p><p class="mt-4">© 2026 Proptech Guide Sverige | Utvecklad av Adviseo</p></footer>"""

for filepath in files:
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace empty footer or add standard footer before </body>
        import re
        content = re.sub(r'<footer[^>]*>.*?</footer>', standard_footer, content, flags=re.DOTALL)
        
        if standard_footer not in content:
            content = content.replace('</body>', f'{standard_footer}</body>')
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {os.path.basename(filepath)}")
