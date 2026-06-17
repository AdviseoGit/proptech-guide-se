import sys

def add_companies():
    filepath = "/data/workspace/projects/proptech-guide-se/static/directory.html"
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_companies = """
            <!-- New Company 1 -->
            <div class="company-card bg-white p-6 rounded-2xl shadow-sm border border-slate-200 hover:shadow-md transition-shadow" data-category="uthyrning">
                <div class="flex justify-between items-start mb-4">
                    <h3 class="text-2xl font-bold text-slate-900">Bostadsregistraturet</h3>
                    <span class="bg-blue-100 text-blue-800 text-xs font-semibold px-2.5 py-0.5 rounded">Uthyrning</span>
                </div>
                <p class="text-slate-600 mb-6">Digitaliserar uthyrningsprocessen och tillhandahåller smidiga system för bostadsförmedling, hantering av köer och matchning av sökande med lediga objekt.</p>
                <a href="https://bostadsregistraturet.se/" target="_blank" class="text-sky-600 font-semibold hover:underline">Besök hemsida &rarr;</a>
            </div>

            <!-- New Company 2 -->
            <div class="company-card bg-white p-6 rounded-2xl shadow-sm border border-slate-200 hover:shadow-md transition-shadow" data-category="forvaltning">
                <div class="flex justify-between items-start mb-4">
                    <h3 class="text-2xl font-bold text-slate-900">Nabo</h3>
                    <span class="bg-indigo-100 text-indigo-800 text-xs font-semibold px-2.5 py-0.5 rounded">Förvaltning</span>
                </div>
                <p class="text-slate-600 mb-6">En helhetsleverantör av förvaltning för bostadsrättsföreningar. Erbjuder en modern plattform för ekonomisk och teknisk förvaltning samt juridik och boendeapp.</p>
                <a href="https://nabo.se/" target="_blank" class="text-sky-600 font-semibold hover:underline">Besök hemsida &rarr;</a>
            </div>

            <!-- New Company 3 -->
            <div class="company-card bg-white p-6 rounded-2xl shadow-sm border border-slate-200 hover:shadow-md transition-shadow" data-category="energi">
                <div class="flex justify-between items-start mb-4">
                    <h3 class="text-2xl font-bold text-slate-900">Metry</h3>
                    <span class="bg-green-100 text-green-800 text-xs font-semibold px-2.5 py-0.5 rounded">Energi & Hållbarhet</span>
                </div>
                <p class="text-slate-600 mb-6">Automatiserar insamling av miljö- och energidata. Plattformen är designad för att hjälpa fastighetsägare strukturera och följa upp sin energianvändning och hållbarhet (ESG).</p>
                <a href="https://metry.io/sv/" target="_blank" class="text-sky-600 font-semibold hover:underline">Besök hemsida &rarr;</a>
            </div>
"""
    
    insert_idx = -1
    for i, line in enumerate(lines):
        if 'id="noResults"' in line:
            insert_idx = i - 2
            break
            
    if insert_idx == -1:
        print("Fallback index finding")
        for i, line in enumerate(lines):
            if '</main>' in line:
                insert_idx = i - 1
                break
                
    if insert_idx != -1:
        lines.insert(insert_idx, new_companies)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print("Success")
    else:
        print("Failed to find insert location")

add_companies()
