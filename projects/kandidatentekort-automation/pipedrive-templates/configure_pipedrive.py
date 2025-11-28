#!/usr/bin/env python3
"""
Pipedrive Trust-First Email Campaign Configuration Script
Configures custom fields and email templates via Pipedrive API
"""

import requests
import json
import os
from datetime import datetime

# Pipedrive API configuration
PIPEDRIVE_API_TOKEN = os.environ.get('PIPEDRIVE_API_TOKEN', '57720aa8b264cb9060c9dd5af8ae0c096dbbebb5')
PIPEDRIVE_BASE_URL = 'https://api.pipedrive.com/v1'

# Email templates content
EMAIL_TEMPLATES = [
    {
        "name": "Trust-First Email 1 - Check-in Dag 1",
        "subject": "Even checken - alles goed ontvangen?",
        "content": """Hoi {person.first_name},

Gisteren stuurde ik je de geoptimaliseerde versie van je vacature voor {deal.title}.

Even een snelle check: is alles goed aangekomen?

Als je vragen hebt over de analyse of tips - reply gerust op deze mail. Ik help je graag verder.

Groeten,
Wouter
kandidatentekort.nl

PS: Geen verkooppraatje vandaag - gewoon even checken of alles werkt."""
    },
    {
        "name": "Trust-First Email 2 - Is het gelukt Dag 3",
        "subject": "Is het gelukt om de aanpassingen door te voeren?",
        "content": """Hoi {person.first_name},

Even nieuwsgierig: is het gelukt om de verbeterde vacaturetekst te plaatsen?

Ik hoor het graag als je ergens tegenaan loopt, bijvoorbeeld:

- Intern akkoord nodig voor de nieuwe tekst?
- Technische problemen met het platform?
- Twijfels over bepaalde aanpassingen?

Geen probleem - reply gewoon en ik denk met je mee.

Groeten,
Wouter

Tip: De meeste recruiters zien binnen 48 uur na plaatsing al verschil in response."""
    },
    {
        "name": "Trust-First Email 3 - Resultaten Dag 5",
        "subject": "Benieuwd - merk je al verschil?",
        "content": """Hoi {person.first_name},

Het is nu een paar dagen geleden sinds je de verbeterde vacature voor {deal.title} hebt ontvangen.

Ik ben oprecht benieuwd: merk je al verschil in de reacties?

---
MAG IK JE IETS VRAGEN?

Als je 2 minuten hebt, zou je me kunnen vertellen:

1. Heb je de nieuwe tekst al live gezet?
2. Zo ja, zie je verschil in aantal/kwaliteit reacties?
3. Wat vond je het meest nuttig aan de analyse?

Jouw feedback helpt me om de service te verbeteren voor andere recruiters.
---

Reply gewoon op deze mail - ik lees alles persoonlijk.

Alvast bedankt,
Wouter

Geen resultaten? Geen probleem - soms duurt het even. Laat het me weten en ik denk mee."""
    },
    {
        "name": "Trust-First Email 4 - Tip Functietitel Dag 8",
        "subject": "Recruitment tip: De kracht van de juiste functietitel",
        "content": """Hoi {person.first_name},

Deze week deel ik een tip die veel recruiters over het hoofd zien:

---
DE FUNCTIETITEL BEPAALT 70% VAN JE ZICHTBAARHEID

Kandidaten zoeken op specifieke termen. Een creatieve titel als "Teamspeler Extraordinaire" klinkt leuk, maar niemand zoekt daarop.

Wat werkt:
- Gebruik de exacte term die kandidaten googlen
- Voeg niveau toe (Junior/Medior/Senior)
- Houd het onder 60 karakters

Voorbeeld:
"Commerciele Binnendienst Medewerker" krijgt 3x meer views dan "Sales Ninja"
---

Heb je al gedacht aan het A/B testen van je functietitels? Veel jobboards bieden deze optie gratis.

Succes deze week,
Wouter

Volgende week: Waarom salaris vermelden je 35% meer sollicitaties oplevert"""
    },
    {
        "name": "Trust-First Email 5 - Tip Salaris Dag 11",
        "subject": "Recruitment tip: Het salarisvraagstuk",
        "content": """Hoi {person.first_name},

"Salaris: marktconform" - de meest waardeloze zin in recruitment.

Hier is wat de data zegt:

---
VACATURES MET SALARISINDICATIE KRIJGEN:

+ 35% meer sollicitaties
+ 27% hogere kwaliteit kandidaten
+ 40% snellere time-to-hire

Bron: Indeed Hiring Lab 2024
---

Maar wat als je het niet mag vermelden?

Alternatieven die ook werken:

- "Salarisindicatie: vanaf EUR 3.500 bruto/maand"
- "Indicatie: schaal 8-10 CAO [naam]"
- "Budget: EUR 45.000 - 55.000 op jaarbasis"

Zelfs een range is beter dan niets.

Groeten,
Wouter

Vragen? Reply gewoon op deze mail."""
    },
    {
        "name": "Trust-First Email 6 - Tip Opening Dag 14",
        "subject": "Recruitment tip: De eerste 6 seconden",
        "content": """Hoi {person.first_name},

Wist je dat kandidaten gemiddeld 6 seconden besteden aan de eerste scan van een vacature?

In die 6 seconden beslissen ze of ze doorlezen of wegklikken.

---
WAT ZE SCANNEN:

1. Functietitel (check)
2. Salaris (als het er staat)
3. De eerste 2-3 zinnen
4. Locatie
5. Logo/bedrijfsnaam

HET PROBLEEM:
90% van de vacatures begint met "Wij zoeken een enthousiaste..."

DE OPLOSSING:
Start met een vraag of een bold statement.

Bijvoorbeeld:
- "Frustreert het je dat je klanten niet snel genoeg geholpen worden?"
- "Dit is geen gewone sales functie."
- "EUR 4.500 bruto. Fulltime. Rotterdam."
---

Pak eens een van je huidige vacatures erbij. Hoe is de opening?

Tot volgende week,
Wouter

Dit was de laatste tip in deze serie. Vond je ze nuttig? Laat het me weten."""
    },
    {
        "name": "Trust-First Email 7 - Gesprek Aanbod Dag 21",
        "subject": "Zullen we eens bellen?",
        "content": """Hoi {person.first_name},

Het is nu drie weken geleden dat je de vacature-analyse ontving.

Ik ben benieuwd hoe het gaat met je werving. Heb je de kandidaat al gevonden? Of loop je nog ergens tegenaan?

---
ZULLEN WE EVEN BELLEN?

Geen verkooppraatje, gewoon een kort gesprek (15 min) om te kijken of ik je ergens mee kan helpen.

We kunnen het hebben over:
- De resultaten van je huidige vacature
- Andere openstaande posities
- Recruitment uitdagingen waar je tegenaan loopt

Plan hier een moment dat jou uitkomt:
https://calendly.com/wouter-arts-/vacature-analyse-advies
---

Geen zin of geen tijd? Helemaal prima - reply dan gewoon even met een update. Ik hoor graag hoe het gaat.

Groeten,
Wouter

PS: Ik reageer ook gewoon op een reply - wat jou het makkelijkst is."""
    },
    {
        "name": "Trust-First Email 8 - Final Check-in Dag 30",
        "subject": "Laatste check - hoe staat het ervoor?",
        "content": """Hoi {person.first_name},

Een maand geleden verstuurde ik de analyse voor je {deal.title} vacature.

Dit is mijn laatste mail in deze serie - daarna laat ik je met rust.

Maar voor ik ga, ben ik nieuwsgierig:

---
HOE IS HET GEGAAN?

A. Kandidaat gevonden - top!
B. Nog bezig - maar gaat goed
C. Vacature on hold gezet
D. Hulp nodig - laten we bellen

Reply met A, B, C of D (of vertel gewoon je verhaal)
---

Hoe dan ook - succes met je recruitment. En mocht je in de toekomst weer een vacature willen laten checken, je weet me te vinden.

Groeten,
Wouter
kandidatentekort.nl

---
Contact: warts@recruitin.nl
Nieuwe vacature? https://kandidatentekort.nl"""
    }
]

