import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI(title="Proptech Guide Sverige")

app.mount("/static", StaticFiles(directory="static"), name="static")

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

@app.get("/kalkylator", response_class=HTMLResponse)
async def kalkylator():
    return FileResponse("static/kalkylator.html")

@app.get("/artikel/rise-of-proptech", response_class=HTMLResponse)
async def article1():
    return FileResponse("static/article.html")

@app.get("/artikel/digitala-tvillingar", response_class=HTMLResponse)
async def article2():
    return FileResponse("static/article2.html")

@app.get("/artikel/smarta-hem", response_class=HTMLResponse)
async def article3():
    return FileResponse("static/article3.html")

@app.get("/artikel/ai-fastighetsvarde", response_class=HTMLResponse)
async def article4():
    return FileResponse("static/article4.html")

@app.get("/robots.txt")
async def robots():
    return FileResponse("static/robots.txt")

@app.get("/sitemap.xml")
async def sitemap():
    return FileResponse("static/sitemap.xml")

@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favicon.svg")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
