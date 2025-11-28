# Pipedrive Automations - Recruitment APK Pipeline

## Pipeline Configuratie

**Pipeline:** Recruitment APK (id: 2)
**Typeform:** https://form.typeform.com/to/cuGe3IEC
**Website:** www.recruitmentapk.nl

---

## Deal Stages (Aanbevolen Setup)

| Stage | Naam | Beschrijving | Rotting Days |
|-------|------|--------------|--------------|
| 1 | Nieuw | Typeform ingevuld, wacht op APK | 3 |
| 2 | APK in Behandeling | Bezig met APK genereren | 2 |
| 3 | APK Verzonden | APK rapport verstuurd | 7 |
| 4 | Follow-up | Email sequence actief | 30 |
| 5 | Gesprek Gepland | Calendly afspraak gemaakt | 7 |
| 6 | Gewonnen | Klant/Samenwerking | - |
| 7 | Verloren | Geen interesse/reactie | - |

---

## Custom Fields Aanmaken

Ga naar: **Settings > Data fields > Deal fields**

### Verplichte velden:

| Veldnaam | Type | Opties |
|----------|------|--------|
| APK Verzonden Op | Date | - |
| APK Score | Number | - |
| Email Sequence Status | Single option | Actief, Gepauzeerd, Voltooid |
| Laatste Email Verzonden | Single option | Email 1, Email 2, Email 3, Email 4, Email 5, Email 6, Email 7, Email 8 |
| Typeform Response ID | Text | - |
| Verbeterpunten | Large text | - |

---

## Voorbereiding

1. Open Pipedrive
2. Ga naar **Automations** (linker menu, of via tandwiel > Automations)
3. Klik **+ Create automation**

---

## AUTOMATION 1: Start Sequence + Email 1 (Dag 1)

### Stap 1: Trigger instellen
1. Klik **+ Create automation**
2. Geef naam: `APK Email 1 - Dag 1 - APK Ontvangen`
3. Bij **Trigger**, kies: **Deal enters stage**
4. Selecteer pipeline: **Recruitment APK**
5. Selecteer stage: **APK Verzonden**

### Stap 2: Actions toevoegen

**Action 1: Update deal field**
- Klik **+ Add action**
- Kies: **Update deal**
- Field: **APK Verzonden Op**
- Value: **Trigger date** (of "Current date")

**Action 2: Update deal field**
- Klik **+ Add action**
- Kies: **Update deal**
- Field: **Email Sequence Status**
- Value: **Actief**

**Action 3: Wait**
- Klik **+ Add action**
- Kies: **Wait**
- Duration: **1 day**

**Action 4: Send email**
- Klik **+ Add action**
- Kies: **Send email**
- From: warts@recruitin.nl
- To: **Person email** (linked to deal)
- Template: **APK Email 1 - APK Ontvangen Dag 1**

**Action 5: Update deal field**
- Klik **+ Add action**
- Kies: **Update deal**
- Field: **Laatste Email Verzonden**
- Value: **Email 1**

**Action 6: Move deal to stage**
- Klik **+ Add action**
- Kies: **Move deal**
- Stage: **Follow-up**

### Stap 3: Opslaan
- Klik **Save**
- Zet automation **Active**

---

## AUTOMATION 2: Email 2 (Dag 3)

### Trigger
- **Deal field updated**
- Field: **Laatste Email Verzonden**
- Value changed to: **Email 1**

### Condition
- **Email Sequence Status** equals **Actief**

### Actions
1. **Wait**: 2 days (totaal 3 dagen)
2. **Send email**: APK Email 2 - Al Bekeken Dag 3
3. **Update deal**: Laatste Email Verzonden = **Email 2**

---

## AUTOMATION 3: Email 3 (Dag 5)

### Trigger
- **Deal field updated**
- Field: **Laatste Email Verzonden**
- Value changed to: **Email 2**

### Condition
- **Email Sequence Status** equals **Actief**

### Actions
1. **Wait**: 2 days
2. **Send email**: APK Email 3 - Eerste Stappen Dag 5
3. **Update deal**: Laatste Email Verzonden = **Email 3**

---

## AUTOMATION 4: Email 4 (Dag 8)

### Trigger
- **Deal field updated**
- Field: **Laatste Email Verzonden**
- Value changed to: **Email 3**

### Condition
- **Email Sequence Status** equals **Actief**

### Actions
1. **Wait**: 3 days
2. **Send email**: APK Email 4 - Tip Time-to-Hire Dag 8
3. **Update deal**: Laatste Email Verzonden = **Email 4**

---

## AUTOMATION 5: Email 5 (Dag 11)

### Trigger
- **Deal field updated**
- Field: **Laatste Email Verzonden**
- Value changed to: **Email 4**

### Condition
- **Email Sequence Status** equals **Actief**

### Actions
1. **Wait**: 3 days
2. **Send email**: APK Email 5 - Tip Candidate Experience Dag 11
3. **Update deal**: Laatste Email Verzonden = **Email 5**

---

## AUTOMATION 6: Email 6 (Dag 14)

### Trigger
- **Deal field updated**
- Field: **Laatste Email Verzonden**
- Value changed to: **Email 5**

### Condition
- **Email Sequence Status** equals **Actief**

### Actions
1. **Wait**: 3 days
2. **Send email**: APK Email 6 - Tip Meten Weten Dag 14
3. **Update deal**: Laatste Email Verzonden = **Email 6**

---

## AUTOMATION 7: Email 7 (Dag 21)

### Trigger
- **Deal field updated**
- Field: **Laatste Email Verzonden**
- Value changed to: **Email 6**

### Condition
- **Email Sequence Status** equals **Actief**

