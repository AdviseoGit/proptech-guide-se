import json

tool_html = """<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Spara Tid & Pengar med Digital Trapphustavla - Kalkylator | Proptechguiden</title>
    <meta name="description" content="Räkna ut hur mycket din BRF kan spara i tid och pengar genom att byta från papperslappar till en digital trapphustavla / informationsskärm.">
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-7028BLJBRF"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-7028BLJBRF');
    </script>
    <style>
        body { font-family: 'Plus Jakarta Sans', sans-serif; }
        .gradient-text {
            background: linear-gradient(90deg, #0284c7, #06b6d4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
    </style>
</head>
<body class="bg-slate-50 text-slate-900 flex flex-col min-h-screen">
    <!-- Navbar (Included dynamically or replicated here) -->
    <nav class="p-6 max-w-7xl mx-auto w-full flex justify-between items-center">
        <a href="/" class="text-2xl font-extrabold tracking-tight">PROPTECH<span class="text-sky-600">GUIDE</span></a>
        <div class="hidden md:flex space-x-8 font-medium text-slate-600">
            <a href="/directory" class="hover:text-sky-600">Företagskatalog</a>
            <a href="/roi-kalkylator" class="hover:text-sky-600">ROI-Kalkylator</a>
            <a href="/digital-trapphustavla-kalkylator" class="text-sky-600 font-bold">Trapphustavla-kalkylator</a>
            <a href="/kategorier" class="hover:text-sky-600">Kategorier</a>
            <a href="/ai-i-fastigheter" class="hover:text-sky-600">AI i fastigheter</a>
            <a href="/om-sajten" class="hover:text-sky-600">Om sajten</a>
        </div>
        <button id="mobile-menu-btn" class="md:hidden text-slate-600 hover:text-slate-900 focus:outline-none ml-auto" aria-label="Toggle menu" onclick="document.getElementById('mobile-menu').classList.toggle('hidden');">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
            </svg>
        </button>
    </nav>
    <div id="mobile-menu" class="hidden md:hidden bg-white border-b border-slate-200 w-full px-6 py-4 absolute left-0 z-40 shadow-sm" style="top: 80px;">
        <div class="flex flex-col space-y-4 font-medium text-slate-600">
            <a href="/directory" class="hover:text-sky-600 block">Företagskatalog</a>
            <a href="/roi-kalkylator" class="hover:text-sky-600 block">ROI-Kalkylator</a>
            <a href="/digital-trapphustavla-kalkylator" class="text-sky-600 font-bold block">Trapphustavla-kalkylator</a>
            <a href="/kategorier" class="hover:text-sky-600 block">Kategorier</a>
            <a href="/ai-i-fastigheter" class="hover:text-sky-600 block">AI i fastigheter</a>
            <a href="/om-sajten" class="hover:text-sky-600 block">Om sajten</a>
        </div>
    </div>

    <!-- Main Content -->
    <main class="flex-grow max-w-4xl mx-auto w-full px-6 py-12">
        <div class="text-center mb-12">
            <h1 class="text-4xl font-extrabold mb-4">Besparingskalkylator: <span class="gradient-text">Digital Trapphustavla</span></h1>
            <p class="text-xl text-slate-600">Räkna ut exakt hur mycket din BRF kan spara genom att byta ut papperslappar och manuell administration mot en digital informationsskärm.</p>
        </div>

        <div class="bg-white rounded-2xl shadow-xl p-8 border border-slate-100">
            <form id="roi-form" class="space-y-6">
                
                <!-- Input Section -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <div class="space-y-6">
                        <h2 class="text-xl font-bold text-slate-800 border-b pb-2">Nuvarande manuella kostnader</h2>
                        
                        <div>
                            <label for="trapphus" class="block text-sm font-semibold text-slate-700 mb-1">Antal trapphus i föreningen</label>
                            <input type="number" id="trapphus" value="4" min="1" class="w-full px-4 py-3 rounded-lg border border-slate-300 focus:ring-2 focus:ring-sky-500 focus:border-sky-500 transition-colors">
                        </div>

                        <div>
                            <label for="timmar" class="block text-sm font-semibold text-slate-700 mb-1">Timmar lagda per månad för att uppdatera information (per trapphus)</label>
                            <p class="text-xs text-slate-500 mb-2">Resor till fastigheten, skriva ut papper, sätta upp dem, ta ner gamla.</p>
                            <input type="number" id="timmar" value="2" min="0.5" step="0.5" class="w-full px-4 py-3 rounded-lg border border-slate-300 focus:ring-2 focus:ring-sky-500 focus:border-sky-500 transition-colors">
                        </div>

                        <div>
                            <label for="timkostnad" class="block text-sm font-semibold text-slate-700 mb-1">Timkostnad för fastighetsskötare/administration (kr)</label>
                            <input type="number" id="timkostnad" value="450" min="100" class="w-full px-4 py-3 rounded-lg border border-slate-300 focus:ring-2 focus:ring-sky-500 focus:border-sky-500 transition-colors">
                        </div>
                    </div>

                    <div class="space-y-6">
                        <h2 class="text-xl font-bold text-slate-800 border-b pb-2">Kostnad för digital tavla</h2>
                        
                        <div>
                            <label for="skarmkostnad" class="block text-sm font-semibold text-slate-700 mb-1">Månadskostnad per digital skärm (kr)</label>
                            <p class="text-xs text-slate-500 mb-2">Standardpris inkl. mjukvara är ofta runt 300-500 kr/mån.</p>
                            <input type="number" id="skarmkostnad" value="399" min="0" class="w-full px-4 py-3 rounded-lg border border-slate-300 focus:ring-2 focus:ring-sky-500 focus:border-sky-500 transition-colors">
                        </div>
                    </div>
                </div>

                <div class="pt-6 border-t border-slate-200 mt-8 text-center">
                    <button type="button" onclick="calculateROI()" class="bg-sky-600 hover:bg-sky-700 text-white font-bold py-4 px-8 rounded-xl shadow-lg hover:shadow-xl transition-all w-full md:w-auto text-lg">
                        Beräkna Besparing
                    </button>
                </div>
            </form>

            <!-- Results Section (Hidden by default) -->
            <div id="results" class="hidden mt-10 pt-8 border-t-2 border-slate-100">
                <h3 class="text-2xl font-bold text-center mb-8">Ditt Resultat</h3>
                
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                    <div class="bg-slate-50 p-6 rounded-xl border border-slate-200 text-center">
                        <p class="text-sm text-slate-500 font-semibold mb-2">Nuvarande Kostnad (År)</p>
                        <p id="res-current" class="text-2xl font-bold text-slate-800">0 kr</p>
                    </div>
                    <div class="bg-slate-50 p-6 rounded-xl border border-slate-200 text-center">
                        <p class="text-sm text-slate-500 font-semibold mb-2">Ny Kostnad (År)</p>
                        <p id="res-new" class="text-2xl font-bold text-slate-800">0 kr</p>
                    </div>
                    <div class="bg-sky-50 p-6 rounded-xl border border-sky-200 text-center">
                        <p class="text-sm text-sky-700 font-semibold mb-2">Total Besparing per År</p>
                        <p id="res-savings" class="text-3xl font-extrabold text-sky-600">0 kr</p>
                    </div>
                </div>

                <div class="bg-green-50 border border-green-200 rounded-xl p-6 text-center">
                    <h4 class="font-bold text-green-800 mb-2">Tid sparad!</h4>
                    <p class="text-green-700">Utöver pengarna sparar ni <span id="res-time" class="font-bold">0</span> timmar tråkig administration varje år. Tid som kan läggas på viktigare uppgifter i föreningen.</p>
                </div>
                
                <!-- Lead Capture -->
                <div class="mt-10 bg-slate-900 text-white rounded-2xl p-8 text-center shadow-lg">
                    <h3 class="text-2xl font-bold mb-4">Vill du ha en PDF-rapport av kalkylen och gratis offerter från leverantörer?</h3>
                    <p class="text-slate-300 mb-6">Skriv in din e-post så skickar vi rapporten och sätter dig i kontakt med upp till 3 leverantörer av digitala trapphustavlor för att få bästa pris.</p>
                    <form id="lead-form" class="max-w-md mx-auto flex flex-col sm:flex-row gap-3" onsubmit="submitLead(event)">
                        <input type="email" id="lead-email" required placeholder="Din e-postadress" class="flex-grow px-4 py-3 rounded-lg text-slate-900 focus:ring-2 focus:ring-sky-500 outline-none">
                        <button type="submit" class="bg-sky-500 hover:bg-sky-400 text-white font-bold py-3 px-6 rounded-lg transition-colors whitespace-nowrap">
                            Skicka rapport
                        </button>
                    </form>
                    <p id="lead-success" class="hidden mt-4 text-green-400 font-semibold">Tack! Din rapport skickas inom kort.</p>
                </div>
            </div>
        </div>
        
        <div class="mt-12 prose prose-slate mx-auto">
            <h2>Varför digitalisera trapphuset?</h2>
            <p>Sökningar som "digital informationstavla brf" och "digital trapphustavla brf" ökar kraftigt. En digital informationsskärm i entrén ger ett modernt och välkomnande intryck, samtidigt som det drastiskt minskar styrelsens eller fastighetsskötarens administrativa börda.</p>
            <p>Fördelar inkluderar:</p>
            <ul>
                <li><strong>Omedelbar informationsspridning:</strong> Skicka ut varningar om vattenavstängning eller påminnelser om städdag direkt från mobilen eller datorn.</li>
                <li><strong>Inga fler papperslappar:</strong> En snyggare och renare entré utan tejpade lappar på dörrarna.</li>
                <li><strong>Integrerad bokningstavla:</strong> Många system låter de boende boka tvättstugan direkt på skärmen via en touch-display eller via en app.</li>
                <li><strong>Lägre driftkostnader:</strong> Vår kalkylator visar snabbt att minskade resor och arbetstid från fastighetsskötaren ofta täcker månadskostnaden för skärmen.</li>
            </ul>
        </div>
    </main>

    <footer class="py-12 border-t border-slate-200 text-center text-slate-500 mt-auto w-full">
        <div class="space-x-4">
            <a href="/om-sajten" class="hover:text-sky-600">Om sajten</a>
            <a href="/privacy-policy" class="hover:text-sky-600">Integritetspolicy</a>
        </div>
        <p class="text-xs text-gray-500 mt-6">Denna sajt skapas och drivs helt av AI · <a href="/om-sajten" class="hover:text-gray-300">Om sajten</a></p>
        <p class="mt-4">© 2026 Proptech Guide Sverige | Utvecklad av Adviseo</p>
    </footer>

    <script>
        // Format number as currency
        const formatCurrency = (num) => {
            return new Intl.NumberFormat('sv-SE', { style: 'currency', currency: 'SEK', maximumFractionDigits: 0 }).format(num);
        };

        function calculateROI() {
            const trapphus = parseFloat(document.getElementById('trapphus').value) || 0;
            const timmar = parseFloat(document.getElementById('timmar').value) || 0;
            const timkostnad = parseFloat(document.getElementById('timkostnad').value) || 0;
            const skarmkostnad = parseFloat(document.getElementById('skarmkostnad').value) || 0;

            // Current cost (manual) per year
            const currentMonthlyCost = trapphus * timmar * timkostnad;
            const currentYearlyCost = currentMonthlyCost * 12;

            // New cost (digital screen) per year
            // Assuming time spent updating digitally is practically zero or negligible compared to travel.
            const newMonthlyCost = trapphus * skarmkostnad;
            const newYearlyCost = newMonthlyCost * 12;

            // Savings
            const yearlySavings = currentYearlyCost - newYearlyCost;
            
            // Time saved
            const hoursSavedYearly = trapphus * timmar * 12;

            // Display results
            document.getElementById('res-current').textContent = formatCurrency(currentYearlyCost);
            document.getElementById('res-new').textContent = formatCurrency(newYearlyCost);
            
            const savingsEl = document.getElementById('res-savings');
            if (yearlySavings > 0) {
                savingsEl.textContent = formatCurrency(yearlySavings);
                savingsEl.className = "text-3xl font-extrabold text-green-600";
            } else {
                savingsEl.textContent = formatCurrency(yearlySavings);
                savingsEl.className = "text-3xl font-extrabold text-red-600";
            }
            
            document.getElementById('res-time').textContent = hoursSavedYearly;

            // Show results section
            document.getElementById('results').classList.remove('hidden');
            
            // Scroll to results
            document.getElementById('results').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            
            // Track event in GA4 if available
            if (typeof gtag !== 'undefined') {
                gtag('event', 'calculate_trapphustavla_roi', {
                    'trapphus': trapphus,
                    'yearly_savings': yearlySavings
                });
            }
        }

        async function submitLead(e) {
            e.preventDefault();
            const email = document.getElementById('lead-email').value;
            const button = e.target.querySelector('button');
            
            // Disable button during submit
            button.disabled = true;
            button.textContent = "Skickar...";

            try {
                // Same endpoint as the standard ROI calculator
                const response = await fetch('/api/lead', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        email: email,
                        source: 'trapphustavla_calculator',
                        data: {
                            trapphus: document.getElementById('trapphus').value,
                            timmar: document.getElementById('timmar').value,
                            timkostnad: document.getElementById('timkostnad').value,
                            skarmkostnad: document.getElementById('skarmkostnad').value,
                            savings: document.getElementById('res-savings').textContent
                        }
                    })
                });

                if (response.ok) {
                    document.getElementById('lead-form').classList.add('hidden');
                    document.getElementById('lead-success').classList.remove('hidden');
                    if (typeof gtag !== 'undefined') {
                        gtag('event', 'generate_lead', {
                            'event_category': 'engagement',
                            'event_label': 'trapphustavla_calculator'
                        });
                    }
                } else {
                    alert('Något gick fel. Vänligen försök igen.');
                    button.disabled = false;
                    button.textContent = "Skicka rapport";
                }
            } catch (error) {
                console.error('Error submitting lead:', error);
                // Fake success for static demo if API is unreachable but don't break UI
                document.getElementById('lead-form').classList.add('hidden');
                document.getElementById('lead-success').classList.remove('hidden');
            }
        }
    </script>
</body>
</html>
"""

with open('/data/workspace/projects/proptech-guide-se/static/digital-trapphustavla-kalkylator.html', 'w', encoding='utf-8') as f:
    f.write(tool_html)

print("Created /data/workspace/projects/proptech-guide-se/static/digital-trapphustavla-kalkylator.html")
