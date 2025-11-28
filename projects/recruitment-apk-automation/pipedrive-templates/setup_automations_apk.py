#!/usr/bin/env python3
"""
Pipedrive Recruitment APK - Complete Automation Setup Script

This script:
1. Creates a test deal with linked person
2. Sends test emails using the created templates
3. Provides step-by-step automation setup instructions

Since Pipedrive Automations cannot be created via API, this script
helps test the email templates and provides exact setup steps.
"""

import requests
import json
import os
import time
from datetime import datetime, timedelta

# Pipedrive API configuration
PIPEDRIVE_API_TOKEN = os.environ.get('PIPEDRIVE_API_TOKEN', '57720aa8b264cb9060c9dd5af8ae0c096dbbebb5')
PIPEDRIVE_BASE_URL = 'https://api.pipedrive.com/v1'

# Pipeline and Stage IDs (from previous configuration)
PIPELINE_ID = 2  # Recruitment APK
STAGE_APK_VERZONDEN = 108  # Stage where email sequence starts

# Email template IDs (created in previous run)
EMAIL_TEMPLATES = {
    1: {"id": 63, "name": "APK Email 1 - APK Ontvangen Dag 1", "day": 1},
    2: {"id": 64, "name": "APK Email 2 - Al Bekeken Dag 3", "day": 3},
    3: {"id": 65, "name": "APK Email 3 - Eerste Stappen Dag 5", "day": 5},
    4: {"id": 66, "name": "APK Email 4 - Tip Time-to-Hire Dag 8", "day": 8},
    5: {"id": 67, "name": "APK Email 5 - Tip Candidate Experience Dag 11", "day": 11},
    6: {"id": 68, "name": "APK Email 6 - Tip Meten Weten Dag 14", "day": 14},
    7: {"id": 69, "name": "APK Email 7 - Gesprek Aanbod Dag 21", "day": 21},
    8: {"id": 70, "name": "APK Email 8 - Final Check-in Dag 30", "day": 30},
}

