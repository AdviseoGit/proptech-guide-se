import re

with open('/data/workspace/projects/proptech-guide-se/static/directory.html', 'r') as f:
    content = f.read()

new_companies = """
            <!-- Company Card: Iver -->
            <div class="company-card bg-white p-6 rounded-2xl shadow-sm border border-slate-200 hover:shadow-md transition-shadow" data-category="Förvaltning">
                <div class="flex justify-between items-start mb-4">
                    <h3 class="text-2xl font-bold text-slate-900">Iver</h3>
                    <span class="bg-indigo-100 text-indigo-800 text-xs font-semibold px-2.5 py-0.5 rounded-full">Förvaltning</span>
                </div>
                <p class="text-slate-600 mb-6 text-sm">Erbjuder IT-tjänster och digitala plattformar anpassade för fastighetsbranschen, med fokus på säkerhet och modern infrastruktur.</p>
                <div class="mt-auto">
                    <a href="https://www.iver.com/sv/" target="_blank" rel="noopener noreferrer" class="text-sky-600 font-semibold hover:text-sky-700 text-sm flex items-center">
                        Besök webbplats
                        <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
                    </a>
                </div>
            </div>

            <!-- Company Card: Vironova -->
            <div class="company-card bg-white p-6 rounded-2xl shadow-sm border border-slate-200 hover:shadow-md transition-shadow" data-category="Energi">
                <div class="flex justify-between items-start mb-4">
                    <h3 class="text-2xl font-bold text-slate-900">Vironova</h3>
                    <span class="bg-sky-100 text-sky-800 text-xs font-semibold px-2.5 py-0.5 rounded-full">Energi</span>
                </div>
                <p class="text-slate-600 mb-6 text-sm">Specialiserade på energieffektivisering och optimering av inomhusklimat för kommersiella fastigheter och flerbostadshus.</p>
                <div class="mt-auto">
                    <a href="https://vironova.se" target="_blank" rel="noopener noreferrer" class="text-sky-600 font-semibold hover:text-sky-700 text-sm flex items-center">
                        Besök webbplats
                        <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
                    </a>
                </div>
            </div>

            <!-- Company Card: Zesec -->
            <div class="company-card bg-white p-6 rounded-2xl shadow-sm border border-slate-200 hover:shadow-md transition-shadow" data-category="Passersystem">
                <div class="flex justify-between items-start mb-4">
                    <h3 class="text-2xl font-bold text-slate-900">Zesec</h3>
                    <span class="bg-emerald-100 text-emerald-800 text-xs font-semibold px-2.5 py-0.5 rounded-full">Passersystem</span>
                </div>
                <p class="text-slate-600 mb-6 text-sm">Molnbaserat passersystem som låter användare öppna dörrar och portar via mobilen, oberoende av befintlig hårdvara.</p>
                <div class="mt-auto">
                    <a href="https://zesec.com" target="_blank" rel="noopener noreferrer" class="text-sky-600 font-semibold hover:text-sky-700 text-sm flex items-center">
                        Besök webbplats
                        <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
                    </a>
                </div>
            </div>
"""

# Insert right before the end of the grid
content = re.sub(r'(</main>)', new_companies + r'\n        </div>\n    \1', content)
# Wait, this regex might be tricky if the grid div closing tag isn't easily targeted before </main>. Let's target the Nordomatic card instead.

nordomatic_pattern = r'(<!-- Company Card: Nordomatic -->.*?</div>\s*</div>)'
content = re.sub(nordomatic_pattern, r'\1\n' + new_companies, content, flags=re.DOTALL)

with open('/data/workspace/projects/proptech-guide-se/static/directory.html', 'w') as f:
    f.write(content)
