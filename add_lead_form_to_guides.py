import re

GUIDES = [
    "/data/workspace/projects/proptech-guide-se/static/smarta-byggnader-guide.html",
    "/data/workspace/projects/proptech-guide-se/static/brf-digitalisering-guide.html",
    "/data/workspace/projects/proptech-guide-se/static/proptech-roi-guide.html"
]

LEAD_FORM_HTML = """
            <!-- Lead Capture Form -->
            <div class="mt-16 bg-sky-50 border border-sky-100 p-8 rounded-2xl text-center">
                <h3 class="text-2xl font-bold mb-3 text-slate-900">Ladda ner vår kompletta PropTech ROI-guide (PDF)</h3>
                <p class="text-slate-600 mb-6 max-w-xl mx-auto">Få djupare insikter och konkreta räkneexempel direkt till din inkorg. Perfekt underlag för ditt nästa styrelsemöte eller ledningsgrupp.</p>
                <form id="lead-form-guide" class="flex flex-col sm:flex-row justify-center max-w-lg mx-auto gap-3">
                    <input type="email" id="email-guide" placeholder="Din e-postadress" class="w-full px-4 py-3 rounded-xl border border-slate-300 focus:ring-2 focus:ring-sky-500 outline-none transition-shadow" required>
                    <button type="submit" class="bg-sky-600 text-white font-bold px-8 py-3 rounded-xl hover:bg-sky-700 transition-colors whitespace-nowrap">Ladda ner PDF</button>
                </form>
                <p id="form-message-guide" class="mt-4 text-emerald-600 font-medium"></p>
            </div>
            
            <script>
            document.addEventListener('DOMContentLoaded', function() {
                const leadForm = document.getElementById('lead-form-guide');
                if(leadForm) {
                    leadForm.addEventListener('submit', async function(e) {
                        e.preventDefault();
                        const email = document.getElementById('email-guide').value;
                        const messageEl = document.getElementById('form-message-guide');
                        messageEl.textContent = 'Skickar...';

                        try {
                            const response = await fetch('/api/lead', {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({ email: email })
                            });
                            if (response.ok) {
                                messageEl.textContent = 'Tack! Guiden har skickats till din e-post.';
                                document.getElementById('email-guide').value = '';
                            } else {
                                messageEl.textContent = 'Ett fel uppstod. Försök igen senare.';
                                messageEl.classList.remove('text-emerald-600');
                                messageEl.classList.add('text-red-600');
                            }
                        } catch(err) {
                            messageEl.textContent = 'Kunde inte ansluta till servern.';
                            messageEl.classList.remove('text-emerald-600');
                            messageEl.classList.add('text-red-600');
                        }
                    });
                }
            });
            </script>
"""

for filepath in GUIDES:
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()
    
    if "lead-form-guide" in html:
        print(f"Skipping {filepath} - form already exists")
        continue

    # Insert right before </article> or before the final </div> in main
    if "</article>" in html:
        html = html.replace("</article>", f"{LEAD_FORM_HTML}\n        </article>")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Added form to {filepath}")
    else:
        # Fallback for pages without <article>
        match = re.search(r'</main>', html)
        if match:
             html = html[:match.start()] + LEAD_FORM_HTML + "\n    </main>" + html[match.end():]
             with open(filepath, "w", encoding="utf-8") as f:
                 f.write(html)
             print(f"Added form to {filepath} (before </main>)")
        else:
             print(f"Failed to find insertion point in {filepath}")
