# Struktur och intäktsmodell — proptechguiden.se

Sajten är byggd kring två saker: att **sortera besökaren på målgrupp** direkt, och att
**kvalificera varje förfrågan** så den går att sälja vidare som ett lead.

## Sidkarta

```
/                          Startsida — sorterar besökaren på målgrupp
├── /fastighetsagare       Segmenthubb: fastighetsägare
├── /forvaltare            Segmenthubb: kommersiella förvaltare
├── /brf                   Segmenthubb: BRF-styrelser
├── /directory             Leverantörskatalog (filtrerbar på kategori + målgrupp)
│   └── /leverantor/<slug> Profilsida (endast tier verifierad/partner)
├── /verktyg               Kalkylatoröversikt
│   ├── /roi-kalkylator
│   └── /digital-trapphustavla-kalkylator
├── /guider                Guidehubb, grupperad per målgrupp, med sponsorplatser
└── /for-leverantorer      Säljsidan för de tre intäktsströmmarna
```

Varje segmenthubb länkar vidare till katalogen med förvald filtrering
(`/directory?segment=brf&kategori=energi`), så besökaren aldrig möter hela listan
på 107 bolag utan alltid ser sitt eget urval.

## De tre intäktsströmmarna

### 1. Katalogplaceringar

Styrs av fältet `tier` i `data/companies.json`:

| tier | Sortering | Länk | Profilsida | Får leads |
|---|---|---|---|---|
| `free` | Sist, bokstavsordning | nofollow | Nej | Nej |
| `verifierad` | Före gratisposter | dofollow | Ja | Nej |
| `partner` | Överst + egen sektion "Utvalda partners" | dofollow | Ja | Ja |

Att bara betalande nivåer får följbar länk är avsiktligt — delas länkvärdet ut gratis
till alla 107 poster finns ingenting kvar att sälja.

**Uppgradera ett bolag:** sätt `tier`, fyll i `usp`, `cases` och `contact_email`,
sätt `receives_leads: true`, kör `python build.py`.

> Alla bolag ligger på `free` idag. Sätt aldrig `partner` på ett bolag ni inte har
> avtal med — det är ett partnerskapspåstående om ett riktigt företag.

### 2. Kvalificerade leads

Alla förfrågningar går genom `POST /api/lead` och poängsätts i `lead_engine.py`:

| Faktor | Max poäng |
|---|---|
| Roll (beslutsfattare väger tyngst) | 25 |
| Portföljstorlek (kvm, eller lägenheter × 70) | 30 |
| Tidsram | 25 |
| Budgetläge | 20 |
| Telefon / företag / samtycke | 20 |

Betyg: **A** ≥ 70, **B** ≥ 45, **C** < 45. Prissättningen per betyg står på
`/for-leverantorer`.

`estimate_deal_value()` räknar dessutom fram ett grovt förstaårsvärde
(yta × kr/kvm per kategori) som följer med i leadnotisen, så det går att se vilka
leads som är värda att ringa på först.

Leads delas bara vidare till partners när användaren aktivt kryssat i samtycke.

### 3. Sponsrade guider

`data/guides.json` har `sponsor` och `sponsor_slot_open` per guide. Sätts `sponsor`
visas "I samarbete med X" på guidekortet, och antalet lediga platser räknas
automatiskt ned på `/guider` och `/for-leverantorer`.

## Leadwidgeten

`static/lead-engine.js` är ett trestegsformulär som droppas in var som helst:

```html
<div data-lead-form
     data-source="roi-kalkylator"
     data-segment="brf"          <!-- valfritt: låser målgruppssteget -->
     data-need="energi"          <!-- valfritt: låser behovssteget -->
     data-title="Få offert"></div>
<script src="/lead-engine.js"></script>
```

Stegen är ordnade så att kvalificeringen sker först och e-postadressen begärs sist,
när besökaren redan investerat i flödet. Kalkylatorer skickar med sina siffror genom
att sätta `window.proptechCalcData` innan submit.

## Bygga om sajten

```bash
python build.py       # genererar startsida, katalog, segmenthubbar, guider, säljsida, sitemap
python sync_nav.py    # synkar delad nav + footer på de handskrivna sidorna
```

`site_template.py` äger nav, footer och all segment-/kategorikonfiguration.
Ändra där, kör om båda skripten — då följer hela sajten med.

Genererade filer (skrivs över av `build.py`, redigera dem inte för hand):
`index.html`, `directory.html`, `fastighetsagare.html`, `forvaltare.html`,
`brf.html`, `verktyg.html`, `guider.html`, `for-leverantorer.html`,
`leverantor/*.html`, `sitemap.xml`.

## API

| Endpoint | Vad den gör |
|---|---|
| `POST /api/lead` | Kvalificerat lead. Payload med enbart `email` behandlas som PDF-fångst (bakåtkompatibelt). |
| `POST /api/roi-lead` | Äldre alias, matas in i samma funnel. |
| `POST /api/partner-ansokan` | Leverantörers intresseanmälan. |

Leads sparas alltid till `data/leads.jsonl` först och därefter till Postgres
(`proptech_leads_v2`) om `DATABASE_URL` är satt — så inget lead går förlorat om
databasen strular.

## Nästa steg för att skärpa leadgen

1. Sätt upp gated PDF-nedladdning för guiderna som har `"gated": true` — idag är
   fältet förberett men PDF:erna genereras bara för ROI-guiden (`report_pt.py`).
2. Bygg en enkel adminvy över `proptech_leads_v2` så leads kan följas upp utan
   att gå via mejlen.
3. Sälj in de tre första partnerplatserna i kategorin `energi` — det är den
   kategori som har flest leverantörer och högst estimerat affärsvärde per kvm.
