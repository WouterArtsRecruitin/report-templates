#!/usr/bin/env python3
"""
RECRUITMENT APK - WEBHOOK HANDLER
=================================
Typeform: https://form.typeform.com/to/cuGe3IEC
Pipeline: Recruitment APK (id: 2)
Website: www.recruitmentapk.nl

Deploy to Render for Typeform webhook processing.

Flow:
1. Receive Typeform submission (recruitment maturity scan)
2. Create/update deal in Pipedrive
3. Generate APK report with Claude AI
4. Send email with report
5. Trigger email automation sequence
"""

import os
import json
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Dict, Any, Optional, List
from flask import Flask, request, jsonify
import requests

# Import email automation service
from email_automation_service import start_email_sequence

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Environment variables
CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')
PIPEDRIVE_API_TOKEN = os.getenv('PIPEDRIVE_API_TOKEN', '57720aa8b264cb9060c9dd5af8ae0c096dbbebb5')
SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SMTP_USER = os.getenv('SMTP_USER', 'artsrecruitin@gmail.com')
SMTP_PASS = os.getenv('SMTP_PASS')

# Pipedrive configuration
PIPEDRIVE_BASE_URL = 'https://api.pipedrive.com/v1'
PIPELINE_ID = 2  # Recruitment APK
STAGE_APK_VERZONDEN = 108  # Triggers email automation

# Custom field keys
FIELD_KEYS = {
    "apk_verzonden_op": "7f23d557432ba403b5534be430151b827384ec43",
    "apk_score": "b0d1e96af884d111b66f812ee4293735393f1624",
    "email_sequence_status": "22d33c7f119119e178f391a272739c571cf2e29b",
    "laatste_email": "753f37a1abc8e161c7982c1379a306b21fae1bab",
    "typeform_response_id": "d3b5fc1d2cb519aac33d381bc3806c5c5fef734e",
    "verbeterpunten": "1f61f3dc8f0d5396c12eaa713c62b2ad1d71f794",
}


# ==============================================================================
# HEALTH CHECK ENDPOINTS
# ==============================================================================

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'recruitment-apk-webhook',
        'version': '1.0.0',
        'pipeline': 'Recruitment APK',
        'typeform': 'cuGe3IEC'
    })


@app.route('/health', methods=['GET'])
def health():
    """Alternative health check"""
    return jsonify({'status': 'ok'})


# ==============================================================================
# TYPEFORM WEBHOOK HANDLER
# ==============================================================================

