"""Sidgenerator för proptechguiden.se.

Renderar allt som ska hänga ihop med katalogdatat och målgruppsindelningen:

    directory.html            leverantörskatalog, sorterad på tier
    leverantor/<slug>.html    profilsida per leverantör
    fastighetsagare.html      segmenthubb
    forvaltare.html           segmenthubb
    brf.html                  segmenthubb
    verktyg.html              kalkylatoröversikt
    guider.html               guidehubb med sponsorplatser
    for-leverantorer.html     säljsida för de tre intäktsströmmarna
    sitemap.xml

Kör:  python build.py
"""
import json
from datetime import date
from pathlib import Path

import site_template as T

ROOT = Path(__file__).parent
STATIC = ROOT / "static"
DATA = ROOT / "data"


def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def write(path, html):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    print(f"  {path.relative_to(ROOT)}")


def tier_rank(company):
    return T.TIERS.get(company.get("tier", "free"), T.TIERS["free"])["rank"]


def sort_companies(companies):
    """Partners först, sedan verifierade, sedan övriga i bokstavsordning.

    Det är själva produkten i intäktsström 1: en betald placering syns överst
    i både katalogen och varje kategorilistning.
    """
    return sorted(companies, key=lambda c: (tier_rank(c), c["name"].lower()))


# --------------------------------------------------------------------------
# Komponenter
# --------------------------------------------------------------------------

def tier_badge(company):
    tier = T.TIERS.get(company.get("tier", "free"), T.TIERS["free"])
    if not tier["label"]:
        return ""
    return (f'<span class="text-xs font-bold px-2 py-0.5 rounded-full border {tier["badge"]}">'
            f'{tier["label"]}</span>')


def company_link(company):
    """Betalande nivåer får följbar länk, gratisposter får nofollow.

    Länkvärdet är en del av det partners betalar för, och att dela ut det
    gratis till 100+ poster urholkar både produkten och sajtens egen profil.
    """
    url = company.get("url") or ""
    if not url.startswith("http"):
        return ""
    tier = T.TIERS.get(company.get("tier", "free"), T.TIERS["free"])
    rel = "noopener noreferrer" if tier["dofollow"] else "nofollow noopener noreferrer"
    return (f'<a href="{url}" target="_blank" rel="{rel}" '
            f'class="inline-flex items-center text-sm font-bold text-slate-900 hover:text-sky-600">'
            f'Besök hemsida →</a>')


def company_card(company):
    partner = company.get("tier") == "partner"
    ring = ("border-amber-200 ring-1 ring-amber-100" if partner
            else "border-slate-100")
    profile = ""
    if company.get("tier") in ("partner", "verifierad"):
        profile = (f'<a href="/leverantor/{company["slug"]}" '
                   f'class="text-sm font-bold text-sky-600 hover:underline">Läs mer</a>')
    return f"""
<div class="company-card bg-white rounded-2xl p-6 shadow-sm border {ring} hover:shadow-md transition-shadow flex flex-col"
     data-category="{company['category']}" data-segments="{' '.join(company.get('segments', []))}"
     data-tier="{company.get('tier', 'free')}" data-name="{company['name'].lower()}">
  <div class="flex items-start justify-between gap-2 mb-2">
    <h3 class="text-xl font-bold text-slate-900">{company['name']}</h3>
    {tier_badge(company)}
  </div>
  <p class="text-sm font-semibold text-sky-600 mb-3">{T.CATEGORY_LABELS.get(company['category'], company['category'])}</p>
  <p class="text-slate-600 text-sm mb-6 flex-grow">{company['description']}</p>
  <div class="flex items-center gap-4">{company_link(company)}{profile}</div>
</div>"""


def cta_band(source, segment="", need="", heading="", text=""):
    heading = heading or "Vet du inte vilken leverantör som passar?"
    text = text or ("Beskriv ert behov en gång. Vi matchar mot leverantörer som "
                    "arbetar med er typ av fastighet och storlek.")
    return f"""
<section class="max-w-4xl mx-auto px-6 py-16">
  <div class="grid md:grid-cols-2 gap-10 items-start">
    <div>
      <h2 class="text-3xl font-extrabold tracking-tight mb-4">{heading}</h2>
      <p class="text-slate-600 text-lg mb-6">{text}</p>
      <ul class="space-y-3 text-slate-600">
        <li class="flex gap-3"><span class="text-emerald-600 font-bold">✓</span> Kostnadsfritt och utan köpkrav</li>
        <li class="flex gap-3"><span class="text-emerald-600 font-bold">✓</span> Vi är oberoende av leverantörerna</li>
        <li class="flex gap-3"><span class="text-emerald-600 font-bold">✓</span> Svar inom en arbetsdag</li>
      </ul>
    </div>
    <div>{T.lead_form(source, segment=segment, need=need)}</div>
  </div>
</section>"""


# --------------------------------------------------------------------------
# Katalog
# --------------------------------------------------------------------------

