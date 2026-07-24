"""Lead engine för proptechguiden.se.

Ett enda kvalificeringsschema för hela sajten. Alla kalkylatorer, guider och
segmentsidor postar samma payload till /api/lead, så varje lead går att poängsätta,
värdera och dirigera till rätt partner oavsett var på sajten det fångades.

Tre intäktsströmmar hänger på det här:
  1. Katalogplaceringar  -> tier-fältet i data/companies.json
  2. Kvalificerade leads -> score + estimerat affärsvärde nedan
  3. Sponsrade guider    -> source-fältet bär sponsorn genom hela kedjan
"""
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

DATABASE_URL = os.environ.get("DATABASE_URL")
DATA_DIR = Path(__file__).parent / "data"


# --------------------------------------------------------------------------
# Schema
# --------------------------------------------------------------------------

SEGMENTS = {
    "fastighetsagare": "Fastighetsägare",
    "forvaltare": "Kommersiell förvaltare",
    "brf": "BRF-styrelse",
}

TIMEFRAMES = {
    "omgaende": "Omgående",
    "inom_3_man": "Inom 3 månader",
    "3_6_man": "3–6 månader",
    "6_12_man": "6–12 månader",
    "orienterar": "Orienterar mig bara",
}

BUDGET_STATES = {
    "beslutad": "Budget beslutad",
    "under_beredning": "Budget under beredning",
    "ingen": "Ingen budget ännu",
}


class Lead(BaseModel):
    """Enhetligt leadschema. Bara e-post är obligatoriskt — resten höjer poängen."""

    email: EmailStr
    name: Optional[str] = None
    company: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = None

    segment: Optional[str] = None          # fastighetsagare | forvaltare | brf
    need: Optional[str] = None             # kategori-slug ur katalogen
    sqm: Optional[int] = None              # förvaltad yta
    units: Optional[int] = None            # antal lägenheter/lokaler
    timeframe: Optional[str] = None
    budget_state: Optional[str] = None
    message: Optional[str] = None

    consent: bool = False                  # GDPR: får vi dela med leverantörer
    source: str = "okand"                  # vilken sida/verktyg leadet kom från
    calc_data: dict = Field(default_factory=dict)   # kalkylatorns indata/utfall


# --------------------------------------------------------------------------
# Scoring
# --------------------------------------------------------------------------

ROLE_POINTS = [
    (("vd", "ceo", "ägare", "agare", "fastighetschef", "teknisk chef", "ordförande",
      "ordforande", "styrelseordförande", "direktör", "direktor"), 25),
    (("förvaltare", "forvaltare", "driftchef", "driftansvarig", "energiansvarig",
      "projektledare", "styrelse"), 18),
    (("konsult", "rådgivare", "radgivare", "leverantör", "leverantor"), 6),
]

TIMEFRAME_POINTS = {
    "omgaende": 25,
    "inom_3_man": 22,
    "3_6_man": 15,
    "6_12_man": 8,
    "orienterar": 3,
}

BUDGET_POINTS = {
    "beslutad": 20,
    "under_beredning": 12,
    "ingen": 4,
}


def _role_points(role):
    if not role:
        return 0
    r = role.lower()
    for keywords, points in ROLE_POINTS:
        if any(k in r for k in keywords):
            return points
    return 8


def _size_points(sqm, units):
    # Räkna om lägenheter till yta när ytan saknas (svenskt snitt ~70 kvm/lgh).
    area = sqm or (units * 70 if units else 0)
    if area >= 50000:
        return 30
    if area >= 10000:
        return 22
    if area >= 3000:
        return 14
    if area > 0:
        return 6
    return 0


