import sys

def main():
    file_path = "/data/workspace/projects/proptech-guide-se/PROGRESS_LOG.md"
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    new_line = "2026-07-01 | TILLVÄXT | Expandera directory till 64 bolag (+Nodeledge, Zesec, Bygglet) | directory poster | nästa: Fler directory poster eller nytt verktyg\n"
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_line + content)
        
    print("Updated PROGRESS_LOG.md")

if __name__ == "__main__":
    main()
