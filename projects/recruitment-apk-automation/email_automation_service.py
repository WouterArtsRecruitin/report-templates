#!/usr/bin/env python3
"""
RECRUITMENT APK - EMAIL AUTOMATION SERVICE
==========================================
Handles the 8-email nurture sequence over 30 days.

Since Pipedrive doesn't have an API for automations, we build
the automation logic directly into our webhook service.

This service:
1. Schedules emails based on deal creation date
2. Checks email sequence status before sending
3. Updates Pipedrive deal fields after each email
4. Stops sequence when status is "Gepauzeerd" or "Voltooid"
"""

import os
import json
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import requests
from threading import Thread
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Environment variables
PIPEDRIVE_API_TOKEN = os.getenv('PIPEDRIVE_API_TOKEN', '57720aa8b264cb9060c9dd5af8ae0c096dbbebb5')
PIPEDRIVE_BASE_URL = 'https://api.pipedrive.com/v1'
SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SMTP_USER = os.getenv('SMTP_USER', 'artsrecruitin@gmail.com')
SMTP_PASS = os.getenv('SMTP_PASS')

# Custom field keys
FIELD_KEYS = {
    "apk_verzonden_op": "7f23d557432ba403b5534be430151b827384ec43",
    "apk_score": "b0d1e96af884d111b66f812ee4293735393f1624",
    "email_sequence_status": "22d33c7f119119e178f391a272739c571cf2e29b",
    "laatste_email": "753f37a1abc8e161c7982c1379a306b21fae1bab",
    "typeform_response_id": "d3b5fc1d2cb519aac33d381bc3806c5c5fef734e",
    "verbeterpunten": "1f61f3dc8f0d5396c12eaa713c62b2ad1d71f794",
}

# Email sequence schedule (days after APK sent)
EMAIL_SCHEDULE = [
    {"email_num": 1, "day": 1, "template_id": 63},
    {"email_num": 2, "day": 3, "template_id": 64},
    {"email_num": 3, "day": 5, "template_id": 65},
    {"email_num": 4, "day": 8, "template_id": 66},
    {"email_num": 5, "day": 11, "template_id": 67},
    {"email_num": 6, "day": 14, "template_id": 68},
    {"email_num": 7, "day": 21, "template_id": 69},
    {"email_num": 8, "day": 30, "template_id": 70},
]