# Custom fields to create for email sequence tracking
CUSTOM_FIELDS = [
    {
        "name": "Rapport Verzonden Op",
        "field_type": "date",
        "add_visible_flag": True
    },
    {
        "name": "Email Sequence Status",
        "field_type": "enum",
        "options": ["Actief", "Gepauzeerd", "Voltooid"],
        "add_visible_flag": True
    },
    {
        "name": "Laatste Email Verzonden",
        "field_type": "enum",
        "options": ["Email 1", "Email 2", "Email 3", "Email 4", "Email 5", "Email 6", "Email 7", "Email 8"],
        "add_visible_flag": True
    }
]


def api_request(method, endpoint, data=None):
    """Make API request to Pipedrive"""
    url = f"{PIPEDRIVE_BASE_URL}/{endpoint}"
    params = {"api_token": PIPEDRIVE_API_TOKEN}

    try:
        if method == "GET":
            response = requests.get(url, params=params)
        elif method == "POST":
            response = requests.post(url, params=params, json=data)
        elif method == "PUT":
            response = requests.put(url, params=params, json=data)
        elif method == "DELETE":
            response = requests.delete(url, params=params)

        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return None


def get_existing_deal_fields():
    """Get existing deal custom fields"""
    print("\n📋 Checking existing deal fields...")
    result = api_request("GET", "dealFields")
    if result and result.get("success"):
        fields = result.get("data", [])
        print(f"   Found {len(fields)} existing fields")
        return {f["name"]: f for f in fields}
    return {}


