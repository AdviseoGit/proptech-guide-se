"""Delade sidbyggstenar för proptechguiden.se.

Sajten har vuxit som lösa HTML-filer där nav och footer klistrats in för hand,
vilket gjort att menyerna glidit isär mellan sidorna. Allt som genereras går
härifrån istället, så navigering och struktur är samma överallt.
"""

GA_ID = "G-7028BLJBRF"
BASE_URL = "https://proptechguiden.se"

# Målgrupperna sajten ska sortera besökare på. Ordningen styr menyn.
SEGMENTS = {
    "fastighetsagare": {
        "label": "Fastighetsägare",
        "title": "Proptech för fastighetsägare",
        "tagline": "Sänk driftnettots kostnadssida och höj fastighetsvärdet.",
        "pains": [
            ("Energikostnaderna äter driftnettot",
             "Värme, kyla och el står för merparten av driftkostnaden. Rätt styrning "
             "kapar 15–25 % utan att röra stammarna."),
            ("EU-krav och ESG-rapportering",
             "CSRD, EU-taxonomin och energideklarationer kräver data ni troligen inte "
             "samlar in systematiskt idag."),
            ("Fastighetsdata sitter fast i olika system",
             "Ekonomi, drift och teknik pratar inte med varandra, vilket gör "
             "investeringsbeslut till gissningar."),
            ("Grön finansiering kräver bevis",
             "Gröna lån och obligationer prissätts på verifierad prestanda, inte på "
             "ambitioner."),
        ],
        "needs": ["energi", "analys", "plattform", "forvaltning"],
        "tools": ["roi-kalkylator"],
    },
    "forvaltare": {
        "label": "Kommersiella förvaltare",
        "title": "Proptech för kommersiella förvaltare",
        "tagline": "Fler kvadratmeter per förvaltare, utan att servicenivån faller.",
        "pains": [
            ("Ärendehanteringen är manuell",
             "Felanmälningar via telefon och mejl gör att inget går att mäta, "
             "prioritera eller följa upp."),
            ("Ingen överblick över beståndet",
             "Utan gemensam driftbild upptäcks fel när hyresgästen ringer, inte när "
             "de uppstår."),
            ("Hyresgästupplevelsen avgör omförhandlingar",
             "I kommersiella lägen är service och tillgänglighet det som håller kvar "
             "hyresgäster."),
            ("Passage och bokning löses per fastighet",
             "Varje objekt får sitt eget system, vilket gör förvaltningen dyrare för "
             "varje nytt uppdrag."),
        ],
        "needs": ["forvaltning", "boende", "access", "iot"],
        "tools": ["digital-trapphustavla-kalkylator", "roi-kalkylator"],
    },
    "brf": {
        "label": "BRF-styrelser",
        "title": "Proptech för BRF-styrelser",
        "tagline": "Lägre månadsavgift och mindre styrelsearbete.",
        "pains": [
            ("Avgiftshöjningar på grund av energipriser",
             "Föreningens största rörliga kostnad går att styra ner utan att medlemmarna "
             "märker skillnad i komforten."),
            ("Styrelsearbetet tar för mycket tid",
             "Bokningar, felanmälan, nyckelhantering och information sköts ideellt på "
             "kvällar och helger."),
            ("Nyckelhanteringen är ett säkerhetshål",
             "Borttappade nycklar innebär i praktiken låsbyte för hela föreningen."),
            ("Svårt att jämföra offerter",
             "Styrelsen är inte upphandlare och saknar referenspriser att bedöma "
             "förslagen mot."),
        ],
        "needs": ["energi", "access", "boende", "forvaltning"],
        "tools": ["digital-trapphustavla-kalkylator"],
    },
}

CATEGORY_LABELS = {
    "forvaltning": "Digital Förvaltning & Drift",
    "energi": "Energi & Hållbarhet",
    "iot": "IoT & Hårdvara",
    "access": "Lås & Passagesystem",
    "uthyrning": "Uthyrning & Marknad",
    "boende": "Boendeapp & Hyresgäst",
    "analys": "Analys & AI",
    "plattform": "Öppen Plattform",
}

