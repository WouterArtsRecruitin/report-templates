#!/usr/bin/env python3
"""
Update Pipedrive Email Templates with Professional HTML Formatting

This script updates all 8 APK email templates with:
- Professional HTML layout
- Brand colors (Recruitin Orange #FF6B35, Professional Blue #1E3A8A)
- Responsive design
- Outlook-compatible tables
- Clean typography
"""

import requests
import os
from datetime import datetime

# Pipedrive API configuration
PIPEDRIVE_API_TOKEN = os.environ.get('PIPEDRIVE_API_TOKEN', '57720aa8b264cb9060c9dd5af8ae0c096dbbebb5')
PIPEDRIVE_BASE_URL = 'https://api.pipedrive.com/v1'

# Email template IDs
TEMPLATE_IDS = {
    1: 63,  # APK Email 1
    2: 64,  # APK Email 2
    3: 65,  # APK Email 3
    4: 66,  # APK Email 4
    5: 67,  # APK Email 5
    6: 68,  # APK Email 6
    7: 69,  # APK Email 7
    8: 70,  # APK Email 8
}

# HTML wrapper for professional formatting
def create_html_email(body_content, footer_text=""):
    """Create HTML email with professional formatting"""
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; font-family: Arial, Helvetica, sans-serif; background-color: #f5f5f5;">
    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background-color: #f5f5f5;">
        <tr>
            <td style="padding: 20px;">
                <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="600" style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                    <!-- Logo Header -->
                    <tr>
                        <td style="padding: 25px 30px 20px;">
                            <table role="presentation" cellspacing="0" cellpadding="0" border="0">
                                <tr>
                                    <td style="background-color: #FF6B35; width: 40px; height: 40px; text-align: center; vertical-align: middle; border-radius: 4px;">
                                        <span style="color: #FFFFFF; font-size: 20px; font-weight: bold;">R</span>
                                    </td>
                                    <td style="padding-left: 12px;">
                                        <span style="color: #1E3A8A; font-size: 16px; font-weight: bold;">recruitmentapk.nl</span>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>

                    <!-- Email Body -->
                    <tr>
                        <td style="padding: 0 30px 25px;">
                            {body_content}
                        </td>
                    </tr>

                    <!-- Footer -->
                    <tr>
                        <td style="padding: 20px 30px; background-color: #F9FAFB; border-top: 1px solid #E5E7EB;">
                            <p style="color: #9CA3AF; font-size: 12px; margin: 0; font-family: Arial, sans-serif;">
                                {footer_text}
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>"""


# Email templates with HTML content
EMAIL_TEMPLATES_HTML = {
    1: {
        "name": "APK Email 1 - APK Ontvangen Dag 1",
        "subject": "Je Recruitment APK - alles goed ontvangen?",
        "body": """<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0 0 18px; font-family: Arial, sans-serif;">
    Hoi {person.first_name},
</p>

<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0 0 18px; font-family: Arial, sans-serif;">
    Gisteren stuurde ik je de <strong>Recruitment APK</strong> - de complete analyse van jullie wervingsproces.
</p>

<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0 0 18px; font-family: Arial, sans-serif;">
    Even een snelle check: is alles goed aangekomen?
</p>

<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0 0 18px; font-family: Arial, sans-serif;">
    Als je vragen hebt over je score of de aanbevelingen - reply gerust op deze mail. Ik help je graag verder.
</p>

<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0 0 5px; font-family: Arial, sans-serif;">
    Groeten,
</p>
<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0; font-family: Arial, sans-serif;">
    <strong>Wouter</strong><br>
    <span style="color: #6B7280; font-size: 13px;">recruitmentapk.nl</span>
</p>""",
        "footer": "PS: Geen verkooppraatje vandaag - gewoon even checken of alles werkt."
    },

    2: {
        "name": "APK Email 2 - Al Bekeken Dag 3",
        "subject": "Heb je de APK al kunnen bekijken?",
        "body": """<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0 0 18px; font-family: Arial, sans-serif;">
    Hoi {person.first_name},
</p>

<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0 0 18px; font-family: Arial, sans-serif;">
    Even nieuwsgierig: heb je de Recruitment APK al kunnen doornemen?
</p>

