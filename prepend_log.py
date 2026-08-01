import os
import sys

def prepend_line(file_path, line):
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        content = "Historik\n"
        
    with open(file_path, 'w') as f:
        f.write(line + "\n" + content)

prepend_line('/data/workspace/projects/proptech-guide-se/PROGRESS_LOG.md', '2026-08-01 | TILLVÄXT | Utökade katalogen med 3 proptech-bolag (+Iqnite, Nivéus, Noda) till 114 | katalogstorlek | nästa: Ny artikel eller directory poster')
