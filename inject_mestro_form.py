import re
from pathlib import Path

path = Path("/data/workspace/projects/proptech-guide-se/static/iot-energieffektivisering.html")
html = path.read_text("utf-8")

form_html = """
<!-- Lead Capture Form -->
<div class="mt-16 bg-sky-50 border border-sky-100 p-8 rounded-2xl text-center">
<h3 class="text-2xl font-bold mb-3 text-slate-900">Ladda ner vår kompletta IoT & Energieffektivisering-guide (PDF)</h3>
<p class="text-slate-600 mb-6 max-w-xl mx-auto">Få djupare insikter och konkreta räkneexempel direkt till din inkorg. I stolt samarbete med Mestro.</p>
<form class="flex flex-col sm:flex-row justify-center max-w-lg mx-auto gap-3" id="lead-form-guide">
<input class="w-full px-4 py-3 rounded-xl border border-slate-300 focus:ring-2 focus:ring-sky-500 outline-none transition-shadow" id="email-guide" placeholder="Din e-postadress" required="" type="email"/>
<button class="bg-sky-600 text-white font-bold px-8 py-3 rounded-xl hover:bg-sky-700 transition-colors whitespace-nowrap" type="submit">Ladda ner PDF</button>
</form>
<p class="mt-4 text-emerald-600 font-medium" id="form-message-guide"></p>
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
                    body: JSON.stringify({ email: email, guide_slug: 'iot-energieffektivisering' })
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

# Insert before </article>
if "<!-- Lead Capture Form -->" not in html:
    html = html.replace("</article>", form_html + "\n</article>")
    path.write_text(html, "utf-8")
    print("Form injected")
else:
    print("Form already exists")
