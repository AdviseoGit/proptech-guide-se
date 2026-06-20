import re

with open('/data/workspace/projects/proptech-guide-se/static/directory.html', 'r') as f:
    content = f.read()

# Remove duplicate companies at the bottom
companies_to_remove = ["Bostadsregistraturet", "Nabo", "Metry"]

for company in companies_to_remove:
    # Use regex to find and remove the whole company card
    pattern = r'<!--\s*Company Card: ' + company + r'\s*-->.*?</div>\s*</div>\s*</div>'
    content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    # Try a different pattern if the above doesn't work
    pattern2 = r'<!--\s*Company Card:\s*' + company + r'\s*-->.*?<div class="mt-auto">.*?</div>\s*</div>'
    content = re.sub(pattern2, '', content, flags=re.DOTALL)

with open('/data/workspace/projects/proptech-guide-se/static/directory.html', 'w') as f:
    f.write(content)