def create_deal_field(field_config):
    """Create a custom deal field"""
    name = field_config["name"]
    print(f"\n➕ Creating field: {name}")

    data = {
        "name": name,
        "field_type": field_config["field_type"],
        "add_visible_flag": field_config.get("add_visible_flag", True)
    }

    # For enum fields, add options
    if field_config["field_type"] == "enum" and "options" in field_config:
        data["options"] = [{"label": opt} for opt in field_config["options"]]

    result = api_request("POST", "dealFields", data)

    if result and result.get("success"):
        field_data = result.get("data", {})
        print(f"   ✅ Created: {name} (key: {field_data.get('key')})")
        return field_data
    else:
        print(f"   ❌ Failed to create: {name}")
        if result:
            print(f"   Error: {result.get('error', 'Unknown error')}")
        return None


def get_existing_mail_templates():
    """Get existing email templates"""
    print("\n📧 Checking existing email templates...")
    result = api_request("GET", "mailbox/mailTemplates")
    if result and result.get("success"):
        templates = result.get("data", [])
        print(f"   Found {len(templates)} existing templates")
        return {t["name"]: t for t in templates}
    return {}


def create_mail_template(template_config):
    """Create an email template"""
    name = template_config["name"]
    print(f"\n📝 Creating template: {name}")

    data = {
        "name": name,
        "subject": template_config["subject"],
        "content": template_config["content"],
        "shared_flag": 1  # Make template available to all users
    }

    result = api_request("POST", "mailbox/mailTemplates", data)

    if result and result.get("success"):
        template_data = result.get("data", {})
        print(f"   ✅ Created: {name} (id: {template_data.get('id')})")
        return template_data
    else:
        print(f"   ❌ Failed to create: {name}")
        if result:
            print(f"   Error: {result.get('error', 'Unknown error')}")
        return None


def get_pipelines():
    """Get all pipelines"""
    print("\n🔄 Fetching pipelines...")
    result = api_request("GET", "pipelines")
    if result and result.get("success"):
        pipelines = result.get("data", [])
        for p in pipelines:
            print(f"   - {p['name']} (id: {p['id']})")
        return pipelines
    return []


