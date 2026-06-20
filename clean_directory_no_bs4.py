import re

with open('/data/workspace/projects/proptech-guide-se/static/directory.html', 'r') as f:
    html = f.read()

# Find the grid
start = html.find('<div id="directoryGrid"')
if start != -1:
    grid_end = html.find('</main>', start)
    grid_content = html[start:grid_end]
    
    # regex to find cards
    # A card is roughly <div class="company-card ... </div> </div> </div></div> etc
    # To be safe, let's split by '<div class="company-card'
    parts = grid_content.split('<div class="company-card')
    
    new_grid_content = parts[0]
    seen_names = set()
    
    for part in parts[1:]:
        card = '<div class="company-card' + part
        
        # Extract the company name
        match = re.search(r'<h3[^>]*>([^<]+)</h3>', card)
        if match:
            name = match.group(1).strip()
            if name not in seen_names:
                seen_names.add(name)
                # find where this card ends and the next one begins.
                # Actually, split split by '<div class="company-card' means `part` contains exactly one card PLUS maybe some trailing spaces/closing tags if it's the last one.
                # Oh wait, the last part contains the closing tags of the grid.
                new_grid_content += card
        else:
            # Maybe an ad block or something, just keep it if it's not a company card
            new_grid_content += card
            
    html = html[:start] + new_grid_content + html[grid_end:]

with open('/data/workspace/projects/proptech-guide-se/static/directory.html', 'w') as f:
    f.write(html)