### Actions
1. **Wait**: 7 days
2. **Send email**: APK Email 7 - Gesprek Aanbod Dag 21
3. **Update deal**: Laatste Email Verzonden = **Email 7**

---

## AUTOMATION 8: Email 8 - Final (Dag 30)

### Trigger
- **Deal field updated**
- Field: **Laatste Email Verzonden**
- Value changed to: **Email 7**

### Condition
- **Email Sequence Status** equals **Actief**

### Actions
1. **Wait**: 9 days
2. **Send email**: APK Email 8 - Final Check-in Dag 30
3. **Update deal**: Laatste Email Verzonden = **Email 8**
4. **Update deal**: Email Sequence Status = **Voltooid**

---

## AUTOMATION 9: Stop bij Reply

### Trigger
- **Email reply received** (indien beschikbaar)
- OF: **Activity created** met type "Email"

### Actions
1. **Update deal**: Email Sequence Status = **Gepauzeerd**

---

## AUTOMATION 10: Stop bij Stage Wijziging (Gesprek)

### Trigger
- **Deal enters stage**
- Stage: **Gesprek Gepland**

### Actions
1. **Update deal**: Email Sequence Status = **Gepauzeerd**

---

## AUTOMATION 11: Typeform naar Pipedrive (Webhook)

### Optie A: Zapier Integration
1. Trigger: New Typeform Response
2. Action: Create Pipedrive Deal
3. Mapping:
   - Deal title: "APK - {Company Name}"
   - Person: Create/Find by email
   - Pipeline: Recruitment APK
   - Stage: Nieuw

### Optie B: Native Pipedrive Webhook
- Gebruik de bestaande webhook handler in `/fixed_webhook_handler.py`

---

## Timing Overzicht

```
Dag 0:  Deal enters stage "APK Verzonden"
        |
        Set "APK Verzonden Op" = today
        Set "Email Sequence Status" = Actief
        Move deal to "Follow-up"
        |
Dag 1:  Email 1 verzonden -> "Laatste Email" = Email 1
        | (trigger automation 2)
Dag 3:  Email 2 verzonden -> "Laatste Email" = Email 2
        |
Dag 5:  Email 3 verzonden -> "Laatste Email" = Email 3
        |
Dag 8:  Email 4 verzonden -> "Laatste Email" = Email 4
        |
Dag 11: Email 5 verzonden -> "Laatste Email" = Email 5
        |
Dag 14: Email 6 verzonden -> "Laatste Email" = Email 6
        |
Dag 21: Email 7 verzonden -> "Laatste Email" = Email 7
        |
Dag 30: Email 8 verzonden -> "Laatste Email" = Email 8
        Set "Email Sequence Status" = Voltooid
```

---

## Checklist

### Custom Fields
- [ ] APK Verzonden Op (Date)
- [ ] APK Score (Number)
- [ ] Email Sequence Status (Single option)
- [ ] Laatste Email Verzonden (Single option)
- [ ] Typeform Response ID (Text)
- [ ] Verbeterpunten (Large text)

### Deal Stages
- [ ] Nieuw
- [ ] APK in Behandeling
- [ ] APK Verzonden
- [ ] Follow-up
- [ ] Gesprek Gepland
- [ ] Gewonnen
- [ ] Verloren

### Email Templates
- [ ] APK Email 1 - APK Ontvangen Dag 1
- [ ] APK Email 2 - Al Bekeken Dag 3
- [ ] APK Email 3 - Eerste Stappen Dag 5
- [ ] APK Email 4 - Tip Time-to-Hire Dag 8
- [ ] APK Email 5 - Tip Candidate Experience Dag 11
- [ ] APK Email 6 - Tip Meten Weten Dag 14
- [ ] APK Email 7 - Gesprek Aanbod Dag 21
- [ ] APK Email 8 - Final Check-in Dag 30

### Automations
- [ ] Automation 1: Email 1 (Dag 1) - Start sequence
- [ ] Automation 2: Email 2 (Dag 3)
- [ ] Automation 3: Email 3 (Dag 5)
- [ ] Automation 4: Email 4 (Dag 8)
- [ ] Automation 5: Email 5 (Dag 11)
- [ ] Automation 6: Email 6 (Dag 14)
- [ ] Automation 7: Email 7 (Dag 21)
- [ ] Automation 8: Email 8 (Dag 30) - Final + set Voltooid
- [ ] Automation 9: Stop bij reply
- [ ] Automation 10: Stop bij stage wijziging

---

## Test Procedure

1. Maak een test deal aan met je eigen email
2. Verplaats de deal naar stage "APK Verzonden"
3. Check of "APK Verzonden Op" en "Email Sequence Status" worden gezet
4. Check of deal naar "Follow-up" stage gaat
5. Wacht 1 dag (of pas tijdelijk de wait aan naar minuten)
6. Check of Email 1 binnenkomt
7. Verifieer dat "Laatste Email Verzonden" = "Email 1"

**Tip:** Voor testen, zet de Wait tijdelijk op 1-5 minuten ipv dagen.

---

## Troubleshooting

**Emails komen niet aan:**
- Check of je email sync actief is in Pipedrive
- Verifieer dat de deal een linked person heeft met email
- Check spam folder

**Automation triggert niet:**
- Verifieer dat automation op "Active" staat
- Check of de condition "Email Sequence Status = Actief" klopt
- Kijk in Automation > History voor errors

**Verkeerde volgorde:**
- Elke automation triggered op de vorige "Laatste Email" value
- Als Email 2 niet triggert, check of Email 1 correct "Email 1" heeft gezet

---

*Laatste update: November 2024*
