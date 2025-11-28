# Pipedrive Automations - Stap voor Stap Instructies

## Voorbereiding

1. Open Pipedrive
2. Ga naar **Automations** (linker menu, of via tandwiel > Automations)
3. Klik **+ Create automation**

---

## Pipeline Keuze

Kies de juiste pipeline voor je automations. Op basis van je setup:

- **vacature analyse** (id: 4) - Voor kandidatentekort.nl leads
- **Recruitment APK** (id: 2) - Voor APK leads

Ik gebruik hieronder "vacature analyse" als voorbeeld.

---

## AUTOMATION 1: Start Sequence + Email 1 (Dag 1)

### Stap 1: Trigger instellen
1. Klik **+ Create automation**
2. Geef naam: `Trust-First Email 1 - Dag 1`
3. Bij **Trigger**, kies: **Deal enters stage**
4. Selecteer pipeline: **vacature analyse**
5. Selecteer stage: **Gekwalificeerd** (of maak een nieuwe stage "Rapport Verzonden")

### Stap 2: Actions toevoegen

**Action 1: Update deal field**
- Klik **+ Add action**
- Kies: **Update deal**
- Field: **Rapport Verzonden Op**
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
- From: Jouw email (wouter@recruitin.nl of warts@recruitin.nl)
- To: **Person email** (linked to deal)
- Template: **Trust-First Email 1 - Check-in Dag 1**

**Action 5: Update deal field**
- Klik **+ Add action**
- Kies: **Update deal**
- Field: **Laatste Email Verzonden**
- Value: **Email 1**

### Stap 3: Opslaan
- Klik **Save**
- Zet automation **Active**

---

## AUTOMATION 2: Email 2 (Dag 3)

### Stap 1: Trigger instellen
1. Klik **+ Create automation**
2. Geef naam: `Trust-First Email 2 - Dag 3`
3. Bij **Trigger**, kies: **Deal field updated**
4. Field: **Laatste Email Verzonden**
5. Value changed to: **Email 1**

### Stap 2: Condition toevoegen
- Klik **+ Add condition**
- Field: **Email Sequence Status**
- Condition: **equals**
- Value: **Actief**

### Stap 3: Actions toevoegen

**Action 1: Wait**
- Kies: **Wait**
- Duration: **2 days** (totaal 3 dagen sinds start)

**Action 2: Send email**
- Kies: **Send email**
- Template: **Trust-First Email 2 - Is het gelukt Dag 3**

**Action 3: Update deal field**
- Field: **Laatste Email Verzonden**
- Value: **Email 2**

### Stap 4: Opslaan en activeren

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
2. **Send email**: Trust-First Email 3 - Resultaten Dag 5
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
2. **Send email**: Trust-First Email 4 - Tip Functietitel Dag 8
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
2. **Send email**: Trust-First Email 5 - Tip Salaris Dag 11
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
2. **Send email**: Trust-First Email 6 - Tip Opening Dag 14
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
2. **Send email**: Trust-First Email 7 - Gesprek Aanbod Dag 21
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
2. **Send email**: Trust-First Email 8 - Final Check-in Dag 30
3. **Update deal**: Laatste Email Verzonden = **Email 8**
4. **Update deal**: Email Sequence Status = **Voltooid**

---

## AUTOMATION 9: Stop bij Reply (Optioneel)

### Trigger
- **Email reply received** (als beschikbaar in jouw Pipedrive plan)
- OF: **Activity created** met type "Email"

### Actions
1. **Update deal**: Email Sequence Status = **Gepauzeerd**

---

## AUTOMATION 10: Stop bij Stage Wijziging (Optioneel)

### Trigger
- **Deal enters stage**
- Stage: **Afspraak** of **Demo gepland** of **Contact opgenomen**

### Actions
1. **Update deal**: Email Sequence Status = **Gepauzeerd**

---

## Samenvatting Timing

```
Dag 0:  Deal enters stage "Rapport Verzonden"
        ↓
        Set "Rapport Verzonden Op" = today
        Set "Email Sequence Status" = Actief
        ↓
Dag 1:  Email 1 verzonden → "Laatste Email" = Email 1
        ↓ (trigger automation 2)
Dag 3:  Email 2 verzonden → "Laatste Email" = Email 2
        ↓
Dag 5:  Email 3 verzonden → "Laatste Email" = Email 3
        ↓
Dag 8:  Email 4 verzonden → "Laatste Email" = Email 4
        ↓
Dag 11: Email 5 verzonden → "Laatste Email" = Email 5
        ↓
Dag 14: Email 6 verzonden → "Laatste Email" = Email 6
        ↓
Dag 21: Email 7 verzonden → "Laatste Email" = Email 7
        ↓
Dag 30: Email 8 verzonden → "Laatste Email" = Email 8
        Set "Email Sequence Status" = Voltooid
```

---

## Checklist

- [ ] Automation 1: Email 1 (Dag 1) - Start sequence
- [ ] Automation 2: Email 2 (Dag 3)
- [ ] Automation 3: Email 3 (Dag 5)
- [ ] Automation 4: Email 4 (Dag 8)
- [ ] Automation 5: Email 5 (Dag 11)
- [ ] Automation 6: Email 6 (Dag 14)
- [ ] Automation 7: Email 7 (Dag 21)
- [ ] Automation 8: Email 8 (Dag 30) - Final + set Voltooid
- [ ] Automation 9: Stop bij reply (optioneel)
- [ ] Automation 10: Stop bij stage wijziging (optioneel)

---

## Test Procedure

1. Maak een test deal aan met je eigen email
2. Verplaats de deal naar de trigger stage
3. Check of "Rapport Verzonden Op" en "Email Sequence Status" worden gezet
4. Wacht 1 dag (of pas tijdelijk de wait aan naar minuten voor testing)
5. Check of Email 1 binnenkomt
6. Verifieer dat "Laatste Email Verzonden" = "Email 1"

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
