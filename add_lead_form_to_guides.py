import os
import re

guider_path = "/data/workspace/projects/proptech-guide-se/static/guider.html"

with open(guider_path, "r") as f:
    content = f.read()

# Replace the "Sponsra en guide" section with a lead capture form and the sponsor pitch side-by-side or below
lead_form_html = """
<section class="max-w-5xl mx-auto px-6 pb-16">
  <div class="grid md:grid-cols-2 gap-6">
    <div class="bg-white rounded-2xl border border-slate-200 p-8 shadow-sm">
      <h2 class="text-2xl font-extrabold tracking-tight mb-3">Har ni ett specifikt behov just nu?</h2>
      <p class="text-slate-600 mb-6">Beskriv vad ni söker så matchar vi er med upp till tre relevanta leverantörer som kan lösa problemet.</p>
      <div data-lead-form data-source="guider-sida" data-title="Få offerter och förslag"></div>
    </div>
    <div class="bg-slate-900 text-white rounded-2xl p-8 shadow-sm">
      <h2 class="text-2xl font-extrabold tracking-tight mb-3">Sponsra en guide</h2>
      <p class="text-slate-300 mb-6">Våra guider laddas ner av fastighetsägare, förvaltare
      och BRF-styrelser som står inför ett konkret beslut. Som exklusiv sponsor står ert namn på guiden,
      ni får er logotyp i PDF:en och samtliga nedladdningsleads som samtyckt till kontakt.
      Just nu finns 13 lediga sponsorplatser.</p>
      <a href="/for-leverantorer#sponsring" class="inline-block bg-white text-slate-900 px-6 py-3 rounded-xl font-bold hover:bg-slate-100 transition">Se upplägg och priser</a>
    </div>
  </div>
</section>
"""

# replace the sponsor section
content = re.sub(r'<section class="max-w-5xl mx-auto px-6 pb-16">.*?<div class="bg-slate-900 text-white rounded-2xl p-8 md:p-10">.*?Sponsra en guide.*?Se upplägg och priser</a>\s*</div>\s*</section>', lead_form_html, content, flags=re.DOTALL)

with open(guider_path, "w") as f:
    f.write(content)