# Katalognivåer. Ordningen är också sorteringsordningen i katalogen.
TIERS = {
    "partner": {
        "rank": 0,
        "label": "Partner",
        "badge": "bg-amber-100 text-amber-800 border-amber-200",
        "dofollow": True,
    },
    "verifierad": {
        "rank": 1,
        "label": "Verifierad",
        "badge": "bg-sky-100 text-sky-800 border-sky-200",
        "dofollow": True,
    },
    "free": {
        "rank": 2,
        "label": "",
        "badge": "",
        "dofollow": False,
    },
}

TOOLS = {
    "roi-kalkylator": {
        "title": "ROI-kalkylator för proptech",
        "desc": "Räkna på återbetalningstid och besparing för en energi- eller "
                "driftinvestering utifrån er yta och energikostnad.",
    },
    "digital-trapphustavla-kalkylator": {
        "title": "Kalkylator för digitala trapphustavlor",
        "desc": "Jämför kostnaden för tryckt information och namntavlor mot en "
                "digital lösning över fem år.",
    },
}


def head(title, description, canonical, extra_head=""):
    return f"""<!DOCTYPE html>
<html lang="sv">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{BASE_URL}{canonical}">
<meta name="robots" content="index, follow">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
<meta property="og:url" content="{BASE_URL}{canonical}">
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{GA_ID}');
</script>
<script src="https://cdn.tailwindcss.com"></script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
<link rel="icon" type="image/svg+xml" href="/static/favicon.svg">
<style>
  body {{ font-family: 'Plus Jakarta Sans', sans-serif; }}
  .gradient-text {{
    background: linear-gradient(90deg, #0284c7, #06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }}
</style>
{extra_head}
<script src="/cookie-banner.min.js"></script>
</head>
<body class="bg-slate-50 text-slate-900 flex flex-col min-h-screen">
"""


def nav(active=""):
    """Global navigering: målgrupp först, sedan katalog, verktyg, guider, säljsida."""
    def cls(key, base):
        return f"{base} text-sky-600 font-bold" if key == active else f"{base} hover:text-sky-600"

    segment_links = "".join(
        f'<a href="/{slug}" class="block px-4 py-2.5 hover:bg-slate-50 {"text-sky-600 font-bold" if slug == active else ""}">'
        f'<span class="font-semibold block">{s["label"]}</span>'
        f'<span class="text-xs text-slate-500">{s["tagline"]}</span></a>'
        for slug, s in SEGMENTS.items()
    )
    mobile_segments = "".join(
        f'<a href="/{slug}" class="{cls(slug, "block pl-4 text-sm")}">{s["label"]}</a>'
        for slug, s in SEGMENTS.items()
    )

    return f"""<nav class="bg-white border-b border-slate-200 sticky top-0 z-50">
<div class="p-5 max-w-7xl mx-auto w-full flex justify-between items-center">
<a href="/" class="text-2xl font-extrabold tracking-tight">PROPTECH<span class="text-sky-600">GUIDE</span></a>
<div class="hidden lg:flex items-center space-x-7 font-medium text-slate-600">
  <div class="relative group">
    <button class="{cls('segment', 'flex items-center gap-1 py-2')}">För dig som är
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
    </button>
    <div class="absolute left-0 top-full w-72 bg-white border border-slate-200 rounded-xl shadow-lg py-2 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition">
      {segment_links}
    </div>
  </div>
  <a href="/directory" class="{cls('directory', '')}">Leverantörer</a>
  <a href="/verktyg" class="{cls('verktyg', '')}">Verktyg</a>
  <a href="/guider" class="{cls('guider', '')}">Guider</a>
  <a href="/for-leverantorer" class="bg-slate-900 text-white px-4 py-2.5 rounded-xl font-bold hover:bg-slate-800 transition">För leverantörer</a>
</div>
<button class="lg:hidden text-slate-600" aria-label="Meny" aria-expanded="false" aria-controls="mobile-menu"
  onclick="var m=document.getElementById('mobile-menu');m.classList.toggle('hidden');this.setAttribute('aria-expanded',m.classList.contains('hidden')?'false':'true');">
  <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>
</button>
</div>
<div id="mobile-menu" class="hidden lg:hidden border-t border-slate-200 px-6 py-4">
<div class="flex flex-col space-y-3 font-medium text-slate-600">
  <span class="text-xs uppercase tracking-wide text-slate-400 font-bold">För dig som är</span>
  {mobile_segments}
  <a href="/directory" class="{cls('directory', 'block pt-2 border-t border-slate-100')}">Leverantörer</a>
  <a href="/verktyg" class="{cls('verktyg', 'block')}">Verktyg</a>
  <a href="/guider" class="{cls('guider', 'block')}">Guider</a>
  <a href="/for-leverantorer" class="{cls('for-leverantorer', 'block')}">För leverantörer</a>
</div>
</div>
</nav>
"""


