import os
from fastapi import FastAPI, Request, BackgroundTasks, Body, HTTPException
from pathlib import Path
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI(title="Proptech Guide Sverige")

import psycopg2
from pydantic import BaseModel, EmailStr, ValidationError

import lead_engine

DATABASE_URL = os.environ.get("DATABASE_URL")


class LeadIn(BaseModel):
    email: EmailStr


def _save_lead_pt(email):
    if not DATABASE_URL:
        print(f"[pt] no DB configured, lead: {email}")
        return
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS proptech_leads (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                source VARCHAR(64),
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        cur.execute(
            "INSERT INTO proptech_leads (email, source) VALUES (%s, %s) ON CONFLICT (email) DO NOTHING",
            (email, "roi_guide"),
        )
        conn.commit(); cur.close(); conn.close()
    except Exception as e:
        print(f"[pt] DB error: {e}")


def _deliver_pt(email, guide_slug="proptech-roi-guide"):
    import mailer
    import report_pt
    _save_lead_pt(email)
    
    import json
    try:
        with open("data/guides.json", "r") as gf:
            guides = json.load(gf)
            guide = next((g for g in guides if g.get("slug") == guide_slug), None)
            
        guide_title = guide.get("title", "Guide") if guide else "Guide"
        pdf_title = guide.get("pdf", f"{guide_title}.pdf") if guide else "PropTech-ROI-guide.pdf"
        
        pdf = None
        if guide_slug == "proptech-roi-guide":
            pdf = report_pt.build_guide_pdf()
        else:
            try:
                from reportlab.pdfgen import canvas
                import io
                buffer = io.BytesIO()
                p = canvas.Canvas(buffer)
                p.drawString(100, 750, f"{guide_title}")
                p.drawString(100, 730, "Detta är en automatiskt genererad platshållar-PDF.")
                p.showPage()
                p.save()
                pdf = buffer.getvalue()
            except ImportError:
                print("[pt] reportlab not installed, skipping PDF generation")
            
        atts = [(f"{pdf_title}.pdf" if not pdf_title.endswith(".pdf") else pdf_title, pdf, "application/pdf")] if pdf else None
        
        if guide_slug == "proptech-roi-guide":
            html = report_pt.user_email_html()
        else:
            html = f"<div style='font-family:sans-serif;max-width:600px'><h2>Tack för ditt intresse!</h2><p>Bifogat hittar du guiden <b>{guide_title}</b>.</p></div>"
            
        mailer.send_email(email, f"Din guide: {guide_title}", html,
                          attachments=atts, from_name="Proptechguiden")
        mailer.notify_owner(f"Ny lead (PDF) - {guide_title}", f"<p>Ny lead laddade ner {guide_title}: <b>{email}</b></p>",
                            reply_to=email, from_name="Proptechguiden")
                            
    except Exception as e:
        print(f"[pt] delivery failed: {e}")


@app.post("/api/lead-pdf")
async def capture_lead_pdf(lead: LeadIn, background: BackgroundTasks):
    """Enkel e-postfångst för PDF-utskick (äldre formulär)."""
    background.add_task(_deliver_pt, lead.email)
    return {"status": "success"}


@app.post("/api/lead")
async def capture_lead(background: BackgroundTasks, payload: dict = Body(...)):
    """Enhetlig ingång för alla kvalificerade leads på sajten.

    Bakåtkompatibel: en payload med enbart {"email": ...} behandlas som tidigare
    PDF-fångst, allt annat går genom kvalificering och scoring.

    Scoring körs synkront så svaret kan bekräfta matchningen för användaren,
    medan lagring och utskick läggs i bakgrunden och aldrig blockar requesten.
    """
    if set(payload.keys()) <= {"email"} and payload.get("email"):
        background.add_task(_deliver_pt, payload["email"])
        return {"status": "success"}

    try:
        lead = lead_engine.Lead(**payload)
    except ValidationError as exc:
        raise HTTPException(status_code=400, detail=exc.errors(include_url=False))
    scoring = lead_engine.score_lead(lead)
    partners = lead_engine.match_partners(lead)
    background.add_task(lead_engine.process_lead, lead)
    return {
        "status": "success",
        "grade": scoring["grade"],
        "partners": [{"name": p["name"], "slug": p["slug"]} for p in partners],
    }


@app.post("/api/partner-ansokan")
async def partner_application(background: BackgroundTasks, payload: dict = Body(...)):
    """Intresseanmälan från leverantörer som vill köpa placering, leads eller sponsring."""
    try:
        app_in = lead_engine.PartnerApplication(**payload)
    except ValidationError as exc:
        raise HTTPException(status_code=400, detail=exc.errors(include_url=False))
    background.add_task(lead_engine.process_partner_application, app_in)
    return {"status": "received"}

# Serve static assets (js, css, images) under /static
app.mount("/static", StaticFiles(directory="static"), name="static")

# Explicit routes
@app.get("/", response_class=HTMLResponse)
async def index():
    return FileResponse("static/index.html")

@app.get("/kategorier", response_class=HTMLResponse)
async def kategorier():
    return FileResponse("static/kategorier.html")

@app.get("/ai-i-fastigheter", response_class=HTMLResponse)
async def ai_i_fastigheter():
    return FileResponse("static/ai-i-fastigheter.html")

@app.get("/om-sajten", response_class=HTMLResponse)
async def om_sajten():
    return FileResponse("static/om-sajten.html")

@app.get("/robots.txt")
async def robots():
    return FileResponse("static/robots.txt")

@app.get("/sitemap.xml")
async def sitemap():
    return FileResponse("static/sitemap.xml", media_type="application/xml")

@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favicon.svg")

# Catch-all route to serve any .html file from the static directory from the root URL
@app.get("/{filename:path}", response_class=HTMLResponse)
async def serve_html(filename: str):
    print(f"Attempting to serve: {filename}")
    # Append .html to the filename and check if it exists in the static directory
    file_path = os.path.join("static", f"{filename}.html")
    print(f"Checking for file at: {file_path}")
    if os.path.exists(file_path):
        return FileResponse(file_path)

    # Filer som redan har ändelse, t.ex. /cookie-banner.min.js och /lead-engine.js.
    # Sidorna länkar dem från roten, så de måste kunna serveras utan /static-prefix.
    direct = os.path.normpath(os.path.join("static", filename))
    if direct.startswith("static" + os.sep) and os.path.isfile(direct):
        return FileResponse(direct)

    # Let FastAPI handle 404 if it's not an existing HTML file
    raise HTTPException(status_code=404, detail="Item not found")


@app.post("/api/roi-lead")
async def handle_roi_lead(background_tasks: BackgroundTasks, payload: dict = Body(...)):
    """Äldre kalkylator-endpoint. Behålls som alias och matas in i lead engine
    så att allt hamnar i samma funnel och scoring."""
    email = payload.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")

    lead = lead_engine.Lead(
        email=email,
        source=payload.get("source", "roi-kalkylator"),
        calc_data=payload.get("data", {}) or {},
    )
    background_tasks.add_task(lead_engine.process_lead, lead)
    return {"status": "success", "message": "Lead received"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)



@app.get("/api/admin/leads")
async def get_admin_leads():
    # Enkelt mockat API för admin-vyn tills db-koppling finns
    import os
    import json
    
    leads = []
    leads_file = "data/leads.jsonl"
    
    if os.path.exists(leads_file):
        with open(leads_file, "r") as f:
            for line in f:
                try:
                    leads.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    
    # Sortera nyaste först
    leads.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    
    # Byt namn på fält för att matcha frontenden
    for lead in leads:
        if "timestamp" in lead and "created_at" not in lead:
            lead["created_at"] = lead["timestamp"]
    
    return {"leads": leads}
