import re
with open('/data/workspace/projects/proptech-guide-se/static/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add to verktyg section on index
if 'Digital Trapphustavla' not in content:
    content = content.replace(
        '<a href="roi-kalkylator" class="block mt-1 text-lg leading-tight font-medium text-black hover:underline">ROI-Kalkylator: Proptech</a>',
        '<a href="roi-kalkylator" class="block mt-1 text-lg leading-tight font-medium text-black hover:underline">ROI-Kalkylator: Proptech</a>\n                                <p class="mt-2 text-slate-500">Beräkna den potentiella avkastningen för dina fastighetsinvesteringar.</p>\n                            </div>\n                        </div>\n                    </li>\n                    <li>\n                        <div class="md:flex">\n                            <div class="p-8">\n                                <div class="uppercase tracking-wide text-sm text-sky-600 font-semibold">Nytt verktyg</div>\n                                <a href="digital-trapphustavla-kalkylator" class="block mt-1 text-lg leading-tight font-medium text-black hover:underline">Besparingskalkylator: Digital Trapphustavla</a>\n                                <p class="mt-2 text-slate-500">Räkna ut hur mycket din BRF sparar i tid och pengar på att digitalisera entrén.</p>'
    )
    with open('/data/workspace/projects/proptech-guide-se/static/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
        print("Updated tools section on index.html")