def footer():
    segment_links = "".join(
        f'<li><a href="/{slug}" class="hover:text-sky-600">{s["label"]}</a></li>'
        for slug, s in SEGMENTS.items()
    )
    return f"""<footer class="bg-white border-t border-slate-200 mt-auto">
<div class="max-w-7xl mx-auto px-6 py-12 grid grid-cols-2 md:grid-cols-4 gap-8 text-sm">
  <div>
    <div class="text-lg font-extrabold tracking-tight mb-3">PROPTECH<span class="text-sky-600">GUIDE</span></div>
    <p class="text-slate-500">Oberoende guide till fastighetsteknik i Sverige.</p>
  </div>
  <div>
    <h3 class="font-bold mb-3">Målgrupper</h3>
    <ul class="space-y-2 text-slate-500">{segment_links}</ul>
  </div>
  <div>
    <h3 class="font-bold mb-3">Innehåll</h3>
    <ul class="space-y-2 text-slate-500">
      <li><a href="/directory" class="hover:text-sky-600">Leverantörskatalog</a></li>
      <li><a href="/verktyg" class="hover:text-sky-600">Kalkylatorer</a></li>
      <li><a href="/guider" class="hover:text-sky-600">Guider</a></li>
      <li><a href="/kategorier" class="hover:text-sky-600">Kategorier</a></li>
    </ul>
  </div>
  <div>
    <h3 class="font-bold mb-3">Om</h3>
    <ul class="space-y-2 text-slate-500">
      <li><a href="/for-leverantorer" class="hover:text-sky-600">Bli partner</a></li>
      <li><a href="/om-sajten" class="hover:text-sky-600">Om sajten</a></li>
      <li><a href="/privacy-policy" class="hover:text-sky-600">Integritetspolicy</a></li>
    </ul>
  </div>
</div>
<div class="border-t border-slate-100 py-6 text-center text-slate-400 text-sm">
  <p>Denna sajt skapas och drivs med hjälp av AI &middot; <a href="/om-sajten" class="hover:text-sky-600">Om sajten</a></p>
  <p class="mt-1">© 2026 Proptech Guide Sverige | Utvecklad av Adviseo</p>
</div>
</footer>
</body>
</html>
"""


def lead_form(source, segment="", need="", title="", intro=""):
    """Bädda in den delade leadwidgeten."""
    attrs = f'data-lead-form data-source="{source}"'
    if segment:
        attrs += f' data-segment="{segment}"'
    if need:
        attrs += f' data-need="{need}"'
    if title:
        attrs += f' data-title="{title}"'
    if intro:
        attrs += f' data-intro="{intro}"'
    return f'<div {attrs}></div>\n<script src="/lead-engine.js"></script>'


def breadcrumbs(items):
    """items = [(label, href), ...]. Sista posten renderas utan länk."""
    parts = []
    for i, (label, href) in enumerate(items):
        if i == len(items) - 1:
            parts.append(f'<span class="text-slate-900 font-medium">{label}</span>')
        else:
            parts.append(f'<a href="{href}" class="hover:text-sky-600">{label}</a>')
    return ('<nav class="text-sm text-slate-500 mb-6 flex gap-2 flex-wrap">'
            + '<span class="text-slate-300">/</span>'.join(parts) + "</nav>")
