#!/usr/bin/env python3
"""
Pipedrive Recruitment APK Email Campaign Configuration Script
Configures custom fields, deal stages, and email templates via Pipedrive API

Pipeline: Recruitment APK (id: 2)
Typeform: https://form.typeform.com/to/cuGe3IEC
Website: www.recruitmentapk.nl
"""

import requests
import json
import os
from datetime import datetime

# Pipedrive API configuration
PIPEDRIVE_API_TOKEN = os.environ.get('PIPEDRIVE_API_TOKEN', '57720aa8b264cb9060c9dd5af8ae0c096dbbebb5')
PIPEDRIVE_BASE_URL = 'https://api.pipedrive.com/v1'

# Target pipeline
PIPELINE_NAME = "Recruitment APK"
PIPELINE_ID = 2  # Known ID from existing setup

# Deal stages to configure
DEAL_STAGES = [
    {"name": "Nieuw", "order_nr": 1, "rotten_flag": True, "rotten_days": 3},
    {"name": "APK in Behandeling", "order_nr": 2, "rotten_flag": True, "rotten_days": 2},
    {"name": "APK Verzonden", "order_nr": 3, "rotten_flag": True, "rotten_days": 7},
    {"name": "Follow-up", "order_nr": 4, "rotten_flag": True, "rotten_days": 30},
    {"name": "Gesprek Gepland", "order_nr": 5, "rotten_flag": True, "rotten_days": 7},
    {"name": "Gewonnen", "order_nr": 6, "rotten_flag": False, "rotten_days": None},
    {"name": "Verloren", "order_nr": 7, "rotten_flag": False, "rotten_days": None},
]

# Custom fields to create for APK email sequence tracking
CUSTOM_FIELDS = [
    {
        "name": "APK Verzonden Op",
        "field_type": "date",
        "add_visible_flag": True
    },
    {
        "name": "APK Score",
        "field_type": "double",  # Number field
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
    },
    {
        "name": "Typeform Response ID",
        "field_type": "varchar",  # Text field
        "add_visible_flag": True
    },
    {
        "name": "Verbeterpunten",
        "field_type": "text",  # Large text field
        "add_visible_flag": True
    }
]

