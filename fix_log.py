with open('/data/workspace/projects/proptech-guide-se/PROGRESS_LOG.md', 'r') as f:
    lines = f.readlines()
    
# Remove the bad line
lines.pop(0)

# Insert the right one
new_line = "2026-07-20 | TILLVÄXT | Expandera directory till 135 bolag (+Schneider Electric, Siemens, Caverion, Bravida, Assemblin, Kiona, Myrspoven, Pigello, DeDu, Tmpl) | directory poster | nästa: Publicera original-data-artikel eller optimera startsidan för SEO\n"
lines.insert(0, new_line)

with open('/data/workspace/projects/proptech-guide-se/PROGRESS_LOG.md', 'w') as f:
    f.writelines(lines)
    
print("Log fixed")
