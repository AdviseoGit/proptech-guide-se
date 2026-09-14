import re

index_path = "/data/workspace/projects/proptech-guide-se/static/index.html"
with open(index_path, "r") as f:
    content = f.read()

# Make the CTA stronger and more action-oriented
old_cta = """<h2 class="text-3xl font-extrabold tracking-tight mb-4">Vet du inte vilken leverantör som passar?</h2>
      <p class="text-slate-600 text-lg mb-6">Beskriv ert behov en gång. Vi matchar mot leverantörer som arbetar med er typ av fastighet och storlek.</p>"""

new_cta = """<h2 class="text-3xl font-extrabold tracking-tight mb-4">Få prisförslag från matchande leverantörer</h2>
      <p class="text-slate-600 text-lg mb-6">Beskriv ert behov så tar vi fram upp till tre leverantörer som matchar er fastighetstyp och beståndsstorlek.</p>"""

content = content.replace(old_cta, new_cta)

with open(index_path, "w") as f:
    f.write(content)
