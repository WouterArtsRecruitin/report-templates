#!/usr/bin/env python3
"""
KANDIDATENTEKORT.NL - SIMPLIFIED WEBHOOK HANDLER
Focus on Typeform → Claude → Email workflow (Pipedrive disabled)
"""

import os
import json
import logging
import requests
from flask import Flask, request, jsonify
from typing import Dict, Any, Optional

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Environment variables
CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')
SMTP_USER = os.getenv('SMTP_USER', 'artsrecruitin@gmail.com')

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'kandidatentekort-simplified',
        'version': '2.0.0',
        'pipedrive_disabled': True
    })

@app.route('/webhook/typeform', methods=['POST'])
def handle_typeform_webhook():
    try:
        # Log raw request data
        logger.info("=== TYPEFORM WEBHOOK RECEIVED ===")
        logger.info(f"Content-Type: {request.content_type}")
        logger.info(f"Method: {request.method}")
        
        # Get raw data
        raw_data = request.get_data(as_text=True)
        logger.info(f"Raw data length: {len(raw_data)} chars")
        
        # Try to parse JSON
        try:
            data = json.loads(raw_data) if raw_data else {}
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            data = {}
        
        logger.info(f"Parsed data keys: {list(data.keys()) if data else 'No data'}")
        
        # Check for Typeform structure
        if 'form_response' not in data:
            logger.warning("No form_response found - might be test data")
            return jsonify({
                'status': 'received',
                'message': 'Webhook received but no form_response found',
                'debug': {
                    'content_type': request.content_type,
                    'data_keys': list(data.keys()) if data else [],
                    'raw_length': len(raw_data)
                }
            }), 200
        
        # Extract form data
        form_response = data.get('form_response', {})
        answers = form_response.get('answers', [])
        
        logger.info(f"Processing {len(answers)} answers")
        
        # Simple data extraction
        extracted_data = {
            'email': 'test@example.com',  # Default for testing
            'company_name': 'Test Company',
            'vacancy_text': 'Test vacancy description',
            'contact_person': 'Test User'
        }
        
        # Try to extract from answers
        for i, answer in enumerate(answers):
            logger.info(f"Answer {i}: {answer}")

            # Handle contact_info block (Typeform contact info fields)
            if isinstance(answer, dict):
                field_type = answer.get('field', {}).get('type', '') if 'field' in answer else answer.get('type', '')

                if field_type == 'contact_info' or 'contact_info' in answer:
                    contact_info = answer.get('contact_info', {})
                    if contact_info:
                        if contact_info.get('email'):
                            extracted_data['email'] = contact_info['email']
                        if contact_info.get('first_name'):
                            first_name = contact_info.get('first_name', '')
                            last_name = contact_info.get('last_name', '')
                            extracted_data['contact_person'] = f"{first_name} {last_name}".strip()
                        if contact_info.get('company'):
                            extracted_data['company_name'] = contact_info['company']
                        continue

            # Extract email if available (standalone email field)
            if 'email' in str(answer).lower():
                if isinstance(answer, dict) and 'email' in answer:
                    extracted_data['email'] = answer['email']

            # Extract text answers
            if isinstance(answer, dict) and 'text' in answer:
                text_value = answer['text']
                if len(text_value) > 50:  # Likely vacancy text
                    extracted_data['vacancy_text'] = text_value
                elif '@' not in text_value and len(text_value) < 50:  # Likely name/company
                    if 'company' in str(answer).lower():
                        extracted_data['company_name'] = text_value
                    else:
                        extracted_data['contact_person'] = text_value
        
        logger.info(f"Extracted data: {extracted_data}")
        
        # Analyze with Claude (simplified)
        claude_result = analyze_with_claude_simple(extracted_data)
        
        logger.info("=== PROCESSING COMPLETE ===")
        return jsonify({
            'status': 'success',
            'processed': True,
            'email_sent': False,  # Email functionality disabled for now
            'claude_analysis': claude_result.get('success', False),
            'extracted_data': {
                'email': extracted_data.get('email'),
                'company': extracted_data.get('company_name'),
                'has_vacancy_text': len(extracted_data.get('vacancy_text', '')) > 10
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Webhook error: {str(e)}")
        return jsonify({
            'error': f'Processing error: {str(e)}',
            'debug_info': {
                'content_type': request.content_type,
                'method': request.method,
                'has_data': bool(request.get_data())
            }
        }), 500

@app.route('/test', methods=['GET'])
def test_endpoint():
    email = request.args.get('email', 'test@example.com')
    
    # Simulate successful processing without Pipedrive
    test_data = {
        'email': email,
        'company_name': 'Test BV',
        'vacancy_text': 'Software Developer gezocht voor innovatief bedrijf. Werk met moderne technologieën.',
        'contact_person': 'Test User'
    }
    
    logger.info(f"Test endpoint called with email: {email}")
    
    # Test Claude analysis
    claude_result = analyze_with_claude_simple(test_data)
    
    return jsonify({
        'status': 'success',
        'test_mode': True,
        'pipedrive_disabled': True,
        'claude_analysis': claude_result.get('success', False),
        'message': 'Test completed without Pipedrive integration'
    })

def analyze_with_claude_simple(vacancy_data: Dict[str, Any]) -> Dict[str, Any]:
    """Simplified Claude analysis"""
    try:
        if not CLAUDE_API_KEY:
            logger.warning("Claude API key not available")
            return {'success': False, 'error': 'No API key'}
        
        prompt = f"""
Analyseer deze Nederlandse vacature kort:

Bedrijf: {vacancy_data.get('company_name', 'Niet bekend')}
Vacature: {vacancy_data.get('vacancy_text', 'Geen tekst')}

Geef alleen een score van 1-10 en de belangrijkste verbetering.
"""
        
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': CLAUDE_API_KEY,
            'anthropic-version': '2023-06-01'
        }
        
        payload = {
            'model': 'claude-3-5-sonnet-20241022',
            'max_tokens': 500,
            'messages': [{'role': 'user', 'content': prompt}]
        }
        
        response = requests.post(
            'https://api.anthropic.com/v1/messages',
            headers=headers,
            json=payload,
            timeout=15
        )
        
        if response.status_code == 200:
            logger.info("Claude analysis successful")
            return {'success': True, 'response': 'Analysis completed'}
        else:
            logger.error(f"Claude API error: {response.status_code}")
            return {'success': False, 'error': f'API error {response.status_code}'}
            
    except Exception as e:
        logger.error(f"Claude analysis error: {str(e)}")
        return {'success': False, 'error': str(e)}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting simplified webhook handler on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)