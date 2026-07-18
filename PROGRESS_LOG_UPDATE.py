with open('/data/workspace/projects/proptech-guide-se/PROGRESS_LOG.md', 'r') as f:
    lines = f.readlines()

new_line = "2026-07-18 | TILLVÄXT | Expandera directory till 125 bolag (+Nivika, Hyresvärd.se, Smartvatten, HomeRun, Paligo, Iqnect, InviSense, Sally R, Noda, RCO, Hydda, Infobric, Flowbird, Amido, Propely) | directory poster | nästa: Bygg innehåll/sida för sökordet 'smarta byggnader' (klättrar)\n"
lines.insert(0, new_line)

with open('/data/workspace/projects/proptech-guide-se/PROGRESS_LOG.md', 'w') as f:
    f.writelines(lines)
