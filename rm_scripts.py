import os
import glob
for f in glob.glob('/data/workspace/projects/proptech-guide-se/add_new_companies*.py'):
    os.remove(f)
os.remove('/data/workspace/projects/proptech-guide-se/prepend_log.py')