def build_directory(companies):
    ordered = sort_companies(companies)
    partners = [c for c in ordered if c.get("tier") == "partner"]

    category_options = "".join(
        f'<option value="{k}">{v}</option>' for k, v in T.CATEGORY_LABELS.items()
    )
    segment_options = "".join(
        f'<option value="{k}">{v["label"]}</option>' for k, v in T.SEGMENTS.items()
    )

    featured = ""
    if partners:
        featured = f"""
<section class="mb-12">
  <div class="flex items-center gap-3 mb-4">
    <h2 class="text-2xl font-extrabold tracking-tight">Utvalda partners</h2>
    <span class="text-xs text-slate-400">Betald placering</span>
  </div>
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    {''.join(company_card(c) for c in partners)}
  </div>
</section>"""

    cards = "".join(company_card(c) for c in ordered)

    body = f"""
<main class="max-w-7xl mx-auto px-6 py-12 flex-grow w-full">
{T.breadcrumbs([("Hem", "/"), ("Leverantörer", "/directory")])}
<div class="text-center mb-10">
  <h1 class="text-4xl md:text-5xl font-extrabold mb-4 tracking-tight">Hitta rätt <span class="gradient-text">proptech</span>-leverantör</h1>
  <p class="text-xl text-slate-600 max-w-2xl mx-auto">{len(ordered)} bolag inom fastighetsteknik i Sverige. Filtrera på kategori och målgrupp.</p>
</div>

<div class="bg-white p-5 rounded-2xl shadow-sm border border-slate-200 mb-8 grid md:grid-cols-4 gap-4">
  <input id="searchInput" type="text" placeholder="Sök bolag eller nyckelord…"
    class="md:col-span-2 w-full px-4 py-3 rounded-xl border border-slate-300 focus:ring-2 focus:ring-sky-500 outline-none">
  <select id="categoryFilter" class="w-full px-4 py-3 rounded-xl border border-slate-300 bg-white focus:ring-2 focus:ring-sky-500 outline-none">
    <option value="all">Alla kategorier</option>{category_options}
  </select>
  <select id="segmentFilter" class="w-full px-4 py-3 rounded-xl border border-slate-300 bg-white focus:ring-2 focus:ring-sky-500 outline-none">
    <option value="all">Alla målgrupper</option>{segment_options}
  </select>
</div>

{featured}

<h2 class="text-2xl font-extrabold tracking-tight mb-4">Alla leverantörer</h2>
<p class="text-slate-500 text-sm mb-6" id="resultCount"></p>
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6" id="directoryGrid">{cards}</div>
<p class="hidden text-center text-slate-500 py-12" id="noResults">Inga bolag matchar din filtrering.</p>
</main>

{cta_band("directory")}

<script>
(function () {{
  var search = document.getElementById('searchInput');
  var cat = document.getElementById('categoryFilter');
  var seg = document.getElementById('segmentFilter');
  var cards = document.querySelectorAll('#directoryGrid .company-card');
  var count = document.getElementById('resultCount');
  var empty = document.getElementById('noResults');

  function apply() {{
    var q = search.value.toLowerCase().trim();
    var c = cat.value, s = seg.value, shown = 0;
    cards.forEach(function (card) {{
      var okText = !q || card.textContent.toLowerCase().indexOf(q) !== -1;
      var okCat = c === 'all' || card.dataset.category === c;
      var okSeg = s === 'all' || card.dataset.segments.split(' ').indexOf(s) !== -1;
      var visible = okText && okCat && okSeg;
      card.classList.toggle('hidden', !visible);
      if (visible) shown++;
    }});
    count.textContent = 'Visar ' + shown + ' av {len(ordered)} bolag';
    empty.classList.toggle('hidden', shown > 0);
  }}

  [search, cat, seg].forEach(function (el) {{
    el.addEventListener('input', apply);
    el.addEventListener('change', apply);
  }});

  // Tillåt djuplänkning från segmentsidorna: /directory?segment=brf&kategori=energi
  var params = new URLSearchParams(location.search);
  if (params.get('segment')) seg.value = params.get('segment');
  if (params.get('kategori')) cat.value = params.get('kategori');
  apply();
}})();
</script>"""

    html = (T.head("Leverantörskatalog för proptech i Sverige | Proptechguiden",
                   f"Sök och filtrera bland {len(ordered)} svenska proptech-bolag. "
                   "Filtrera på kategori och målgrupp och få offert från rätt leverantör.",
                   "/directory")
            + T.nav("directory") + body + T.footer())
    write(STATIC / "directory.html", html)


def build_company_pages(companies):
    """Profilsidor för betalande nivåer — en del av vad en partnerplats ger."""
    built = 0
    for c in companies:
        if c.get("tier") not in ("partner", "verifierad"):
            continue
        usp = "".join(f'<li class="flex gap-3"><span class="text-emerald-600 font-bold">✓</span> {u}</li>'
                      for u in c.get("usp", []))
        usp_block = f'<ul class="space-y-3 text-slate-600 mb-8">{usp}</ul>' if usp else ""
        cases = "".join(
            f'<div class="bg-white rounded-2xl border border-slate-200 p-6">'
            f'<h3 class="font-bold mb-2">{case.get("title", "")}</h3>'
            f'<p class="text-slate-600 text-sm">{case.get("text", "")}</p></div>'
            for case in c.get("cases", [])
        )
        cases_block = (f'<section class="mt-12"><h2 class="text-2xl font-extrabold mb-4">Kundcase</h2>'
                       f'<div class="grid md:grid-cols-2 gap-6">{cases}</div></section>') if cases else ""

        body = f"""
<main class="max-w-4xl mx-auto px-6 py-12 flex-grow w-full">
{T.breadcrumbs([("Hem", "/"), ("Leverantörer", "/directory"), (c["name"], "")])}
<div class="flex items-start justify-between gap-4 mb-2">
  <h1 class="text-4xl font-extrabold tracking-tight">{c['name']}</h1>
  {tier_badge(c)}
</div>
<p class="text-sky-600 font-semibold mb-6">{T.CATEGORY_LABELS.get(c['category'], c['category'])}</p>
<p class="text-xl text-slate-600 mb-8">{c['description']}</p>
{usp_block}
<div class="flex flex-wrap gap-3 mb-4">{company_link(c)}</div>
<p class="text-sm text-slate-400">Målgrupper: {', '.join(T.SEGMENTS[s]['label'] for s in c.get('segments', []) if s in T.SEGMENTS)}</p>
{cases_block}
</main>

{cta_band('leverantor-' + c['slug'], need=c['category'],
          heading='Vill ni ha offert från ' + c['name'] + '?',
          text='Beskriv ert behov så förmedlar vi kontakten och tar samtidigt fram jämförbara alternativ.')}"""

        html = (T.head(f"{c['name']} – proptech-leverantör | Proptechguiden",
                       c["description"][:155],
                       f"/leverantor/{c['slug']}")
                + T.nav("directory") + body + T.footer())
        write(STATIC / "leverantor" / f"{c['slug']}.html", html)
        built += 1
    if built == 0:
        print("  (inga profilsidor — inga bolag har tier verifierad/partner ännu)")


