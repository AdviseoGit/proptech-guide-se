import os

main_py_path = "/data/workspace/projects/proptech-guide-se/main.py"

with open(main_py_path, 'r', encoding='utf-8') as f:
    content = f.read()

if 'from fastapi import BackgroundTasks' not in content:
    content = content.replace('from fastapi import FastAPI, Request, HTTPException', 'from fastapi import FastAPI, Request, HTTPException, BackgroundTasks, Body')

if '/api/roi-lead' not in content:
    api_code = """
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
        f.write(json.dumps(lead_entry) + "\\n")
        
    # Forward to the site owner
    try:
        from mailer import send_email
        email_body = f"Nytt lead från ROI-kalkylatorn!\\n\\nE-post: {email}\\nKälla: {source}\\nData: {json.dumps(data, indent=2)}"
        background_tasks.add_task(send_email, "simon@adviseo.se", "Nytt lead: Proptech ROI Kalkylator", email_body)
    except Exception as e:
        print(f"Failed to queue email task: {e}")
        
    return {"status": "success", "message": "Lead received"}
"""
    
    # Find a good place to insert (before if __name__ == "__main__":)
    insert_pos = content.rfind('if __name__ == "__main__":')
    if insert_pos != -1:
        content = content[:insert_pos] + api_code + '\n' + content[insert_pos:]
        
        with open(main_py_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Added /api/roi-lead route to main.py")
