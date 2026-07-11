import json

new_companies = [
    {
        "name": "Mestro",
        "category": "energi",
        "category_label": "Energi & Hållbarhet",
        "description": "Ledande plattform för energiuppföljning. Samlar automatiskt in mätdata och hjälper fastighetsägare att visualisera, analysera och sänka sin energiförbrukning.",
        "tags": ["Energiuppföljning", "EMS", "API-integration"]
    },
    {
        "name": "Sengera",
        "category": "energi",
        "category_label": "Energi & Hållbarhet",
        "description": "AI-baserad energioptimering för fastigheter. Använder maskininlärning för att styra värmesystem dynamiskt och minska energikostnader med bibehållen komfort.",
        "tags": ["AI Värmestyrning", "Optimering", "Prediktiv analys"]
    },
    {
        "name": "Enjay",
        "category": "energi",
        "category_label": "Energi & Hållbarhet",
        "description": "Svensk greentech-lösning för återvinning av energi i tuffa miljöer. Deras Lepido-system återvinner värme från exempelvis restaurangventilation, vilket radikalt sänker byggnadens energibehov.",
        "tags": ["Värmeåtervinning", "Greentech", "Hårdvara"]
    }
]

html_path = "/data/workspace/projects/proptech-guide-se/static/directory.html"

with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# Hitta insättningspunkt: efter sista company-card
import re
cards = list(re.finditer(r'<div class="company-card.*?(?=<!-- Company: |<div class="company-card|</div>\s*</section>)', content, re.DOTALL))
if not cards:
    print("Could not find cards")
    exit(1)

last_card_match = cards[-1]
insertion_point = last_card_match.end()

new_html = ""
for c in new_companies:
    tags_html = ""
    for t in c["tags"]:
        tags_html += f'<span class="inline-block bg-slate-100 text-slate-600 text-xs px-2 py-1 rounded">{t}</span> '
    
    card_html = f"""
        <div class="company-card bg-white rounded-2xl p-6 shadow-sm border border-slate-100 hover:shadow-md transition-shadow" data-category="{c['category']}">
            <h3 class="text-xl font-bold text-slate-900 mb-2">{c['name']}</h3>
            <p class="text-sm font-semibold text-sky-600 mb-3">{c['category_label']}</p>
            <p class="text-slate-600 text-sm mb-4">{c['description']}</p>
            <div class="mt-auto">
                {tags_html.strip()}
            </div>
        </div>
"""
    new_html += card_html

content = content[:insertion_point] + new_html + content[insertion_point:]

with open(html_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Added 3 companies.")