@app.route('/webhook/typeform', methods=['POST'])
def handle_typeform_webhook():
    """
    Handle Typeform webhook for Recruitment APK assessments
    Typeform: https://form.typeform.com/to/cuGe3IEC
    """
    try:
        # Parse incoming JSON
        data = request.get_json(force=True, silent=True)
        if not data:
            logger.error("No JSON data received")
            return jsonify({'error': 'No JSON data'}), 400

        logger.info(f"Received webhook with keys: {list(data.keys())}")

        # Validate Typeform structure
        if 'form_response' not in data:
            logger.error("Invalid Typeform structure")
            return jsonify({'error': 'Invalid Typeform structure'}), 400

        form_response = data.get('form_response', {})
        response_id = form_response.get('token', '')
        answers = form_response.get('answers', [])

        logger.info(f"Processing {len(answers)} answers, response_id: {response_id}")

        # Extract assessment data
        assessment_data = extract_assessment_data(answers)
        assessment_data['response_id'] = response_id

        if not assessment_data.get('email'):
            logger.error("Missing email in submission")
            return jsonify({'error': 'Missing email'}), 400

        # Calculate maturity score from answers
        maturity_result = calculate_maturity_score(answers)
        assessment_data['maturity_score'] = maturity_result['score']
        assessment_data['maturity_level'] = maturity_result['level']
        assessment_data['answer_scores'] = maturity_result['details']

        # Generate APK report with Claude
        apk_report = generate_apk_report(assessment_data)

        # Create/update Pipedrive deal
        deal = create_or_update_pipedrive_deal(assessment_data, apk_report)

        # Send email with APK report
        email_sent = send_apk_email(assessment_data, apk_report)

        # Start email automation sequence (runs in background thread)
        if deal and email_sent:
            deal_id = deal.get('id')
            today = datetime.now().strftime("%Y-%m-%d")
            start_email_sequence(
                deal_id=deal_id,
                to_email=assessment_data.get('email', ''),
                first_name=assessment_data.get('first_name', ''),
                company=assessment_data.get('company_name', ''),
                apk_sent_date=today
            )
            logger.info(f"Email sequence started for deal {deal_id}")

        logger.info(f"Webhook processed successfully for {assessment_data.get('email')}")

        return jsonify({
            'status': 'success',
            'email': assessment_data.get('email'),
            'maturity_score': maturity_result['score'],
            'maturity_level': maturity_result['level'],
            'deal_id': deal.get('id') if deal else None,
            'email_sent': email_sent,
            'email_sequence_started': bool(deal and email_sent)
        }), 200

    except Exception as e:
        logger.error(f"Webhook error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


# ==============================================================================
# DATA EXTRACTION
# ==============================================================================

def extract_assessment_data(answers: List[Dict]) -> Dict[str, Any]:
    """Extract contact and company data from Typeform answers"""
    data = {
        'first_name': '',
        'last_name': '',
        'email': '',
        'phone': '',
        'company_name': '',
        'industry': '',
        'raw_answers': []
    }

    for answer in answers:
        if not isinstance(answer, dict):
            continue

        field_type = answer.get('type', '')
        field_title = answer.get('field', {}).get('title', '').lower()

        # Handle contact_info block
        if field_type == 'contact_info':
            contact_info = answer.get('contact_info', {})
            if contact_info:
                data['first_name'] = contact_info.get('first_name', '')
                data['last_name'] = contact_info.get('last_name', '')
                data['email'] = contact_info.get('email', '')
                data['phone'] = contact_info.get('phone_number', '')
                data['company_name'] = contact_info.get('company', '')

        # Handle email field
        elif field_type == 'email':
            data['email'] = answer.get('email', '')

        # Handle text fields for name/company
        elif field_type in ['short_text', 'long_text']:
            text_value = answer.get('text', '')
            if 'naam' in field_title or 'name' in field_title:
                if not data['first_name']:
                    data['first_name'] = text_value
            elif 'bedrijf' in field_title or 'company' in field_title:
                if not data['company_name']:
                    data['company_name'] = text_value

        # Handle choice fields for industry
        elif field_type in ['multiple_choice', 'dropdown']:
            choice = answer.get('choice', {})
            choice_label = choice.get('label', '') if choice else ''
            if 'sector' in field_title or 'branche' in field_title or 'industry' in field_title:
                data['industry'] = choice_label

        # Store raw answers for scoring
        data['raw_answers'].append({
            'field_id': answer.get('field', {}).get('id', ''),
            'field_title': answer.get('field', {}).get('title', ''),
            'type': field_type,
            'value': get_answer_value(answer)
        })

    return data


def get_answer_value(answer: Dict) -> Any:
    """Get the value from any answer type"""
    field_type = answer.get('type', '')

    if field_type in ['short_text', 'long_text']:
        return answer.get('text', '')
    elif field_type == 'email':
        return answer.get('email', '')
    elif field_type == 'phone_number':
        return answer.get('phone_number', '')
    elif field_type in ['multiple_choice', 'dropdown']:
        choice = answer.get('choice', {})
        return choice.get('label', '') if choice else ''
    elif field_type == 'number':
        return answer.get('number', 0)
    elif field_type == 'rating':
        return answer.get('number', 0)
    elif field_type == 'boolean':
        return answer.get('boolean', False)
    elif field_type == 'contact_info':
        return answer.get('contact_info', {})

    return ''


# ==============================================================================
# MATURITY SCORE CALCULATION
# ==============================================================================

def calculate_maturity_score(answers: List[Dict]) -> Dict[str, Any]:
    """
    Calculate recruitment maturity score from Typeform answers
    Based on the assessment questions in the Typeform
    """
    score_mapping = {
        # Map answer options to scores (0-10)
        'nooit': 1,
        'zelden': 3,
        'soms': 5,
        'vaak': 7,
        'altijd': 9,
        'ja': 8,
        'nee': 2,
        'gedeeltelijk': 5,
        'niet': 1,
        'een beetje': 4,
        'redelijk': 6,
        'goed': 8,
        'uitstekend': 10,
        # Time-based answers
        'minder dan 2 weken': 9,
        '2-4 weken': 7,
        '4-6 weken': 5,
        '6-8 weken': 3,
        'meer dan 8 weken': 1,
        # Numeric ranges
        '0-20%': 2,
        '20-40%': 4,
        '40-60%': 6,
        '60-80%': 8,
        '80-100%': 10,
    }

    scores = []
    details = []

    for answer in answers:
        if not isinstance(answer, dict):
            continue

        field_type = answer.get('type', '')
        field_title = answer.get('field', {}).get('title', '')

        # Skip contact info and email fields
        if field_type in ['contact_info', 'email', 'phone_number']:
            continue

        value = get_answer_value(answer)

        # Calculate score based on answer
        score = 5  # Default middle score

        if isinstance(value, str):
            value_lower = value.lower()
            for key, mapped_score in score_mapping.items():
                if key in value_lower:
                    score = mapped_score
                    break

        elif isinstance(value, (int, float)):
            # Rating scales are typically 1-5 or 1-10
            if value <= 5:
                score = value * 2  # Scale 1-5 to 2-10
            else:
                score = value  # Already 1-10

        if isinstance(score, (int, float)) and score > 0:
            scores.append(score)
            details.append({
                'question': field_title,
                'answer': str(value),
                'score': score
            })

    # Calculate overall score
    if scores:
        overall_score = round(sum(scores) / len(scores) * 10)  # Scale to 0-100
    else:
        overall_score = 50  # Default

    # Determine maturity level
    if overall_score >= 80:
        level = 'Optimized'
        level_nl = 'Geoptimaliseerd'
    elif overall_score >= 60:
        level = 'Managed'
        level_nl = 'Gemanaged'
    elif overall_score >= 40:
        level = 'Developing'
        level_nl = 'In Ontwikkeling'
    else:
        level = 'Initial'
        level_nl = 'Initieel'

    return {
        'score': overall_score,
        'level': level,
        'level_nl': level_nl,
        'details': details,
        'num_questions': len(scores)
    }


# ==============================================================================
# APK REPORT GENERATION (CLAUDE AI)
# ==============================================================================

def generate_apk_report(assessment_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate detailed APK report using Claude AI"""
    if not CLAUDE_API_KEY:
        logger.warning("Claude API key not configured, using basic report")
        return generate_basic_report(assessment_data)

    try:
        score = assessment_data.get('maturity_score', 50)
        level = assessment_data.get('maturity_level', 'Developing')
        company = assessment_data.get('company_name', 'Uw organisatie')
        industry = assessment_data.get('industry', 'Niet opgegeven')
        answers = assessment_data.get('answer_scores', [])

        # Format answers for prompt
        answers_text = "\n".join([
            f"- {a['question']}: {a['answer']} (score: {a['score']}/10)"
            for a in answers[:15]  # Limit to first 15 questions
        ])

        prompt = f"""Je bent een expert Nederlandse recruitment consultant. Genereer een professioneel Recruitment APK rapport.

ASSESSMENT RESULTATEN:
- Bedrijf: {company}
- Sector: {industry}
- Maturity Score: {score}/100
- Maturity Level: {level}

ANTWOORDEN:
{answers_text}

Genereer een JSON response met deze structuur:
{{
    "overall_score": {score},
    "maturity_level": "{level}",
    "executive_summary": "2-3 zinnen samenvatting van de belangrijkste bevindingen",
    "strengths": [
        "Sterk punt 1 met concrete beschrijving",
        "Sterk punt 2 met concrete beschrijving",
        "Sterk punt 3 met concrete beschrijving"
    ],
    "improvement_areas": [
        {{
            "area": "Verbetergebied 1",
            "current_state": "Huidige situatie beschrijving",
            "recommendation": "Concrete aanbeveling",
            "impact": "Verwachte impact",
            "priority": "Hoog/Medium/Laag"
        }},
        {{
            "area": "Verbetergebied 2",
            "current_state": "Huidige situatie beschrijving",
            "recommendation": "Concrete aanbeveling",
            "impact": "Verwachte impact",
            "priority": "Hoog/Medium/Laag"
        }},
        {{
            "area": "Verbetergebied 3",
            "current_state": "Huidige situatie beschrijving",
            "recommendation": "Concrete aanbeveling",
            "impact": "Verwachte impact",
            "priority": "Hoog/Medium/Laag"
        }}
    ],
    "quick_wins": [
        "Quick win 1 - implementeerbaar binnen 1 week",
        "Quick win 2 - implementeerbaar binnen 1 week",
        "Quick win 3 - implementeerbaar binnen 1 week"
    ],
    "benchmark_comparison": {{
        "vs_industry_average": "+5% / -5% / gelijk aan",
        "vs_top_performers": "beschrijving hoe ver van top performers",
        "improvement_potential": "percentage verbetering mogelijk"
    }},
    "roadmap": {{
        "month_1": ["Actie 1", "Actie 2"],
        "month_2_3": ["Actie 3", "Actie 4"],
        "month_4_6": ["Actie 5", "Actie 6"]
    }},
    "kpis_to_track": [
        "KPI 1 met target",
        "KPI 2 met target",
        "KPI 3 met target"
    ]
}}

Zorg dat alle tekst in het Nederlands is en praktisch toepasbaar voor een Nederlands bedrijf."""

        headers = {
            'Content-Type': 'application/json',
            'x-api-key': CLAUDE_API_KEY,
            'anthropic-version': '2023-06-01'
        }

        payload = {
            'model': 'claude-3-5-sonnet-20241022',
            'max_tokens': 4000,
            'messages': [{'role': 'user', 'content': prompt}]
        }

        response = requests.post(
            'https://api.anthropic.com/v1/messages',
            headers=headers,
            json=payload,
            timeout=60
        )

        if response.status_code == 200:
            result = response.json()
            content = result['content'][0]['text']

            # Extract JSON from response
            json_start = content.find('{')
            json_end = content.rfind('}') + 1

            if json_start != -1 and json_end > json_start:
                report = json.loads(content[json_start:json_end])
                report['generated_by'] = 'claude'
                return report

        logger.error(f"Claude API error: {response.status_code}")
        return generate_basic_report(assessment_data)

    except Exception as e:
        logger.error(f"Report generation error: {str(e)}")
        return generate_basic_report(assessment_data)


def generate_basic_report(assessment_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate basic report without AI"""
    score = assessment_data.get('maturity_score', 50)
    level = assessment_data.get('maturity_level', 'Developing')

    return {
        'overall_score': score,
        'maturity_level': level,
        'executive_summary': f'Uw recruitment maturity score is {score}/100. Dit plaatst uw organisatie in de "{level}" fase.',
        'strengths': ['Score berekend op basis van uw antwoorden'],
        'improvement_areas': [
            {
                'area': 'Algemene verbetering',
                'recommendation': 'Bekijk de gedetailleerde resultaten',
                'priority': 'Medium'
            }
        ],
        'quick_wins': ['Implementeer de belangrijkste aanbevelingen'],
        'generated_by': 'basic'
    }


# ==============================================================================
# PIPEDRIVE INTEGRATION
# ==============================================================================

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
        else:
            logger.error(f"Pipedrive API error: {response.status_code}")
            return None

    except Exception as e:
        logger.error(f"Pipedrive request error: {str(e)}")
        return None


def create_or_update_pipedrive_deal(assessment_data: Dict, report: Dict) -> Optional[Dict]:
    """Create or update Pipedrive deal with APK results"""
    try:
        email = assessment_data.get('email', '')
        company = assessment_data.get('company_name', 'Onbekend')
        first_name = assessment_data.get('first_name', '')
        last_name = assessment_data.get('last_name', '')
        phone = assessment_data.get('phone', '')
        score = report.get('overall_score', 50)

        # Find or create person
        person_result = pipedrive_request("GET", f"persons/search?term={email}&fields=email")
        person_id = None

        if person_result and person_result.get("success"):
            items = person_result.get("data", {}).get("items", [])
            if items:
                person_id = items[0].get("item", {}).get("id")

        if not person_id:
            person_data = {
                "name": f"{first_name} {last_name}".strip() or email.split('@')[0],
                "email": [{"value": email, "primary": True}],
            }
            if phone:
                person_data["phone"] = [{"value": phone, "primary": True}]

            result = pipedrive_request("POST", "persons", person_data)
            if result and result.get("success"):
                person_id = result.get("data", {}).get("id")

        # Find or create organization
        org_id = None
        if company and company != 'Onbekend':
            org_result = pipedrive_request("GET", f"organizations/search?term={company}")
            if org_result and org_result.get("success"):
                items = org_result.get("data", {}).get("items", [])
                if items:
                    org_id = items[0].get("item", {}).get("id")

            if not org_id:
                result = pipedrive_request("POST", "organizations", {"name": company})
                if result and result.get("success"):
                    org_id = result.get("data", {}).get("id")

        # Format improvement areas for Pipedrive
        improvements = report.get('improvement_areas', [])
        improvements_text = "\n".join([
            f"• {imp.get('area', '')}: {imp.get('recommendation', '')}"
            for imp in improvements[:3]
        ])

        # Create deal
        today = datetime.now().strftime("%Y-%m-%d")
        deal_data = {
            "title": f"APK - {company}",
            "pipeline_id": PIPELINE_ID,
            "stage_id": STAGE_APK_VERZONDEN,  # This triggers email automation
            "person_id": person_id,
            FIELD_KEYS["apk_verzonden_op"]: today,
            FIELD_KEYS["apk_score"]: score,
            FIELD_KEYS["email_sequence_status"]: "Actief",
            FIELD_KEYS["typeform_response_id"]: assessment_data.get('response_id', ''),
            FIELD_KEYS["verbeterpunten"]: improvements_text,
        }

        if org_id:
            deal_data["org_id"] = org_id

        result = pipedrive_request("POST", "deals", deal_data)
        if result and result.get("success"):
            deal = result.get("data", {})
            logger.info(f"Created Pipedrive deal: {deal.get('id')}")
            return deal

        return None

    except Exception as e:
        logger.error(f"Pipedrive deal creation error: {str(e)}")
        return None


# ==============================================================================
# EMAIL SENDING
# ==============================================================================

def send_apk_email(assessment_data: Dict, report: Dict) -> bool:
    """Send APK report email to the contact"""
    if not SMTP_PASS:
        logger.warning("SMTP password not configured, skipping email")
        return False

    try:
        to_email = assessment_data.get('email', '')
        first_name = assessment_data.get('first_name', '')
        company = assessment_data.get('company_name', 'uw organisatie')
        score = report.get('overall_score', 50)
        level = report.get('maturity_level', 'Developing')
        summary = report.get('executive_summary', '')

        # Format improvements
        improvements = report.get('improvement_areas', [])
        improvements_html = ""
        for imp in improvements[:3]:
            improvements_html += f"""
            <tr>
                <td style="padding: 15px; border-left: 4px solid #FF6B35; background-color: #F9FAFB;">
                    <strong style="color: #1E3A8A;">{imp.get('area', '')}</strong><br>
                    <span style="color: #374151;">{imp.get('recommendation', '')}</span><br>
                    <span style="color: #6B7280; font-size: 12px;">Prioriteit: {imp.get('priority', 'Medium')}</span>
                </td>
            </tr>
            <tr><td style="height: 10px;"></td></tr>
            """

        # Format quick wins
        quick_wins = report.get('quick_wins', [])
        quick_wins_html = "".join([f"<li style='margin-bottom: 8px;'>{qw}</li>" for qw in quick_wins[:3]])

        html_content = f"""
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f5f5f5;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f5f5f5;">
        <tr>
            <td style="padding: 20px;">
                <table width="600" cellpadding="0" cellspacing="0" style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; overflow: hidden;">
                    <!-- Header -->
                    <tr>
                        <td style="background-color: #1E3A8A; padding: 30px; text-align: center;">
                            <h1 style="color: #ffffff; margin: 0; font-size: 24px;">Recruitment APK</h1>
                            <p style="color: #93C5FD; margin: 10px 0 0; font-size: 14px;">Uw persoonlijke assessment rapport</p>
                        </td>
                    </tr>

                    <!-- Score Section -->
                    <tr>
                        <td style="padding: 30px; text-align: center; background-color: #F0F9FF;">
                            <p style="color: #1E3A8A; margin: 0 0 10px; font-size: 16px;">Uw Recruitment Maturity Score</p>
                            <div style="display: inline-block; width: 120px; height: 120px; border-radius: 50%; background-color: #FF6B35; line-height: 120px; text-align: center;">
                                <span style="color: #ffffff; font-size: 36px; font-weight: bold;">{score}</span>
                            </div>
                            <p style="color: #374151; margin: 15px 0 0; font-size: 18px;">Niveau: <strong>{level}</strong></p>
                        </td>
                    </tr>

                    <!-- Content -->
                    <tr>
                        <td style="padding: 30px;">
                            <p style="color: #374151; font-size: 15px; line-height: 1.6;">
                                Hoi {first_name or 'daar'},
                            </p>
                            <p style="color: #374151; font-size: 15px; line-height: 1.6;">
                                Bedankt voor het invullen van de Recruitment APK voor <strong>{company}</strong>.
                                Hieronder vind je een samenvatting van de resultaten.
                            </p>
                            <p style="color: #374151; font-size: 15px; line-height: 1.6; background-color: #F3F4F6; padding: 15px; border-radius: 6px;">
                                {summary}
                            </p>

                            <h2 style="color: #1E3A8A; font-size: 18px; margin-top: 30px;">Top 3 Verbeterpunten</h2>
                            <table width="100%" cellpadding="0" cellspacing="0">
                                {improvements_html}
                            </table>

                            <h2 style="color: #1E3A8A; font-size: 18px; margin-top: 30px;">Quick Wins</h2>
                            <ul style="color: #374151; font-size: 14px; line-height: 1.8; padding-left: 20px;">
                                {quick_wins_html}
                            </ul>

                            <!-- CTA -->
                            <table width="100%" cellpadding="0" cellspacing="0" style="margin-top: 30px;">
                                <tr>
                                    <td style="padding: 25px; background-color: #F0F9FF; border-radius: 8px; text-align: center;">
                                        <p style="color: #1E3A8A; font-size: 16px; margin: 0 0 15px;">
                                            <strong>Wil je deze resultaten samen bespreken?</strong>
                                        </p>
                                        <a href="https://calendly.com/wouter-arts-/recruitment-apk-review"
                                           style="display: inline-block; background-color: #FF6B35; color: #ffffff; padding: 14px 28px; text-decoration: none; border-radius: 6px; font-weight: bold;">
                                            Plan een gratis gesprek (30 min)
                                        </a>
                                    </td>
                                </tr>
                            </table>

                            <p style="color: #374151; font-size: 15px; line-height: 1.6; margin-top: 30px;">
                                Groeten,<br>
                                <strong>Wouter</strong><br>
                                <span style="color: #6B7280; font-size: 13px;">recruitmentapk.nl</span>
                            </p>
                        </td>
                    </tr>

                    <!-- Footer -->
                    <tr>
                        <td style="padding: 20px 30px; background-color: #F9FAFB; border-top: 1px solid #E5E7EB;">
                            <p style="color: #9CA3AF; font-size: 12px; margin: 0; text-align: center;">
                                © {datetime.now().year} recruitmentapk.nl | warts@recruitin.nl
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""

        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"Je Recruitment APK - Score: {score}/100"
        msg['From'] = f"Recruitment APK <{SMTP_USER}>"
        msg['To'] = to_email

        # Plain text version
        text_content = f"""
Hoi {first_name or 'daar'},

Je Recruitment APK score: {score}/100
Maturity Level: {level}

{summary}

Plan een gratis gesprek: https://calendly.com/wouter-arts-/recruitment-apk-review

Groeten,
Wouter
recruitmentapk.nl
"""

        msg.attach(MIMEText(text_content, 'plain'))
        msg.attach(MIMEText(html_content, 'html'))

        # Send email
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)

        logger.info(f"APK email sent to {to_email}")
        return True

    except Exception as e:
        logger.error(f"Email sending error: {str(e)}")
        return False


# ==============================================================================
# MAIN
# ==============================================================================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
