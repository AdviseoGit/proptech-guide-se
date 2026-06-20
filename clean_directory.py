import re
from bs4 import BeautifulSoup

with open('/data/workspace/projects/proptech-guide-se/static/directory.html', 'r') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
grid = soup.find('div', id='directoryGrid')

if grid:
    cards = grid.find_all('div', class_='company-card')
    seen = set()
    cards_to_keep = []
    
    for card in cards:
        h3 = card.find('h3')
        if h3:
            name = h3.text.strip()
            if name not in seen:
                seen.add(name)
                cards_to_keep.append(card)
        else:
            cards_to_keep.append(card) # keep if no h3 (ad slots)

    print(f"Keeping {len(cards_to_keep)} unique items out of {len(cards)}")
    
    # Remove all children of grid
    grid.clear()
    
    # Add back unique cards
    for card in cards_to_keep:
        grid.append(card)

with open('/data/workspace/projects/proptech-guide-se/static/directory.html', 'w') as f:
    f.write(str(soup))