# --------------------------------------------------------------------------
# Segmenthubbar
# --------------------------------------------------------------------------

def build_segment_pages(companies, guides):
    for slug, seg in T.SEGMENTS.items():
        pains = "".join(
            f"""<div class="bg-white rounded-2xl border border-slate-200 p-6">
  <h3 class="font-bold text-lg mb-2">{title}</h3>
  <p class="text-slate-600">{text}</p>
</div>""" for title, text in seg["pains"]
        )

        # Katalogingångar: en genväg per kategori som är relevant för målgruppen.
        cat_cards = ""
        for need in seg["needs"]:
            matching = [c for c in companies
                        if c["category"] == need and slug in c.get("segments", [])]
            cat_cards += f"""
<a href="/directory?segment={slug}&kategori={need}" class="group bg-white rounded-2xl border border-slate-200 p-6 hover:border-sky-300 hover:shadow-md transition">
  <h3 class="font-bold text-lg mb-1 group-hover:text-sky-600">{T.CATEGORY_LABELS[need]}</h3>
  <p class="text-slate-500 text-sm">{len(matching)} leverantörer för {seg['label'].lower()}</p>
</a>"""

        tool_cards = "".join(
            f"""<a href="/{t}" class="group bg-white rounded-2xl border border-slate-200 p-6 hover:border-sky-300 hover:shadow-md transition">
  <h3 class="font-bold text-lg mb-1 group-hover:text-sky-600">{T.TOOLS[t]['title']}</h3>
  <p class="text-slate-500 text-sm">{T.TOOLS[t]['desc']}</p>
</a>""" for t in seg["tools"] if t in T.TOOLS
        )

        seg_guides = [g for g in guides if slug in g.get("segments", [])][:6]
        guide_cards = "".join(
            f"""<a href="/{g['slug']}" class="group bg-white rounded-2xl border border-slate-200 p-6 hover:border-sky-300 hover:shadow-md transition">
  <h3 class="font-bold text-lg mb-1 group-hover:text-sky-600">{g['title']}</h3>
  <p class="text-slate-500 text-sm">{g['summary']}</p>
</a>""" for g in seg_guides
        )

        body = f"""
<main class="flex-grow w-full">
<header class="max-w-5xl mx-auto px-6 pt-12 pb-4">
  {T.breadcrumbs([("Hem", "/"), (seg["label"], "")])}
  <p class="text-sky-600 font-bold uppercase tracking-wide text-sm mb-3">För {seg['label'].lower()}</p>
  <h1 class="text-4xl md:text-6xl font-extrabold tracking-tight mb-5">{seg['title']}</h1>
  <p class="text-xl text-slate-600 max-w-2xl">{seg['tagline']} Vi kartlägger leverantörerna, räknar på affären och matchar er mot rätt partner.</p>
  <div class="flex flex-col sm:flex-row gap-4 mt-8">
    <a href="#offert" class="bg-sky-600 text-white px-8 py-4 rounded-xl font-bold hover:bg-sky-700 transition shadow-lg shadow-sky-600/25 text-center">Få matchade offerter</a>
    <a href="/directory?segment={slug}" class="bg-white border border-slate-300 px-8 py-4 rounded-xl font-bold hover:border-slate-400 transition text-center">Se leverantörer</a>
  </div>
</header>

<section class="max-w-5xl mx-auto px-6 py-14">
  <h2 class="text-3xl font-extrabold tracking-tight mb-6">Utmaningarna vi hör oftast</h2>
  <div class="grid md:grid-cols-2 gap-6">{pains}</div>
</section>

<section class="max-w-5xl mx-auto px-6 py-8">
  <h2 class="text-3xl font-extrabold tracking-tight mb-6">Leverantörer per område</h2>
  <div class="grid md:grid-cols-2 gap-6">{cat_cards}</div>
</section>

<section class="max-w-5xl mx-auto px-6 py-8">
  <h2 class="text-3xl font-extrabold tracking-tight mb-6">Räkna på investeringen</h2>
  <div class="grid md:grid-cols-2 gap-6">{tool_cards}</div>
</section>

<section class="max-w-5xl mx-auto px-6 py-8">
  <h2 class="text-3xl font-extrabold tracking-tight mb-6">Guider för {seg['label'].lower()}</h2>
  <div class="grid md:grid-cols-2 gap-6">{guide_cards}</div>
</section>

<div id="offert">
{cta_band("segment-" + slug, segment=slug,
          heading="Beskriv ert behov – vi matchar",
          text="Ett formulär, tre minuter. Vi går igenom vilka leverantörer som passar er "
               "storlek och tidplan och förmedlar kontakten.")}
</div>
</main>"""

        html = (T.head(f"{seg['title']} | Proptechguiden",
                       f"{seg['tagline']} Jämför leverantörer, räkna på ROI och få offerter "
                       f"anpassade för {seg['label'].lower()}.",
                       f"/{slug}")
                + T.nav(slug) + body + T.footer())
        write(STATIC / f"{slug}.html", html)


