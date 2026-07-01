import sys

def main():
    file_path = "/data/workspace/projects/proptech-guide-se/SITE_VISION.md"
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    new_line = "  - 2026-07-01: 64 företag (61→64, +Nodeledge, Zesec, Bygglet).\n"
    
    if "2026-06-30: 62 företag" in content:
        content = content.replace("  - 2026-06-30: 62 företag (59→62, +KTC, Incoord, Aareon).\n", 
                                "  - 2026-06-30: 62 företag (59→62, +KTC, Incoord, Aareon).\n" + new_line)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print("Updated SITE_VISION.md")

if __name__ == "__main__":
    main()
