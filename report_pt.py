"""
Proptech Guide lead magnet — "PropTech ROI-guide för fastighetsägare".

Deluxe, multi-section PDF (shared design language with the other portfolio
sites). fpdf2 core font = latin-1, which covers å/ä/ö; _s() keeps those and
only strips characters latin-1 cannot represent (em-dash, smart quotes, ...).
"""

BRAND = (2, 132, 199)     # sky blue
BRAND_DK = (3, 105, 161)
INK = (15, 23, 42)
MUTED = (100, 116, 139)
LINE = (226, 232, 240)
WASH = (240, 249, 255)

INTRO = ("Digitalisering av fastigheter sänker driftskostnader och höjer värdet - men bara om ni "
         "väljer rätt och kan räkna hem investeringen. Den här guiden ger dig ROI-modellen, "
         "urvalskriterierna och fallgroparna att undvika.")

SECTIONS = [
    ("Varför PropTech lönar sig", [
        "Sänkta driftskostnader via energioptimering och automation.",
        "Högre fastighetsvärde - digitaliserade fastigheter är mer attraktiva.",
        "Bättre hyresgästservice och färdig ESG-/hållbarhetsrapportering.",
    ]),
    ("Så räknar du ROI (enkelt)", [
        "1. Summera årlig besparing (energi, tid, färre fel) + ev. ökad intäkt.",
        "2. Dela investeringen med årlig besparing = återbetalningstid i år.",
        "3. Räkna på 3-5 år - de flesta system betalar sig på 1-3 år.",
        "Exempel: 120 000 kr i system som sparar 60 000 kr/år = 2 års payback.",
    ]),
    ("Så väljer du rätt lösning", [
        "Börja med ert största problem (energi? felanmälan? access?).",
        "Krav på öppna API:er och integration mot befintliga system.",
        "EU-/EES-datalagring och tydlig GDPR-hantering.",
        "Be om referenser från liknande fastigheter och en pilot.",
    ]),
    ("Vanliga fallgropar", [
        "Köp teknik utan tydligt problem att lösa - börja med behovet.",
        "Glöm inte förvaltning/drift och utbildning av personalen.",
        "Lås inte in er i slutna system utan exportmöjlighet.",
    ]),
]
TOOLS = [
    ("OurLiving", "Boendekommunikation och förvaltning"),
    ("Vyer", "AI-driven energioptimering och inomhusklimat"),
    ("HomeQ", "Digital marknadsplats för uthyrning"),
    ("Parakey", "Mobilbaserade access-system"),
    ("Defigo", "Digital porttelefon och passage"),
]
CLOSING = ("Vill du jämföra konkreta system? Vår katalog över svenska PropTech-bolag växer "
           "löpande på proptechguiden.se.")


def _s(t):
    t = str(t)
    for a, b in [("—", "-"), ("–", "-"), ("’", "'"), ("‘", "'"),
                 ("“", '"'), ("”", '"'), ("…", "..."), (" ", " ")]:
        t = t.replace(a, b)
    return t.encode("latin-1", "replace").decode("latin-1")


