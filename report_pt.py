"""
Proptech Guide lead magnet — "PropTech ROI-guide for fastighetsagare".
Matches the site's ROI/guide content. Static PDF + email body.
fpdf2 core font = latin-1 (a/a/o ok; avoid em-dash/smart quotes -> _s()).
"""

SKY = (2, 132, 199)
INK = (15, 23, 42)
MUTED = (100, 116, 139)

SECTIONS = [
    ("Varfor PropTech lonar sig", [
        "Sankta driftskostnader via energioptimering och automation.",
        "Hogre fastighetsvarde - digitaliserade fastigheter ar mer attraktiva.",
        "Battre hyresgastservice och fardig ESG-/hallbarhetsrapportering.",
    ]),
    ("Sa raknar du ROI (enkelt)", [
        "1. Summera arlig besparing (energi, tid, fardre fel) + ev. okad intakt.",
        "2. Dela investeringen med arlig besparing = aterbetalningstid i ar.",
        "3. Rakna pa 3-5 ar - de flesta system betalar sig pa 1-3 ar.",
        "Exempel: 120 000 kr i system som sparar 60 000 kr/ar = 2 ars payback.",
    ]),
    ("Sa valjer du ratt losning", [
        "Borja med ert storsta problem (energi? felanmalan? access?).",
        "Krav pa oppna API:er och integration mot befintliga system.",
        "EU-/EES-datalagring och tydlig GDPR-hantering.",
        "Be om referenser fran liknande fastigheter och en pilot.",
    ]),
    ("Vanliga fallgropar", [
        "Kop teknik utan tydligt problem att losa - borja med behovet.",
        "Glom inte forvaltning/drift och utbildning av personalen.",
        "Las inte in er i slutna system utan exportmojlighet.",
    ]),
]
TOOLS = [
    ("OurLiving", "Boendekommunikation och forvaltning"),
    ("Vyer", "AI-driven energioptimering och inomhusklimat"),
    ("HomeQ", "Digital marknadsplats for uthyrning"),
    ("Parakey", "Mobilbaserade access-system"),
    ("Defigo", "Digital porttelefon och passage"),
]


def _s(t):
    t = str(t)
    for a, b in [("—", "-"), ("–", "-"), ("’", "'"), ("‘", "'"),
                 ("“", '"'), ("”", '"'), ("…", "..."), (" ", " ")]:
        t = t.replace(a, b)
    return t.encode("latin-1", "replace").decode("latin-1")


def build_guide_pdf() -> bytes:
    from fpdf import FPDF
    pdf = FPDF(format="A4")
    pdf.set_auto_page_break(auto=True, margin=16)
    pdf.add_page()

    pdf.set_fill_color(*SKY)
    pdf.rect(0, 0, 210, 30, "F")
    pdf.set_xy(14, 9)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 10, "Proptech Guide Sverige", ln=1)
    pdf.set_xy(14, 19)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, _s("PropTech ROI-guide for fastighetsagare"), ln=1)

    pdf.set_xy(14, 38)
    pdf.set_text_color(*MUTED)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(182, 5, _s(
        "Digitalisering av fastigheter sanker driftskostnader och hojer vardet - "
        "men bara om ni valjer ratt och kan rakna hem investeringen. Den har guiden "
        "ger dig ROI-modellen, urvalskriterierna och fallgroparna att undvika."))
    pdf.ln(2)

    for title, items in SECTIONS:
        pdf.set_text_color(*SKY)
        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 9, _s(title), ln=1)
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(*INK)
        for it in items:
            y = pdf.get_y()
            pdf.set_draw_color(*MUTED)
            pdf.rect(15, y + 1.2, 3.5, 3.5)
            pdf.set_x(22)
            pdf.multi_cell(173, 6, _s(it))
        pdf.ln(2)

    pdf.set_text_color(*SKY)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 9, _s("Nagra ledande svenska losningar"), ln=1)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(*INK)
    for name, desc in TOOLS:
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(40, 6, _s(name))
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(*MUTED)
        pdf.multi_cell(142, 6, _s(desc))
        pdf.set_text_color(*INK)

    pdf.set_y(-18)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(182, 4, _s("Proptech Guide Sverige | proptechguiden.se | "
                              "Oberoende vagledning, inte investeringsradgivning."))
    return bytes(pdf.output())


def user_email_html() -> str:
    return """\
<div style="font-family:Segoe UI,Arial,sans-serif;max-width:560px;margin:auto;color:#0f172a">
  <div style="background:#0284c7;color:#fff;padding:22px 24px;border-radius:12px 12px 0 0">
    <h2 style="margin:0;font-size:20px">Din PropTech ROI-guide 🏢</h2>
  </div>
  <div style="border:1px solid #e2e8f0;border-top:0;border-radius:0 0 12px 12px;padding:24px">
    <p>Hej, och tack!</p>
    <p>Här kommer din <b>PropTech ROI-guide</b> som <b>PDF i bilagan</b> — den hjälper dig
       räkna hem investeringen, välja rätt lösning och undvika de vanligaste fallgroparna.</p>
    <p>Vill du jämföra konkreta system hittar du vår katalog på
       <a href="https://proptechguiden.se/directory.html" style="color:#0284c7">proptechguiden.se</a>.</p>
    <p style="margin-top:22px">Vänliga hälsningar,<br><b>Proptech Guide Sverige</b></p>
    <p style="font-size:11px;color:#94a3b8;margin-top:22px">Du får detta för att du laddade ner
       guiden på proptechguiden.se. Vill du av listan, svara på detta mejl.</p>
  </div>
</div>"""
