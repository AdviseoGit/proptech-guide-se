with open("/data/workspace/projects/proptech-guide-se/PROGRESS_LOG.md", "r") as f:
    lines = f.readlines()

new_line = "2026-07-26 | LEADFLOW | Byggde adminvy för leads (static/admin_leads.html) och API endpoint | leadhantering | nästa: Implementera gated PDF nedladdning för sponsrade guider\n"
lines.insert(0, new_line)

with open("/data/workspace/projects/proptech-guide-se/PROGRESS_LOG.md", "w") as f:
    f.writelines(lines)
