import json

with open("data/companies.json", "r") as f:
    companies = json.load(f)

for c in companies:
    if c["name"] in ["Mestro", "Egain", "Metry"]:
        print(c["tier"])

