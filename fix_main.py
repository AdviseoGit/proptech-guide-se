import os

main_py_path = "/data/workspace/projects/proptech-guide-se/main.py"

with open(main_py_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add missing imports (Body, Path)
if 'from fastapi import Body' not in content:
    content = content.replace('from fastapi import FastAPI, Request, BackgroundTasks', 'from fastapi import FastAPI, Request, BackgroundTasks, Body\nfrom pathlib import Path')

with open(main_py_path, 'w', encoding='utf-8') as f:
    f.write(content)
