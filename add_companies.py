import re

content = ""
with open("/data/workspace/projects/proptech-guide-se/static/directory.html", "r") as f:
    content = f.read()

new_companies = """
            <div class="company-card bg-white p-6 rounded-2xl shadow-sm border border-slate-200 hover:shadow-md transition-shadow" data-category="drönare">
                <div class="flex justify-between items-start mb-4">
                    <h3 class="text-xl font-bold">FastOut</h3>
                    <span class="bg-sky-100 text-sky-800 text-xs px-2 py-1 rounded font-bold uppercase">Visualisering</span>
                </div>
                <p class="text-slate-600 mb-4 line-clamp-3">Plattform för 360-graders drönarvyer och fastighetsvisualisering. Hjälper fastighetsbolag att skapa interaktiva upplevelser av utemiljöer och omgivningar.</p>
                <div class="mt-auto">
                    <a href="https://fastout.com" target="_blank" rel="noopener" class="text-sky-600 font-bold hover:underline flex items-center">
                        Besök webbplats <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
                    </a>
                </div>
            </div>

            <div class="company-card bg-white p-6 rounded-2xl shadow-sm border border-slate-200 hover:shadow-md transition-shadow" data-category="uthyrning">
                <div class="flex justify-between items-start mb-4">
                    <h3 class="text-xl font-bold">HomeQ</h3>
                    <span class="bg-sky-100 text-sky-800 text-xs px-2 py-1 rounded font-bold uppercase">Uthyrning</span>
                </div>
                <p class="text-slate-600 mb-4 line-clamp-3">Sveriges största marknadsplats för förstahandslägenheter. Automatiserar uthyrningsprocessen för hyresvärdar, från publicering till kreditkontroll och signering.</p>
                <div class="mt-auto">
                    <a href="https://homeq.se" target="_blank" rel="noopener" class="text-sky-600 font-bold hover:underline flex items-center">
                        Besök webbplats <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
                    </a>
                </div>
            </div>

            <div class="company-card bg-white p-6 rounded-2xl shadow-sm border border-slate-200 hover:shadow-md transition-shadow" data-category="energi">
                <div class="flex justify-between items-start mb-4">
                    <h3 class="text-xl font-bold">Ferroamp</h3>
                    <span class="bg-sky-100 text-sky-800 text-xs px-2 py-1 rounded font-bold uppercase">Energi</span>
                </div>
                <p class="text-slate-600 mb-4 line-clamp-3">Smart system för energioptimering i fastigheter. Deras EnergyHub integrerar solceller, energilagring och elbilsladdning i ett gemensamt likströmsnät för minskade effekttoppar.</p>
                <div class="mt-auto">
                    <a href="https://ferroamp.com" target="_blank" rel="noopener" class="text-sky-600 font-bold hover:underline flex items-center">
                        Besök webbplats <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
                    </a>
                </div>
            </div>

            <div class="company-card bg-white p-6 rounded-2xl shadow-sm border border-slate-200 hover:shadow-md transition-shadow" data-category="forvaltning">
                <div class="flex justify-between items-start mb-4">
                    <h3 class="text-xl font-bold">Zynka BIM</h3>
                    <span class="bg-sky-100 text-sky-800 text-xs px-2 py-1 rounded font-bold uppercase">Förvaltning</span>
                </div>
                <p class="text-slate-600 mb-4 line-clamp-3">Experter på BIM och digitalisering av fastigheter. Deras plattform hjälper fastighetsägare att skapa och förvalta digitala tvillingar för effektivare drift och beslutsfattande.</p>
                <div class="mt-auto">
                    <a href="https://zynkagroup.se" target="_blank" rel="noopener" class="text-sky-600 font-bold hover:underline flex items-center">
                        Besök webbplats <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
                    </a>
                </div>
            </div>
"""

# Find the end of the grid
grid_end = content.find("</div>\n\n        <!-- No Results Message -->")
if grid_end != -1:
    new_content = content[:grid_end] + new_companies + content[grid_end:]
    with open("/data/workspace/projects/proptech-guide-se/static/directory.html", "w") as f:
        f.write(new_content)
    print("Added new companies")
else:
    print("Could not find grid end")