<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0 0 12px; font-family: Arial, sans-serif;">
    Ik hoor het graag als je ergens tegenaan loopt, bijvoorbeeld:
</p>

<table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="margin-bottom: 18px;">
    <tr><td style="padding: 6px 0; color: #374151; font-size: 14px; font-family: Arial, sans-serif;">• Vragen over je recruitment maturity score?</td></tr>
    <tr><td style="padding: 6px 0; color: #374151; font-size: 14px; font-family: Arial, sans-serif;">• Onduidelijkheid over de verbeterpunten?</td></tr>
    <tr><td style="padding: 6px 0; color: #374151; font-size: 14px; font-family: Arial, sans-serif;">• Hulp nodig bij de prioritering?</td></tr>
</table>

<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0 0 18px; font-family: Arial, sans-serif;">
    Geen probleem - reply gewoon en ik denk met je mee.
</p>

<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0 0 5px; font-family: Arial, sans-serif;">
    Groeten,
</p>
<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0; font-family: Arial, sans-serif;">
    <strong>Wouter</strong>
</p>""",
        "footer": "Tip: De meeste bedrijven focussen eerst op de \"quick wins\" uit de APK - de punten die snel resultaat opleveren."
    },

    3: {
        "name": "APK Email 3 - Eerste Stappen Dag 5",
        "subject": "Ben je al ergens mee gestart?",
        "body": """<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0 0 18px; font-family: Arial, sans-serif;">
    Hoi {person.first_name},
</p>

<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0 0 18px; font-family: Arial, sans-serif;">
    Het is nu een paar dagen geleden sinds je de Recruitment APK hebt ontvangen.
</p>

<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0 0 18px; font-family: Arial, sans-serif;">
    Ik ben oprecht benieuwd: ben je al ergens mee aan de slag gegaan?
</p>

<!-- Feedback Box -->
<table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background-color: #F3F4F6; margin-bottom: 18px; border-radius: 6px;">
    <tr>
        <td style="padding: 20px; border-left: 4px solid #FF6B35;">
            <p style="color: #374151; font-size: 14px; line-height: 1.6; margin: 0; font-family: Arial, sans-serif;">
                <strong style="font-size: 15px;">Mag ik je iets vragen?</strong><br><br>
                Als je 2 minuten hebt, zou je me kunnen vertellen:<br><br>
                1. Heb je de APK intern al gedeeld?<br>
                2. Welk verbeterpunt pak je als eerste aan?<br>
                3. Wat vond je het meest verrassend aan de uitkomst?<br><br>
                <em>Jouw feedback helpt me om de APK te verbeteren voor andere bedrijven.</em>
            </p>
        </td>
    </tr>
</table>

<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0 0 18px; font-family: Arial, sans-serif;">
    Reply gewoon op deze mail - ik lees alles persoonlijk.
</p>

<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0 0 5px; font-family: Arial, sans-serif;">
    Alvast bedankt,
</p>
<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0; font-family: Arial, sans-serif;">
    <strong>Wouter</strong>
</p>""",
        "footer": "Nog niet aan toegekomen? Geen probleem - de APK blijft relevant. Bewaar hem voor wanneer het wel past."
    },

    4: {
        "name": "APK Email 4 - Tip Time-to-Hire Dag 8",
        "subject": "Recruitment tip: Time-to-hire halveren",
        "body": """<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0 0 18px; font-family: Arial, sans-serif;">
    Hoi {person.first_name},
</p>

<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0 0 18px; font-family: Arial, sans-serif;">
    Deze week deel ik een tip die veel bedrijven over het hoofd zien:
</p>

<!-- Tip Box -->
<table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background-color: #FEF3C7; margin-bottom: 18px; border-radius: 6px;">
    <tr>
        <td style="padding: 20px; border-left: 4px solid #F59E0B;">
            <p style="color: #92400E; font-size: 16px; font-weight: bold; margin: 0 0 12px; font-family: Arial, sans-serif;">
                Je time-to-hire zit niet in de selectie, maar in de voorkant
            </p>
            <p style="color: #78350F; font-size: 14px; line-height: 1.6; margin: 0; font-family: Arial, sans-serif;">
                De gemiddelde time-to-hire in Nederland is <strong>42 dagen</strong>. Maar wist je dat 60% van die tijd opgaat aan het vinden van kandidaten - niet aan het selecteren?<br><br>

                <strong>Wat de snelste bedrijven doen:</strong><br>
                • Talent pools opbouwen VOOR de vacature ontstaat<br>
                • Hiring managers trainen op snelle besluitvorming<br>
                • Standaard response binnen 48 uur naar kandidaten<br><br>

                <strong>Quick win:</strong><br>
                Meet eens hoelang kandidaten wachten tussen sollicitatie en eerste contact. Als dat meer dan 5 dagen is, verlies je de beste mensen.
            </p>
        </td>
    </tr>
