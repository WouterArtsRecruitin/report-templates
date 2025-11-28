# Pipedrive Trust-First Email Automation Setup

## Overzicht

**Campagne:** Trust-First Nurture (8 emails over 30 dagen)
**Strategie:** Eerst vertrouwen opbouwen, dan pas conversie

| Fase | Emails | Dagen | Doel |
|------|--------|-------|------|
| Check-in | 1-3 | 1, 3, 5 | Oprechte interesse tonen |
| Waarde | 4-6 | 8, 11, 14 | Gratis tips & expertise |
| Conversie | 7-8 | 21, 30 | Zachte gesprek uitnodiging |

---

## STAP 1: Custom Fields Aanmaken

### In Pipedrive: Settings > Data fields > Deal fields

| Veld Naam | Type | Opties | Doel |
|-----------|------|--------|------|
| Rapport Verzonden Op | Date | - | Startdatum sequence |
| Email Sequence Status | Single option | Actief / Gepauzeerd / Voltooid | Controle sequence |
| Laatste Email Verzonden | Single option | Email 1 / Email 2 / ... / Email 8 | Track progress |
| Functie Titel | Text | - | Merge field content |

---

## STAP 2: Email Templates Aanmaken

### In Pipedrive: Settings > Email templates > New template

Maak 8 templates aan met de volgende onderwerpen:

### Template 1: Check-in Dag 1
- **Naam:** Trust-First Email 1
- **Onderwerp:** Even checken - alles goed ontvangen?
- **Content:** Zie Trust_First_Email_Campaign.html - Email 1

### Template 2: Is Het Gelukt? Dag 3
- **Naam:** Trust-First Email 2
- **Onderwerp:** Is het gelukt om de aanpassingen door te voeren?
- **Content:** Zie Trust_First_Email_Campaign.html - Email 2

### Template 3: Resultaten? Dag 5
- **Naam:** Trust-First Email 3
- **Onderwerp:** Benieuwd - merk je al verschil?
- **Content:** Zie Trust_First_Email_Campaign.html - Email 3

### Template 4: Tip Functietitel Dag 8
- **Naam:** Trust-First Email 4
- **Onderwerp:** Recruitment tip: De kracht van de juiste functietitel
- **Content:** Zie Trust_First_Email_Campaign.html - Email 4

### Template 5: Tip Salaris Dag 11
- **Naam:** Trust-First Email 5
- **Onderwerp:** Recruitment tip: Het salarisvraagstuk
- **Content:** Zie Trust_First_Email_Campaign.html - Email 5

### Template 6: Tip Opening Dag 14
- **Naam:** Trust-First Email 6
- **Onderwerp:** Recruitment tip: De eerste 6 seconden
- **Content:** Zie Trust_First_Email_Campaign.html - Email 6

### Template 7: Gesprek Aanbod Dag 21
- **Naam:** Trust-First Email 7
- **Onderwerp:** Zullen we eens bellen?
- **Content:** Zie Trust_First_Email_Campaign.html - Email 7

### Template 8: Final Check-in Dag 30
- **Naam:** Trust-First Email 8
- **Onderwerp:** Laatste check - hoe staat het ervoor?
- **Content:** Zie Trust_First_Email_Campaign.html - Email 8

---

## STAP 3: Automations Instellen

### In Pipedrive: Automations > Create automation

---

### Automation 1: Start Sequence + Email 1

**Trigger:** Deal moves to stage "Rapport Verzonden"

**Actions:**
1. Update deal field: "Rapport Verzonden Op" = Current date
2. Update deal field: "Email Sequence Status" = "Actief"
3. Wait: 1 day
4. Send email: Template "Trust-First Email 1"
5. Update deal field: "Laatste Email Verzonden" = "Email 1"

---

### Automation 2: Email 2 (Dag 3)

**Trigger:** Deal field updated

**Conditions:**
- "Email Sequence Status" equals "Actief"
- "Laatste Email Verzonden" equals "Email 1"
- "Rapport Verzonden Op" is 2 or more days ago

**Actions:**
1. Wait: Until "Rapport Verzonden Op" + 3 days
2. Send email: Template "Trust-First Email 2"
3. Update deal field: "Laatste Email Verzonden" = "Email 2"

---

### Automation 3: Email 3 (Dag 5)

**Trigger:** Deal field updated

**Conditions:**
- "Email Sequence Status" equals "Actief"
- "Laatste Email Verzonden" equals "Email 2"

**Actions:**
1. Wait: 2 days
2. Send email: Template "Trust-First Email 3"
3. Update deal field: "Laatste Email Verzonden" = "Email 3"

---

### Automation 4: Email 4 (Dag 8)

