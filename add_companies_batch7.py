import re
import sys

def main():
    file_path = "static/directory.html"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    new_companies_html = """
        <!-- New Company 1 -->
        <div class="company-card bg-white p-6 rounded-2xl border border-slate-100 shadow-sm hover:shadow-md transition-shadow" data-category="Energi & Hållbarhet">
            <div class="flex justify-between items-start mb-4">
                <h3 class="text-xl font-bold">KTC</h3>
                <span class="bg-emerald-100 text-emerald-800 text-xs font-semibold px-2.5 py-0.5 rounded">Energi & Hållbarhet</span>
            </div>
            <p class="text-slate-600 mb-4 text-sm">Specialister på energioptimering och fastighetsautomation. KTC erbjuder helhetslösningar för att digitalisera och energieffektivisera fastigheter, med stort fokus på öppna system och hållbarhet.</p>
            <div class="space-y-2 mb-6">
                <div class="flex text-sm"><span class="font-semibold w-24 text-slate-900">För vem:</span><span class="text-slate-600">Fastighetsägare, BRF:er</span></div>
                <div class="flex text-sm"><span class="font-semibold w-24 text-slate-900">Modell:</span><span class="text-slate-600">Projekt, Tjänst, SaaS</span></div>
            </div>
            <a href="https://ktc.se" target="_blank" rel="noopener noreferrer" class="text-sky-600 font-semibold hover:text-sky-700 flex items-center text-sm">
                Besök hemsida <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
            </a>
        </div>

        <!-- New Company 2 -->
        <div class="company-card bg-white p-6 rounded-2xl border border-slate-100 shadow-sm hover:shadow-md transition-shadow" data-category="Drift & Underhåll">
            <div class="flex justify-between items-start mb-4">
                <h3 class="text-xl font-bold">Incoord</h3>
                <span class="bg-orange-100 text-orange-800 text-xs font-semibold px-2.5 py-0.5 rounded">Drift & Underhåll</span>
            </div>
            <p class="text-slate-600 mb-4 text-sm">Tekniska konsulter och innovatörer inom installationsteknik, energi och hållbarhet. Skapar digitala tvillingar och simulerar fastigheters framtida prestanda och klimatpåverkan.</p>
            <div class="space-y-2 mb-6">
                <div class="flex text-sm"><span class="font-semibold w-24 text-slate-900">För vem:</span><span class="text-slate-600">Fastighetsutvecklare, Ägare</span></div>
                <div class="flex text-sm"><span class="font-semibold w-24 text-slate-900">Modell:</span><span class="text-slate-600">Konsulttjänst, Mjukvara</span></div>
            </div>
            <a href="https://incoord.se" target="_blank" rel="noopener noreferrer" class="text-sky-600 font-semibold hover:text-sky-700 flex items-center text-sm">
                Besök hemsida <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
            </a>
        </div>

        <!-- New Company 3 -->
        <div class="company-card bg-white p-6 rounded-2xl border border-slate-100 shadow-sm hover:shadow-md transition-shadow" data-category="Ekonomi & Uthyrning">
            <div class="flex justify-between items-start mb-4">
                <h3 class="text-xl font-bold">Aareon</h3>
                <span class="bg-blue-100 text-blue-800 text-xs font-semibold px-2.5 py-0.5 rounded">Ekonomi & Uthyrning</span>
            </div>
            <p class="text-slate-600 mb-4 text-sm">Ledande leverantör av affärssystem och digitala lösningar för fastighetsbranschen i Europa. Erbjuder kompletta ERP-system, appar för hyresgäster och besiktningsverktyg.</p>
            <div class="space-y-2 mb-6">
                <div class="flex text-sm"><span class="font-semibold w-24 text-slate-900">För vem:</span><span class="text-slate-600">Allmännyttan, Större Ägare</span></div>
                <div class="flex text-sm"><span class="font-semibold w-24 text-slate-900">Modell:</span><span class="text-slate-600">SaaS, Affärssystem</span></div>
            </div>
            <a href="https://www.aareon.se" target="_blank" rel="noopener noreferrer" class="text-sky-600 font-semibold hover:text-sky-700 flex items-center text-sm">
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