# Email templates for Recruitment APK pipeline
EMAIL_TEMPLATES = [
    {
        "name": "APK Email 1 - APK Ontvangen Dag 1",
        "subject": "Je Recruitment APK - alles goed ontvangen?",
        "content": """Hoi {person.first_name},

Gisteren stuurde ik je de Recruitment APK - de complete analyse van jullie wervingsproces.

Even een snelle check: is alles goed aangekomen?

Als je vragen hebt over je score of de aanbevelingen - reply gerust op deze mail. Ik help je graag verder.

Groeten,
Wouter
recruitmentapk.nl

PS: Geen verkooppraatje vandaag - gewoon even checken of alles werkt."""
    },
    {
        "name": "APK Email 2 - Al Bekeken Dag 3",
        "subject": "Heb je de APK al kunnen bekijken?",
        "content": """Hoi {person.first_name},

Even nieuwsgierig: heb je de Recruitment APK al kunnen doornemen?

Ik hoor het graag als je ergens tegenaan loopt, bijvoorbeeld:

- Vragen over je recruitment maturity score?
- Onduidelijkheid over de verbeterpunten?
- Hulp nodig bij de prioritering?

Geen probleem - reply gewoon en ik denk met je mee.

Groeten,
Wouter

Tip: De meeste bedrijven focussen eerst op de "quick wins" uit de APK - de punten die snel resultaat opleveren."""
    },
    {
        "name": "APK Email 3 - Eerste Stappen Dag 5",
        "subject": "Ben je al ergens mee gestart?",
        "content": """Hoi {person.first_name},

Het is nu een paar dagen geleden sinds je de Recruitment APK hebt ontvangen.

Ik ben oprecht benieuwd: ben je al ergens mee aan de slag gegaan?

---
MAG IK JE IETS VRAGEN?

Als je 2 minuten hebt, zou je me kunnen vertellen:

1. Heb je de APK intern al gedeeld?
2. Welk verbeterpunt pak je als eerste aan?
3. Wat vond je het meest verrassend aan de uitkomst?

Jouw feedback helpt me om de APK te verbeteren voor andere bedrijven.
---

Reply gewoon op deze mail - ik lees alles persoonlijk.

Alvast bedankt,
Wouter

Nog niet aan toegekomen? Geen probleem - de APK blijft relevant. Bewaar hem voor wanneer het wel past."""
    },
    {
        "name": "APK Email 4 - Tip Time-to-Hire Dag 8",
        "subject": "Recruitment tip: Time-to-hire halveren",
        "content": """Hoi {person.first_name},

Deze week deel ik een tip die veel bedrijven over het hoofd zien:

---
JE TIME-TO-HIRE ZIT NIET IN DE SELECTIE, MAAR IN DE VOORKANT

De gemiddelde time-to-hire in Nederland is 42 dagen. Maar wist je dat 60% van die tijd opgaat aan het vinden van kandidaten - niet aan het selecteren?

Wat de snelste bedrijven doen:
- Talent pools opbouwen VOOR de vacature ontstaat
- Hiring managers trainen op snelle besluitvorming
- Standaard response binnen 48 uur naar kandidaten

Quick win:
Meet eens hoelang kandidaten wachten tussen sollicitatie en eerste contact. Als dat meer dan 5 dagen is, verlies je de beste mensen.
---

Hoe snel schakelt jouw organisatie na een sollicitatie?

Succes deze week,
Wouter

Volgende week: Waarom de candidate experience je employer brand bepaalt"""
    },
    {
        "name": "APK Email 5 - Tip Candidate Experience Dag 11",
        "subject": "Recruitment tip: Candidate experience als geheim wapen",
        "content": """Hoi {person.first_name},

"We hebben een negatieve Glassdoor review gekregen van een afgewezen kandidaat."

Dat hoor ik vaker dan je denkt. Hier is wat de data zegt:

---
IMPACT VAN CANDIDATE EXPERIENCE:

- 72% deelt slechte ervaringen met anderen
- 52% stopt met kopen bij het bedrijf na slechte ervaring
- 78% zou opnieuw solliciteren bij goede afwijzing

Bron: Talent Board 2024
---

De oplossing is simpeler dan je denkt:

- Stuur ALTIJD een persoonlijke afwijzing (geen standaardmail)
- Geef binnen 1 week feedback na het laatste gesprek
- Vraag afgewezen kandidaten om feedback over het proces
- Behandel kandidaten zoals je klanten behandelt

Groeten,
Wouter

Vragen? Reply gewoon op deze mail."""
    },
    {
        "name": "APK Email 6 - Tip Meten Weten Dag 14",
        "subject": "Recruitment tip: Meten = weten",
        "content": """Hoi {person.first_name},

"We weten niet precies waar het misgaat in ons wervingsproces."

Dat is logisch als je niet meet. Maar welke metrics zijn eigenlijk belangrijk?

---
DE 5 RECRUITMENT KPIs DIE ERTOE DOEN:

1. Time-to-hire - Van vacature tot handtekening
2. Quality of hire - Prestatie na 6/12 maanden
3. Cost per hire - Totale kosten per aanname
4. Source effectiveness - Welke kanalen leveren?
5. Candidate satisfaction - NPS van sollicitanten

Start simpel:
Meet eerst alleen time-to-hire en source effectiveness. Dat geeft al 80% van de inzichten.
---

Welke van deze 5 meet jouw organisatie al? Reply en laat het me weten.

Tot volgende week,
Wouter

Dit was de laatste tip in deze serie. Vond je ze nuttig? Laat het me weten."""
    },
    {
        "name": "APK Email 7 - Gesprek Aanbod Dag 21",
        "subject": "Zullen we je APK samen doornemen?",
        "content": """Hoi {person.first_name},

Het is nu drie weken geleden dat je de Recruitment APK ontving.

Ik ben benieuwd: heb je al stappen kunnen zetten op basis van de uitkomsten? Of ligt het rapport nog op de stapel?

---
ZULLEN WE EVEN BELLEN?

Geen verkooppraatje, gewoon een kort gesprek (30 min gratis) om je APK samen door te nemen.

We kunnen het hebben over:
- De belangrijkste verbeterpunten voor {organization.name}
- Quick wins die je direct kunt implementeren
- Hoe je draagvlak krijgt voor recruitment verbeteringen

Plan hier een moment dat jou uitkomt:
https://calendly.com/wouter-arts-/recruitment-apk-review
---

Geen zin of geen tijd? Helemaal prima - reply dan gewoon even met een update. Ik hoor graag hoe het gaat.

Groeten,
Wouter

PS: Ik reageer ook gewoon op een reply - wat jou het makkelijkst is."""
    },
    {
        "name": "APK Email 8 - Final Check-in Dag 30",
        "subject": "Laatste check - hoe staat het met jullie recruitment?",
        "content": """Hoi {person.first_name},

Een maand geleden verstuurde ik de Recruitment APK voor {organization.name}.

Dit is mijn laatste mail in deze serie - daarna laat ik je met rust.

Maar voor ik ga, ben ik nieuwsgierig:

---
HOE STAAT HET ERVOOR?

A. We zijn aan de slag - al verbeteringen doorgevoerd!
B. APK ligt klaar - maar nog geen tijd gehad
C. Recruitment staat even on hold bij ons
D. Ik wil graag sparren - laten we bellen

Reply met A, B, C of D (of vertel gewoon je verhaal)
---

Hoe dan ook - succes met jullie recruitment. En mocht je in de toekomst weer een APK willen doen, of hulp nodig hebben bij de implementatie, je weet me te vinden.

Groeten,
Wouter
recruitmentapk.nl

---
Contact: warts@recruitin.nl
Nieuwe APK? https://recruitmentapk.nl"""
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
    print("\n   Checking existing deal fields...")
    result = api_request("GET", "dealFields")
    if result and result.get("success"):
        fields = result.get("data", [])
        print(f"   Found {len(fields)} existing fields")
        return {f["name"]: f for f in fields}
    return {}


def create_deal_field(field_config):
    """Create a custom deal field"""
    name = field_config["name"]
    print(f"\n   Creating field: {name}")

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
        print(f"   Created: {name} (key: {field_data.get('key')})")
        return field_data
    else:
        print(f"   Failed to create: {name}")
        if result:
            print(f"   Error: {result.get('error', 'Unknown error')}")
        return None


def get_existing_mail_templates():
    """Get existing email templates"""
    print("\n   Checking existing email templates...")
    result = api_request("GET", "mailbox/mailTemplates")
    if result and result.get("success"):
        templates = result.get("data", [])
        print(f"   Found {len(templates)} existing templates")
        return {t["name"]: t for t in templates}
    return {}


def create_mail_template(template_config):
    """Create an email template"""
    name = template_config["name"]
    print(f"\n   Creating template: {name}")

    data = {
        "name": name,
        "subject": template_config["subject"],
        "content": template_config["content"],
        "shared_flag": 1  # Make template available to all users
    }

    result = api_request("POST", "mailbox/mailTemplates", data)

    if result and result.get("success"):
        template_data = result.get("data", {})
        print(f"   Created: {name} (id: {template_data.get('id')})")
        return template_data
    else:
        print(f"   Failed to create: {name}")
        if result:
            print(f"   Error: {result.get('error', 'Unknown error')}")
        return None


def get_pipelines():
    """Get all pipelines"""
    print("\n   Fetching pipelines...")
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


def create_or_update_stage(pipeline_id, stage_config, existing_stages):
    """Create or update a pipeline stage"""
    stage_name = stage_config["name"]

    # Check if stage exists
    existing_stage = next((s for s in existing_stages if s["name"] == stage_name), None)

    if existing_stage:
        # Update existing stage
        data = {
            "name": stage_name,
            "order_nr": stage_config["order_nr"],
            "rotten_flag": stage_config.get("rotten_flag", False),
        }
        if stage_config.get("rotten_days"):
            data["rotten_days"] = stage_config["rotten_days"]

        result = api_request("PUT", f"stages/{existing_stage['id']}", data)
        if result and result.get("success"):
            print(f"   Updated stage: {stage_name}")
            return result.get("data")
    else:
        # Create new stage
        data = {
            "name": stage_name,
            "pipeline_id": pipeline_id,
            "order_nr": stage_config["order_nr"],
            "rotten_flag": stage_config.get("rotten_flag", False),
        }
        if stage_config.get("rotten_days"):
            data["rotten_days"] = stage_config["rotten_days"]

        result = api_request("POST", "stages", data)
        if result and result.get("success"):
            print(f"   Created stage: {stage_name}")
            return result.get("data")

    return None


def create_test_deal(pipeline_id, stage_id, person_email):
    """Create a test deal for email sequence testing"""
    print(f"\n   Creating test deal...")

    # First create or find person
    person_result = api_request("GET", f"persons/search?term={person_email}&fields=email")
    person_id = None

    if person_result and person_result.get("success"):
        items = person_result.get("data", {}).get("items", [])
        if items:
            person_id = items[0].get("item", {}).get("id")
            print(f"   Found existing person: {person_id}")

    if not person_id:
        # Create new person
        person_data = {
            "name": "Test User APK",
            "email": [{"value": person_email, "primary": True}],
        }
        person_result = api_request("POST", "persons", person_data)
        if person_result and person_result.get("success"):
            person_id = person_result.get("data", {}).get("id")
            print(f"   Created person: {person_id}")

    # Create deal
    deal_data = {
        "title": f"TEST APK - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "pipeline_id": pipeline_id,
        "stage_id": stage_id,
        "person_id": person_id,
    }

    deal_result = api_request("POST", "deals", deal_data)
    if deal_result and deal_result.get("success"):
        deal = deal_result.get("data", {})
        print(f"   Created test deal: {deal.get('title')} (id: {deal.get('id')})")
        return deal

    return None


def send_test_email(deal_id, template_id, to_email):
    """Send a test email using a template"""
    print(f"\n   Sending test email to {to_email}...")

    # Note: Pipedrive doesn't have a direct "send email" API
    # Emails are typically sent through automations or manual actions
    # This function shows the intent - actual sending happens via automation

    print(f"   Test email would be sent using template {template_id}")
    print(f"   To: {to_email}")
    print(f"   Deal ID: {deal_id}")
    print("")
    print("   NOTE: In production, this email will be sent automatically")
    print("   when the deal enters the 'APK Verzonden' stage and the")
    print("   automation is triggered.")

    return True


def main():
    """Main configuration function"""
    print("=" * 70)
    print("PIPEDRIVE RECRUITMENT APK EMAIL CAMPAIGN CONFIGURATION")
    print("=" * 70)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Pipeline: {PIPELINE_NAME}")
    print(f"Typeform: https://form.typeform.com/to/cuGe3IEC")

    # Test API connection
    print("\n" + "=" * 70)
    print("STEP 1: Testing API Connection")
    print("=" * 70)

    test = api_request("GET", "users/me")
    if not test or not test.get("success"):
        print("   API connection failed. Check your API token.")
        return False

    user = test.get("data", {})
    print(f"   Connected as: {user.get('name')} ({user.get('email')})")

    # Get pipelines and find Recruitment APK
    print("\n" + "=" * 70)
    print("STEP 2: Checking Pipeline Configuration")
    print("=" * 70)

    pipelines = get_pipelines()
    apk_pipeline = next((p for p in pipelines if p["name"] == PIPELINE_NAME or p["id"] == PIPELINE_ID), None)

    if not apk_pipeline:
        print(f"   Pipeline '{PIPELINE_NAME}' not found!")
        print("   Please create the pipeline manually in Pipedrive first.")
        return False

    print(f"\n   Found pipeline: {apk_pipeline['name']} (id: {apk_pipeline['id']})")

    # Configure deal stages
    print("\n" + "=" * 70)
    print("STEP 3: Configuring Deal Stages")
    print("=" * 70)

    existing_stages = get_stages(apk_pipeline["id"])
    print(f"\n   Current stages in pipeline:")
    for stage in existing_stages:
        print(f"   - {stage['name']} (id: {stage['id']}, order: {stage.get('order_nr', 'N/A')})")

    print(f"\n   Configuring {len(DEAL_STAGES)} stages...")
    configured_stages = []
    for stage_config in DEAL_STAGES:
        result = create_or_update_stage(apk_pipeline["id"], stage_config, existing_stages)
        if result:
            configured_stages.append(result)

    # Create custom fields
    print("\n" + "=" * 70)
    print("STEP 4: Creating Custom Deal Fields")
    print("=" * 70)

    existing_fields = get_existing_deal_fields()
    created_fields = {}

    for field_config in CUSTOM_FIELDS:
        if field_config["name"] in existing_fields:
            print(f"\n   Field already exists: {field_config['name']}")
            created_fields[field_config["name"]] = existing_fields[field_config["name"]]
        else:
            result = create_deal_field(field_config)
            if result:
                created_fields[field_config["name"]] = result

    # Create email templates
    print("\n" + "=" * 70)
    print("STEP 5: Creating Email Templates")
    print("=" * 70)

    existing_templates = get_existing_mail_templates()
    created_templates = {}

    for template_config in EMAIL_TEMPLATES:
        if template_config["name"] in existing_templates:
            print(f"\n   Template already exists: {template_config['name']}")
            created_templates[template_config["name"]] = existing_templates[template_config["name"]]
        else:
            result = create_mail_template(template_config)
            if result:
                created_templates[template_config["name"]] = result

    # Summary
    print("\n" + "=" * 70)
    print("CONFIGURATION SUMMARY")
    print("=" * 70)

    print(f"\n   Pipeline: {apk_pipeline['name']} (id: {apk_pipeline['id']})")

    print(f"\n   Deal Stages Configured: {len(configured_stages)}")
    for stage in configured_stages:
        print(f"   - {stage.get('name')} (id: {stage.get('id')})")

    print(f"\n   Custom Fields: {len(created_fields)}/{len(CUSTOM_FIELDS)}")
    for name, field in created_fields.items():
        print(f"   - {name}: {field.get('key', 'unknown key')}")

    print(f"\n   Email Templates: {len(created_templates)}/{len(EMAIL_TEMPLATES)}")
    for name, template in created_templates.items():
        print(f"   - {name}: id={template.get('id', 'unknown')}")

    # Test deal creation (optional)
    print("\n" + "=" * 70)
    print("STEP 6: Test Deal Creation (Optional)")
    print("=" * 70)

    create_test = input("\n   Create a test deal? (y/n): ").strip().lower()
    if create_test == 'y':
        test_email = input("   Enter your test email: ").strip()
        if test_email:
            # Find the "APK Verzonden" stage
            apk_stage = next((s for s in configured_stages if s.get("name") == "APK Verzonden"), None)
            if apk_stage:
                test_deal = create_test_deal(apk_pipeline["id"], apk_stage["id"], test_email)
                if test_deal:
                    print(f"\n   Test deal created successfully!")
                    print(f"   Deal ID: {test_deal.get('id')}")
                    print(f"   The email automation should trigger within 1 day")

    # Next steps
    print("\n" + "=" * 70)
    print("NEXT STEPS - MANUAL AUTOMATION SETUP REQUIRED")
    print("=" * 70)
    print("""
   The custom fields and email templates are now configured.

   You still need to manually create the automations in Pipedrive:

   1. Go to Pipedrive > Automations > Create automation

   2. Create 8 email automations (see documentation for details):
      - APK Email 1: Trigger on "APK Verzonden" stage, Wait 1 day
      - APK Email 2-8: Trigger on "Laatste Email" field change

   3. Create stop automations:
      - Stop on reply
      - Stop on stage change to "Gesprek Gepland"

   Full documentation:
   ./projects/recruitment-apk-automation/pipedrive-templates/Pipedrive_Automations_APK_Stap_voor_Stap.md
""")

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
