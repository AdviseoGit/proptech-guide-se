"""
Proptech Guide lead magnet — "PropTech ROI-guide för fastighetsägare".

Deluxe, multi-section PDF (shared design language with the other portfolio
sites). fpdf2 core font = latin-1, which covers å/ä/ö; _s() keeps those and
only strips characters latin-1 cannot represent (em-dash, smart quotes, ...).

Schablonerna i guiden speglar medvetet ROI-kalkylatorn på sajten
(static/roi-kalkylator.html) så att PDF och kalkylator ger samma svar.
"""

from fpdf.enums import XPos, YPos

BRAND = (2, 132, 199)     # sky blue
BRAND_DK = (3, 105, 161)
INK = (15, 23, 42)
MUTED = (100, 116, 139)
LINE = (226, 232, 240)
WASH = (240, 249, 255)

UPDATED = "september 2026"
VERSION = "1.1"

INTRO = ("Digitalisering av fastigheter sänker driftskostnader och höjer värdet - men bara om ni "
         "väljer rätt och kan räkna hem investeringen. Den här guiden ger dig ROI-modellen, "
         "schablonerna att räkna med, två färdiga räkneexempel, urvalskriterierna och "
         "fallgroparna att undvika.")

VALUE_DRIVERS = [
    ("Sänkta driftkostnader", "Lägre energi- och vattenförbrukning, optimerat underhåll, "
                              "effektivare personal. Enklast att räkna på."),
    ("Ökade intäkter", "Lägre vakansgrad, högre hyra för smarta och hållbara ytor, "
                       "nya tjänster som datadriven parkering."),
    ("Minskad risk", "Vattenläckor, ventilationsfel och säkerhetsbrister upptäcks innan "
                     "de blir dyra skador."),
    ("Ökat fastighetsvärde", "En datadriven och hållbar byggnad har lägre riskprofil och "
                             "är mer attraktiv vid värdering och försäljning."),
]

ROI_STEPS = [
    "1. Summera årlig besparing: energi, arbetstid, färre akutfel - plus ev. ökad intäkt.",
    "2. Dela investeringen med årlig besparing = återbetalningstid (payback) i år.",
    "3. Räkna sedan nettot över 3-5 år: besparing x antal år minus investering.",
    "4. Lägg till löpande kostnader (licens, drift, support) innan ni beslutar.",
]

# Schabloner - samma procentsatser som ROI-kalkylatorn på proptechguiden.se.
SAVINGS_TABLE = [
    ("Energioptimering & AI", "ca 25 %", "Behovsstyrd värme och ventilation"),
    ("Smart värmestyrning", "ca 15 %", "Reglering mot utetemperatur och närvaro"),
    ("Smart belysning", "ca 10 %", "Närvaro- och dagsljusstyrning"),
    ("Enkel undermätning", "ca 5 %", "Synliggör förbrukning per byggnad/del"),
]

EXAMPLE_A = [
    ("Fastighet", "Kontor, 5 000 kvm"),
    ("Energikostnad idag", "1 200 000 kr/år"),
    ("Lösning", "Energioptimering & AI (25 %)"),
    ("Årlig besparing", "300 000 kr"),
    ("Investering", "750 000 kr"),
    ("Payback", "2,5 år"),
    ("Netto efter 5 år", "750 000 kr"),
]

EXAMPLE_B = [
    ("Fastighet", "BRF, 2 000 kvm"),
    ("Energikostnad idag", "400 000 kr/år"),
    ("Lösning", "Smart värmestyrning (15 %)"),
    ("Årlig besparing", "60 000 kr"),
    ("Investering", "120 000 kr"),
    ("Payback", "2,0 år"),
    ("Netto efter 5 år", "180 000 kr"),
]

SOFT_VALUES = [
    "Nöjdare hyresgäster och lägre omflyttning - syns i vakansgraden, inte i elräkningen.",
    "Färdigt underlag för ESG- och hållbarhetsrapportering i stället för manuell insamling.",
    "Mindre nyckelhantering och färre utryckningar - räkna i timmar, inte kronor, först.",
    "Data ni äger och kan ta med er till nästa system.",
]

CHOOSE = [
    "Börja med ert största problem (energi? felanmälan? access?) - inte med tekniken.",
    "Krav på öppna API:er och integration mot befintliga system.",
    "EU-/EES-datalagring och tydlig GDPR-hantering.",
    "Be om referenser från liknande fastigheter - och kör en pilot innan ni skalar.",
    "Begär prisbild för hela livscykeln: licens, drift, support och avveckling.",
]