</table>

<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0 0 18px; font-family: Arial, sans-serif;">
    Hoe snel schakelt jouw organisatie na een sollicitatie?
</p>

<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0 0 5px; font-family: Arial, sans-serif;">
    Succes deze week,
</p>
<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0; font-family: Arial, sans-serif;">
    <strong>Wouter</strong>
</p>""",
        "footer": "Volgende week: Waarom de candidate experience je employer brand bepaalt"
    },

    5: {
        "name": "APK Email 5 - Tip Candidate Experience Dag 11",
        "subject": "Recruitment tip: Candidate experience als geheim wapen",
        "body": """<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0 0 18px; font-family: Arial, sans-serif;">
    Hoi {person.first_name},
</p>

<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0 0 18px; font-family: Arial, sans-serif;">
    <em>"We hebben een negatieve Glassdoor review gekregen van een afgewezen kandidaat."</em>
</p>

<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0 0 15px; font-family: Arial, sans-serif;">
    Dat hoor ik vaker dan je denkt. Hier is wat de data zegt:
</p>

<!-- Stats Box -->
<table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background-color: #D1FAE5; margin-bottom: 18px; border-radius: 6px;">
    <tr>
        <td style="padding: 20px; border-left: 4px solid #10B981;">
            <p style="color: #065F46; font-size: 14px; line-height: 1.8; margin: 0; font-family: Arial, sans-serif;">
                <strong style="font-size: 15px;">Impact van candidate experience:</strong><br><br>
                • <strong>72%</strong> deelt slechte ervaringen met anderen<br>
                • <strong>52%</strong> stopt met kopen bij het bedrijf na slechte ervaring<br>
                • <strong>78%</strong> zou opnieuw solliciteren bij goede afwijzing<br><br>
                <em style="font-size: 12px;">Bron: Talent Board 2024</em>
            </p>
        </td>
    </tr>
</table>

<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0 0 12px; font-family: Arial, sans-serif;">
    <strong>De oplossing is simpeler dan je denkt:</strong>
</p>

<table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="margin-bottom: 18px;">
    <tr><td style="padding: 6px 0; color: #374151; font-size: 14px; font-family: Arial, sans-serif;">• Stuur ALTIJD een persoonlijke afwijzing (geen standaardmail)</td></tr>
    <tr><td style="padding: 6px 0; color: #374151; font-size: 14px; font-family: Arial, sans-serif;">• Geef binnen 1 week feedback na het laatste gesprek</td></tr>
    <tr><td style="padding: 6px 0; color: #374151; font-size: 14px; font-family: Arial, sans-serif;">• Vraag afgewezen kandidaten om feedback over het proces</td></tr>
    <tr><td style="padding: 6px 0; color: #374151; font-size: 14px; font-family: Arial, sans-serif;">• Behandel kandidaten zoals je klanten behandelt</td></tr>
</table>

<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0 0 5px; font-family: Arial, sans-serif;">
    Groeten,
</p>
<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0; font-family: Arial, sans-serif;">
    <strong>Wouter</strong>
</p>""",
        "footer": "Vragen? Reply gewoon op deze mail."
    },

    6: {
        "name": "APK Email 6 - Tip Meten Weten Dag 14",
        "subject": "Recruitment tip: Meten = weten",
        "body": """<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0 0 18px; font-family: Arial, sans-serif;">
    Hoi {person.first_name},
</p>

<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0 0 18px; font-family: Arial, sans-serif;">
    <em>"We weten niet precies waar het misgaat in ons wervingsproces."</em>
</p>

<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0 0 15px; font-family: Arial, sans-serif;">
    Dat is logisch als je niet meet. Maar welke metrics zijn eigenlijk belangrijk?