class DeluxeReport:
    MARGIN = 14
    WIDTH = 210 - 2 * 14

    def __init__(self, brand, brand_dk):
        from fpdf import FPDF
        self.brand, self.brand_dk = brand, brand_dk
        self.pdf = FPDF(format="A4")
        self.pdf.set_auto_page_break(auto=True, margin=20)
        self.pdf.set_margins(self.MARGIN, self.MARGIN, self.MARGIN)

    def cover(self, brandname, title, subtitle, intro):
        pdf = self.pdf
        pdf.add_page()
        pdf.set_fill_color(*self.brand)
        pdf.rect(0, 0, 210, 60, "F")
        pdf.set_fill_color(*self.brand_dk)
        pdf.rect(0, 56, 210, 4, "F")
        pdf.set_xy(14, 13)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 23)
        pdf.cell(0, 12, _s(brandname), ln=1)
        pdf.set_x(14)
        pdf.set_font("Helvetica", "", 14)
        pdf.cell(0, 8, _s(title), ln=1)
        pdf.set_x(14)
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 6, _s(subtitle), ln=1)
        pdf.set_y(70)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*MUTED)
        pdf.multi_cell(self.WIDTH, 5, _s(intro))
        pdf.set_text_color(*INK)
        pdf.ln(2)

    def section(self, title):
        pdf = self.pdf
        if pdf.get_y() > 250:
            pdf.add_page()
        pdf.ln(2)
        y = pdf.get_y()
        pdf.set_fill_color(*self.brand)
        pdf.rect(self.MARGIN, y, self.WIDTH, 9, "F")
        pdf.set_xy(self.MARGIN + 3, y + 1)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(self.WIDTH - 6, 7, _s(title), ln=1)
        pdf.set_text_color(*INK)
        pdf.ln(2)

    def checks(self, items):
        pdf = self.pdf
        for it in items:
            if pdf.get_y() > 262:
                pdf.add_page()
            y = pdf.get_y()
            pdf.set_draw_color(*self.brand)
            pdf.rect(self.MARGIN + 1, y + 1.2, 4, 4)
            pdf.set_xy(self.MARGIN + 8, y)
            pdf.set_font("Helvetica", "", 10.5)
            pdf.multi_cell(self.WIDTH - 8, 5.5, _s(it))
            pdf.ln(1)

    def deflist(self, rows):
        pdf = self.pdf
        for i, (name, desc) in enumerate(rows):
            if pdf.get_y() > 264:
                pdf.add_page()
            pdf.set_fill_color(*(WASH if i % 2 == 0 else (255, 255, 255)))
            y = pdf.get_y()
            pdf.set_font("Helvetica", "B", 10.5)
            pdf.set_text_color(*self.brand_dk)
            pdf.cell(38, 7, "  " + _s(name), border=0, fill=True)
            pdf.set_font("Helvetica", "", 10.5)
            pdf.set_text_color(*INK)
            pdf.multi_cell(self.WIDTH - 38, 7, _s(desc), border=0, fill=True)
        pdf.ln(1)

    def callout(self, text):
        pdf = self.pdf
        import math
        if pdf.get_y() > 250:
            pdf.add_page()
        pdf.ln(2)
        y = pdf.get_y()
        approx = max(1, math.ceil(pdf.get_string_width(_s(text)) / (self.WIDTH - 10)))
        h = approx * 5 + 8
        pdf.set_fill_color(*WASH)
        pdf.set_draw_color(*self.brand)
        pdf.rect(self.MARGIN, y, self.WIDTH, h, "DF")
        pdf.set_xy(self.MARGIN + 4, y + 3)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*INK)
        pdf.multi_cell(self.WIDTH - 8, 5, _s(text))
        pdf.set_y(y + h + 2)


def build_guide_pdf() -> bytes:
    r = DeluxeReport(BRAND, BRAND_DK)
    pdf = r.pdf

    def footer_fn():
        pdf.set_y(-15)
        pdf.set_draw_color(*LINE)
        pdf.line(r.MARGIN, pdf.get_y(), 210 - r.MARGIN, pdf.get_y())
        pdf.set_y(-13)
        pdf.set_font("Helvetica", "I", 7.5)
        pdf.set_text_color(*MUTED)
        pdf.cell(0, 4, _s("Proptech Guide Sverige | proptechguiden.se | Oberoende vägledning, "
                          "inte investeringsrådgivning."), align="C")

    pdf.footer = footer_fn
    r.cover("Proptech Guide Sverige", "PropTech ROI-guide",
            "För fastighetsägare som vill räkna hem digitaliseringen", INTRO)
    for title, items in SECTIONS:
        r.section(title)
        r.checks(items)
    r.section("Några ledande svenska lösningar")
    r.deflist(TOOLS)
    r.callout(CLOSING)
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
