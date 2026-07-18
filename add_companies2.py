import re
import sys

def add_companies():
    html_file = '/data/workspace/projects/proptech-guide-se/static/directory.html'
    
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    new_companies = [
        {
            "name": "Iqnect",
            "category": "plattform",
            "desc": "Proptech-plattform som samlar data från olika system i fastigheter för att ge en enhetlig vy och möjlighet till datadriven optimering.",
            "url": "https://iqnect.se/"
        },
        {
            "name": "InviSense",
            "category": "sakerhet",
            "desc": "Utvecklar mikrotunna fuktsensorer som mäts trådlöst och möjliggör tidig upptäckt av fukt i byggnadskonstruktioner.",
            "url": "https://invisense.com/"
        },
        {
            "name": "Sally R",
            "category": "energi",
            "desc": "Optimerar ventilation i kommersiella byggnader med hjälp av AI och algoritmbaserad styrning för att spara energi och förbättra luftkvalitet.",
            "url": "https://sally-r.com/"
        },
        {
            "name": "Noda Intelligent Systems",
            "category": "energi",
            "desc": "Levererar AI-baserade lösningar för optimering av fjärrvärme och kylsystem i fastigheter och hela nätverk.",
            "url": "https://noda.se/"
        },
        {
            "name": "RCO Security",
            "category": "sakerhet",
            "desc": "Svensk tillverkare av passerkontroll och säkerhetssystem för fastigheter, med fokus på integration och smarta lösningar.",
            "url": "https://www.rco.se/"
        }
    ]
    
    grid_end_match = re.search(r'(</main>)', html_content)
    if not grid_end_match:
        print("Could not find </main>")
        return
        
    grid_end_pos = html_content.rfind('</div>', 0, grid_end_match.start())
    if grid_end_pos == -1:
        print("Could not find end of grid")
        return
        
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
