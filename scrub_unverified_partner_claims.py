"""Stoppa vidarebefordran av leads till overifierade partneradresser, och ta bort
kundcase som inte går att belägga.

Bakgrund: partnerposterna lades in med kontaktadresser och kundcase som inte är
kontrollerade. Två konkreta problem följde av det:

1. receives_leads=True innebär att lead_engine mejlar namn, telefon, bolag,
   portföljstorlek och budgetläge till adressen i contact_email. Adresserna är
   gissade — partner@mestro.se ligger till exempel på en annan domän än bolagets
   egen (mestro.com). Personuppgifter går då till en mottagare som varken har
   avtal eller personuppgiftsbiträdesavtal. Samtyckestexten i formuläret täcker
   inte det.

2. cases innehåller namngivna fastighetsbolag som referenskunder. Det är
   påståenden om tredje part som vi inte kan styrka.

Tier-fältet lämnas orört — om avtalen finns är det en affärsuppgift, inte en
teknisk. Men leadflödet och kundcasen stängs av tills uppgifterna är bekräftade.

Kör:  python scrub_unverified_partner_claims.py
"""
import json
from pathlib import Path

DATA = Path(__file__).parent / "data"


def main():
    path = DATA / "companies.json"
    companies = json.loads(path.read_text(encoding="utf-8"))

    parked = []
    for c in companies:
        changes = []
        if c.get("receives_leads"):
            c["receives_leads"] = False
            changes.append("leadutskick av")
        if c.get("contact_email"):
            changes.append(f"kontaktadress borttagen ({c['contact_email']})")
            c["contact_email"] = ""
        if c.get("cases"):
            changes.append(f"{len(c['cases'])} kundcase borttagna")
            c["cases"] = []
        if changes:
            parked.append((c["name"], changes))

    path.write_text(json.dumps(companies, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8")

    for name, changes in parked:
        print(f"  {name}: " + "; ".join(changes))
    print(f"\n{len(parked)} poster åtgärdade. Inga leads vidarebefordras nu till "
          f"externa mottagare.")


if __name__ == "__main__":
    main()