</p>

<!-- KPI Box -->
<table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background-color: #EDE9FE; margin-bottom: 18px; border-radius: 6px;">
    <tr>
        <td style="padding: 20px; border-left: 4px solid #7C3AED;">
            <p style="color: #5B21B6; font-size: 14px; line-height: 1.6; margin: 0; font-family: Arial, sans-serif;">
                <strong style="font-size: 15px;">De 5 recruitment KPIs die ertoe doen:</strong><br><br>
                1. <strong>Time-to-hire</strong> - Van vacature tot handtekening<br>
                2. <strong>Quality of hire</strong> - Prestatie na 6/12 maanden<br>
                3. <strong>Cost per hire</strong> - Totale kosten per aanname<br>
                4. <strong>Source effectiveness</strong> - Welke kanalen leveren?<br>
                5. <strong>Candidate satisfaction</strong> - NPS van sollicitanten<br><br>

                <strong>Start simpel:</strong><br>
                Meet eerst alleen time-to-hire en source effectiveness. Dat geeft al 80% van de inzichten.
            </p>
        </td>
    </tr>
</table>

<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0 0 18px; font-family: Arial, sans-serif;">
    Welke van deze 5 meet jouw organisatie al? Reply en laat het me weten.
</p>

<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0 0 5px; font-family: Arial, sans-serif;">
    Tot volgende week,
</p>
<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0; font-family: Arial, sans-serif;">
    <strong>Wouter</strong>
</p>""",
        "footer": "Dit was de laatste tip in deze serie. Vond je ze nuttig? Laat het me weten."
    },

    7: {
        "name": "APK Email 7 - Gesprek Aanbod Dag 21",
        "subject": "Zullen we je APK samen doornemen?",
        "body": """<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0 0 18px; font-family: Arial, sans-serif;">
    Hoi {person.first_name},
</p>

<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0 0 18px; font-family: Arial, sans-serif;">
    Het is nu drie weken geleden dat je de Recruitment APK ontving.
</p>

<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0 0 18px; font-family: Arial, sans-serif;">
    Ik ben benieuwd: heb je al stappen kunnen zetten op basis van de uitkomsten? Of ligt het rapport nog op de stapel?
</p>

<!-- CTA Box -->
<table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background-color: #F3F4F6; margin-bottom: 18px; border-radius: 6px;">
    <tr>
        <td style="padding: 20px; border-left: 4px solid #FF6B35;">
            <p style="color: #374151; font-size: 14px; line-height: 1.6; margin: 0; font-family: Arial, sans-serif;">
                <strong style="font-size: 16px; color: #1E3A8A;">Zullen we even bellen?</strong><br><br>
                Geen verkooppraatje, gewoon een kort gesprek (<strong>30 min gratis</strong>) om je APK samen door te nemen.<br><br>

                We kunnen het hebben over:<br>
                • De belangrijkste verbeterpunten voor {organization.name}<br>
                • Quick wins die je direct kunt implementeren<br>
                • Hoe je draagvlak krijgt voor recruitment verbeteringen<br><br>

                <a href="https://calendly.com/wouter-arts-/recruitment-apk-review" style="display: inline-block; background-color: #FF6B35; color: #FFFFFF; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 14px;">Plan een moment →</a>
            </p>
        </td>
    </tr>
</table>

<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0 0 18px; font-family: Arial, sans-serif;">
    Geen zin of geen tijd? Helemaal prima - reply dan gewoon even met een update. Ik hoor graag hoe het gaat.
</p>

<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0 0 5px; font-family: Arial, sans-serif;">
    Groeten,
</p>
<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0; font-family: Arial, sans-serif;">
    <strong>Wouter</strong>
</p>""",
        "footer": "PS: Ik reageer ook gewoon op een reply - wat jou het makkelijkst is."
    },

    8: {
        "name": "APK Email 8 - Final Check-in Dag 30",
        "subject": "Laatste check - hoe staat het met jullie recruitment?",
        "body": """<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0 0 18px; font-family: Arial, sans-serif;">
    Hoi {person.first_name},
</p>

<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0 0 18px; font-family: Arial, sans-serif;">
    Een maand geleden verstuurde ik de Recruitment APK voor {organization.name}.
