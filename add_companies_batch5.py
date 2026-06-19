import re
import os

filepath = "/data/workspace/projects/proptech-guide-se/static/directory.html"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

new_companies = """
            <!-- HomeMaker -->
            <div class="company-card bg-white p-6 rounded-2xl shadow-sm border border-slate-200 hover:shadow-md transition-shadow" data-category="hyresgast">
                <div class="flex items-start justify-between mb-4">
                    <div>
                        <h3 class="text-xl font-bold text-slate-900">HomeMaker</h3>
                        <p class="text-sky-600 font-medium text-sm mt-1">Hyresgäst- & Tillvalsportal</p>
                    </div>
                    <span class="px-3 py-1 bg-sky-100 text-sky-700 rounded-full text-xs font-bold uppercase tracking-wide">Hyresgäst</span>
                </div>
                <p class="text-slate-600 mb-6 text-sm">Digital plattform för att hantera tillval, eftermarknad och kundrelationer vid nyproduktion och ROT-projekt.</p>
                <a href="https://homemaker.se" target="_blank" class="block w-full py-2 px-4 bg-slate-50 text-slate-900 text-center font-bold rounded-xl border border-slate-200 hover:bg-slate-100 transition-colors">Besök hemsida</a>
            </div>

            <!-- TenFAST -->
            <div class="company-card bg-white p-6 rounded-2xl shadow-sm border border-slate-200 hover:shadow-md transition-shadow" data-category="forvaltning">
                <div class="flex items-start justify-between mb-4">
                    <div>
                        <h3 class="text-xl font-bold text-slate-900">TenFAST</h3>
                        <p class="text-sky-600 font-medium text-sm mt-1">Fastighetssystem</p>
                    </div>
                    <span class="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-xs font-bold uppercase tracking-wide">Förvaltning</span>
                </div>
                <p class="text-slate-600 mb-6 text-sm">Ett modernt och molnbaserat fastighetssystem för hyresavisering, bokföring och avtalshantering, anpassat för små och medelstora hyresvärdar.</p>
                <a href="https://tenfast.se" target="_blank" class="block w-full py-2 px-4 bg-slate-50 text-slate-900 text-center font-bold rounded-xl border border-slate-200 hover:bg-slate-100 transition-colors">Besök hemsida</a>
            </div>

            <!-- Greenely -->
            <div class="company-card bg-white p-6 rounded-2xl shadow-sm border border-slate-200 hover:shadow-md transition-shadow" data-category="energi">
                <div class="flex items-start justify-between mb-4">
                    <div>
                        <h3 class="text-xl font-bold text-slate-900">Greenely</h3>
                        <p class="text-sky-600 font-medium text-sm mt-1">Energioptimering</p>
                    </div>
                    <span class="px-3 py-1 bg-emerald-100 text-emerald-700 rounded-full text-xs font-bold uppercase tracking-wide">Energi</span>
                </div>
                <p class="text-slate-600 mb-6 text-sm">Smart energiplattform som hjälper både företag och privatpersoner att optimera sin elförbrukning med hjälp av AI och timprisavtal.</p>
                <a href="https://greenely.se" target="_blank" class="block w-full py-2 px-4 bg-slate-50 text-slate-900 text-center font-bold rounded-xl border border-slate-200 hover:bg-slate-100 transition-colors">Besök hemsida</a>
            </div>
"""

new_content = content.replace(
    '<div id="directoryGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">',
    '<div id="directoryGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">\n' + new_companies
)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(new_content)
print("Added 3 new companies to directory.html")

