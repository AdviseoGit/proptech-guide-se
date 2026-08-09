import re

file_path = "static/digital-trapphustavla-kalkylator.html"
with open(file_path, "r") as f:
    content = f.read()

# Optimera title
content = re.sub(
    r'<title>.*?</title>',
    r'<title>Digital Trapphustavla BRF & Fastighet - Räkna ut pris & besparing | Proptechguiden</title>',
    content
)

# Optimera description 
content = re.sub(
    r'<meta content="Räkna ut hur mycket.*?name="description"/>',
    r'<meta content="Räkna ut exakt hur mycket din BRF eller fastighet kan spara i tid och pengar på en digital trapphustavla. Få pris direkt och jämför offerter från leverantörer." name="description"/>',
    content
)

# Add clear FAQ / AI-citerbarhet section
if "## Vanliga frågor" not in content and "Vanliga frågor" not in content:
    faq_section = """
    <div class="mt-12 bg-white rounded-2xl shadow-sm p-8 border border-slate-200" id="faq" itemscope itemtype="https://schema.org/FAQPage">
      <h2 class="text-2xl font-bold mb-6">Vanliga frågor om digitala trapphustavlor</h2>
      
      <div class="space-y-6">
        <div itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">
          <h3 class="font-bold text-lg text-slate-800" itemprop="name">Vad kostar en digital trapphustavla?</h3>
          <div itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer">
            <p class="text-slate-600" itemprop="text">En digital trapphustavla kostar normalt <strong>mellan 300 kr och 500 kr per månad</strong> per skärm inklusive mjukvarulicens och drift. Hårdvaran (skärmen) kan antingen köpas loss för cirka 10 000 - 15 000 kr, eller ingå i en förhöjd månadskostnad.</p>
          </div>
        </div>

        <div itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">
          <h3 class="font-bold text-lg text-slate-800" itemprop="name">Lönar det sig för en BRF att skaffa informationsskärmar?</h3>
          <div itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer">
            <p class="text-slate-600" itemprop="text">Ja, i de flesta fall lönar det sig genom minskad administration och färre resor för fastighetsskötare. Om er förvaltare/vaktmästare lägger 2 timmar per månad (ca 900 kr) på att uppdatera papperslappar i trapphusen, betalar den digitala skärmen (400 kr/mån) av sig direkt från dag ett.</p>
          </div>
        </div>
      </div>
    </div>
    """
    
    # Insert before closing main
    content = content.replace("</main>", f"{faq_section}\n</main>")

with open(file_path, "w") as f:
    f.write(content)
print("Updated calculator SEO/GEO.")