**Trigger:** Deal field updated

**Conditions:**
- "Email Sequence Status" equals "Actief"
- "Laatste Email Verzonden" equals "Email 3"

**Actions:**
1. Wait: 3 days
2. Send email: Template "Trust-First Email 4"
3. Update deal field: "Laatste Email Verzonden" = "Email 4"

---

### Automation 5: Email 5 (Dag 11)

**Trigger:** Deal field updated

**Conditions:**
- "Email Sequence Status" equals "Actief"
- "Laatste Email Verzonden" equals "Email 4"

**Actions:**
1. Wait: 3 days
2. Send email: Template "Trust-First Email 5"
3. Update deal field: "Laatste Email Verzonden" = "Email 5"

---

### Automation 6: Email 6 (Dag 14)

**Trigger:** Deal field updated

**Conditions:**
- "Email Sequence Status" equals "Actief"
- "Laatste Email Verzonden" equals "Email 5"

**Actions:**
1. Wait: 3 days
2. Send email: Template "Trust-First Email 6"
3. Update deal field: "Laatste Email Verzonden" = "Email 6"

---

### Automation 7: Email 7 (Dag 21)

**Trigger:** Deal field updated

**Conditions:**
- "Email Sequence Status" equals "Actief"
- "Laatste Email Verzonden" equals "Email 6"

**Actions:**
1. Wait: 7 days
2. Send email: Template "Trust-First Email 7"
3. Update deal field: "Laatste Email Verzonden" = "Email 7"

---

### Automation 8: Email 8 - Final (Dag 30)

**Trigger:** Deal field updated

**Conditions:**
- "Email Sequence Status" equals "Actief"
- "Laatste Email Verzonden" equals "Email 7"

**Actions:**
1. Wait: 9 days
2. Send email: Template "Trust-First Email 8"
3. Update deal field: "Laatste Email Verzonden" = "Email 8"
4. Update deal field: "Email Sequence Status" = "Voltooid"

---

### Automation 9: Stop bij Reply/Conversie

**Trigger:** Email opened OR Email reply received OR Deal moves to "Gesprek Gepland"

**Actions:**
1. Update deal field: "Email Sequence Status" = "Gepauzeerd"

*(Optioneel: maak aparte automation voor replies vs conversies)*

---

## STAP 4: Pipeline Stages

### Aanbevolen Deal Stages:

```
Pipeline: Kandidatentekort Klanten

Stage 1: Nieuwe Aanvraag
Stage 2: In Analyse
Stage 3: Rapport Verzonden    <-- TRIGGER VOOR EMAIL SEQUENCE
Stage 4: In Contact (replied)
Stage 5: Gesprek Gepland
Stage 6: Klant (won)
Stage 7: Geen Interesse (lost)
```

---

## Merge Fields Referentie

Gebruik in je email templates:

| Merge Field | Wat het toont |
|-------------|---------------|
| `{person.first_name}` | Voornaam van contact |
| `{person.name}` | Volledige naam |
| `{deal.title}` | Deal titel (functienaam) |
| `{organization.name}` | Bedrijfsnaam |
| `{deal.Rapport Verzonden Op}` | Custom field datum |

---

## Timing Overzicht

```
DAG 0:  Rapport verzonden (handmatig/automatisch)
        |
DAG 1:  Email 1 - "Even checken - alles goed ontvangen?"
        |
DAG 3:  Email 2 - "Is het gelukt om de aanpassingen door te voeren?"
        |
DAG 5:  Email 3 - "Benieuwd - merk je al verschil?"
        |
DAG 8:  Email 4 - "Recruitment tip: De kracht van de juiste functietitel"
        |
DAG 11: Email 5 - "Recruitment tip: Het salarisvraagstuk"
        |
DAG 14: Email 6 - "Recruitment tip: De eerste 6 seconden"
        |
DAG 21: Email 7 - "Zullen we eens bellen?"
        |
DAG 30: Email 8 - "Laatste check - hoe staat het ervoor?"
        |
        [SEQUENCE VOLTOOID]
```

---

## Tips voor Succes

1. **Houd het persoonlijk**: Geen fancy HTML, gewoon tekst-emails die eruitzien als echt geschreven
2. **Reply monitoring**: Check dagelijks op replies - die zijn goud waard
3. **Pauzeer bij interesse**: Zodra iemand reageert, stop de sequence en ga persoonlijk verder
4. **Test eerst**: Stuur de sequence eerst naar jezelf om timing en content te checken
5. **Analyseer na 30 dagen**: Welke emails krijgen de meeste opens/replies?

---

*Laatst bijgewerkt: November 2024*
*Campagne: Trust-First Nurture v1.0*
