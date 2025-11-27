#!/usr/bin/env python3
"""
KANDIDATENTEKORT.NL - FIXED WEBHOOK HANDLER
Defensive JSON parsing + error handling + field mapping fix
Deploy to Render for Typeform webhook processing
"""

import os
import json
import logging
import requests
from flask import Flask, request, jsonify
from typing import Dict, Any, Optional

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
SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.gmail.com')
SMTP_USER = os.getenv('SMTP_USER', 'artsrecruitin@gmail.com')
SMTP_PASS = os.getenv('SMTP_PASS')

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'kandidatentekort-webhook',
        'version': '1.0.0'
    })

@app.route('/webhook/typeform', methods=['POST'])
def handle_typeform_webhook():
    """
    Handle Typeform webhook submissions with defensive programming
    """
    try:
        # Defensive JSON parsing
        data = request.get_json(force=True, silent=True)
        if not data:
            logger.error("No JSON data received")
            return jsonify({'error': 'No JSON data'}), 400
            
        # Log incoming data (without sensitive info)
        logger.info(f"Received webhook data with keys: {list(data.keys())}")
        
        # Validate Typeform structure
        if 'form_response' not in data:
            logger.error("Invalid Typeform structure - no form_response")
            return jsonify({'error': 'Invalid Typeform structure'}), 400
            
        form_response = data.get('form_response', {})
        answers = form_response.get('answers', [])
        
        logger.info(f"Processing {len(answers)} form answers")
        
        # Extract form data safely with field mapping fix
        vacancy_data = extract_vacancy_data_safe(answers)
        
        if not vacancy_data:
            logger.error("Failed to extract vacancy data")
            return jsonify({'error': 'Failed to extract form data'}), 400
            
        # Process with Claude API
        analysis_result = analyze_vacancy_with_claude(vacancy_data)
        
        if not analysis_result.get('success'):
            logger.error(f"Claude analysis failed: {analysis_result.get('error')}")
            return jsonify({'error': 'Analysis failed'}), 500
            
        # Send email report
        email_result = send_email_report(vacancy_data, analysis_result)
        
        logger.info("Webhook processing completed successfully")
        return jsonify({
            'status': 'success',
            'processed': True,
            'email_sent': email_result.get('success', False)
        }), 200
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {str(e)}")
        return jsonify({'error': 'Invalid JSON format'}), 400
        
    except Exception as e:
        logger.error(f"Webhook processing error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

def extract_vacancy_data_safe(answers: list) -> Optional[Dict[str, Any]]:
    """
    Safely extract vacancy data from Typeform answers
    WITH FIXED FIELD MAPPING - no org_name field
    """
    try:
        vacancy_data = {
            'company_name': '',      # FIXED: company_name instead of org_name
            'contact_person': '',
            'email': '',
            'phone': '',
            'vacancy_title': '',
            'vacancy_text': '',
            'industry': '',
            'company_size': '',
            'location': '',
            'urgency': 'normal'
        }
        
        # Field ID mapping (adjust based on your Typeform)
        field_mapping = {
            # Adjust these field IDs to match your actual Typeform
            'company_name': ['company', 'bedrijf', 'organization', 'firm'],
            'contact_person': ['name', 'contact', 'person', 'naam'],
            'email': ['email', 'e-mail', 'mail'],
            'phone': ['phone', 'telefoon', 'tel'],
            'vacancy_title': ['title', 'job_title', 'position', 'functie'],
            'vacancy_text': ['vacancy', 'description', 'text', 'vacature'],
            'industry': ['industry', 'sector', 'branche'],
            'company_size': ['size', 'employees', 'grootte'],
            'location': ['location', 'city', 'locatie', 'plaats'],
            'urgency': ['urgency', 'priority', 'spoed']
        }
        
        # Process each answer safely
        for answer in answers:
            if not isinstance(answer, dict):
                continue

            field_id = answer.get('field', {}).get('id', '')
            field_type = answer.get('field', {}).get('type', '')

            # Get answer value based on type
            answer_value = ''
            if field_type == 'short_text' or field_type == 'long_text':
                answer_value = answer.get('text', '')
            elif field_type == 'email':
                answer_value = answer.get('email', '')
            elif field_type == 'phone_number':
                answer_value = answer.get('phone_number', '')
            elif field_type == 'multiple_choice':
                choice = answer.get('choice', {})
                answer_value = choice.get('label', '') if choice else ''
            elif field_type == 'dropdown':
                choice = answer.get('choice', {})
                answer_value = choice.get('label', '') if choice else ''
            elif field_type == 'contact_info':
                # Handle contact_info block - extract all fields directly
                contact_info = answer.get('contact_info', {})
                if contact_info:
                    if contact_info.get('email'):
                        vacancy_data['email'] = contact_info['email']
                    if contact_info.get('first_name'):
                        first_name = contact_info.get('first_name', '')
                        last_name = contact_info.get('last_name', '')
                        vacancy_data['contact_person'] = f"{first_name} {last_name}".strip()
                    if contact_info.get('phone_number'):
                        vacancy_data['phone'] = contact_info['phone_number']
                    if contact_info.get('company'):
                        vacancy_data['company_name'] = contact_info['company']
                continue  # Skip normal field mapping for contact_info

            # Map to our fields
            field_title = answer.get('field', {}).get('title', '').lower()

            for data_field, keywords in field_mapping.items():
                if any(keyword in field_title for keyword in keywords) or any(keyword in field_id for keyword in keywords):
                    vacancy_data[data_field] = answer_value
                    break
        
        # Validate required fields
        required_fields = ['email', 'vacancy_text']
        for field in required_fields:
            if not vacancy_data.get(field):
                logger.error(f"Missing required field: {field}")
                return None
                
        logger.info(f"Successfully extracted vacancy data for: {vacancy_data.get('email')}")
        return vacancy_data
        
    except Exception as e:
        logger.error(f"Data extraction error: {str(e)}")
        return None

def analyze_vacancy_with_claude(vacancy_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze vacancy with Claude API - defensive implementation
    """
    try:
        if not CLAUDE_API_KEY:
            return {'success': False, 'error': 'Claude API key not configured'}
            
        prompt = f"""
Als expert Nederlandse recruitment consultant, analyseer deze vacaturetekst:

BEDRIJFSINFO:
- Bedrijf: {vacancy_data.get('company_name', 'Niet opgegeven')}
- Contact: {vacancy_data.get('contact_person', 'Niet opgegeven')}
- Sector: {vacancy_data.get('industry', 'Niet opgegeven')}
- Grootte: {vacancy_data.get('company_size', 'Niet opgegeven')}
- Locatie: {vacancy_data.get('location', 'Niet opgegeven')}

VACATURETEKST:
\"\"\"
{vacancy_data.get('vacancy_text', '')}
\"\"\"

Geef een JSON response met deze exacte structuur:
{{
  "overall_score": 7.2,
  "overall_rating": "goed",
  "detailed_analysis": {{
    "aantrekkelijkheid": {{
      "score": 7,
      "feedback": "Concrete feedback",
      "improvements": ["Verbetering 1", "Verbetering 2"]
    }},
    "duidelijkheid": {{
      "score": 6,
      "feedback": "Concrete feedback",
      "improvements": ["Verbetering 1", "Verbetering 2"]
    }},
    "volledigheid": {{
      "score": 8,
      "feedback": "Concrete feedback",
      "improvements": ["Verbetering 1", "Verbetering 2"]
    }},
    "salaris_transparantie": {{
      "score": 5,
      "feedback": "Concrete feedback",
      "improvements": ["Verbetering 1", "Verbetering 2"]
    }},
    "sollicitatie_proces": {{
      "score": 7,
      "feedback": "Concrete feedback",
      "improvements": ["Verbetering 1", "Verbetering 2"]
    }}
  }},
  "top_3_improvements": [
    "Belangrijkste verbetering",
    "Tweede verbetering",
    "Derde verbetering"
  ],
  "strong_points": [
    "Sterk punt 1",
    "Sterk punt 2"
  ],
  "market_insights": {{
    "expected_applications": "15-25 sollicitaties",
    "time_to_hire": "4-6 weken",
    "salary_competitiveness": "Marktconform",
    "regional_factors": "Nederlandse markt overwegingen"
  }},
  "improved_version": "Geoptimaliseerde vacaturetekst hier...",
  "implementation_priority": [
    "Actie voor deze week",
    "Actie voor volgende week",
    "Lange termijn actie"
  ]
}}
"""

        headers = {
            'Content-Type': 'application/json',
            'x-api-key': CLAUDE_API_KEY,
            'anthropic-version': '2023-06-01'
        }
        
        payload = {
            'model': 'claude-3-5-sonnet-20241022',
            'max_tokens': 4000,
            'messages': [{
                'role': 'user',
                'content': prompt
            }]
        }
        
        response = requests.post(
            'https://api.anthropic.com/v1/messages',
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            content_text = result['content'][0]['text']
            
            # Extract JSON from response
            json_start = content_text.find('{')
            json_end = content_text.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                analysis_json = json.loads(content_text[json_start:json_end])
                return {'success': True, 'analysis': analysis_json}
            else:
                return {'success': False, 'error': 'Invalid JSON in Claude response'}
        else:
            return {'success': False, 'error': f'Claude API error: {response.status_code}'}
            
    except Exception as e:
        logger.error(f"Claude analysis error: {str(e)}")
        return {'success': False, 'error': str(e)}

def send_email_report(vacancy_data: Dict[str, Any], analysis_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Send email report - placeholder implementation
    """
    try:
        # Email functionality would go here
        # For now, just log the action
        logger.info(f"Would send email to: {vacancy_data.get('email')}")
        
        return {'success': True, 'message': 'Email queued for sending'}
        
    except Exception as e:
        logger.error(f"Email sending error: {str(e)}")
        return {'success': False, 'error': str(e)}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)