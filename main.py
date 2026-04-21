import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI(title="Proptech Guide Sverige")

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

@app.get("/om-oss", response_class=HTMLResponse)
async def om_oss():
    return FileResponse("static/om-oss.html")

@app.get("/robots.txt")
async def robots():
    return FileResponse("static/robots.txt")

@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favicon.svg")

# Catch-all route to serve any .html file from the static directory from the root URL
@app.get("/{filename}", response_class=HTMLResponse)
async def serve_html(filename: str):
    if filename.endswith(".html"):
        file_path = os.path.join("static", filename)
        if os.path.exists(file_path):
            return FileResponse(file_path)
    # Let FastAPI handle 404 if it's not an existing HTML file
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Item not found")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
