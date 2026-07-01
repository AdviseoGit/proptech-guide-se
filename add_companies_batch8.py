import re
import sys
import os

def main():
    file_path = "/data/workspace/projects/proptech-guide-se/static/directory.html"
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        sys.exit(1)
        
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    new_companies_html = """
        <!-- New Company 1 -->
        <div class="company-card bg-white p-6 rounded-2xl border border-slate-100 shadow-sm hover:shadow-md transition-shadow" data-category="Energi & Hållbarhet">
            <div class="flex justify-between items-start mb-4">
                <h3 class="text-xl font-bold">Nodeledge</h3>
                <span class="bg-emerald-100 text-emerald-800 text-xs font-semibold px-2.5 py-0.5 rounded">Energi & Hållbarhet</span>
            </div>
            <p class="text-slate-600 mb-4 text-sm">Specialiserade på energiuppföljning och analys. Nodeledge tillhandahåller system som hjälper fastighetsägare att visualisera, förstå och minska sin energianvändning.</p>
            <div class="space-y-2 mb-6">
                <div class="flex text-sm"><span class="font-semibold w-24 text-slate-900">För vem:</span><span class="text-slate-600">Fastighetsägare, Kommuner</span></div>
                <div class="flex text-sm"><span class="font-semibold w-24 text-slate-900">Modell:</span><span class="text-slate-600">SaaS</span></div>
            </div>
            <a href="https://nodeledge.se" target="_blank" rel="noopener noreferrer" class="text-sky-600 font-semibold hover:text-sky-700 flex items-center text-sm">
                Besök hemsida <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
            </a>
        </div>

        <!-- New Company 2 -->
        <div class="company-card bg-white p-6 rounded-2xl border border-slate-100 shadow-sm hover:shadow-md transition-shadow" data-category="Bokning & Tillgång">
            <div class="flex justify-between items-start mb-4">
                <h3 class="text-xl font-bold">Zesec</h3>
                <span class="bg-purple-100 text-purple-800 text-xs font-semibold px-2.5 py-0.5 rounded">Bokning & Tillgång</span>
            </div>
            <p class="text-slate-600 mb-4 text-sm">Utvecklar molnbaserad mobil access. Zesecs lösning gör att dörrar, portar och grindar kan öppnas med mobilen, vilket förenklar leveranser och vardagen för boende.</p>
            <div class="space-y-2 mb-6">
                <div class="flex text-sm"><span class="font-semibold w-24 text-slate-900">För vem:</span><span class="text-slate-600">BRF:er, Företag</span></div>
                <div class="flex text-sm"><span class="font-semibold w-24 text-slate-900">Modell:</span><span class="text-slate-600">Hårdvara + SaaS</span></div>
            </div>
            <a href="https://zesec.com" target="_blank" rel="noopener noreferrer" class="text-sky-600 font-semibold hover:text-sky-700 flex items-center text-sm">
                Besök hemsida <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
            </a>
        </div>

        <!-- New Company 3 -->
        <div class="company-card bg-white p-6 rounded-2xl border border-slate-100 shadow-sm hover:shadow-md transition-shadow" data-category="Drift & Underhåll">
            <div class="flex justify-between items-start mb-4">
                <h3 class="text-xl font-bold">Bygglet</h3>
                <span class="bg-orange-100 text-orange-800 text-xs font-semibold px-2.5 py-0.5 rounded">Drift & Underhåll</span>
            </div>
            <p class="text-slate-600 mb-4 text-sm">Projektverktyg för bygg- och entreprenadföretag. Digitaliserar hela flödet från offert till faktura, inklusive tidrapportering och hantering av ÄTA, vilket underlättar vid ombyggnationer av fastigheter.</p>
            <div class="space-y-2 mb-6">
                <div class="flex text-sm"><span class="font-semibold w-24 text-slate-900">För vem:</span><span class="text-slate-600">Entreprenörer, Byggbolag</span></div>
                <div class="flex text-sm"><span class="font-semibold w-24 text-slate-900">Modell:</span><span class="text-slate-600">SaaS</span></div>
            </div>
            <a href="https://bygglet.com" target="_blank" rel="noopener noreferrer" class="text-sky-600 font-semibold hover:text-sky-700 flex items-center text-sm">
                Besök hemsida <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
            </a>
        </div>
"""

    grid_start = content.find('<div id="directoryGrid"')
    if grid_start == -1:
        print("Error: Could not find directoryGrid.")
        sys.exit(1)
        
    grid_end = content.find('>', grid_start)
    
    new_content = content[:grid_end+1] + new_companies_html + content[grid_end+1:]
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
        
    print("Added 3 new companies to directory.")

if __name__ == "__main__":
    main()
