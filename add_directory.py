import re
import sys

def add_companies():
    html_path = '/data/workspace/projects/proptech-guide-se/static/directory.html'
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
        
    new_companies = """
        <div class="company-card bg-white rounded-2xl p-6 shadow-sm border border-slate-100 hover:shadow-md transition-shadow" data-category="boende">
            <h3 class="text-xl font-bold text-slate-900 mb-2">Parakey</h3>
            <p class="text-sm font-semibold text-sky-600 mb-3">Boende & Hyresgäst</p>
            <p class="text-slate-600 text-sm mb-4">Molnbaserat passerkontrollsystem som använder smartphones istället för nycklar och taggar, perfekt för både bostäder och kommersiella fastigheter.</p>
            <div class="mt-auto">
                <span class="inline-block bg-slate-100 text-slate-600 text-xs px-2 py-1 rounded">Mobil Passerkontroll</span>
                <span class="inline-block bg-slate-100 text-slate-600 text-xs px-2 py-1 rounded">Säkerhet</span>
            </div>
            <a href="https://parakey.co" target="_blank" rel="noopener noreferrer" class="mt-4 block text-center text-sky-600 font-semibold hover:text-sky-700 text-sm border border-sky-100 rounded-lg py-2 hover:bg-sky-50 transition-colors">Besök webbplats &rarr;</a>
        </div>

        <div class="company-card bg-white rounded-2xl p-6 shadow-sm border border-slate-100 hover:shadow-md transition-shadow" data-category="plattform">
            <h3 class="text-xl font-bold text-slate-900 mb-2">Basefarm (Orange Business)</h3>
            <p class="text-sm font-semibold text-sky-600 mb-3">Öppen Plattform</p>
            <p class="text-slate-600 text-sm mb-4">Erbjuder robusta IoT-plattformar och data management-lösningar för storskaliga fastighetsbestånd, med starkt fokus på säkerhet och upptid.</p>
            <div class="mt-auto">
                <span class="inline-block bg-slate-100 text-slate-600 text-xs px-2 py-1 rounded">IoT Infrastruktur</span>
                <span class="inline-block bg-slate-100 text-slate-600 text-xs px-2 py-1 rounded">Data Management</span>
            </div>
            <a href="https://www.orange-business.com/en" target="_blank" rel="noopener noreferrer" class="mt-4 block text-center text-sky-600 font-semibold hover:text-sky-700 text-sm border border-sky-100 rounded-lg py-2 hover:bg-sky-50 transition-colors">Besök webbplats &rarr;</a>
        </div>

        <div class="company-card bg-white rounded-2xl p-6 shadow-sm border border-slate-100 hover:shadow-md transition-shadow" data-category="forvaltning">
            <h3 class="text-xl font-bold text-slate-900 mb-2">Service Works Global</h3>
            <p class="text-sm font-semibold text-sky-600 mb-3">Förvaltning & Drift</p>
            <p class="text-slate-600 text-sm mb-4">Leverantör av BIM och CAFM-programvara (QFM) som hjälper fastighetsförvaltare att optimera utrymmeshantering, schemaläggning och underhåll.</p>
            <div class="mt-auto">
                <span class="inline-block bg-slate-100 text-slate-600 text-xs px-2 py-1 rounded">CAFM / IWMS</span>
                <span class="inline-block bg-slate-100 text-slate-600 text-xs px-2 py-1 rounded">BIM-integration</span>
            </div>
            <a href="https://www.swg.com/se/" target="_blank" rel="noopener noreferrer" class="mt-4 block text-center text-sky-600 font-semibold hover:text-sky-700 text-sm border border-sky-100 rounded-lg py-2 hover:bg-sky-50 transition-colors">Besök webbplats &rarr;</a>
        </div>
    """
    
    grid_start_idx = html.find('<div id="directoryGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">')
    if grid_start_idx == -1:
        print("Kunde inte hitta directoryGrid")
        return
        
    grid_content_start = html.find('>', grid_start_idx) + 1
    
    new_html = html[:grid_content_start] + "\n" + new_companies + html[grid_content_start:]
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("La till 3 företag i directory.html")

add_companies()