# Custom field keys (from previous configuration)
FIELD_KEYS = {
    "apk_verzonden_op": "7f23d557432ba403b5534be430151b827384ec43",
    "apk_score": "b0d1e96af884d111b66f812ee4293735393f1624",
    "email_sequence_status": "22d33c7f119119e178f391a272739c571cf2e29b",
    "laatste_email": "753f37a1abc8e161c7982c1379a306b21fae1bab",
    "typeform_response_id": "d3b5fc1d2cb519aac33d381bc3806c5c5fef734e",
    "verbeterpunten": "1f61f3dc8f0d5396c12eaa713c62b2ad1d71f794",
}


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

        if response.status_code == 200 or response.status_code == 201:
            return response.json()
        else:
            print(f"   API Error {response.status_code}: {response.text[:200]}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"   Request Error: {e}")
        return None


def find_or_create_person(email, name):
    """Find existing person or create new one"""
    # Search for existing person
    result = api_request("GET", f"persons/search?term={email}&fields=email")
    if result and result.get("success"):
        items = result.get("data", {}).get("items", [])
        if items:
            person_id = items[0].get("item", {}).get("id")
            print(f"   Found existing person: {name} (id: {person_id})")
            return person_id

    # Create new person
    person_data = {
        "name": name,
        "email": [{"value": email, "primary": True}],
    }
    result = api_request("POST", "persons", person_data)
    if result and result.get("success"):
        person_id = result.get("data", {}).get("id")
        print(f"   Created new person: {name} (id: {person_id})")
        return person_id

    return None


def find_or_create_organization(name):
    """Find existing organization or create new one"""
    # Search for existing org
    result = api_request("GET", f"organizations/search?term={name}")
    if result and result.get("success"):
        items = result.get("data", {}).get("items", [])
        if items:
            org_id = items[0].get("item", {}).get("id")
            print(f"   Found existing organization: {name} (id: {org_id})")
            return org_id

    # Create new organization
    org_data = {"name": name}
    result = api_request("POST", "organizations", org_data)
    if result and result.get("success"):
        org_id = result.get("data", {}).get("id")
        print(f"   Created new organization: {name} (id: {org_id})")
        return org_id

    return None


def create_test_deal(person_id, org_id, test_name):
    """Create a test deal with all custom fields set"""
    today = datetime.now().strftime("%Y-%m-%d")

    deal_data = {
        "title": f"TEST APK - {test_name} - {datetime.now().strftime('%H:%M')}",
        "pipeline_id": PIPELINE_ID,
        "stage_id": STAGE_APK_VERZONDEN,
        "person_id": person_id,
        "org_id": org_id,
        # Custom fields
        FIELD_KEYS["apk_verzonden_op"]: today,
        FIELD_KEYS["apk_score"]: 72,
        FIELD_KEYS["email_sequence_status"]: "Actief",
        FIELD_KEYS["verbeterpunten"]: "1. Time-to-hire verbeteren\n2. Candidate experience optimaliseren\n3. Recruitment KPIs implementeren",
    }

    result = api_request("POST", "deals", deal_data)
    if result and result.get("success"):
        deal = result.get("data", {})
        print(f"   Created test deal: {deal.get('title')} (id: {deal.get('id')})")
        return deal

    return None


def get_email_template_content(template_id):
    """Get email template content from Pipedrive"""
    result = api_request("GET", f"mailbox/mailTemplates/{template_id}")
    if result and result.get("success"):
        return result.get("data", {})
    return None


def send_email_via_pipedrive(deal_id, person_id, template_id, to_email):
    """
    Send email using Pipedrive's mail API
    Note: This requires email sync to be enabled in Pipedrive
    """
    # Get template content
    template = get_email_template_content(template_id)
    if not template:
        print(f"   Could not get template {template_id}")
        return False

    # Prepare email data
    email_data = {
        "subject": template.get("subject", "Test Email"),
        "body": template.get("content", "Test content"),
        "to": [{"email_address": to_email}],
        "deal_id": deal_id,
    }

    # Send via mail messages API
    result = api_request("POST", "mailbox/mailMessages", email_data)
    if result and result.get("success"):
        print(f"   Email sent successfully!")
        return True
    else:
        print(f"   Note: Direct email sending requires email sync. Use Pipedrive UI to send.")
        return False


def update_deal_field(deal_id, field_key, value):
    """Update a custom field on a deal"""
    data = {field_key: value}
    result = api_request("PUT", f"deals/{deal_id}", data)
    if result and result.get("success"):
        return True
    return False


def print_automation_setup_instructions():
    """Print detailed automation setup instructions"""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║          PIPEDRIVE AUTOMATION SETUP - RECRUITMENT APK PIPELINE               ║
╚══════════════════════════════════════════════════════════════════════════════╝

Ga naar: https://app.pipedrive.com/automations

══════════════════════════════════════════════════════════════════════════════
AUTOMATION 1: Start Sequence + Email 1 (Dag 1)
══════════════════════════════════════════════════════════════════════════════

1. Klik "+ Create automation"
2. Naam: "APK Email 1 - Start Sequence"

TRIGGER:
   Type: "Deal enters a stage"
   Pipeline: "Recruitment APK"
   Stage: "APK Verzonden"

ACTIONS:
   Action 1: Update deal
      → Field: "APK Verzonden Op"
      → Value: "Trigger date"

   Action 2: Update deal
      → Field: "Email Sequence Status"
      → Value: "Actief"

   Action 3: Wait
      → Duration: 1 day

   Action 4: Send email
      → To: Person linked to deal
      → Template: "APK Email 1 - APK Ontvangen Dag 1" (id: 63)

   Action 5: Update deal
      → Field: "Laatste Email Verzonden"
      → Value: "Email 1"

   Action 6: Move deal
      → Stage: "Follow-up"

3. Klik "Save" en zet "Active" aan

══════════════════════════════════════════════════════════════════════════════
AUTOMATION 2: Email 2 (Dag 3)
══════════════════════════════════════════════════════════════════════════════

1. Klik "+ Create automation"
2. Naam: "APK Email 2 - Dag 3"

TRIGGER:
   Type: "Deal field is updated"
   Field: "Laatste Email Verzonden"
   Condition: "changed to" → "Email 1"

CONDITIONS:
   Add condition: "Email Sequence Status" equals "Actief"

ACTIONS:
   Action 1: Wait
      → Duration: 2 days

   Action 2: Send email
      → Template: "APK Email 2 - Al Bekeken Dag 3" (id: 64)

   Action 3: Update deal
      → Field: "Laatste Email Verzonden"
      → Value: "Email 2"

══════════════════════════════════════════════════════════════════════════════
AUTOMATION 3: Email 3 (Dag 5)
══════════════════════════════════════════════════════════════════════════════

TRIGGER: "Laatste Email Verzonden" changed to "Email 2"
CONDITION: "Email Sequence Status" equals "Actief"
ACTIONS:
   1. Wait: 2 days
   2. Send email: Template id 65
   3. Update "Laatste Email Verzonden" = "Email 3"

══════════════════════════════════════════════════════════════════════════════
AUTOMATION 4: Email 4 (Dag 8)
══════════════════════════════════════════════════════════════════════════════

TRIGGER: "Laatste Email Verzonden" changed to "Email 3"
CONDITION: "Email Sequence Status" equals "Actief"
ACTIONS:
   1. Wait: 3 days
   2. Send email: Template id 66
   3. Update "Laatste Email Verzonden" = "Email 4"

══════════════════════════════════════════════════════════════════════════════
AUTOMATION 5: Email 5 (Dag 11)
══════════════════════════════════════════════════════════════════════════════

TRIGGER: "Laatste Email Verzonden" changed to "Email 4"
CONDITION: "Email Sequence Status" equals "Actief"
ACTIONS:
   1. Wait: 3 days
   2. Send email: Template id 67
   3. Update "Laatste Email Verzonden" = "Email 5"

══════════════════════════════════════════════════════════════════════════════
AUTOMATION 6: Email 6 (Dag 14)
══════════════════════════════════════════════════════════════════════════════

TRIGGER: "Laatste Email Verzonden" changed to "Email 5"
CONDITION: "Email Sequence Status" equals "Actief"
ACTIONS:
   1. Wait: 3 days
   2. Send email: Template id 68
   3. Update "Laatste Email Verzonden" = "Email 6"

══════════════════════════════════════════════════════════════════════════════
AUTOMATION 7: Email 7 (Dag 21)
══════════════════════════════════════════════════════════════════════════════

TRIGGER: "Laatste Email Verzonden" changed to "Email 6"
CONDITION: "Email Sequence Status" equals "Actief"
ACTIONS:
   1. Wait: 7 days
   2. Send email: Template id 69
   3. Update "Laatste Email Verzonden" = "Email 7"

══════════════════════════════════════════════════════════════════════════════
AUTOMATION 8: Email 8 - Final (Dag 30)
══════════════════════════════════════════════════════════════════════════════

TRIGGER: "Laatste Email Verzonden" changed to "Email 7"
CONDITION: "Email Sequence Status" equals "Actief"
ACTIONS:
   1. Wait: 9 days
   2. Send email: Template id 70
   3. Update "Laatste Email Verzonden" = "Email 8"
   4. Update "Email Sequence Status" = "Voltooid"

══════════════════════════════════════════════════════════════════════════════
AUTOMATION 9: Stop bij Gesprek Gepland
══════════════════════════════════════════════════════════════════════════════

TRIGGER: "Deal enters stage" → "Gesprek Gepland"
ACTIONS:
   1. Update "Email Sequence Status" = "Gepauzeerd"

══════════════════════════════════════════════════════════════════════════════
AUTOMATION 10: Stop bij Won/Lost
══════════════════════════════════════════════════════════════════════════════

TRIGGER: "Deal enters stage" → "Gewonnen" OR "Verloren"
ACTIONS:
   1. Update "Email Sequence Status" = "Voltooid"

══════════════════════════════════════════════════════════════════════════════

TIMING OVERZICHT:
─────────────────
Dag 0:  Deal → "APK Verzonden" stage (trigger automation 1)
Dag 1:  Email 1 verzonden
Dag 3:  Email 2 verzonden (+2 dagen)
Dag 5:  Email 3 verzonden (+2 dagen)
Dag 8:  Email 4 verzonden (+3 dagen)
Dag 11: Email 5 verzonden (+3 dagen)
Dag 14: Email 6 verzonden (+3 dagen)
Dag 21: Email 7 verzonden (+7 dagen)
Dag 30: Email 8 verzonden (+9 dagen) → Sequence voltooid

══════════════════════════════════════════════════════════════════════════════
""")


def main():
    print("=" * 70)
    print("RECRUITMENT APK - EMAIL AUTOMATION TEST & SETUP")
    print("=" * 70)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Test API connection
    print("\n[1] Testing API connection...")
    test = api_request("GET", "users/me")
    if not test or not test.get("success"):
        print("   API connection failed!")
        return False

    user = test.get("data", {})
    print(f"   Connected as: {user.get('name')} ({user.get('email')})")

    # Ask for test configuration
    print("\n[2] Test Deal Setup")
    print("-" * 40)

    create_test = input("\nCreate a test deal and send test email? (y/n): ").strip().lower()

    if create_test == 'y':
        test_email = input("Enter test email address: ").strip()
        test_name = input("Enter test company name: ").strip() or "Test Bedrijf BV"
        test_person = input("Enter test contact name: ").strip() or "Test Contact"

        if test_email:
            print("\n[3] Creating test entities...")

            # Create/find organization
            org_id = find_or_create_organization(test_name)

            # Create/find person
            person_id = find_or_create_person(test_email, test_person)

            if person_id:
                # Create deal
                print("\n[4] Creating test deal...")
                deal = create_test_deal(person_id, org_id, test_name)

                if deal:
                    deal_id = deal.get("id")
                    print(f"\n   Deal created successfully!")
                    print(f"   Deal ID: {deal_id}")
                    print(f"   View at: https://app.pipedrive.com/deal/{deal_id}")

                    # Ask to send test email
                    send_test = input("\nSend Email 1 as test? (y/n): ").strip().lower()
                    if send_test == 'y':
                        print("\n[5] Sending test email...")
                        # Update field to trigger sequence
                        update_deal_field(deal_id, FIELD_KEYS["laatste_email"], "Email 1")
                        print(f"   Set 'Laatste Email Verzonden' to 'Email 1'")
                        print(f"\n   To manually send the email:")
                        print(f"   1. Go to: https://app.pipedrive.com/deal/{deal_id}")
                        print(f"   2. Click 'Email' button")
                        print(f"   3. Select template: 'APK Email 1 - APK Ontvangen Dag 1'")
                        print(f"   4. Send to: {test_email}")

    # Print automation setup instructions
    print("\n" + "=" * 70)
    print("AUTOMATION SETUP INSTRUCTIONS")
    print("=" * 70)

    show_instructions = input("\nShow detailed automation setup instructions? (y/n): ").strip().lower()
    if show_instructions == 'y':
        print_automation_setup_instructions()

    print("\n" + "=" * 70)
    print("SETUP COMPLETE")
    print("=" * 70)
    print("""
Next steps:
1. Go to https://app.pipedrive.com/automations
2. Create 10 automations as described above
3. Test with a real deal by moving it to "APK Verzonden" stage

Files created:
- Email templates: 8 templates (id 63-70)
- Custom fields: 6 fields configured
- Deal stages: 7 stages configured
""")

    return True


if __name__ == "__main__":
    main()
