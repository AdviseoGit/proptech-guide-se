import os
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI(title="Proptech Guide Sverige")

import psycopg2
from pydantic import BaseModel, EmailStr

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


def _deliver_pt(email):
    import mailer
    import report_pt
    _save_lead_pt(email)
    pdf = None
    try:
        pdf = report_pt.build_guide_pdf()
    except Exception as e:
        print(f"[pt] guide pdf failed: {e}")
    atts = [("PropTech-ROI-guide.pdf", pdf, "application/pdf")] if pdf else None
    mailer.send_email(email, "Din PropTech ROI-guide", report_pt.user_email_html(),
                      attachments=atts, from_name="Proptech Guide Sverige")
    mailer.notify_owner("Ny lead - Proptech Guide", f"<p>Ny lead: <b>{email}</b></p>",
                        reply_to=email, from_name="Proptech Guide Sverige")


@app.post("/api/lead")
async def capture_lead(lead: LeadIn, background: BackgroundTasks):
    background.add_task(_deliver_pt, lead.email)
    return {"status": "success"}

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

    # Original logic for files that might already have .html
    if filename.endswith(".html"):
        file_path_original = os.path.join("static", filename)
        if os.path.exists(file_path_original):
            return FileResponse(file_path_original)
            
    # Let FastAPI handle 404 if it's not an existing HTML file
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Item not found")


@app.post("/api/roi-lead")
async def handle_roi_lead(background_tasks: BackgroundTasks, payload: dict = Body(...)):
    email = payload.get("email")
    data = payload.get("data", {})
    source = payload.get("source", "roi-kalkylator")
    
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")
        
    # Process lead asynchronously (send email, save to db, etc)
    # For now, we simulate processing
    print(f"New ROI lead received: {email}")
    print(f"Data: {data}")
    
    # Store lead data locally (append to a JSON lines file for data accumulation)
    import json
    from datetime import datetime
    
    lead_entry = {
        "timestamp": datetime.now().isoformat(),
        "email": email,
        "source": source,
        "data": data
    }
    
    # Save to data directory to accumulate own data
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    with open(data_dir / "leads.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(lead_entry) + "\n")
        
    # Forward to the site owner
    try:
        from mailer import send_email
        email_body = f"Nytt lead från ROI-kalkylatorn!\n\nE-post: {email}\nKälla: {source}\nData: {json.dumps(data, indent=2)}"
        background_tasks.add_task(send_email, "simon@adviseo.se", "Nytt lead: Proptech ROI Kalkylator", email_body)
    except Exception as e:
        print(f"Failed to queue email task: {e}")
        
    return {"status": "success", "message": "Lead received"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