def get_stages(pipeline_id):
    """Get stages for a pipeline"""
    result = api_request("GET", f"stages?pipeline_id={pipeline_id}")
    if result and result.get("success"):
        return result.get("data", [])
    return []


def main():
    """Main configuration function"""
    print("=" * 60)
    print("PIPEDRIVE TRUST-FIRST EMAIL CAMPAIGN CONFIGURATION")
    print("=" * 60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Test API connection
    print("\n🔌 Testing API connection...")
    test = api_request("GET", "users/me")
    if not test or not test.get("success"):
        print("❌ API connection failed. Check your API token.")
        return False

    user = test.get("data", {})
    print(f"   ✅ Connected as: {user.get('name')} ({user.get('email')})")

    # Get existing fields
    existing_fields = get_existing_deal_fields()

    # Create custom fields if they don't exist
    print("\n" + "=" * 60)
    print("CREATING CUSTOM DEAL FIELDS")
    print("=" * 60)

    created_fields = {}
    for field_config in CUSTOM_FIELDS:
        if field_config["name"] in existing_fields:
            print(f"\n⏭️  Field already exists: {field_config['name']}")
            created_fields[field_config["name"]] = existing_fields[field_config["name"]]
        else:
            result = create_deal_field(field_config)
            if result:
                created_fields[field_config["name"]] = result

    # Create email templates
    print("\n" + "=" * 60)
    print("CREATING EMAIL TEMPLATES")
    print("=" * 60)

    existing_templates = get_existing_mail_templates()
    created_templates = {}

    for template_config in EMAIL_TEMPLATES:
        if template_config["name"] in existing_templates:
            print(f"\n⏭️  Template already exists: {template_config['name']}")
            created_templates[template_config["name"]] = existing_templates[template_config["name"]]
        else:
            result = create_mail_template(template_config)
            if result:
                created_templates[template_config["name"]] = result

    # Show pipeline info
    print("\n" + "=" * 60)
    print("PIPELINE INFORMATION")
    print("=" * 60)

    pipelines = get_pipelines()
    for pipeline in pipelines:
        stages = get_stages(pipeline["id"])
        print(f"\n📊 Pipeline: {pipeline['name']}")
        for stage in stages:
            print(f"   └─ {stage['name']} (id: {stage['id']})")

    # Summary
    print("\n" + "=" * 60)
    print("CONFIGURATION COMPLETE")
    print("=" * 60)

    print(f"\n✅ Custom Fields: {len(created_fields)}/{len(CUSTOM_FIELDS)}")
    for name, field in created_fields.items():
        print(f"   - {name}: {field.get('key', 'unknown key')}")

    print(f"\n✅ Email Templates: {len(created_templates)}/{len(EMAIL_TEMPLATES)}")
    for name, template in created_templates.items():
        print(f"   - {name}: id={template.get('id', 'unknown')}")

    print("\n" + "=" * 60)
    print("NEXT STEPS - MANUAL CONFIGURATION REQUIRED")
    print("=" * 60)
    print("""
1. Ga naar Pipedrive > Automations > Create automation

2. Maak automation voor elke email:

   AUTOMATION 1 (Email 1 - Dag 1):
   - Trigger: Deal moves to "Rapport Verzonden" stage
   - Action 1: Update field "Rapport Verzonden Op" = Today
   - Action 2: Update field "Email Sequence Status" = "Actief"
   - Action 3: Wait 1 day
   - Action 4: Send email using template "Trust-First Email 1"
   - Action 5: Update field "Laatste Email Verzonden" = "Email 1"

   AUTOMATION 2-8: Vergelijkbaar met delays van 3, 5, 8, 11, 14, 21, 30 dagen

3. Maak stop-automation:
   - Trigger: Deal field "Email Sequence Status" changes
   - Condition: New value = "Gepauzeerd" OR "Voltooid"
   - Action: Stop all running automations for this deal

Zie Pipedrive_Automation_Setup.md voor gedetailleerde instructies.
""")

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