</p>

<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0 0 18px; font-family: Arial, sans-serif;">
    Dit is mijn laatste mail in deze serie - daarna laat ik je met rust.
</p>

<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0 0 15px; font-family: Arial, sans-serif;">
    Maar voor ik ga, ben ik nieuwsgierig:
</p>

<!-- Options Box -->
<table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background-color: #F3F4F6; margin-bottom: 18px; border-radius: 6px;">
    <tr>
        <td style="padding: 20px;">
            <p style="color: #374151; font-size: 14px; line-height: 1.8; margin: 0; font-family: Arial, sans-serif;">
                <strong style="font-size: 15px; color: #1E3A8A;">Hoe staat het ervoor?</strong><br><br>

                <strong>A.</strong> We zijn aan de slag - al verbeteringen doorgevoerd! 🎉<br>
                <strong>B.</strong> APK ligt klaar - maar nog geen tijd gehad<br>
                <strong>C.</strong> Recruitment staat even on hold bij ons<br>
                <strong>D.</strong> Ik wil graag sparren - laten we bellen<br><br>

                <em>Reply met A, B, C of D (of vertel gewoon je verhaal)</em>
            </p>
        </td>
    </tr>
</table>

<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0 0 18px; font-family: Arial, sans-serif;">
    Hoe dan ook - succes met jullie recruitment. En mocht je in de toekomst weer een APK willen doen, of hulp nodig hebben bij de implementatie, je weet me te vinden.
</p>

<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0 0 5px; font-family: Arial, sans-serif;">
    Groeten,
</p>
<p style="color: #374151; font-size: 15px; line-height: 1.7; margin: 0; font-family: Arial, sans-serif;">
    <strong>Wouter</strong><br>
    <span style="color: #6B7280; font-size: 13px;">recruitmentapk.nl</span>
</p>""",
        "footer": "Contact: warts@recruitin.nl | Nieuwe APK? <a href=\"https://recruitmentapk.nl\" style=\"color: #FF6B35;\">Start hier</a>"
    }
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

        if response.status_code in [200, 201]:
            return response.json()
        else:
            print(f"   Error {response.status_code}: {response.text[:200]}")
            return None
    except Exception as e:
        print(f"   Error: {e}")
        return None


def update_template(template_id, name, subject, html_content):
    """Update an email template with new HTML content"""
    data = {
        "name": name,
        "subject": subject,
        "content": html_content,
        "shared_flag": 1
    }

    result = api_request("PUT", f"mailbox/mailTemplates/{template_id}", data)
    if result and result.get("success"):
        return True
    return False


def main():
    print("=" * 70)
    print("UPDATING EMAIL TEMPLATES WITH PROFESSIONAL HTML FORMATTING")
    print("=" * 70)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Test API connection
    print("\n[1] Testing API connection...")
    test = api_request("GET", "users/me")
    if not test or not test.get("success"):
        print("   API connection failed!")
        return False

    user = test.get("data", {})
    print(f"   Connected as: {user.get('name')}")

    # Update each template
    print("\n[2] Updating email templates...")
    print("-" * 50)

    success_count = 0
    for email_num, template_data in EMAIL_TEMPLATES_HTML.items():
        template_id = TEMPLATE_IDS[email_num]
        name = template_data["name"]
        subject = template_data["subject"]
        body = template_data["body"]
        footer = template_data["footer"]

        # Create full HTML email
        html_content = create_html_email(body, footer)

        print(f"\n   Updating: {name} (id: {template_id})")
        if update_template(template_id, name, subject, html_content):
            print(f"   ✓ Updated successfully")
            success_count += 1
        else:
            print(f"   ✗ Update failed")

    # Summary
    print("\n" + "=" * 70)
    print("UPDATE COMPLETE")
    print("=" * 70)
    print(f"\n   Templates updated: {success_count}/8")
    print(f"\n   Features added:")
    print(f"   • Professional HTML layout with brand colors")
    print(f"   • Outlook-compatible table-based design")
    print(f"   • Colored tip/info boxes for visual appeal")
    print(f"   • CTA button in Email 7 for Calendly booking")
    print(f"   • Consistent typography and spacing")
    print(f"   • Mobile-responsive design")

    return True


if __name__ == "__main__":
    main()