# --------------------------------------------------------------------------
# Verktyg och guider
# --------------------------------------------------------------------------

def build_tools_page():
    cards = "".join(
        f"""<a href="/{slug}" class="group bg-white rounded-2xl border border-slate-200 p-8 hover:border-sky-300 hover:shadow-md transition">
  <h2 class="text-2xl font-bold mb-2 group-hover:text-sky-600">{t['title']}</h2>
  <p class="text-slate-600">{t['desc']}</p>
  <span class="inline-block mt-4 font-bold text-sky-600">Öppna kalkylatorn →</span>
</a>""" for slug, t in T.TOOLS.items()
    )
    body = f"""
<main class="max-w-5xl mx-auto px-6 py-12 flex-grow w-full">
{T.breadcrumbs([("Hem", "/"), ("Verktyg", "/verktyg")])}
<h1 class="text-4xl md:text-5xl font-extrabold tracking-tight mb-4">Kalkylatorer för fastighetsteknik</h1>
<p class="text-xl text-slate-600 mb-10 max-w-2xl">Räkna på investeringen innan ni går ut med förfrågan. Alla kalkylatorer bygger på era egna siffror.</p>
<div class="grid md:grid-cols-2 gap-6">{cards}</div>
</main>
{cta_band("verktyg")}"""
    html = (T.head("Kalkylatorer för proptech och fastighetsdrift | Proptechguiden",
                   "Räkna på ROI, återbetalningstid och besparing för proptech-investeringar "
                   "med våra kostnadsfria kalkylatorer.",
                   "/verktyg")
            + T.nav("verktyg") + body + T.footer())
    write(STATIC / "verktyg.html", html)


def build_guides_page(guides):
    def card(g):
        sponsor = ""
        if g.get("sponsor"):
            s = g["sponsor"]
            sponsor = (f'<p class="text-xs text-slate-400 mt-3">I samarbete med '
                       f'<span class="font-bold text-slate-600">{s}</span></p>')
        badge = ('<span class="text-xs font-bold px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800">PDF</span>'
                 if g.get("gated") else "")
        return f"""<a href="/{g['slug']}" class="group bg-white rounded-2xl border border-slate-200 p-6 hover:border-sky-300 hover:shadow-md transition flex flex-col">
  <div class="flex items-start justify-between gap-2 mb-2">
    <h3 class="text-lg font-bold group-hover:text-sky-600">{g['title']}</h3>{badge}
  </div>
  <p class="text-slate-600 text-sm flex-grow">{g['summary']}</p>{sponsor}
</a>"""

    sections = ""
    for slug, seg in T.SEGMENTS.items():
        matching = [g for g in guides if slug in g.get("segments", [])]
        if not matching:
            continue
        sections += f"""
<section class="mb-14">
  <h2 class="text-2xl font-extrabold tracking-tight mb-1">För {seg['label'].lower()}</h2>
  <p class="text-slate-500 mb-6">{seg['tagline']}</p>
  <div class="grid md:grid-cols-3 gap-6">{''.join(card(g) for g in matching)}</div>
</section>"""

    open_slots = [g for g in guides if g.get("sponsor_slot_open") and not g.get("sponsor")]
    sponsor_pitch = f"""
<section class="max-w-5xl mx-auto px-6 pb-16">
  <div class="bg-slate-900 text-white rounded-2xl p-8 md:p-10">
    <h2 class="text-2xl font-extrabold tracking-tight mb-3">Sponsra en guide</h2>
    <p class="text-slate-300 mb-6 max-w-2xl">Våra guider laddas ner av fastighetsägare, förvaltare
    och BRF-styrelser som står inför ett konkret beslut. Som exklusiv sponsor står ert namn på guiden,
    ni får er logotyp i PDF:en och samtliga nedladdningsleads som samtyckt till kontakt.
    Just nu finns {len(open_slots)} lediga sponsorplatser.</p>
    <a href="/for-leverantorer#sponsring" class="inline-block bg-white text-slate-900 px-6 py-3 rounded-xl font-bold hover:bg-slate-100 transition">Se upplägg och priser</a>
  </div>
</section>"""

    body = f"""
<main class="max-w-5xl mx-auto px-6 py-12 flex-grow w-full">
{T.breadcrumbs([("Hem", "/"), ("Guider", "/guider")])}
<h1 class="text-4xl md:text-5xl font-extrabold tracking-tight mb-4">Guider för fastighetsbranschen</h1>
<p class="text-xl text-slate-600 mb-12 max-w-2xl">Oberoende genomgångar av regelverk, teknik och affärsvärde – sorterade efter vem du är.</p>
{sections}
</main>
{sponsor_pitch}"""
    html = (T.head("Guider om proptech, ESG och fastighetsteknik | Proptechguiden",
                   "Oberoende guider om ESG-rapportering, smarta byggnader, cybersäkerhet och ROI "
                   "för fastighetsägare, förvaltare och BRF:er.",
                   "/guider")
            + T.nav("guider") + body + T.footer())
    write(STATIC / "guider.html", html)