PITFALLS = [
    "Köp teknik utan tydligt problem att lösa - börja med behovet.",
    "Glöm inte förvaltning/drift och utbildning av personalen.",
    "Lås inte in er i slutna system utan exportmöjlighet.",
    "Räkna inte hem besparingar ni inte kan mäta - sätt en baslinje före start.",
    "Underskatta inte tiden till full effekt; ett inkörningsår är normalt.",
]

TOOLS = [
    ("OurLiving", "Boendekommunikation och förvaltning"),
    ("Vyer", "AI-driven energioptimering och inomhusklimat"),
    ("Mestro", "Automatiserad energiuppföljning och mätdata"),
    ("HomeQ", "Digital marknadsplats för uthyrning"),
    ("Parakey", "Mobilbaserade access-system"),
    ("Defigo", "Digital porttelefon och passage"),
]

ASSUMPTIONS = ("Procentsatserna ovan är branschschabloner och samma som i ROI-kalkylatorn på "
               "proptechguiden.se. Stäm av er faktiska energikostnad mot SCB:s statistik över "
               "energipriser och mot era egna fakturor innan ni beslutar. Utfallet varierar med "
               "byggnadens skick, styrsystem och hur väl lösningen driftsätts.")

CLOSING = ("Räkna på era egna siffror i ROI-kalkylatorn: proptechguiden.se/roi-kalkylator.html - "
           "och jämför konkreta system i vår katalog över svenska PropTech-bolag på "
           "proptechguiden.se/directory.html")


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

    def _line(self, w, h, txt, **kw):
        """multi_cell som alltid lämnar markören vid vänstermarginalen på nästa rad.

        fpdf2 lämnar som standard x till höger om cellen (XPos.RIGHT), vilket får
        efterföljande celler att ritas ut i högermarginalen.
        """
        self.pdf.multi_cell(w, h, _s(txt), new_x=XPos.LMARGIN, new_y=YPos.NEXT, **kw)

    def _room(self, needed):
        """Sidbryt i förväg om blocket inte får plats ovanför sidfoten."""
        if self.pdf.get_y() + needed > 297 - 20:
            self.pdf.add_page()

    def cover(self, brandname, title, subtitle, intro, updated=None):
        pdf = self.pdf
        pdf.add_page()
        pdf.set_fill_color(*self.brand)
        pdf.rect(0, 0, 210, 60, "F")
        pdf.set_fill_color(*self.brand_dk)
        pdf.rect(0, 56, 210, 4, "F")
        pdf.set_xy(14, 13)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 23)
        pdf.cell(0, 12, _s(brandname), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_x(14)
        pdf.set_font("Helvetica", "", 14)
        pdf.cell(0, 8, _s(title), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_x(14)
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 6, _s(subtitle), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        if updated:
            pdf.set_x(14)
            pdf.set_font("Helvetica", "", 8.5)
            pdf.cell(0, 5, _s(updated), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_y(70)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*MUTED)
        self._line(self.WIDTH, 5, intro)
        pdf.set_text_color(*INK)
        pdf.ln(2)

    def section(self, title, keep=0):
        """keep = ungefärlig höjd på blocket som följer, så att rubriken inte
        hamnar ensam sist på en sida."""
        pdf = self.pdf
        self._room(22 + keep)
        pdf.ln(2)
        y = pdf.get_y()
        pdf.set_fill_color(*self.brand)
        pdf.rect(self.MARGIN, y, self.WIDTH, 9, "F")
        pdf.set_xy(self.MARGIN + 3, y + 1)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(self.WIDTH - 6, 7, _s(title), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_text_color(*INK)
        pdf.set_y(y + 11)

    def checks(self, items):
        pdf = self.pdf
        for it in items:
            self._room(10)
            y = pdf.get_y()
            pdf.set_draw_color(*self.brand)
            pdf.rect(self.MARGIN + 1, y + 1.2, 4, 4)
            pdf.set_xy(self.MARGIN + 8, y)
            pdf.set_font("Helvetica", "", 10.5)
            self._line(self.WIDTH - 8, 5.5, it)
            pdf.ln(1)

    def deflist(self, rows, label_w=38):
        """Tvåkolumnslista. Höjden sätts av den högsta kolumnen så raderna
        aldrig glider isär eller tappas."""
        pdf = self.pdf
        desc_w = self.WIDTH - label_w
        for i, (name, desc) in enumerate(rows):
            pdf.set_font("Helvetica", "", 10.5)
            lines = len(pdf.multi_cell(desc_w - 4, 5.5, _s(desc), dry_run=True,
                                       output="LINES"))
            h = max(7.5, lines * 5.5 + 2)
            self._room(h + 2)
            y = pdf.get_y()
            fill = WASH if i % 2 == 0 else (255, 255, 255)
            pdf.set_fill_color(*fill)
            pdf.rect(self.MARGIN, y, self.WIDTH, h, "F")
            pdf.set_xy(self.MARGIN + 2, y + 1)
            pdf.set_font("Helvetica", "B", 10.5)
            pdf.set_text_color(*self.brand_dk)
            pdf.cell(label_w - 2, 5.5, _s(name), new_x=XPos.LMARGIN, new_y=YPos.TOP)
            pdf.set_xy(self.MARGIN + label_w, y + 1)
            pdf.set_font("Helvetica", "", 10.5)
            pdf.set_text_color(*INK)
            self._line(desc_w - 4, 5.5, desc)
            pdf.set_y(y + h)
        pdf.ln(2)

    def table(self, headers, rows, widths):
        pdf = self.pdf
        self._room(9 + len(rows) * 7 + 4)
        y = pdf.get_y()
        pdf.set_fill_color(*self.brand_dk)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 9.5)
        x = self.MARGIN
        for w, htxt in zip(widths, headers):
            pdf.set_xy(x, y)
            pdf.cell(w, 8, "  " + _s(htxt), fill=True, new_x=XPos.RIGHT, new_y=YPos.TOP)
            x += w
        pdf.set_y(y + 8)
        pdf.set_text_color(*INK)
        for i, row in enumerate(rows):
            ry = pdf.get_y()
            pdf.set_fill_color(*(WASH if i % 2 == 0 else (255, 255, 255)))
            pdf.rect(self.MARGIN, ry, sum(widths), 7, "F")
            x = self.MARGIN
            for j, (w, cell) in enumerate(zip(widths, row)):
                pdf.set_xy(x, ry)
                pdf.set_font("Helvetica", "B" if j == 0 else "", 9.5)
                pdf.cell(w, 7, "  " + _s(cell), new_x=XPos.RIGHT, new_y=YPos.TOP)
                x += w
            pdf.set_y(ry + 7)
        pdf.set_draw_color(*LINE)
        pdf.line(self.MARGIN, pdf.get_y(), self.MARGIN + sum(widths), pdf.get_y())
        pdf.ln(3)

    def note(self, text, size=8.5):
        pdf = self.pdf
        self._room(14)
        pdf.set_font("Helvetica", "I", size)
        pdf.set_text_color(*MUTED)
        self._line(self.WIDTH, 4.5, text)
        pdf.set_text_color(*INK)
        pdf.ln(2)

    def callout(self, text):
        pdf = self.pdf
        pdf.set_font("Helvetica", "", 10)
        lines = len(pdf.multi_cell(self.WIDTH - 8, 5, _s(text), dry_run=True,
                                   output="LINES"))
        h = lines * 5 + 8
        self._room(h + 4)
        pdf.ln(2)
        y = pdf.get_y()
        pdf.set_fill_color(*WASH)
        pdf.set_draw_color(*self.brand)
        pdf.rect(self.MARGIN, y, self.WIDTH, h, "DF")
        pdf.set_xy(self.MARGIN + 4, y + 3)
        pdf.set_text_color(*INK)
        self._line(self.WIDTH - 8, 5, text)
        pdf.set_y(y + h + 2)


def _install(r):
    """Renderar hela guiden i en färdig DeluxeReport."""
    pdf = r.pdf

    def footer_fn():
        pdf.set_y(-15)
        pdf.set_draw_color(*LINE)
        pdf.line(r.MARGIN, pdf.get_y(), 210 - r.MARGIN, pdf.get_y())
        pdf.set_y(-13)
        pdf.set_font("Helvetica", "I", 7.5)
        pdf.set_text_color(*MUTED)
        pdf.cell(0, 4, _s(f"Proptech Guide Sverige | proptechguiden.se | {UPDATED} | "
                          f"Oberoende vägledning, inte investeringsrådgivning. | "
                          f"Sida {pdf.page_no()}"), align="C")
        pdf.set_text_color(*INK)

    pdf.footer = footer_fn
    r.cover("Proptech Guide Sverige", "PropTech ROI-guide",
            "För fastighetsägare som vill räkna hem digitaliseringen", INTRO,
            updated=f"Uppdaterad {UPDATED} - version {VERSION}")

    r.section("Fyra värdedrivare att räkna på", keep=len(VALUE_DRIVERS) * 13)
    r.deflist(VALUE_DRIVERS, label_w=46)

    r.section("Så räknar du ROI", keep=len(ROI_STEPS) * 7 + 10)
    r.checks(ROI_STEPS)
    r.note("Payback = investering / årlig besparing. De flesta system i den här guiden "
           "landar på 1-3 år.")

    r.section("Schabloner: besparing på energikostnaden", keep=len(SAVINGS_TABLE) * 7 + 12)
    r.table(["Lösning", "Besparing", "Så fungerar den"],
            [list(row) for row in SAVINGS_TABLE],
            [58, 28, 96])
    r.note(ASSUMPTIONS)

    r.section("Räkneexempel 1: kontorsfastighet", keep=len(EXAMPLE_A) * 8)
    r.deflist(EXAMPLE_A, label_w=52)

    r.section("Räkneexempel 2: bostadsrättsförening", keep=len(EXAMPLE_B) * 8)
    r.deflist(EXAMPLE_B, label_w=52)

    r.section("Värden kalkylen inte fångar", keep=len(SOFT_VALUES) * 7)
    r.checks(SOFT_VALUES)

    r.section("Så väljer du rätt lösning", keep=len(CHOOSE) * 7)
    r.checks(CHOOSE)

    r.section("Vanliga fallgropar", keep=len(PITFALLS) * 7)
    r.checks(PITFALLS)

    r.section("Några svenska lösningar i katalogen", keep=len(TOOLS) * 8)
    r.deflist(TOOLS, label_w=38)

    r.callout(CLOSING)


def build_guide_pdf() -> bytes:
    r = DeluxeReport(BRAND, BRAND_DK)
    _install(r)
    return bytes(r.pdf.output())


def _selfcheck():
    """Röktest: bygger guiden okomprimerad och verifierar att varje rad faktiskt
    hamnar i sidinnehållet.

    Bakgrund: fpdf2 lämnar som standard markören till höger om en multi_cell.
    Tidigare version av deflist() ritade därför rad 2 och framåt i högermarginalen,
    vilket tyst tappade fyra av sex leverantörer ur den levererade PDF:en.
    """
    r = DeluxeReport(BRAND, BRAND_DK)
    r.pdf.set_compression(False)
    _install(r)
    blob = bytes(r.pdf.output())
    # PDF-literaler escapar ( ) \ - normalisera bort det före jämförelsen.
    text = (blob.decode("latin-1")
            .replace("\\(", "(").replace("\\)", ")").replace("\\\\", "\\"))
    expected = ([n for n, _ in TOOLS] + [n for n, _ in VALUE_DRIVERS]
                + [n for n, _, _ in SAVINGS_TABLE]
                + [v for _, v in EXAMPLE_A] + [v for _, v in EXAMPLE_B])
    missing = [e for e in expected if _s(e) not in text]
    if missing:
        raise AssertionError(f"Saknas i PDF-innehållet: {missing}")
    print(f"OK - {r.pdf.page_no()} sidor, {len(expected)} rader verifierade.")


def user_email_html() -> str:
    return """\
<div style="font-family:Segoe UI,Arial,sans-serif;max-width:560px;margin:auto;color:#0f172a">
  <div style="background:#0284c7;color:#fff;padding:22px 24px;border-radius:12px 12px 0 0">
    <h2 style="margin:0;font-size:20px">Din PropTech ROI-guide 🏢</h2>
  </div>
  <div style="border:1px solid #e2e8f0;border-top:0;border-radius:0 0 12px 12px;padding:24px">
    <p>Hej, och tack!</p>
    <p>Här kommer din <b>PropTech ROI-guide</b> som <b>PDF i bilagan</b> — med ROI-modellen,
       schablonerna att räkna med, två färdiga räkneexempel och de vanligaste fallgroparna.</p>
    <p>Vill du räkna på era egna siffror direkt? Använd vår
       <a href="https://proptechguiden.se/roi-kalkylator.html" style="color:#0284c7">ROI-kalkylator</a>
       — den bygger på samma schabloner som guiden.</p>
    <p>Vill du jämföra konkreta system hittar du vår katalog på
       <a href="https://proptechguiden.se/directory.html" style="color:#0284c7">proptechguiden.se</a>.</p>
    <p style="margin-top:22px">Vänliga hälsningar,<br><b>Proptech Guide Sverige</b></p>
    <p style="font-size:11px;color:#94a3b8;margin-top:22px">Du får detta för att du laddade ner
       guiden på proptechguiden.se. Vill du av listan, svara på detta mejl.</p>
  </div>
</div>"""


if __name__ == "__main__":
    _selfcheck()
