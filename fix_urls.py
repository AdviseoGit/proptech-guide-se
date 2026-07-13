import os
import re

html_files = [f for f in os.listdir("static") if f.endswith(".html")]

for filename in html_files:
    filepath = os.path.join("static", filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Navigationsfixar: proptech-kalkylator -> kalkylator/proptech-roi har bytts, men det verkar vara det som var felet
    # Nej, proptech-kalkylator existerar ju. Så varför funkade det inte? Det ligger i static och borde bli serverat.
    pass
