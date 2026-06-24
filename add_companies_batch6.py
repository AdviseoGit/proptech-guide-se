import re

with open("/data/workspace/projects/proptech-guide-se/static/directory.html", "r", encoding="utf-8") as f:
    content = f.read()

new_companies = """
            <!-- Avtal24 / Lexly -->
            <div class="company-card bg-white p-6 rounded-2xl shadow-sm border border-slate-200 hover:shadow-md transition-shadow" data-category="forvaltning">
                <div class="flex items-start justify-between mb-4">
                    <div>
                        <h3 class="text-xl font-bold text-slate-900">Avtal24 / Lexly</h3>
                        <p class="text-sky-600 font-medium text-sm mt-1">Avtalshantering</p>
                    </div>
                </div>
                <p class="text-slate-600 mb-6 text-sm">Digital avtalsplattform som används av många fastighetsägare och brf:er för att enkelt hantera hyresavtal och juridiska dokument online.</p>
                <a href="https://lexly.se" target="_blank" class="block w-full py-2 px-4 bg-slate-50 text-slate-900 text-center font-bold rounded-xl border border-slate-200 hover:bg-slate-100 transition-colors">Besök hemsida</a>
            </div>

            <!-- Boappa -->
            <div class="company-card bg-white p-6 rounded-2xl shadow-sm border border-slate-200 hover:shadow-md transition-shadow" data-category="hyresgast">
                <div class="flex items-start justify-between mb-4">
                    <div>
                        <h3 class="text-xl font-bold text-slate-900">Boappa</h3>
                        <p class="text-sky-600 font-medium text-sm mt-1">Boendeapp</p>
                    </div>
                </div>
                <p class="text-slate-600 mb-6 text-sm">En av Sveriges mest populära boendeappar för bostadsrättsföreningar och grannskap. Skapar trygghet och underlättar styrelsens kommunikation.</p>
                <a href="https://boappa.com" target="_blank" class="block w-full py-2 px-4 bg-slate-50 text-slate-900 text-center font-bold rounded-xl border border-slate-200 hover:bg-slate-100 transition-colors">Besök hemsida</a>
            </div>

            <!-- Bemsiq -->
            <div class="company-card bg-white p-6 rounded-2xl shadow-sm border border-slate-200 hover:shadow-md transition-shadow" data-category="iot">
                <div class="flex items-start justify-between mb-4">
                    <div>
                        <h3 class="text-xl font-bold text-slate-900">Bemsiq</h3>
                        <p class="text-sky-600 font-medium text-sm mt-1">IoT & Hårdvara</p>
                    </div>
                </div>
                <p class="text-slate-600 mb-6 text-sm">En svensk företagsgrupp inom byggnadsautomation och fastighets-IT. De erbjuder hårdvara och sensorer som utgör fundamentet i många smarta byggnader.</p>
                <a href="https://bemsiq.com" target="_blank" class="block w-full py-2 px-4 bg-slate-50 text-slate-900 text-center font-bold rounded-xl border border-slate-200 hover:bg-slate-100 transition-colors">Besök hemsida</a>
            </div>
"""

insert_pos = content.find('<div id="directoryGrid"')
if insert_pos != -1:
    inner_div = content.find('>', insert_pos)
    if inner_div != -1:
        content = content[:inner_div+1] + new_companies + content[inner_div+1:]
        with open("/data/workspace/projects/proptech-guide-se/static/directory.html", "w", encoding="utf-8") as f:
            f.write(content)
        print("Added 3 new companies to directory.html")
    else:
        print("inner div not found")
else:
    print("Could not find insertion point")
