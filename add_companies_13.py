import os
from bs4 import BeautifulSoup
from datetime import datetime

file_path = "static/directory.html"

with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")
grid = soup.find("div", class_="grid")

if not grid:
    print("Could not find grid")
    exit(1)

new_companies = [
    {
        "name": "Nenda",
        "description": "B2B-streaming för kommersiella fastigheter och hotell. Ersätter linjär-TV med molnbaserad underhållning och information direkt till skärmarna.",
        "category": "Användarupplevelse",
        "url": "https://nenda.com/"
    },
    {
        "name": "Ambiductor",
        "description": "Sveriges ledande leverantör av smarta mätare för fjärrvärme, vatten och kyla via IoT (LoRaWAN).",
        "category": "Energi & Hållbarhet",
        "url": "https://www.ambiductor.se/"
    },
    {
        "name": "Eways",
        "description": "Helhetslösningar för elbilsladdning i fastigheter och BRF:er. Smart laddinfrastruktur och lastbalansering.",
        "category": "Infrastruktur & IoT",
        "url": "https://eways.se/"
    },
    {
        "name": "Avidly",
        "description": "Automatiserad marknadsföring och CRM för fastighetsbranschen, byggt på HubSpot. Optimerar uthyrningsprocesser och lead management.",
        "category": "Administration",
        "url": "https://www.avidlyagency.com/se/fastighet"
    },
    {
        "name": "Olsbergs",
        "description": "Smarta styrsystem för fastighetsautomation och belysning. Fokus på energieffektivisering i kommersiella lokaler.",
        "category": "Energi & Hållbarhet",
        "url": "https://www.olsbergs.com/"
    }
]

for company in new_companies:
    card = soup.new_tag("div", attrs={"class": "bg-white rounded-xl shadow-sm border border-slate-200 p-6 hover:shadow-md transition-shadow"})
    
    header_div = soup.new_tag("div", attrs={"class": "flex justify-between items-start mb-4"})
    
    title_div = soup.new_tag("div")
    h3 = soup.new_tag("h3", attrs={"class": "text-xl font-bold text-slate-900"})
    h3.string = company["name"]
    category_span = soup.new_tag("span", attrs={"class": "inline-block px-3 py-1 bg-sky-50 text-sky-700 text-xs font-semibold rounded-full mt-2"})
    category_span.string = company["category"]
    
    title_div.append(h3)
    title_div.append(category_span)
    header_div.append(title_div)
    
    desc_p = soup.new_tag("p", attrs={"class": "text-slate-600 mb-6 text-sm"})
    desc_p.string = company["description"]
    
    link = soup.new_tag("a", attrs={"href": company["url"], "target": "_blank", "rel": "noopener noreferrer", "class": "text-sky-600 font-semibold hover:text-sky-700 text-sm flex items-center"})
    link.string = "Besök hemsida →"
    
    card.append(header_div)
    card.append(desc_p)
    card.append(link)
    
    grid.append(card)

# Update count text if exists
count_p = soup.find("p", string=lambda t: t and "Visar" in t and "proptech-bolag" in t)
if count_p:
    import re
    current_count_match = re.search(r'Visar (\d+) proptech-bolag', count_p.string)
    if current_count_match:
        current_count = int(current_count_match.group(1))
        new_count = current_count + len(new_companies)
        count_p.string = f"Visar {new_count} proptech-bolag i Sverige"

with open(file_path, "w", encoding="utf-8") as f:
    f.write(str(soup))

print("Added companies successfully.")