# Email templates content (HTML formatted)
EMAIL_TEMPLATES = {
    1: {
        "subject": "Je Recruitment APK - alles goed ontvangen?",
        "body": """<p>Hoi {first_name},</p>

<p>Gisteren stuurde ik je de <strong>Recruitment APK</strong> - de complete analyse van jullie wervingsproces.</p>

<p>Even een snelle check: is alles goed aangekomen?</p>

<p>Als je vragen hebt over je score of de aanbevelingen - reply gerust op deze mail. Ik help je graag verder.</p>

<p>Groeten,<br>
<strong>Wouter</strong><br>
<span style="color: #6B7280;">recruitmentapk.nl</span></p>

<p style="color: #9CA3AF; font-size: 12px;">PS: Geen verkooppraatje vandaag - gewoon even checken of alles werkt.</p>"""
    },
    2: {
        "subject": "Heb je de APK al kunnen bekijken?",
        "body": """<p>Hoi {first_name},</p>

<p>Even nieuwsgierig: heb je de Recruitment APK al kunnen doornemen?</p>

<p>Ik hoor het graag als je ergens tegenaan loopt, bijvoorbeeld:</p>
<ul>
    <li>Vragen over je recruitment maturity score?</li>
    <li>Onduidelijkheid over de verbeterpunten?</li>
    <li>Hulp nodig bij de prioritering?</li>
</ul>

<p>Geen probleem - reply gewoon en ik denk met je mee.</p>

<p>Groeten,<br><strong>Wouter</strong></p>

<p style="color: #9CA3AF; font-size: 12px;">Tip: De meeste bedrijven focussen eerst op de "quick wins" uit de APK.</p>"""
    },
    3: {
        "subject": "Ben je al ergens mee gestart?",
        "body": """<p>Hoi {first_name},</p>

<p>Het is nu een paar dagen geleden sinds je de Recruitment APK hebt ontvangen.</p>

<p>Ik ben oprecht benieuwd: ben je al ergens mee aan de slag gegaan?</p>

<div style="background-color: #F3F4F6; border-left: 4px solid #FF6B35; padding: 15px; margin: 20px 0;">
    <strong>Mag ik je iets vragen?</strong><br><br>
    Als je 2 minuten hebt, zou je me kunnen vertellen:<br><br>
    1. Heb je de APK intern al gedeeld?<br>
    2. Welk verbeterpunt pak je als eerste aan?<br>
    3. Wat vond je het meest verrassend aan de uitkomst?<br><br>
    <em>Jouw feedback helpt me om de APK te verbeteren.</em>
</div>

<p>Reply gewoon op deze mail - ik lees alles persoonlijk.</p>

<p>Alvast bedankt,<br><strong>Wouter</strong></p>"""
    },
    4: {
        "subject": "Recruitment tip: Time-to-hire halveren",
        "body": """<p>Hoi {first_name},</p>

<p>Deze week deel ik een tip die veel bedrijven over het hoofd zien:</p>

<div style="background-color: #FEF3C7; border-left: 4px solid #F59E0B; padding: 15px; margin: 20px 0;">
    <strong style="color: #92400E; font-size: 16px;">Je time-to-hire zit niet in de selectie, maar in de voorkant</strong><br><br>
    <span style="color: #78350F;">
    De gemiddelde time-to-hire in Nederland is <strong>42 dagen</strong>. Maar 60% van die tijd gaat op aan het vinden van kandidaten - niet aan het selecteren.<br><br>

    <strong>Wat de snelste bedrijven doen:</strong><br>
    • Talent pools opbouwen VOOR de vacature ontstaat<br>
    • Hiring managers trainen op snelle besluitvorming<br>
    • Standaard response binnen 48 uur naar kandidaten<br><br>

    <strong>Quick win:</strong><br>
    Meet eens hoelang kandidaten wachten tussen sollicitatie en eerste contact.
    </span>
</div>

<p>Hoe snel schakelt jouw organisatie na een sollicitatie?</p>

<p>Succes deze week,<br><strong>Wouter</strong></p>"""
    },
    5: {
        "subject": "Recruitment tip: Candidate experience als geheim wapen",
        "body": """<p>Hoi {first_name},</p>

<p><em>"We hebben een negatieve Glassdoor review gekregen van een afgewezen kandidaat."</em></p>

<p>Dat hoor ik vaker dan je denkt. Hier is wat de data zegt:</p>

<div style="background-color: #D1FAE5; border-left: 4px solid #10B981; padding: 15px; margin: 20px 0;">
    <strong style="color: #065F46;">Impact van candidate experience:</strong><br><br>
    <span style="color: #065F46;">
    • <strong>72%</strong> deelt slechte ervaringen met anderen<br>
    • <strong>52%</strong> stopt met kopen bij het bedrijf na slechte ervaring<br>
    • <strong>78%</strong> zou opnieuw solliciteren bij goede afwijzing<br><br>
    <em style="font-size: 12px;">Bron: Talent Board 2024</em>
    </span>
</div>

<p><strong>De oplossing is simpeler dan je denkt:</strong></p>
<ul>
    <li>Stuur ALTIJD een persoonlijke afwijzing</li>
    <li>Geef binnen 1 week feedback na het laatste gesprek</li>
    <li>Vraag afgewezen kandidaten om feedback</li>
    <li>Behandel kandidaten zoals je klanten behandelt</li>
</ul>

<p>Groeten,<br><strong>Wouter</strong></p>"""
    },
    6: {
        "subject": "Recruitment tip: Meten = weten",
        "body": """<p>Hoi {first_name},</p>

<p><em>"We weten niet precies waar het misgaat in ons wervingsproces."</em></p>

<p>Dat is logisch als je niet meet. Maar welke metrics zijn belangrijk?</p>

<div style="background-color: #EDE9FE; border-left: 4px solid #7C3AED; padding: 15px; margin: 20px 0;">
    <strong style="color: #5B21B6; font-size: 15px;">De 5 recruitment KPIs die ertoe doen:</strong><br><br>
    <span style="color: #5B21B6;">
    1. <strong>Time-to-hire</strong> - Van vacature tot handtekening<br>
    2. <strong>Quality of hire</strong> - Prestatie na 6/12 maanden<br>
    3. <strong>Cost per hire</strong> - Totale kosten per aanname<br>
    4. <strong>Source effectiveness</strong> - Welke kanalen leveren?<br>
    5. <strong>Candidate satisfaction</strong> - NPS van sollicitanten<br><br>

    <strong>Start simpel:</strong><br>
    Meet eerst alleen time-to-hire en source effectiveness. Dat geeft al 80% van de inzichten.
    </span>
</div>

<p>Welke van deze 5 meet jouw organisatie al?</p>

<p>Tot volgende week,<br><strong>Wouter</strong></p>

<p style="color: #9CA3AF; font-size: 12px;">Dit was de laatste tip in deze serie. Vond je ze nuttig?</p>"""
    },
    7: {
        "subject": "Zullen we je APK samen doornemen?",
        "body": """<p>Hoi {first_name},</p>

<p>Het is nu drie weken geleden dat je de Recruitment APK ontving.</p>

<p>Ik ben benieuwd: heb je al stappen kunnen zetten op basis van de uitkomsten? Of ligt het rapport nog op de stapel?</p>

<div style="background-color: #F3F4F6; border-left: 4px solid #FF6B35; padding: 20px; margin: 20px 0;">
    <strong style="color: #1E3A8A; font-size: 16px;">Zullen we even bellen?</strong><br><br>
    Geen verkooppraatje, gewoon een kort gesprek (<strong>30 min gratis</strong>) om je APK samen door te nemen.<br><br>

    We kunnen het hebben over:<br>
    • De belangrijkste verbeterpunten voor {company}<br>
    • Quick wins die je direct kunt implementeren<br>
    • Hoe je draagvlak krijgt voor recruitment verbeteringen<br><br>

    <a href="https://calendly.com/wouter-arts-/recruitment-apk-review" style="display: inline-block; background-color: #FF6B35; color: #FFFFFF; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: bold;">Plan een moment →</a>
</div>

<p>Geen zin of geen tijd? Helemaal prima - reply dan gewoon even met een update.</p>

<p>Groeten,<br><strong>Wouter</strong></p>

<p style="color: #9CA3AF; font-size: 12px;">PS: Ik reageer ook gewoon op een reply - wat jou het makkelijkst is.</p>"""
    },
    8: {
        "subject": "Laatste check - hoe staat het met jullie recruitment?",
        "body": """<p>Hoi {first_name},</p>

<p>Een maand geleden verstuurde ik de Recruitment APK voor {company}.</p>

<p>Dit is mijn laatste mail in deze serie - daarna laat ik je met rust.</p>

<p>Maar voor ik ga, ben ik nieuwsgierig:</p>

<div style="background-color: #F3F4F6; padding: 20px; margin: 20px 0; border-radius: 6px;">
    <strong style="color: #1E3A8A;">Hoe staat het ervoor?</strong><br><br>

    <strong>A.</strong> We zijn aan de slag - al verbeteringen doorgevoerd!<br>
    <strong>B.</strong> APK ligt klaar - maar nog geen tijd gehad<br>
    <strong>C.</strong> Recruitment staat even on hold bij ons<br>
    <strong>D.</strong> Ik wil graag sparren - laten we bellen<br><br>

    <em>Reply met A, B, C of D (of vertel gewoon je verhaal)</em>
</div>

<p>Hoe dan ook - succes met jullie recruitment. En mocht je in de toekomst weer een APK willen doen, je weet me te vinden.</p>

<p>Groeten,<br>
<strong>Wouter</strong><br>
<span style="color: #6B7280;">recruitmentapk.nl</span></p>

<p style="color: #9CA3AF; font-size: 12px;">Contact: warts@recruitin.nl | Nieuwe APK? <a href="https://recruitmentapk.nl" style="color: #FF6B35;">Start hier</a></p>"""
    }
}


