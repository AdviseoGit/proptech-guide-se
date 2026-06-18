import re
import datetime

NEW_COMPANIES = [
    {
        "name": "Bostadsregistraturet",
        "category": "Administration",
        "description": "Digitalt lägenhetsregister och överlåtelsehantering för bostadsrättsföreningar och förvaltare.",
        "url": "https://www.bostadsregistraturet.se"
    },
    {
        "name": "Nabo",
        "category": "Administration",
        "description": "Helhetsleverantör av ekonomisk och teknisk förvaltning samt juridik med en egen digital plattform för BRF:er.",
        "url": "https://nabo.se"
    },
    {
        "name": "Metry",
        "category": "Energi",
        "description": "Plattform som automatiserar insamling av energidata från alla dina mätare till ett enda system för enklare uppföljning och hållbarhetsrapportering.",
        "url": "https://metry.io"
    },
    {
        "name": "Kiona",
        "category": "Energi",
        "description": "Öppen och oberoende PropTech-plattform för fastighetsautomation, energistyrning (Edge) och energiuppföljning.",
        "url": "https://kiona.com"
    },
    {
        "name": "Egain",
        "category": "Energi",
        "description": "AI-baserad mjukvara för energioptimering och klimatstyrning av fastigheter med fokus på minskade kostnader och utsläpp.",
        "url": "https://egain.io"
    },
    {
        "name": "Nordomatic",
        "category": "Drift",
        "description": "Ledande integratör av Smart Buildings med lösningar för BMS (Building Management Systems) och energioptimering.",
        "url": "https://nordomatic.com"
    }
]

HTML_FILE = "/data/workspace/projects/proptech-guide-se/static/directory.html"

def read_html(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def write_html(filepath, content):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

def add_companies():
    html_content = read_html(HTML_FILE)
    
    # We'll inject right before the closing div of the grid
    grid_end_marker = "<!-- End of Company Grid -->"
    
    if grid_end_marker not in html_content:
        # Create the marker if it doesn't exist. Find the last </div> before </main>
        # Just use a regex to find where to insert.
        match = re.search(r'</div>\s*</main>', html_content)
        if match:
            # We'll insert the marker right there
             html_content = html_content[:match.start()] + "\n        <!-- End of Company Grid -->\n    </div>\n</main>" + html_content[match.end():]
        else:
             print("Could not find insertion point")
             return

    for company in NEW_COMPANIES:
        # Check if already exists
        if f'class="text-xl font-bold">{company["name"]}</h3>' in html_content:
             print(f"Skipping {company['name']} - already exists")
             continue

        card = f"""
            <!-- Company Card: {company["name"]} -->
            <div class="company-card bg-white p-6 rounded-2xl shadow-sm border border-slate-200 hover:shadow-md transition-shadow" data-category="{company['category']}">
                <div class="flex justify-between items-start mb-4">
                    <h3 class="text-xl font-bold">{company['name']}</h3>
                    <span class="bg-sky-100 text-sky-800 text-xs font-semibold px-2.5 py-0.5 rounded-full">{company['category']}</span>
                </div>
                <p class="text-slate-600 mb-6 text-sm">{company['description']}</p>
                <div class="mt-auto">
                    <a href="{company['url']}" target="_blank" rel="noopener noreferrer" class="text-sky-600 font-semibold hover:text-sky-700 text-sm flex items-center">
                        Besök webbplats
                        <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
                    </a>
                </div>
            </div>"""
        
        html_content = html_content.replace(grid_end_marker, f"{card}\n        {grid_end_marker}")
        print(f"Added {company['name']}")

    write_html(HTML_FILE, html_content)

add_companies()
