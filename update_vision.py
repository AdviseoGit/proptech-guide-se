import re
import sys

def main():
    file_path = "SITE_VISION.md"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Update 58 to 62, and add new entry
    new_entry = "  - 2026-06-30: 62 företag (59→62, +KTC, Incoord, Aareon).\n  - 2026-06-29: 59 företag"
    content = content.replace("  - 2026-06-29: 58 företag (55→58, +Pigra, TenFAST, Momentum Software).", new_entry.replace("59 företag", "59 företag (55→58, +Pigra, TenFAST, Momentum Software)."))

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    main()
