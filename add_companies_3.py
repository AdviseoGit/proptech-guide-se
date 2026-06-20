import re

with open('/data/workspace/projects/proptech-guide-se/static/directory.html', 'r') as f:
    content = f.read()

new_companies = """
            <!-- Company Card: Raybased -->
            <div class="company-card bg-white p-6 rounded-2xl shadow-sm border border-slate-200 hover:shadow-md transition-shadow" data-category="iot">
                <div class="flex items-start justify-between mb-4">
                    <div>
                        <h3 class="text-2xl font-bold text-slate-900">Raybased</h3>
                        <p class="text-sky-600 font-medium text-sm mt-1">IoT-plattform</p>
                    </div>
                    <span class="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-xs font-bold uppercase tracking-wide">IoT</span>
                </div>
                <p class="text-slate-600 mb-6 text-sm">Trådlöst system för styrning och övervakning av fastighetstekniska system med minimal kabeldragning, idealiskt för befintliga byggnader.</p>
                <a href="https://raybased.com" target="_blank" class="block w-full py-2 px-4 bg-slate-50 text-slate-900 text-center font-bold rounded-xl border border-slate-200 hover:bg-slate-100 transition-colors">Besök hemsida</a>
            </div>

            <!-- Company Card: Amido -->
            <div class="company-card bg-white p-6 rounded-2xl shadow-sm border border-slate-200 hover:shadow-md transition-shadow" data-category="passagesystem">
                <div class="flex items-start justify-between mb-4">
                    <div>
                        <h3 class="text-2xl font-bold text-slate-900">Amido</h3>
                        <p class="text-sky-600 font-medium text-sm mt-1">Passagehantering</p>
                    </div>
                    <span class="px-3 py-1 bg-indigo-100 text-indigo-700 rounded-full text-xs font-bold uppercase tracking-wide">Passersystem</span>
                </div>
                <p class="text-slate-600 mb-6 text-sm">Samlar olika passersystem i ett och samma gränssnitt. Gör det enkelt att hantera nycklar och behörigheter över hela fastighetsbeståndet.</p>
                <a href="https://amido.se" target="_blank" class="block w-full py-2 px-4 bg-slate-50 text-slate-900 text-center font-bold rounded-xl border border-slate-200 hover:bg-slate-100 transition-colors">Besök hemsida</a>
            </div>

            <!-- Company Card: Ochno -->
            <div class="company-card bg-white p-6 rounded-2xl shadow-sm border border-slate-200 hover:shadow-md transition-shadow" data-category="iot">
                <div class="flex items-start justify-between mb-4">
                    <div>
                        <h3 class="text-2xl font-bold text-slate-900">Ochno</h3>
                        <p class="text-sky-600 font-medium text-sm mt-1">Smart Kontorsteknik</p>
                    </div>
                    <span class="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-xs font-bold uppercase tracking-wide">IoT</span>
                </div>
                <p class="text-slate-600 mb-6 text-sm">Innovativ plattform som kombinerar smart belysning, sensorer och uttagsstyrning via USB-C, perfekt för det moderna, flexibla kontoret.</p>
                <a href="https://ochno.com" target="_blank" class="block w-full py-2 px-4 bg-slate-50 text-slate-900 text-center font-bold rounded-xl border border-slate-200 hover:bg-slate-100 transition-colors">Besök hemsida</a>
            </div>
"""

# Insert after Zesec
zesec_pattern = r'(<!-- Company Card: Zesec -->.*?</a>\s*</div>)'
content = re.sub(zesec_pattern, r'\1\n' + new_companies, content, flags=re.DOTALL)

with open('/data/workspace/projects/proptech-guide-se/static/directory.html', 'w') as f:
    f.write(content)