def score_lead(lead: Lead) -> dict:
    """Poängsätt ett lead 0–100 och sätt betyg A/B/C.

    Betyget styr både hur snabbt vi larmar och vad leadet får kosta en partner.
    """
    breakdown = {
        "roll": _role_points(lead.role),
        "portfoljstorlek": _size_points(lead.sqm, lead.units),
        "tidsram": TIMEFRAME_POINTS.get(lead.timeframe or "", 0),
        "budget": BUDGET_POINTS.get(lead.budget_state or "", 0),
    }
    # Kontaktbarhet och delningssamtycke avgör om leadet går att sälja vidare.
    if lead.phone:
        breakdown["telefon"] = 5
    if lead.company:
        breakdown["foretag"] = 5
    if lead.consent:
        breakdown["samtycke"] = 10

    total = min(sum(breakdown.values()), 100)
    grade = "A" if total >= 70 else "B" if total >= 45 else "C"
    return {"score": total, "grade": grade, "breakdown": breakdown}


# Grov intäktspotential per kvm och år, per behovskategori. Används för att
# uppskatta affärsvärdet i leadnotisen — inte som utfästelse mot kund.
VALUE_PER_SQM = {
    "energi": 45,
    "analys": 30,
    "iot": 25,
    "forvaltning": 20,
    "plattform": 20,
    "access": 15,
    "boende": 12,
    "uthyrning": 12,
}


def estimate_deal_value(lead: Lead) -> Optional[int]:
    """Uppskattat förstaårsvärde för leverantören, i kronor."""
    area = lead.sqm or (lead.units * 70 if lead.units else 0)
    if not area:
        return None
    per_sqm = VALUE_PER_SQM.get(lead.need or "", 20)
    return int(area * per_sqm)


# --------------------------------------------------------------------------
# Partnermatchning
# --------------------------------------------------------------------------

def load_companies():
    path = DATA_DIR / "companies.json"
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def match_partners(lead: Lead, limit: int = 3):
    """Hitta betalande partners som matchar leadets behov och målgrupp.

    Bara partner-tier tar emot leads — det är själva produkten i intäktsström 2.
    """
    matches = []
    for c in load_companies():
        if c.get("tier") != "partner" or not c.get("receives_leads"):
            continue
        if lead.need and c.get("category") != lead.need:
            continue
        if lead.segment and lead.segment not in c.get("segments", []):
            continue
        matches.append(c)
    return matches[:limit]


# --------------------------------------------------------------------------
# Lagring
# --------------------------------------------------------------------------

DDL = """
CREATE TABLE IF NOT EXISTS proptech_leads_v2 (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    company VARCHAR(255),
    phone VARCHAR(64),
    role VARCHAR(128),
    segment VARCHAR(32),
    need VARCHAR(64),
    sqm INTEGER,
    units INTEGER,
    timeframe VARCHAR(32),
    budget_state VARCHAR(32),
    message TEXT,
    consent BOOLEAN DEFAULT FALSE,
    source VARCHAR(128),
    score INTEGER,
    grade VARCHAR(2),
    estimated_value INTEGER,
    calc_data JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_leads_v2_grade ON proptech_leads_v2 (grade, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_leads_v2_need ON proptech_leads_v2 (need, segment);
"""


def _save_jsonl(record):
    """Fallback så inget lead går förlorat när databasen saknas eller strular."""
    DATA_DIR.mkdir(exist_ok=True)
    with open(DATA_DIR / "leads.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")