# --------------------------------------------------------------------------
# Säljsidan
# --------------------------------------------------------------------------

def build_partner_page(companies, guides):
    total = len(companies)
    open_slots = len([g for g in guides if g.get("sponsor_slot_open") and not g.get("sponsor")])

    def tier_card(name, price, note, features, highlight=False):
        items = "".join(
            f'<li class="flex gap-3"><span class="text-emerald-600 font-bold">✓</span><span>{f}</span></li>'
            for f in features)
        border = "border-sky-500 ring-2 ring-sky-100" if highlight else "border-slate-200"
        tag = ('<span class="absolute -top-3 left-6 bg-sky-600 text-white text-xs font-bold px-3 py-1 rounded-full">Vanligast</span>'
               if highlight else "")
        return f"""<div class="relative bg-white rounded-2xl border {border} p-8 flex flex-col">
  {tag}
  <h3 class="text-xl font-extrabold mb-1">{name}</h3>
  <p class="text-3xl font-extrabold tracking-tight mb-1">{price}</p>
  <p class="text-sm text-slate-500 mb-6">{note}</p>
  <ul class="space-y-3 text-slate-600 text-sm flex-grow">{items}</ul>
  <a href="#ansok" class="mt-8 text-center bg-slate-900 text-white px-6 py-3 rounded-xl font-bold hover:bg-slate-800 transition">Ansök</a>
</div>"""

    categories = "".join(f'<option value="{k}">{v}</option>' for k, v in T.CATEGORY_LABELS.items())
    segment_checks = "".join(
        f"""<label class="flex items-center gap-2 text-sm"><input type="checkbox" name="segments" value="{k}"
        class="h-4 w-4 rounded border-slate-300"> {v['label']}</label>"""
        for k, v in T.SEGMENTS.items())
    product_checks = "".join(
        f"""<label class="flex items-center gap-2 text-sm"><input type="checkbox" name="products" value="{k}"
        class="h-4 w-4 rounded border-slate-300"> {v}</label>"""
        for k, v in {"verifierad": "Verifierad profil", "partner": "Partnerplacering",
                     "leads": "Kvalificerade leads", "guide_sponsor": "Guide-sponsring"}.items())

    inp = ("w-full px-4 py-3 rounded-xl border border-slate-300 focus:ring-2 "
           "focus:ring-sky-500 focus:border-transparent outline-none transition")

    body = f"""
<main class="flex-grow w-full">
<header class="max-w-5xl mx-auto px-6 pt-12 pb-6">
  {T.breadcrumbs([("Hem", "/"), ("För leverantörer", "/for-leverantorer")])}
  <h1 class="text-4xl md:text-6xl font-extrabold tracking-tight mb-5">Nå fastighetsägare som <span class="gradient-text">redan räknar på affären</span></h1>
  <p class="text-xl text-slate-600 max-w-2xl">Proptechguiden är den oberoende ingången när svenska fastighetsägare,
  förvaltare och BRF:er ska välja teknikleverantör. {total} bolag finns i katalogen. Här väljer ni hur ni syns.</p>
</header>

<section class="max-w-5xl mx-auto px-6 py-10 grid md:grid-cols-3 gap-6">
  <div class="bg-white rounded-2xl border border-slate-200 p-6">
    <p class="text-3xl font-extrabold gradient-text mb-1">01</p>
    <h2 class="font-bold text-lg mb-2">Synlighet i katalogen</h2>
    <p class="text-slate-600 text-sm">Fast månadskostnad för topplacering, logotyp, följbar länk och utökad profilsida.</p>
  </div>
  <div class="bg-white rounded-2xl border border-slate-200 p-6">
    <p class="text-3xl font-extrabold gradient-text mb-1">02</p>
    <h2 class="font-bold text-lg mb-2">Kvalificerade leads</h2>
    <p class="text-slate-600 text-sm">Betala per lead där yta, tidsram, budgetläge och beslutsroll redan är kartlagt.</p>
  </div>
  <div class="bg-white rounded-2xl border border-slate-200 p-6">
    <p class="text-3xl font-extrabold gradient-text mb-1">03</p>
    <h2 class="font-bold text-lg mb-2">Sponsrade guider</h2>
    <p class="text-slate-600 text-sm">Exklusivt avsändarskap på våra nedladdningsbara guider. {open_slots} platser lediga.</p>
  </div>
</section>

<section class="max-w-6xl mx-auto px-6 py-12">
  <h2 class="text-3xl font-extrabold tracking-tight mb-2">01. Placering i katalogen</h2>
  <p class="text-slate-600 mb-8 max-w-2xl">Alla bolag finns med gratis. Betalande nivåer sorteras överst,
  får följbar länk och en egen profilsida som rankar på bolagsnamnet.</p>
  <div class="grid md:grid-cols-3 gap-6">
    {tier_card("Grundpost", "0 kr", "Alltid gratis", [
        "Namn, kategori och beskrivning",
        "Länk till er webbplats (nofollow)",
        "Sorteras i bokstavsordning",
        "Vi lägger in er utan att ni ansöker",
    ])}
    {tier_card("Verifierad profil", "Från 1 900 kr/mån", "Bindningstid 6 mån", [
        "Verifierad-märkning i katalogen",
        "Sorteras före gratisposter",
        "Egen profilsida med USP:ar och kundcase",
        "Följbar (dofollow) länk",
        "Ni äger och uppdaterar er egen text",
    ], highlight=True)}
    {tier_card("Partnerplacering", "Från 5 900 kr/mån", "Bindningstid 12 mån", [
        "Topplacering under &quot;Utvalda partners&quot;",
        "Logotyp och framhävd kort-design",
        "Följbar länk från katalog och profilsida",
        "Placering på relevanta målgruppssidor",
        "Får matchade leads i er kategori",
        "Kvartalsrapport med trafik och leads",
    ])}
  </div>
</section>

<section class="max-w-6xl mx-auto px-6 py-12">
  <h2 class="text-3xl font-extrabold tracking-tight mb-2">02. Kvalificerade leads</h2>
  <p class="text-slate-600 mb-8 max-w-2xl">Varje förfrågan på sajten går genom samma kvalificering.
  Vi poängsätter leadet innan det skickas vidare, så ni betalar efter hur nära ett avslut det faktiskt är.</p>
  <div class="bg-white rounded-2xl border border-slate-200 overflow-x-auto">
    <table class="w-full text-sm min-w-[640px]">
      <thead class="bg-slate-50 text-left">
        <tr>
          <th class="px-6 py-4 font-bold">Betyg</th>
          <th class="px-6 py-4 font-bold">Vad det betyder</th>
          <th class="px-6 py-4 font-bold">Riktpris</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-slate-100">
        <tr>
          <td class="px-6 py-4"><span class="font-bold text-emerald-600">A</span></td>
          <td class="px-6 py-4 text-slate-600">Beslutsfattare, beslutad budget, igång inom 3 månader, portfölj över 10 000 kvm</td>
          <td class="px-6 py-4 font-semibold">2 500–4 000 kr</td>
        </tr>
        <tr>
          <td class="px-6 py-4"><span class="font-bold text-amber-600">B</span></td>
          <td class="px-6 py-4 text-slate-600">Tydligt behov och tidplan, budget under beredning</td>
          <td class="px-6 py-4 font-semibold">900–1 500 kr</td>
        </tr>
        <tr>
          <td class="px-6 py-4"><span class="font-bold text-slate-500">C</span></td>
          <td class="px-6 py-4 text-slate-600">Orienterande intresse, ingen tidplan eller budget</td>
          <td class="px-6 py-4 font-semibold">Ingår i partnerplacering</td>
        </tr>
      </tbody>
    </table>
  </div>
  <p class="text-sm text-slate-500 mt-4">Leads delas bara vidare när användaren aktivt samtyckt till att bli kontaktad.
  Vi säljer aldrig samma lead till fler än tre leverantörer.</p>
</section>

<section id="sponsring" class="max-w-6xl mx-auto px-6 py-12">
  <h2 class="text-3xl font-extrabold tracking-tight mb-2">03. Sponsra en guide</h2>
  <p class="text-slate-600 mb-8 max-w-2xl">Våra nedladdningsbara guider laddas ner av personer som står inför
  ett konkret beslut. Som exklusiv sponsor står ni som avsändare tillsammans med oss.</p>
  <div class="grid md:grid-cols-2 gap-6">
    <div class="bg-white rounded-2xl border border-slate-200 p-8">
      <h3 class="font-bold text-lg mb-4">Vad ingår</h3>
      <ul class="space-y-3 text-slate-600 text-sm">
        <li class="flex gap-3"><span class="text-emerald-600 font-bold">✓</span> &quot;I samarbete med [ert bolag]&quot; på guidesida och i PDF</li>
        <li class="flex gap-3"><span class="text-emerald-600 font-bold">✓</span> Er logotyp på omslag och i sidfot</li>
        <li class="flex gap-3"><span class="text-emerald-600 font-bold">✓</span> Ett uppslag där ni får presentera er lösning</li>
        <li class="flex gap-3"><span class="text-emerald-600 font-bold">✓</span> Samtliga nedladdningsleads som samtyckt till kontakt</li>
        <li class="flex gap-3"><span class="text-emerald-600 font-bold">✓</span> Exklusivitet i kategorin under avtalstiden</li>
      </ul>
    </div>
    <div class="bg-white rounded-2xl border border-slate-200 p-8">
      <h3 class="font-bold text-lg mb-4">Upplägg</h3>
      <p class="text-3xl font-extrabold tracking-tight mb-1">Från 19 000 kr</p>
      <p class="text-sm text-slate-500 mb-6">Per guide och 6-månadersperiod</p>
      <p class="text-slate-600 text-sm mb-4">Redaktionellt innehåll skrivs alltid av oss. Sponsorn påverkar
      inte rekommendationerna i guiden — det är förutsättningen för att den ska vara värd att ladda ner.</p>
      <p class="text-slate-600 text-sm">Just nu <b>{open_slots} lediga platser</b>. <a href="/guider" class="text-sky-600 font-bold hover:underline">Se guiderna</a></p>
    </div>
  </div>
</section>

<section id="ansok" class="max-w-3xl mx-auto px-6 py-16">
  <h2 class="text-3xl font-extrabold tracking-tight mb-3">Intresseanmälan</h2>
  <p class="text-slate-600 mb-8">Berätta vad ni är intresserade av så återkommer vi inom två arbetsdagar
  med upplägg, priser och lediga placeringar.</p>
  <div class="bg-white rounded-2xl border border-slate-200 shadow-sm p-8">
    <form id="partner-form" class="space-y-5" novalidate>
      <div class="grid md:grid-cols-2 gap-5">
        <div><label class="block text-sm font-semibold text-slate-700 mb-1.5" for="p-company">Bolag *</label>
          <input id="p-company" name="company" class="{inp}" required></div>
        <div><label class="block text-sm font-semibold text-slate-700 mb-1.5" for="p-website">Webbplats</label>
          <input id="p-website" name="website" class="{inp}" placeholder="https://"></div>
        <div><label class="block text-sm font-semibold text-slate-700 mb-1.5" for="p-name">Kontaktperson</label>
          <input id="p-name" name="name" class="{inp}"></div>
        <div><label class="block text-sm font-semibold text-slate-700 mb-1.5" for="p-email">E-post *</label>
          <input id="p-email" name="email" type="email" class="{inp}" required></div>
        <div><label class="block text-sm font-semibold text-slate-700 mb-1.5" for="p-phone">Telefon</label>
          <input id="p-phone" name="phone" type="tel" class="{inp}"></div>
        <div><label class="block text-sm font-semibold text-slate-700 mb-1.5" for="p-category">Kategori</label>
          <select id="p-category" name="category" class="{inp}"><option value="">Välj kategori</option>{categories}</select></div>
      </div>
      <fieldset>
        <legend class="block text-sm font-semibold text-slate-700 mb-2">Vilka målgrupper säljer ni till?</legend>
        <div class="flex flex-wrap gap-4">{segment_checks}</div>
      </fieldset>
      <fieldset>
        <legend class="block text-sm font-semibold text-slate-700 mb-2">Vad är ni intresserade av?</legend>
        <div class="flex flex-wrap gap-4">{product_checks}</div>
      </fieldset>
      <div><label class="block text-sm font-semibold text-slate-700 mb-1.5" for="p-message">Meddelande</label>
        <textarea id="p-message" name="message" rows="3" class="{inp}"></textarea></div>
      <p class="text-sm text-red-600 hidden" id="p-error"></p>
      <button type="submit" class="w-full bg-sky-600 text-white px-6 py-3.5 rounded-xl font-bold hover:bg-sky-700 transition shadow-lg shadow-sky-600/25">Skicka intresseanmälan</button>
    </form>
  </div>
</section>
</main>

<script>
(function () {{
  var form = document.getElementById('partner-form');
  var err = document.getElementById('p-error');
  var btn = form.querySelector('button[type=submit]');

  form.addEventListener('submit', function (e) {{
    e.preventDefault();
    var d = new FormData(form);
    if (!d.get('company') || !d.get('email')) {{
      err.textContent = 'Fyll i bolag och e-post.';
      err.classList.remove('hidden');
      return;
    }}
    err.classList.add('hidden');
    btn.disabled = true;
    btn.textContent = 'Skickar…';

    fetch('/api/partner-ansokan', {{
      method: 'POST',
      headers: {{ 'Content-Type': 'application/json' }},
      body: JSON.stringify({{
        company: d.get('company'),
        email: d.get('email'),
        name: d.get('name') || null,
        phone: d.get('phone') || null,
        website: d.get('website') || null,
        category: d.get('category') || null,
        segments: d.getAll('segments'),
        products: d.getAll('products'),
        message: d.get('message') || null,
        source: 'for-leverantorer'
      }})
    }}).then(function (r) {{
      if (!r.ok) throw new Error('http ' + r.status);
      if (typeof gtag === 'function') gtag('event', 'partner_application', {{ products: d.getAll('products').join(',') }});
      form.parentNode.innerHTML =
        '<div class="text-center py-8">' +
        '<h3 class="text-2xl font-extrabold mb-2">Tack! Vi hör av oss.</h3>' +
        '<p class="text-slate-600">Ni får en bekräftelse på mejlen och besked inom två arbetsdagar.</p></div>';
    }}).catch(function () {{
      btn.disabled = false;
      btn.textContent = 'Skicka intresseanmälan';
      err.textContent = 'Något gick fel. Mejla oss på simon@adviseo.se så löser vi det.';
      err.classList.remove('hidden');
    }});
  }});
}})();
</script>"""

    html = (T.head("Bli partner – synlighet och leads | Proptechguiden",
                   "Nå svenska fastighetsägare, förvaltare och BRF:er. Katalogplacering, "
                   "kvalificerade leads och sponsrade guider på Proptechguiden.",
                   "/for-leverantorer")
            + T.nav("for-leverantorer") + body + T.footer())
    write(STATIC / "for-leverantorer.html", html)


