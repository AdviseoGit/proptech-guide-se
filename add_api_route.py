import os
import sys

main_file = "main.py"
with open(main_file, "r") as f:
    content = f.read()

if "/api/stats/leads" in content:
    print("Route already exists.")
    sys.exit(0)

# Vi vill lägga till en endpoint:
# @app.get("/api/stats/leads")
# async def stats_leads():
# ...

new_route = """
@app.get("/api/stats/leads")
async def stats_leads():
    import os
    import json
    from datetime import datetime, timedelta, timezone

    leads_file = "data/leads.jsonl"
    total = 0
    last_7_days = 0
    
    if os.path.exists(leads_file):
        try:
            with open(leads_file, "r") as f:
                lines = f.readlines()
                total = len(lines)
                
                # Check last 7 days
                now = datetime.now(timezone.utc)
                seven_days_ago = now - timedelta(days=7)
                
                for line in lines:
                    try:
                        data = json.loads(line)
                        # Check timestamp or created_at
                        ts_str = data.get("created_at") or data.get("timestamp")
                        if ts_str:
                            try:
                                # Try parsing ISO format
                                # simple check:
                                if "T" in ts_str:
                                    ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                                    if ts.tzinfo is None:
                                        ts = ts.replace(tzinfo=timezone.utc)
                                    if ts > seven_days_ago:
                                        last_7_days += 1
                                else:
                                    pass # skip if cant parse easily
                            except Exception:
                                pass
                    except json.JSONDecodeError:
                        pass
        except Exception:
            pass
            
    return {"total": total, "last_7_days": last_7_days}
"""

with open(main_file, "a") as f:
    f.write(new_route)

print("Added /api/stats/leads route to main.py")