def create_html_email(body_content: str) -> str:
    """Wrap email body in HTML template"""
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
                        <td style="padding: 0 30px 25px; color: #374151; font-size: 15px; line-height: 1.7;">
                            {body_content}
                        </td>
                    </tr>

                    <!-- Footer -->
                    <tr>
                        <td style="padding: 20px 30px; background-color: #F9FAFB; border-top: 1px solid #E5E7EB;">
                            <p style="color: #9CA3AF; font-size: 11px; margin: 0; text-align: center;">
                                © {datetime.now().year} recruitmentapk.nl | warts@recruitin.nl
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>"""


def pipedrive_request(method: str, endpoint: str, data: Dict = None) -> Optional[Dict]:
    """Make request to Pipedrive API"""
    url = f"{PIPEDRIVE_BASE_URL}/{endpoint}"
    params = {"api_token": PIPEDRIVE_API_TOKEN}

    try:
        if method == "GET":
            response = requests.get(url, params=params, timeout=30)
        elif method == "POST":
            response = requests.post(url, params=params, json=data, timeout=30)
        elif method == "PUT":
            response = requests.put(url, params=params, json=data, timeout=30)
        else:
            return None

        if response.status_code in [200, 201]:
            return response.json()
        return None
    except Exception as e:
        logger.error(f"Pipedrive request error: {e}")
        return None


def get_deal_info(deal_id: int) -> Optional[Dict]:
    """Get deal information including person and org"""
    result = pipedrive_request("GET", f"deals/{deal_id}")
    if result and result.get("success"):
        return result.get("data")
    return None


def get_person_info(person_id: int) -> Optional[Dict]:
    """Get person information"""
    result = pipedrive_request("GET", f"persons/{person_id}")
    if result and result.get("success"):
        return result.get("data")
    return None


def update_deal_field(deal_id: int, field_key: str, value: Any) -> bool:
    """Update a custom field on a deal"""
    data = {field_key: value}
    result = pipedrive_request("PUT", f"deals/{deal_id}", data)
    return result and result.get("success", False)


def get_sequence_status(deal_id: int) -> str:
    """Get the current email sequence status for a deal"""
    deal = get_deal_info(deal_id)
    if deal:
        return deal.get(FIELD_KEYS["email_sequence_status"], "")
    return ""


def get_last_email_sent(deal_id: int) -> int:
    """Get the last email number sent for a deal"""
    deal = get_deal_info(deal_id)
    if deal:
        last_email = deal.get(FIELD_KEYS["laatste_email"], "")
        if last_email and "Email" in str(last_email):
            try:
                return int(str(last_email).replace("Email ", ""))
            except:
                pass
    return 0


def send_sequence_email(deal_id: int, email_num: int, to_email: str,
                        first_name: str, company: str) -> bool:
    """Send a specific email from the sequence"""
    if not SMTP_PASS:
        logger.warning(f"SMTP password not configured, cannot send email {email_num}")
        return False

    template = EMAIL_TEMPLATES.get(email_num)
    if not template:
        logger.error(f"Template not found for email {email_num}")
        return False

    try:
        # Personalize content
        subject = template["subject"]
        body = template["body"].format(
            first_name=first_name or "daar",
            company=company or "jullie organisatie"
        )

        # Create HTML email
        html_content = create_html_email(body)

        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f"Recruitment APK <{SMTP_USER}>"
        msg['To'] = to_email

        # Plain text fallback
        text_content = body.replace('<p>', '').replace('</p>', '\n\n')
        text_content = text_content.replace('<br>', '\n')
        text_content = text_content.replace('<strong>', '').replace('</strong>', '')
        text_content = text_content.replace('<em>', '').replace('</em>', '')

        msg.attach(MIMEText(text_content, 'plain'))
        msg.attach(MIMEText(html_content, 'html'))

        # Send
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)

        logger.info(f"Email {email_num} sent to {to_email} for deal {deal_id}")

        # Update Pipedrive
        update_deal_field(deal_id, FIELD_KEYS["laatste_email"], f"Email {email_num}")

        # Mark as complete if last email
        if email_num == 8:
            update_deal_field(deal_id, FIELD_KEYS["email_sequence_status"], "Voltooid")

        return True

    except Exception as e:
        logger.error(f"Failed to send email {email_num}: {e}")
        return False


def process_email_sequence(deal_id: int, to_email: str, first_name: str,
                          company: str, apk_sent_date: str):
    """
    Process the email sequence for a deal.
    Called in a background thread after APK is sent.
    """
    logger.info(f"Starting email sequence for deal {deal_id}")

    try:
        # Parse APK sent date
        sent_date = datetime.strptime(apk_sent_date, "%Y-%m-%d")
    except:
        sent_date = datetime.now()

    for schedule in EMAIL_SCHEDULE:
        email_num = schedule["email_num"]
        send_day = schedule["day"]

        # Calculate when to send this email
        send_date = sent_date + timedelta(days=send_day)
        wait_seconds = (send_date - datetime.now()).total_seconds()

        if wait_seconds > 0:
            logger.info(f"Email {email_num} scheduled for {send_date} (waiting {wait_seconds/3600:.1f} hours)")
            time.sleep(wait_seconds)

        # Check if sequence is still active
        status = get_sequence_status(deal_id)
        if status in ["Gepauzeerd", "Voltooid"]:
            logger.info(f"Sequence stopped for deal {deal_id}, status: {status}")
            return

        # Check if this email was already sent
        last_sent = get_last_email_sent(deal_id)
        if last_sent >= email_num:
            logger.info(f"Email {email_num} already sent for deal {deal_id}")
            continue

        # Send the email
        success = send_sequence_email(deal_id, email_num, to_email, first_name, company)

        if not success:
            logger.error(f"Failed to send email {email_num} for deal {deal_id}")
            # Continue with next email anyway

    logger.info(f"Email sequence completed for deal {deal_id}")


def start_email_sequence(deal_id: int, to_email: str, first_name: str,
                        company: str, apk_sent_date: str):
    """
    Start the email sequence in a background thread.
    This is called from the webhook handler after APK is sent.
    """
    thread = Thread(
        target=process_email_sequence,
        args=(deal_id, to_email, first_name, company, apk_sent_date),
        daemon=True
    )
    thread.start()
    logger.info(f"Email sequence thread started for deal {deal_id}")


# For testing
if __name__ == "__main__":
    print("Email Automation Service")
    print("=" * 50)
    print(f"SMTP configured: {bool(SMTP_PASS)}")
    print(f"Templates loaded: {len(EMAIL_TEMPLATES)}")
    print(f"Schedule: {len(EMAIL_SCHEDULE)} emails over {EMAIL_SCHEDULE[-1]['day']} days")