def save_lead(lead: Lead, scoring: dict, value: Optional[int]) -> dict:
    record = lead.model_dump()
    record.update({
        "score": scoring["score"],
        "grade": scoring["grade"],
        "score_breakdown": scoring["breakdown"],
        "estimated_value": value,
        "created_at": datetime.now(timezone.utc).isoformat(),
    })
    _save_jsonl(record)

    if not DATABASE_URL:
        return record
    try:
        import psycopg2
        from psycopg2.extras import Json

        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(DDL)
        cur.execute(
            """
            INSERT INTO proptech_leads_v2
                (email, name, company, phone, role, segment, need, sqm, units,
                 timeframe, budget_state, message, consent, source, score, grade,
                 estimated_value, calc_data)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (lead.email, lead.name, lead.company, lead.phone, lead.role, lead.segment,
             lead.need, lead.sqm, lead.units, lead.timeframe, lead.budget_state,
             lead.message, lead.consent, lead.source, scoring["score"], scoring["grade"],
             value, Json(lead.calc_data)),
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as exc:  # noqa: BLE001
        print(f"[lead_engine] DB-fel, leadet finns kvar i leads.jsonl: {exc}")
    return record


# --------------------------------------------------------------------------
# Notifiering
# --------------------------------------------------------------------------

def _fmt_kr(value):
    return f"{value:,}".replace(",", " ") + " kr" if value else "–"


def owner_email_html(lead: Lead, scoring: dict, value, partners) -> str:
    color = {"A": "#059669", "B": "#d97706", "C": "#64748b"}[scoring["grade"]]
    rows = [
        ("Betyg", f"<b style='color:{color}'>{scoring['grade']} ({scoring['score']}/100)</b>"),
        ("Uppskattat affärsvärde år 1", _fmt_kr(value)),
        ("Namn", lead.name or "–"),
        ("E-post", lead.email),
        ("Telefon", lead.phone or "–"),
        ("Företag", lead.company or "–"),
        ("Roll", lead.role or "–"),
        ("Målgrupp", SEGMENTS.get(lead.segment or "", lead.segment or "–")),
        ("Behov", lead.need or "–"),
        ("Yta", f"{lead.sqm} kvm" if lead.sqm else "–"),
        ("Enheter", str(lead.units) if lead.units else "–"),
        ("Tidsram", TIMEFRAMES.get(lead.timeframe or "", "–")),
        ("Budget", BUDGET_STATES.get(lead.budget_state or "", "–")),
        ("Får delas med leverantör", "Ja" if lead.consent else "Nej"),
        ("Källa", lead.source),
    ]
    table = "".join(
        f"<tr><td style='padding:6px 12px;color:#64748b'>{k}</td>"
        f"<td style='padding:6px 12px'>{v}</td></tr>"
        for k, v in rows
    )
    partner_html = ""
    if partners:
        names = ", ".join(p["name"] for p in partners)
        partner_html = f"<p><b>Matchade partners:</b> {names}</p>"
    msg_html = f"<p><b>Meddelande:</b><br>{lead.message}</p>" if lead.message else ""
    calc_html = ""
    if lead.calc_data:
        calc_html = (
            "<p><b>Kalkylatordata:</b></p><pre style='background:#f1f5f9;padding:12px;"
            f"border-radius:8px'>{json.dumps(lead.calc_data, ensure_ascii=False, indent=2)}</pre>"
        )
    return (
        f"<div style='font-family:sans-serif'>"
        f"<h2>Nytt {scoring['grade']}-lead från Proptechguiden</h2>"
        f"<table style='border-collapse:collapse'>{table}</table>"
        f"{partner_html}{msg_html}{calc_html}</div>"
    )


def user_email_html(lead: Lead, partners) -> str:
    partner_block = ""
    if partners and lead.consent:
        items = "".join(
            f"<li><b>{p['name']}</b> — {p['description']} "
            f"<a href='https://proptechguiden.se/leverantor/{p['slug']}'>Läs mer</a></li>"
            for p in partners
        )
        partner_block = (
            "<p>Utifrån det du fyllt i har vi tagit fram leverantörer som matchar ditt behov. "
            "De hör av sig direkt till dig:</p>"
            f"<ul>{items}</ul>"
        )
    return (
        "<div style='font-family:sans-serif;max-width:600px'>"
        f"<h2>Tack {lead.name or ''}!</h2>"
        "<p>Vi har tagit emot din förfrågan via Proptechguiden.</p>"
        f"{partner_block}"
        "<p>Under tiden kan du jämföra alla leverantörer i vår katalog: "
        "<a href='https://proptechguiden.se/directory'>proptechguiden.se/directory</a></p>"
        "<p style='color:#64748b;font-size:13px'>Proptechguiden är oberoende. "
        "Vi rekommenderar aldrig en leverantör enbart för att de är partner.</p>"
        "</div>"
    )


# --------------------------------------------------------------------------
# Leverantörsansökningar (intäktsström 1 och 3)
# --------------------------------------------------------------------------

PRODUCTS = {
    "verifierad": "Verifierad profil",
    "partner": "Partnerplacering",
    "leads": "Kvalificerade leads",
    "guide_sponsor": "Guide-sponsring",
}


class PartnerApplication(BaseModel):
    company: str
    email: EmailStr
    name: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    category: Optional[str] = None
    segments: list[str] = Field(default_factory=list)
    products: list[str] = Field(default_factory=list)   # nycklar ur PRODUCTS
    message: Optional[str] = None
    source: str = "for-leverantorer"


def process_partner_application(app: PartnerApplication) -> dict:
    record = app.model_dump()
    record["created_at"] = datetime.now(timezone.utc).isoformat()
    DATA_DIR.mkdir(exist_ok=True)
    with open(DATA_DIR / "partner_applications.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")

    wanted = ", ".join(PRODUCTS.get(p, p) for p in app.products) or "–"
    rows = [
        ("Bolag", app.company),
        ("Kontakt", app.name or "–"),
        ("E-post", app.email),
        ("Telefon", app.phone or "–"),
        ("Webb", app.website or "–"),
        ("Kategori", app.category or "–"),
        ("Målgrupper", ", ".join(app.segments) or "–"),
        ("Vill ha", f"<b>{wanted}</b>"),
    ]
    table = "".join(
        f"<tr><td style='padding:6px 12px;color:#64748b'>{k}</td>"
        f"<td style='padding:6px 12px'>{v}</td></tr>" for k, v in rows
    )
    msg = f"<p><b>Meddelande:</b><br>{app.message}</p>" if app.message else ""
    try:
        import mailer
        mailer.notify_owner(
            f"Leverantörsansökan: {app.company} ({wanted})",
            f"<div style='font-family:sans-serif'><h2>Ny leverantörsansökan</h2>"
            f"<table style='border-collapse:collapse'>{table}</table>{msg}</div>",
            reply_to=app.email, from_name="Proptechguiden")
        mailer.send_email(
            app.email, "Tack för din ansökan – Proptechguiden",
            "<div style='font-family:sans-serif;max-width:600px'>"
            f"<h2>Tack {app.name or app.company}!</h2>"
            "<p>Vi har tagit emot er intresseanmälan och återkommer inom två arbetsdagar "
            "med upplägg, priser och lediga placeringar.</p>"
            f"<p><b>Ni har markerat intresse för:</b> {wanted}</p>"
            "</div>", from_name="Proptechguiden")
    except Exception as exc:  # noqa: BLE001
        print(f"[lead_engine] partnerutskick misslyckades: {exc}")
    return {"status": "received"}


def process_lead(lead: Lead) -> dict:
    """Hela kedjan: poängsätt, värdera, matcha, spara, notifiera."""
    scoring = score_lead(lead)
    value = estimate_deal_value(lead)
    partners = match_partners(lead)
    save_lead(lead, scoring, value)

    try:
        import mailer
        subject = f"[{scoring['grade']}] Nytt lead {lead.company or lead.email} – {lead.need or lead.source}"
        mailer.notify_owner(subject, owner_email_html(lead, scoring, value, partners),
                            reply_to=lead.email, from_name="Proptechguiden")
        mailer.send_email(lead.email, "Tack för din förfrågan – Proptechguiden",
                          user_email_html(lead, partners), from_name="Proptechguiden")
        # Partners får bara leadet om användaren aktivt samtyckt till att delas.
        if lead.consent:
            for p in partners:
                if p.get("contact_email"):
                    mailer.send_email(
                        p["contact_email"],
                        f"Nytt kvalificerat lead via Proptechguiden ({scoring['grade']})",
                        owner_email_html(lead, scoring, value, []),
                        reply_to=lead.email, from_name="Proptechguiden")
    except Exception as exc:  # noqa: BLE001
        print(f"[lead_engine] utskick misslyckades: {exc}")

    return {"score": scoring["score"], "grade": scoring["grade"],
            "partners": [{"name": p["name"], "slug": p["slug"]} for p in partners]}
