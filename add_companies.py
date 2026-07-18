import re
import sys

def add_companies():
    html_file = '/data/workspace/projects/proptech-guide-se/static/directory.html'
    
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    new_companies = [
        {
            "name": "Nivika",
            "category": "forvaltning",
            "desc": "Proptech-drivet fastighetsbolag som använder digitala verktyg för effektiv förvaltning, hyresgästkommunikation och energioptimering.",
            "url": "https://nivika.se"
        },
        {
            "name": "Hyresvärd.se",
            "category": "plattform",
            "desc": "Digital plattform som förenklar och effektiviserar uthyrningsprocessen för både privata och kommersiella hyresvärdar.",
            "url": "https://hyresvard.se"
        },
        {
            "name": "Smartvatten",
            "category": "energi",
            "desc": "Kamerabaserad och AI-driven vattenövervakning som automatiskt läser av vattenmätare, upptäcker läckage och hjälper fastighetsägare att minska vattenförbrukningen.",
            "url": "https://smartvatten.com/sv/"
        },
        {
            "name": "HomeRun",
            "category": "boende",
            "desc": "Plattform för bostadsutvecklare och entreprenörer som hanterar tillval, kommunikation och ärenden under och efter byggprocessen.",
            "url": "https://www.homerun.net/sv"
        },
        {
            "name": "Paligo",
            "category": "plattform",
            "desc": "Även om det främst är ett CCMS, används det inom proptech för att hantera komplex teknisk dokumentation och manualer för smarta byggnader och system.",
            "url": "https://paligo.net/"
        }
    ]
    
    # Find the end of the grid container
    # Looking for a closing div right before the javascript or footer
    grid_end_match = re.search(r'(</main>)', html_content)
    if not grid_end_match:
        print("Could not find </main>")
        return
        
    grid_end_pos = html_content.rfind('</div>', 0, grid_end_match.start())
    if grid_end_pos == -1:
        print("Could not find end of grid")
        return
        
    # Build HTML for new companies
    new_html = ""
    for c in new_companies:
        new_html += f"""
        <!-- {c['name']} -->
        <div class="company-card bg-white rounded-2xl p-6 shadow-sm border border-slate-100 hover:shadow-md transition-shadow" data-category="{c['category']}">
            <div class="w-12 h-12 bg-sky-100 rounded-xl flex items-center justify-center text-sky-600 font-bold text-xl mb-4">
                {c['name'][0]}
            </div>
            <h3 class="text-xl font-bold text-slate-900 mb-2">{c['name']}</h3>
            <p class="text-slate-600 mb-6">{c['desc']}</p>
            <a href="{c['url']}" target="_blank" rel="noopener noreferrer" class="text-sky-600 font-medium hover:text-sky-700 inline-flex items-center">
                Besök hemsida
                <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path>
                </svg>
            </a>
        </div>
"""
    
    new_content = html_content[:grid_end_pos] + new_html + html_content[grid_end_pos:]
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print(f"Added {len(new_companies)} companies.")

if __name__ == '__main__':
    add_companies()
