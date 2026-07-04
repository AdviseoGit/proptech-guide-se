import re

with open('/data/workspace/projects/proptech-guide-se/static/directory.html', 'r') as f:
    content = f.read()

new_companies = """
        <!-- New Company: Halmstad Stadsnät -->
        <div class="company-card bg-white p-6 rounded-2xl shadow-sm border border-slate-200 hover:shadow-md transition-shadow" data-category="iot">
                <div class="flex items-start justify-between mb-4">
                    <div>
                        <h3 class="text-2xl font-bold text-slate-900">Halmstad Stadsnät</h3>
                        <span class="inline-block mt-2 px-3 py-1 bg-purple-100 text-purple-700 text-xs font-bold uppercase tracking-wider rounded-full">IoT & Hårdvara</span>
                    </div>
                </div>
                <p class="text-slate-600 mb-6 line-clamp-3">Erbjuder IoT-nät (LoRaWAN) för kommuner och fastighetsägare som möjliggör kostnadseffektiv insamling av sensordata för optimering och drift.</p>
                <div class="space-y-3 mb-6">
                    <div class="flex items-center text-sm text-slate-500">
                        <svg class="w-5 h-5 mr-3 text-sky-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path></svg>
                        Målgrupp: Kommuner, Allmännyttan
                    </div>
                    <div class="flex items-center text-sm text-slate-500">
                        <svg class="w-5 h-5 mr-3 text-sky-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                        Modell: Abonnemang
                    </div>
                </div>
                <a href="https://halmstadstadsnat.se/" target="_blank" class="block w-full py-2 px-4 bg-slate-50 text-slate-900 text-center font-bold rounded-xl border border-slate-200 hover:bg-slate-100 transition-colors">Besök hemsida</a>
        </div>

        <!-- New Company: Ecocloud -->
        <div class="company-card bg-white p-6 rounded-2xl shadow-sm border border-slate-200 hover:shadow-md transition-shadow" data-category="energy">
                <div class="flex items-start justify-between mb-4">
                    <div>
                        <h3 class="text-2xl font-bold text-slate-900">Ecocloud</h3>
                        <span class="inline-block mt-2 px-3 py-1 bg-emerald-100 text-emerald-700 text-xs font-bold uppercase tracking-wider rounded-full">Energi & Hållbarhet</span>
                    </div>
                </div>
                <p class="text-slate-600 mb-6 line-clamp-3">Mjukvara för energi- och miljöuppföljning som hjälper fastighetsägare att visualisera förbrukning och automatisera rapportering för hållbarhetsmål.</p>
                <div class="space-y-3 mb-6">
                    <div class="flex items-center text-sm text-slate-500">
                        <svg class="w-5 h-5 mr-3 text-sky-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path></svg>
                        Målgrupp: Fastighetsägare, Industri
                    </div>
                    <div class="flex items-center text-sm text-slate-500">
                        <svg class="w-5 h-5 mr-3 text-sky-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                        Modell: SaaS
                    </div>
                </div>
                <a href="https://ecocloud.se/" target="_blank" class="block w-full py-2 px-4 bg-slate-50 text-slate-900 text-center font-bold rounded-xl border border-slate-200 hover:bg-slate-100 transition-colors">Besök hemsida</a>
        </div>

        <!-- New Company: Alliera -->
        <div class="company-card bg-white p-6 rounded-2xl shadow-sm border border-slate-200 hover:shadow-md transition-shadow" data-category="management">
                <div class="flex items-start justify-between mb-4">
                    <div>
                        <h3 class="text-2xl font-bold text-slate-900">Alliera</h3>
                        <span class="inline-block mt-2 px-3 py-1 bg-blue-100 text-blue-700 text-xs font-bold uppercase tracking-wider rounded-full">Förvaltning & Drift</span>
                    </div>
                </div>
                <p class="text-slate-600 mb-6 line-clamp-3">En plattform för identitets- och behörighetshantering (IAM) speciellt anpassad för fastighetsbranschen och fysisk accesskontroll.</p>
                <div class="space-y-3 mb-6">
                    <div class="flex items-center text-sm text-slate-500">
                        <svg class="w-5 h-5 mr-3 text-sky-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path></svg>
                        Målgrupp: Kommersiella fastigheter
                    </div>
                    <div class="flex items-center text-sm text-slate-500">
                        <svg class="w-5 h-5 mr-3 text-sky-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                        Modell: B2B
                    </div>
                </div>
                <a href="https://alliera.com/" target="_blank" class="block w-full py-2 px-4 bg-slate-50 text-slate-900 text-center font-bold rounded-xl border border-slate-200 hover:bg-slate-100 transition-colors">Besök hemsida</a>
        </div>
"""

content = content.replace('<div id="directoryGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">', '<div id="directoryGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">\n' + new_companies)

with open('/data/workspace/projects/proptech-guide-se/static/directory.html', 'w') as f:
    f.write(content)
