import re

with open('/data/workspace/projects/proptech-guide-se/static/directory.html', 'r') as f:
    content = f.read()

new_companies = """
            <!-- Company Card: Iver -->
            <div class="company-card bg-white p-6 rounded-2xl shadow-sm border border-slate-200 hover:shadow-md transition-shadow" data-category="forvaltning">
                <div class="flex items-start justify-between mb-4">
                    <div>
                        <h3 class="text-2xl font-bold text-slate-900">Iver</h3>
                        <p class="text-sky-600 font-medium text-sm mt-1">IT & Förvaltning</p>
                    </div>
                    <span class="px-3 py-1 bg-sky-100 text-sky-700 rounded-full text-xs font-bold uppercase tracking-wide">Förvaltning</span>
                </div>
                <p class="text-slate-600 mb-6 text-sm">Erbjuder IT-tjänster och digitala plattformar anpassade för fastighetsbranschen, med fokus på säkerhet och modern infrastruktur.</p>
                <a href="https://www.iver.com/sv/" target="_blank" class="block w-full py-2 px-4 bg-slate-50 text-slate-900 text-center font-bold rounded-xl border border-slate-200 hover:bg-slate-100 transition-colors">Besök hemsida</a>
            </div>

            <!-- Company Card: Vironova -->
            <div class="company-card bg-white p-6 rounded-2xl shadow-sm border border-slate-200 hover:shadow-md transition-shadow" data-category="energi">
                <div class="flex items-start justify-between mb-4">
                    <div>
                        <h3 class="text-2xl font-bold text-slate-900">Vironova</h3>
                        <p class="text-sky-600 font-medium text-sm mt-1">Energioptimering</p>
                    </div>
                    <span class="px-3 py-1 bg-emerald-100 text-emerald-700 rounded-full text-xs font-bold uppercase tracking-wide">Energi</span>
                </div>
                <p class="text-slate-600 mb-6 text-sm">Specialiserade på energieffektivisering och optimering av inomhusklimat för kommersiella fastigheter och flerbostadshus.</p>
                <a href="https://vironova.se" target="_blank" class="block w-full py-2 px-4 bg-slate-50 text-slate-900 text-center font-bold rounded-xl border border-slate-200 hover:bg-slate-100 transition-colors">Besök hemsida</a>
            </div>

            <!-- Company Card: Zesec -->
            <div class="company-card bg-white p-6 rounded-2xl shadow-sm border border-slate-200 hover:shadow-md transition-shadow" data-category="passagesystem">
                <div class="flex items-start justify-between mb-4">
                    <div>
                        <h3 class="text-2xl font-bold text-slate-900">Zesec</h3>
                        <p class="text-sky-600 font-medium text-sm mt-1">Mobil Access</p>
                    </div>
                    <span class="px-3 py-1 bg-indigo-100 text-indigo-700 rounded-full text-xs font-bold uppercase tracking-wide">Passersystem</span>
                </div>
                <p class="text-slate-600 mb-6 text-sm">Molnbaserat passersystem som låter användare öppna dörrar och portar via mobilen, oberoende av befintlig hårdvara.</p>
                <a href="https://zesec.com" target="_blank" class="block w-full py-2 px-4 bg-slate-50 text-slate-900 text-center font-bold rounded-xl border border-slate-200 hover:bg-slate-100 transition-colors">Besök hemsida</a>
            </div>
"""

nordomatic_pattern = r'(<!-- Company Card: Nordomatic -->.*?</div>\s*</div>)'
content = re.sub(nordomatic_pattern, r'\1\n' + new_companies, content, flags=re.DOTALL)

with open('/data/workspace/projects/proptech-guide-se/static/directory.html', 'w') as f:
    f.write(content)
