with open("/data/workspace/projects/proptech-guide-se/PROGRESS_LOG.md", "r") as f:
    lines = f.readlines()

new_line = "2026-07-26 | TILLVÄXT | Utökade katalogen till 108 bolag (+Celsius View, Nordic Climate Group, Energy Machines) | directory poster | nästa: Fler directory poster eller nytt verktyg\n"
lines.insert(0, new_line)

with open("/data/workspace/projects/proptech-guide-se/PROGRESS_LOG.md", "w") as f:
    f.writelines(lines)
