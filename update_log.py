import datetime

log_path = "/data/workspace/projects/proptech-guide-se/PROGRESS_LOG.md"

with open(log_path, "r", encoding="utf-8") as f:
    content = f.read()

date_str = datetime.datetime.now().strftime("%Y-%m-%d")
new_log = f"{date_str} | TILLVÄXT | Expandera directory till 95 bolag (+Mestro, Sengera, Enjay, m.fl) | directory poster | nästa: Fler directory poster eller nytt verktyg\n"

# Lägg till högst upp
content = new_log + content

with open(log_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Progress log updated.")