# --------------------------------------------------------------------------
# Sitemap
# --------------------------------------------------------------------------

def build_sitemap(companies, guides):
    today = date.today().isoformat()
    urls = ["/", "/directory", "/verktyg", "/guider", "/for-leverantorer",
            "/kategorier", "/om-sajten", "/privacy-policy", "/mer"]
    urls += [f"/{s}" for s in T.SEGMENTS]
    urls += [f"/{t}" for t in T.TOOLS]
    urls += [f"/{g['slug']}" for g in guides]
    urls += [f"/leverantor/{c['slug']}" for c in companies
             if c.get("tier") in ("partner", "verifierad")]

    seen, ordered = set(), []
    for u in urls:
        if u not in seen:
            seen.add(u)
            ordered.append(u)

    entries = "".join(
        f"  <url>\n    <loc>{T.BASE_URL}{u}</loc>\n    <lastmod>{today}</lastmod>\n  </url>\n"
        for u in ordered)
    write(STATIC / "sitemap.xml",
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          f"{entries}</urlset>\n")


def build_index(companies, guides):
    """Startsidan har ett jobb: sortera besökaren på målgrupp inom en skärmhöjd."""
    seg_cards = ""
    for slug, seg in T.SEGMENTS.items():
        count = len([c for c in companies if slug in c.get("segments", [])])
        seg_cards += f"""
<a href="/{slug}" class="group bg-white rounded-2xl border border-slate-200 p-8 hover:border-sky-300 hover:shadow-lg transition flex flex-col">
  <h3 class="text-2xl font-extrabold tracking-tight mb-2 group-hover:text-sky-600">{seg['label']}</h3>
  <p class="text-slate-600 flex-grow">{seg['tagline']}</p>
  <p class="text-sm text-slate-400 mt-4">{count} leverantörer · {len([g for g in guides if slug in g.get('segments', [])])} guider</p>
  <span class="mt-4 font-bold text-sky-600">Till er ingång →</span>
</a>"""

    tool_cards = "".join(
        f"""<a href="/{slug}" class="group bg-white rounded-2xl border border-slate-200 p-6 hover:border-sky-300 hover:shadow-md transition">
  <h3 class="font-bold text-lg mb-1 group-hover:text-sky-600">{t['title']}</h3>
  <p class="text-slate-500 text-sm">{t['desc']}</p>
</a>""" for slug, t in T.TOOLS.items())

    guide_cards = "".join(
        f"""<a href="/{g['slug']}" class="group bg-white rounded-2xl border border-slate-200 p-6 hover:border-sky-300 hover:shadow-md transition">
  <h3 class="font-bold text-lg mb-1 group-hover:text-sky-600">{g['title']}</h3>
  <p class="text-slate-500 text-sm">{g['summary']}</p>
</a>""" for g in guides[:6])

    body = f"""
<main class="flex-grow w-full">
<header class="max-w-5xl mx-auto px-6 pt-16 pb-8 text-center">
  <h1 class="text-5xl md:text-7xl font-extrabold tracking-tight mb-6">Digitaliseringen av <span class="gradient-text">svenska fastigheter.</span></h1>
  <p class="text-xl text-slate-600 max-w-2xl mx-auto">Oberoende guide till fastighetsteknik. Vi kartlägger {len(companies)} leverantörer,
  räknar på affären och matchar er mot rätt partner.</p>
</header>

<section class="max-w-6xl mx-auto px-6 py-10">
  <h2 class="text-center text-sm font-bold uppercase tracking-wide text-slate-400 mb-8">Välj din ingång</h2>
  <div class="grid md:grid-cols-3 gap-6">{seg_cards}</div>
</section>

<section class="max-w-6xl mx-auto px-6 py-10">
  <div class="bg-slate-900 text-white rounded-2xl p-8 md:p-12 grid md:grid-cols-3 gap-8 items-center">
    <div class="md:col-span-2">
      <h2 class="text-3xl font-extrabold tracking-tight mb-3">{len(companies)} leverantörer i katalogen</h2>
      <p class="text-slate-300">Filtrera på kategori och målgrupp, jämför lösningar och begär offert från flera bolag samtidigt.</p>
    </div>
    <a href="/directory" class="bg-white text-slate-900 px-6 py-4 rounded-xl font-bold hover:bg-slate-100 transition text-center">Öppna katalogen</a>
  </div>
</section>

<section class="max-w-6xl mx-auto px-6 py-10">
  <h2 class="text-3xl font-extrabold tracking-tight mb-6">Räkna på investeringen</h2>
  <div class="grid md:grid-cols-2 gap-6">{tool_cards}</div>
</section>

<section class="max-w-6xl mx-auto px-6 py-10">
  <div class="flex items-end justify-between mb-6 gap-4">
    <h2 class="text-3xl font-extrabold tracking-tight">Guider</h2>
    <a href="/guider" class="font-bold text-sky-600 hover:underline whitespace-nowrap">Alla guider →</a>
  </div>
  <div class="grid md:grid-cols-3 gap-6">{guide_cards}</div>
</section>

{cta_band("startsida")}
</main>"""

    html = (T.head("Proptechguiden | Fastighetsteknik för ägare, förvaltare och BRF:er",
                   f"Oberoende guide till proptech i Sverige. Jämför {len(companies)} leverantörer, "
                   "räkna på ROI och få offerter anpassade efter er fastighet.",
                   "/")
            + T.nav() + body + T.footer())
    write(STATIC / "index.html", html)


def main():
    companies = load("companies.json")
    guides = load("guides.json")
    print(f"Bygger sajten från {len(companies)} bolag och {len(guides)} guider:")
    build_index(companies, guides)
    build_directory(companies)
    build_company_pages(companies)
    build_segment_pages(companies, guides)
    build_tools_page()
    build_guides_page(guides)
    build_partner_page(companies, guides)
    build_sitemap(companies, guides)
    print("Klart.")


if __name__ == "__main__":
    main()
