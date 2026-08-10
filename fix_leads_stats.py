import json

def patch_main():
    with open('/data/workspace/projects/proptech-guide-se/main.py', 'r') as f:
        content = f.read()

    import re
    
    pattern = re.compile(r'@app\.get\("/api/stats/leads"\)\nasync def stats_leads\(\).*?return \{"total": total, "last_7_days": last_7_days\}', re.DOTALL)
    
    replacement = """@app.get("/api/stats/leads")
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
                        record = json.loads(line)
                        created_at_str = record.get("created_at") or record.get("timestamp")
                        if created_at_str:
                            created_at = datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))
                            if created_at.tzinfo is None:
                                created_at = created_at.replace(tzinfo=timezone.utc)
                            if created_at > seven_days_ago:
                                last_7_days += 1
                    except Exception:
                        pass
        except Exception:
            pass
            
    # Also check DB for legacy leads
    try:
        if DATABASE_URL:
            # We must import psycopg2 here, and handle ModuleNotFoundError just in case
            try:
                import psycopg2
                conn = psycopg2.connect(DATABASE_URL)
                cur = conn.cursor()
                cur.execute("SELECT COUNT(*) FROM proptech_leads")
                db_total = cur.fetchone()[0]
                cur.execute("SELECT COUNT(*) FROM proptech_leads WHERE created_at > NOW() - INTERVAL '7 days'")
                db_7d = cur.fetchone()[0]
                
                total = max(total, db_total)
                last_7_days = max(last_7_days, db_7d)
                
                cur.close()
                conn.close()
            except ImportError:
                pass
    except Exception:
        pass
            
    return {"total": total, "last_7_days": last_7_days}"""
    
    new_content = pattern.sub(replacement, content)
    if new_content != content:
        with open('/data/workspace/projects/proptech-guide-se/main.py', 'w') as f:
            f.write(new_content)
        print("Patched main.py")
    else:
        print("Regex match failed")

patch_main()
