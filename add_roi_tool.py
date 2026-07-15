import json
from pathlib import Path
import os

def create_roi_calc():
    html_content = """<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ROI-kalkylator för Proptech: Räkna ut din avkastning | Proptechguiden</title>
    <meta name="description" content="Beräkna avkastningen (ROI) på din nästa proptech-investering. Få en skräddarsydd rapport över hur mycket du kan spara på smarta fastighetssystem.">
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <style>
        .calc-input { width: 100%; padding: 0.75rem; border: 1px solid #d1d5db; border-radius: 0.375rem; margin-top: 0.25rem; }
        .calc-label { font-weight: 600; color: #374151; font-size: 0.875rem; display: block; margin-top: 1rem; }
        .result-box { background-color: #f0fdf4; border: 1px solid #bbf7d0; padding: 1.5rem; border-radius: 0.5rem; margin-top: 1.5rem; display: none; }
    </style>
</head>
<body class="bg-gray-50 text-gray-800 font-sans leading-normal">
    <!-- Header -->
    <header class="bg-white shadow-sm sticky top-0 z-50">
        <div class="container mx-auto px-4 py-4 flex justify-between items-center">
            <a href="/" class="text-2xl font-bold text-blue-600 tracking-tight">Proptechguiden</a>
            <nav class="hidden md:flex space-x-6">
                <a href="/directory" class="text-gray-600 hover:text-blue-600 transition">Leverantörer</a>
                <a href="/smarta-byggnader-g" class="text-gray-600 hover:text-blue-600 transition">Smarta Byggnader</a>
                <a href="/brf-digitalisering" class="text-gray-600 hover:text-blue-600 transition">BRF Digitalisering</a>
                <a href="/roi-kalkylator" class="text-blue-600 font-medium">ROI-Kalkylator</a>
            </nav>
            <button id="mobile-menu-btn" class="md:hidden text-gray-500 hover:text-gray-700">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7"></path></svg>
            </button>
        </div>
        <div id="mobile-menu" class="hidden md:hidden bg-white border-t border-gray-100 py-2">
            <a href="/directory" class="block px-4 py-2 text-gray-600 hover:bg-gray-50">Leverantörer</a>
            <a href="/smarta-byggnader-g" class="block px-4 py-2 text-gray-600 hover:bg-gray-50">Smarta Byggnader</a>
            <a href="/brf-digitalisering" class="block px-4 py-2 text-gray-600 hover:bg-gray-50">BRF Digitalisering</a>
            <a href="/roi-kalkylator" class="block px-4 py-2 text-blue-600 font-medium bg-blue-50">ROI-Kalkylator</a>
        </div>
    </header>

    <main class="container mx-auto px-4 py-12 max-w-4xl">
        <div class="mb-10 text-center">
            <h1 class="text-4xl font-extrabold text-gray-900 mb-4">ROI-kalkylator för Proptech</h1>
            <p class="text-xl text-gray-600 max-w-2xl mx-auto">Räkna ut hur snabbt din investering i smart fastighetsteknik betalar sig. Få en uppskattning på potentiella besparingar.</p>
        </div>

        <div class="grid md:grid-cols-2 gap-8">
            <div class="bg-white p-6 rounded-lg shadow-md border border-gray-100">
                <h2 class="text-2xl font-bold mb-6 border-b pb-2">Dina förutsättningar</h2>
                <form id="roi-form">
                    <label class="calc-label" for="yta">Fastighetsyta (kvm)</label>
                    <input type="number" id="yta" class="calc-input" placeholder="T.ex. 5000" required>

                    <label class="calc-label" for="energikostnad">Nuvarande energikostnad per år (SEK)</label>
                    <input type="number" id="energikostnad" class="calc-input" placeholder="T.ex. 750000" required>

                    <label class="calc-label" for="investering">Planerad Proptech-investering (SEK)</label>
                    <input type="number" id="investering" class="calc-input" placeholder="T.ex. 250000" required>

                    <label class="calc-label" for="losningstyp">Typ av lösning</label>
                    <select id="losningstyp" class="calc-input">
                        <option value="0.15">Smart Värmestyrning (ca 15% besparing)</option>
                        <option value="0.25">Energioptimering & AI (ca 25% besparing)</option>
                        <option value="0.10">Smart Belysning (ca 10% besparing)</option>
                        <option value="0.05">Enkel undermätning (ca 5% besparing)</option>
                    </select>

                    <button type="button" id="calc-btn" class="w-full mt-6 bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded-md transition duration-200">Beräkna ROI</button>
                </form>
            </div>

            <div>
                <div class="bg-white p-6 rounded-lg shadow-md border border-gray-100 h-full flex flex-col justify-center text-center" id="empty-state">
                    <svg class="w-16 h-16 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path></svg>
                    <p class="text-gray-500">Fyll i dina uppgifter och klicka på beräkna för att se ditt resultat här.</p>
                </div>
                
                <div id="result-container" class="result-box h-full shadow-md">
                    <h2 class="text-2xl font-bold text-green-800 mb-2">Ditt resultat</h2>
                    <p class="text-sm text-green-700 mb-6">Baserat på dina inmatade värden.</p>
                    
                    <div class="mb-4">
                        <p class="text-gray-600 text-sm">Årlig besparing (estimerad)</p>
                        <p class="text-3xl font-extrabold text-gray-900"><span id="res-besparing">0</span> kr</p>
                    </div>
                    
                    <div class="mb-6">
                        <p class="text-gray-600 text-sm">Återbetalningstid (Payback)</p>
                        <p class="text-3xl font-extrabold text-blue-600"><span id="res-tid">0</span> år</p>
                    </div>
                    
                    <div class="mt-8 border-t border-green-200 pt-6">
                        <h3 class="font-bold text-gray-800 mb-2">Spara kalkylen & få anpassade offerter</h3>
                        <p class="text-sm text-gray-600 mb-4">Lämna din e-post så skickar vi en detaljerad rapport samt kopplar ihop dig med relevanta leverantörer ur vår katalog som matchar din profil.</p>
                        <form id="lead-form" class="space-y-3">
                            <input type="email" id="lead-email" placeholder="Din e-postadress" class="w-full px-3 py-2 border border-gray-300 rounded focus:ring-blue-500 focus:border-blue-500" required>
                            <input type="hidden" id="lead-data" name="lead-data">
                            <button type="submit" class="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded transition">Få rapporten (Gratis)</button>
                            <p id="lead-success" class="text-green-700 font-bold hidden text-sm mt-2">✓ Tack! Din rapport skickas inom kort.</p>
                        </form>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="mt-16 bg-white p-8 rounded-lg shadow-sm border border-gray-200">
            <h2 class="text-2xl font-bold mb-4">Varför är ROI viktigt inom Proptech?</h2>
            <div class="prose max-w-none text-gray-600">
                <p>När du investerar i fastighetsteknik (proptech) är det avgörande att förstå när investeringen betalar sig (Return on Investment). Ofta är besparingarna i energi och effektiviserad drift så stora att återbetalningstiden landar på 1-3 år.</p>
                <p class="mt-4"><strong>Så fungerar kalkylatorn:</strong> Denna kalkylator ger ett estimat baserat på branschstandarder. Ett system för energioptimering med AI kan ofta sänka uppvärmningskostnaderna med 15-30%. Kalkylen ger en indikation, men de exakta siffrorna beror på din fastighets specifika förutsättningar, ålder och befintliga system.</p>
                <p class="mt-4">Vill du se vilka leverantörer som erbjuder dessa lösningar? Besök vår <a href="/directory" class="text-blue-600 hover:underline">Leverantörsguide för Proptech</a>.</p>
            </div>
        </div>
    </main>

    <!-- Footer -->
    <footer class="bg-gray-800 text-white mt-12 py-10">
        <div class="container mx-auto px-4 text-center">
            <p class="mb-4">Proptechguiden - Sveriges ledande guide till smarta fastigheter och proptech.</p>
            <div class="text-sm text-gray-400 space-x-4">
                <a href="/om-oss.html" class="hover:text-white">Om oss</a>
                <a href="/privacy-policy.html" class="hover:text-white">Integritetspolicy</a>
                <a href="/om-sajten" class="hover:text-white">Om sajten</a>
            </div>
            <p class="text-xs text-gray-500 mt-6">Denna sajt skapas och drivs helt av AI · <a href="/om-sajten" class="hover:text-gray-300">Om sajten</a></p>
        </div>
    </footer>

    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-7028BLJBRF"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());

        gtag('config', 'G-7028BLJBRF');
    </script>

    <script>
        // Mobile menu toggle
        document.getElementById('mobile-menu-btn').addEventListener('click', function() {
            var menu = document.getElementById('mobile-menu');
            menu.classList.toggle('hidden');
        });

        // Calc Logic
        document.getElementById('calc-btn').addEventListener('click', function() {
            const yta = parseFloat(document.getElementById('yta').value);
            const kostnad = parseFloat(document.getElementById('energikostnad').value);
            const investering = parseFloat(document.getElementById('investering').value);
            const besparingPct = parseFloat(document.getElementById('losningstyp').value);

            if(!yta || !kostnad || !investering) {
                alert('Vänligen fyll i alla fält (yta, kostnad, investering).');
                return;
            }

            const arligBesparing = kostnad * besparingPct;
            const aterbetalning = investering / arligBesparing;

            document.getElementById('res-besparing').innerText = Math.round(arligBesparing).toLocaleString('sv-SE');
            document.getElementById('res-tid').innerText = aterbetalning.toFixed(1).replace('.', ',');
            
            // Prepare lead data
            const leadData = {
                yta: yta,
                kostnad: kostnad,
                investering: investering,
                besparing: arligBesparing,
                payback: aterbetalning,
                typ: document.getElementById('losningstyp').options[document.getElementById('losningstyp').selectedIndex].text
            };
            document.getElementById('lead-data').value = JSON.stringify(leadData);

            document.getElementById('empty-state').style.display = 'none';
            document.getElementById('result-container').style.display = 'block';
        });

        // Lead Form Submit
        document.getElementById('lead-form').addEventListener('submit', async function(e) {
            e.preventDefault();
            const email = document.getElementById('lead-email').value;
            const data = document.getElementById('lead-data').value;
            const submitBtn = this.querySelector('button[type="submit"]');
            
            submitBtn.innerText = 'Skickar...';
            submitBtn.disabled = true;

            try {
                const response = await fetch('/api/roi-lead', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email: email, data: JSON.parse(data), source: 'roi-kalkylator' })
                });

                if(response.ok) {
                    document.getElementById('lead-success').classList.remove('hidden');
                    submitBtn.style.display = 'none';
                    document.getElementById('lead-email').style.display = 'none';
                } else {
                    submitBtn.innerText = 'Något gick fel, försök igen';
                    submitBtn.disabled = false;
                }
            } catch (error) {
                console.error('Error:', error);
                submitBtn.innerText = 'Kunde inte nå servern';
                submitBtn.disabled = false;
            }
        });
    </script>
</body>
</html>
"""
    with open('/data/workspace/projects/proptech-guide-se/static/roi-kalkylator.html', 'w') as f:
        f.write(html_content)
    print("Created static/roi-kalkylator.html")

create_roi_calc()
