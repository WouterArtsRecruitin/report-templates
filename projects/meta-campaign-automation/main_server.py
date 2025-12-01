#!/usr/bin/env python3
"""
META CAMPAIGN AUTOMATION SERVER
===============================
Main Flask server integrating all Meta campaign automation components.

Endpoints:
- /                                 - Health check
- /webhook/meta-leads               - Meta Lead Ads webhook
- /webhook/typeform                 - Typeform webhook with conversion tracking
- /api/pixel/code                   - Get pixel installation code
- /api/conversion/lead              - Send lead conversion event
- /api/conversion/assessment        - Send assessment conversion event
- /api/campaigns                    - List/create campaigns
- /api/campaigns/<id>/insights      - Get campaign insights
- /api/audiences                    - List audience segments
- /api/report                       - Get performance report

Deploy to: Render, Railway, or Heroku
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Any
from flask import Flask, request, jsonify
from flask_cors import CORS

# Import our modules
from meta_api_client import MetaApiClient, MetaApiError, CampaignObjective
from pixel_tracking import (
    PixelCodeGenerator,
    ConversionAPI,
    UserData,
    CustomData,
    PixelConfig
)
from lead_ads_handler import LeadAdsWebhookHandler, LeadAdsConfig
from campaign_automation import (
    CampaignAutomationService,
    CampaignTemplates,
    AudienceBuilder
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize services
pixel_generator = PixelCodeGenerator()
conversion_api = ConversionAPI()
lead_handler = LeadAdsWebhookHandler()
audience_builder = AudienceBuilder()

# Lazy initialization for services that require tokens
_api_client = None
_campaign_service = None


def get_api_client() -> MetaApiClient:
    """Get or create Meta API client"""
    global _api_client
    if _api_client is None:
        _api_client = MetaApiClient()
    return _api_client


def get_campaign_service() -> CampaignAutomationService:
    """Get or create campaign automation service"""
    global _campaign_service
    if _campaign_service is None:
        _campaign_service = CampaignAutomationService(get_api_client())
    return _campaign_service


# ==============================================================================
# HEALTH CHECK ENDPOINTS
# ==============================================================================

@app.route('/', methods=['GET'])
def health_check():
    """Main health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'meta-campaign-automation',
        'version': '1.0.0',
        'pixel_id': PixelConfig.PIXEL_ID,
        'endpoints': {
            'webhooks': ['/webhook/meta-leads', '/webhook/typeform'],
            'pixel': ['/api/pixel/code', '/api/pixel/netlify'],
            'conversion': ['/api/conversion/lead', '/api/conversion/assessment'],
            'campaigns': ['/api/campaigns', '/api/audiences', '/api/report']
        }
    })


@app.route('/health', methods=['GET'])
def health():
    """Simple health check"""
    return jsonify({'status': 'ok'})


# ==============================================================================
# META LEAD ADS WEBHOOK
# ==============================================================================

@app.route('/webhook/meta-leads', methods=['GET', 'POST'])
def meta_leads_webhook():
    """
    Meta Lead Ads webhook endpoint

    GET: Webhook verification
    POST: Lead data processing
    """
    if request.method == 'GET':
        return lead_handler.verify_webhook(request)
    return lead_handler.process_webhook(request)


# ==============================================================================
# TYPEFORM WEBHOOK WITH CONVERSION TRACKING
# ==============================================================================

@app.route('/webhook/typeform', methods=['POST'])
def typeform_webhook():
    """
    Typeform webhook with Meta Conversion API tracking

    Receives Typeform submission and:
    1. Sends Lead event to Meta Conversion API
    2. Sends CompleteRegistration event
    3. Returns success response
    """
    try:
        data = request.get_json(force=True, silent=True)
        if not data:
            return jsonify({'error': 'No JSON data'}), 400

        logger.info(f"Received Typeform webhook")

        form_response = data.get('form_response', {})
        answers = form_response.get('answers', [])

        # Extract user data
        user_data = extract_user_data_from_typeform(answers)

        # Send conversion events
        event_results = []

        # Lead event
        lead_result = conversion_api.send_lead_event(
            user_data=user_data,
            content_name='Kandidatentekort Assessment',
            value=50
        )
        event_results.append({'event': 'Lead', 'result': lead_result})

        # CompleteRegistration event
        registration_result = conversion_api.send_assessment_complete_event(
            user_data=user_data,
            event_source_url='https://kandidatentekort.nl/assessment'
        )
        event_results.append({'event': 'CompleteRegistration', 'result': registration_result})

        logger.info(f"Conversion events sent for {user_data.email}")

        return jsonify({
            'status': 'success',
            'email': user_data.email,
            'conversion_events': event_results
        }), 200

    except Exception as e:
        logger.error(f"Typeform webhook error: {str(e)}")
        return jsonify({'error': str(e)}), 500


def extract_user_data_from_typeform(answers: list) -> UserData:
    """Extract user data from Typeform answers"""
    user_data = UserData()

    for answer in answers:
        if not isinstance(answer, dict):
            continue

        field_type = answer.get('type', '')
        field_title = answer.get('field', {}).get('title', '').lower()

        if field_type == 'contact_info':
            contact_info = answer.get('contact_info', {})
            user_data.email = contact_info.get('email')
            user_data.phone = contact_info.get('phone_number')
            user_data.first_name = contact_info.get('first_name')
            user_data.last_name = contact_info.get('last_name')

        elif field_type == 'email':
            user_data.email = answer.get('email')

        elif field_type == 'phone_number':
            user_data.phone = answer.get('phone_number')

        elif field_type in ['short_text', 'long_text']:
            text = answer.get('text', '')
            if 'naam' in field_title or 'name' in field_title:
                if not user_data.first_name:
                    user_data.first_name = text
            elif 'bedrijf' in field_title or 'company' in field_title:
                pass  # CustomData, not UserData

    # Get IP and user agent from request
    user_data.client_ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_data.client_user_agent = request.headers.get('User-Agent')

    # Get Facebook cookies if available
    user_data.fbc = request.cookies.get('_fbc')
    user_data.fbp = request.cookies.get('_fbp')

    return user_data


# ==============================================================================
# PIXEL CODE ENDPOINTS
# ==============================================================================

@app.route('/api/pixel/code', methods=['GET'])
def get_pixel_code():
    """Get base Meta Pixel installation code"""
    return jsonify({
        'pixel_id': PixelConfig.PIXEL_ID,
        'code': pixel_generator.get_base_pixel_code(),
        'instructions': 'Add this code to the <head> section of your website'
    })


@app.route('/api/pixel/netlify', methods=['GET'])
def get_netlify_pixel_code():
    """Get complete Netlify-ready pixel integration code"""
    return jsonify({
        'pixel_id': PixelConfig.PIXEL_ID,
        'code': pixel_generator.get_netlify_integration_code(),
        'deploy_to': 'kandidatentekortv2.netlify.app',
        'instructions': [
            '1. Copy the code from the "code" field',
            '2. Add to your index.html or layout template',
            '3. Deploy to Netlify',
            '4. Verify in Facebook Pixel Helper extension'
        ]
    })


@app.route('/api/pixel/event/<event_name>', methods=['GET'])
def get_event_code(event_name: str):
    """Get JavaScript code for a specific event"""
    custom_data = request.args.to_dict()

    # Convert string values to appropriate types
    for key in ['value', 'num_items']:
        if key in custom_data:
            try:
                custom_data[key] = float(custom_data[key])
            except ValueError:
                pass

    code = pixel_generator.get_event_code(event_name, custom_data if custom_data else None)

    return jsonify({
        'event_name': event_name,
        'custom_data': custom_data,
        'code': code
    })


# ==============================================================================
# CONVERSION API ENDPOINTS
# ==============================================================================

@app.route('/api/conversion/lead', methods=['POST'])
def send_lead_conversion():
    """
    Send Lead conversion event to Meta Conversion API

    Request body:
    {
        "email": "user@example.com",
        "phone": "+31612345678",
        "first_name": "John",
        "last_name": "Doe",
        "content_name": "Vacature Analyse",
        "value": 50
    }
    """
    try:
        data = request.get_json()

        user_data = UserData(
            email=data.get('email'),
            phone=data.get('phone'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            client_ip_address=request.headers.get('X-Forwarded-For', request.remote_addr),
            client_user_agent=request.headers.get('User-Agent'),
            fbc=request.cookies.get('_fbc'),
            fbp=request.cookies.get('_fbp')
        )

        result = conversion_api.send_lead_event(
            user_data=user_data,
            content_name=data.get('content_name', 'Kandidatentekort Lead'),
            value=data.get('value', 50)
        )

        return jsonify({
            'status': 'success',
            'result': result
        })

    except Exception as e:
        logger.error(f"Lead conversion error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/conversion/assessment', methods=['POST'])
def send_assessment_conversion():
    """
    Send Assessment completion conversion events

    Request body:
    {
        "email": "user@example.com",
        "score": 75,
        "assessment_type": "vacancy_analysis"
    }
    """
    try:
        data = request.get_json()

        user_data = UserData(
            email=data.get('email'),
            phone=data.get('phone'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            client_ip_address=request.headers.get('X-Forwarded-For', request.remote_addr),
            client_user_agent=request.headers.get('User-Agent')
        )

        results = []

        # Send InitiateCheckout (assessment started)
        if data.get('event') == 'start':
            result = conversion_api.send_assessment_start_event(user_data=user_data)
            results.append({'event': 'InitiateCheckout', 'result': result})

        # Send CompleteRegistration (assessment completed)
        if data.get('event') == 'complete' or not data.get('event'):
            result = conversion_api.send_assessment_complete_event(
                user_data=user_data,
                score=data.get('score')
            )
            results.append({'event': 'CompleteRegistration', 'result': result})

            # Also send Lead event
            lead_result = conversion_api.send_lead_event(
                user_data=user_data,
                content_name=data.get('assessment_type', 'Vacancy Assessment'),
                value=data.get('value', 50)
            )
            results.append({'event': 'Lead', 'result': lead_result})

        return jsonify({
            'status': 'success',
            'events_sent': results
        })

    except Exception as e:
        logger.error(f"Assessment conversion error: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ==============================================================================
# CAMPAIGN MANAGEMENT ENDPOINTS
# ==============================================================================

@app.route('/api/campaigns', methods=['GET', 'POST'])
def campaigns():
    """
    GET: List all campaigns
    POST: Create campaign from template
    """
    try:
        if request.method == 'GET':
            client = get_api_client()
            campaigns = client.get_campaigns()
            return jsonify({
                'status': 'success',
                'campaigns': campaigns
            })

        elif request.method == 'POST':
            data = request.get_json()
            template_name = data.get('template')
            status = data.get('status', 'PAUSED')

            # Find template
            templates = CampaignTemplates.get_all_templates()
            template = next(
                (t for t in templates if t.name == template_name),
                None
            )

            if not template:
                return jsonify({
                    'error': 'Template not found',
                    'available_templates': [t.name for t in templates]
                }), 400

            service = get_campaign_service()
            result = service.create_campaign_from_template(template, status)

            return jsonify({
                'status': 'success',
                'result': result
            })

    except MetaApiError as e:
        return jsonify({'error': e.message}), 400
    except Exception as e:
        logger.error(f"Campaign error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/campaigns/<campaign_id>/insights', methods=['GET'])
def campaign_insights(campaign_id: str):
    """Get insights for a specific campaign"""
    try:
        days = request.args.get('days', 7, type=int)
        client = get_api_client()
        insights = client.get_campaign_insights(campaign_id, f'last_{days}d')

        return jsonify({
            'status': 'success',
            'campaign_id': campaign_id,
            'period': f'last_{days}d',
            'insights': insights
        })

    except MetaApiError as e:
        return jsonify({'error': e.message}), 400


@app.route('/api/templates', methods=['GET'])
def get_templates():
    """Get available campaign templates"""
    templates = CampaignTemplates.get_all_templates()

    return jsonify({
        'status': 'success',
        'templates': [
            {
                'name': t.name,
                'description': t.description,
                'objective': t.objective.value,
                'daily_budget_eur': t.daily_budget / 100,
                'audience_segments': [s.value for s in t.audience_segments],
                'ad_variants': len(t.ad_copy_variants)
            }
            for t in templates
        ]
    })


# ==============================================================================
# AUDIENCE ENDPOINTS
# ==============================================================================

@app.route('/api/audiences', methods=['GET'])
def get_audiences():
    """Get all pre-defined audience segments"""
    segments = audience_builder.get_all_segments()

    return jsonify({
        'status': 'success',
        'segments': [
            {
                'name': s.name,
                'description': s.description,
                'segment_key': s.segment.value,
                'estimated_reach': s.estimated_reach,
                'recommended_budget_eur': s.recommended_budget / 100
            }
            for s in segments
        ]
    })


@app.route('/api/audiences/<segment_key>/targeting', methods=['GET'])
def get_audience_targeting(segment_key: str):
    """Get targeting specification for an audience segment"""
    from campaign_automation import AudienceSegment

    try:
        segment = AudienceSegment(segment_key)
        targeting = audience_builder.get_targeting(segment)

        return jsonify({
            'status': 'success',
            'segment': segment_key,
            'targeting': targeting
        })

    except ValueError:
        return jsonify({
            'error': f'Unknown segment: {segment_key}',
            'available_segments': [s.value for s in AudienceSegment]
        }), 400


# ==============================================================================
# REPORTING ENDPOINTS
# ==============================================================================

@app.route('/api/report', methods=['GET'])
def get_report():
    """Get performance report for all campaigns"""
    try:
        days = request.args.get('days', 7, type=int)
        service = get_campaign_service()
        report = service.get_performance_report(days)

        return jsonify({
            'status': 'success',
            'report': report
        })

    except MetaApiError as e:
        return jsonify({'error': e.message}), 400


@app.route('/api/report/recommendations', methods=['GET'])
def get_recommendations():
    """Get budget optimization recommendations"""
    try:
        target_cpl = request.args.get('target_cpl', 25.0, type=float)
        service = get_campaign_service()
        recommendations = service.optimize_budgets(target_cpl)

        return jsonify({
            'status': 'success',
            'recommendations': recommendations
        })

    except MetaApiError as e:
        return jsonify({'error': e.message}), 400


# ==============================================================================
# TOKEN MANAGEMENT ENDPOINTS
# ==============================================================================

@app.route('/api/token/status', methods=['GET'])
def token_status():
    """Check OAuth token status"""
    try:
        client = get_api_client()
        token_info = client.get_token_info()

        return jsonify({
            'status': 'success',
            'token_valid': client.is_token_valid(),
            'token_type': token_info.token_type,
            'expires_at': token_info.expires_at.isoformat(),
            'scopes': token_info.scopes
        })

    except MetaApiError as e:
        return jsonify({
            'status': 'error',
            'token_valid': False,
            'error': e.message,
            'is_expired': e.is_token_expired() if hasattr(e, 'is_token_expired') else None
        })


@app.route('/api/token/refresh', methods=['POST'])
def refresh_token():
    """
    Refresh OAuth token

    Requires META_APP_ID and META_APP_SECRET environment variables
    """
    try:
        client = get_api_client()
        new_token = client.refresh_long_lived_token()

        return jsonify({
            'status': 'success',
            'message': 'Token refreshed successfully',
            'new_token_preview': new_token[:20] + '...' if new_token else None
        })

    except MetaApiError as e:
        return jsonify({
            'status': 'error',
            'error': e.message
        }), 400


# ==============================================================================
# TEST ENDPOINTS
# ==============================================================================

@app.route('/test/lead', methods=['POST'])
def test_lead():
    """Test endpoint for simulating lead processing"""
    data = request.get_json() or {}

    # Create test user data
    user_data = UserData(
        email=data.get('email', 'test@example.com'),
        phone=data.get('phone', '+31612345678'),
        first_name=data.get('first_name', 'Test'),
        last_name=data.get('last_name', 'User')
    )

    results = []

    # Test conversion events
    if PixelConfig.ACCESS_TOKEN:
        lead_result = conversion_api.send_lead_event(
            user_data=user_data,
            content_name='Test Lead',
            value=50
        )
        results.append({'event': 'Lead', 'result': lead_result})

    return jsonify({
        'status': 'success',
        'test_data': {
            'email': user_data.email,
            'first_name': user_data.first_name
        },
        'conversion_results': results,
        'message': 'Test completed. Check Meta Events Manager for events.'
    })


# ==============================================================================
# MAIN
# ==============================================================================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'false').lower() == 'true'

    logger.info(f"Starting Meta Campaign Automation Server on port {port}")
    logger.info(f"Pixel ID: {PixelConfig.PIXEL_ID}")
    logger.info(f"Debug mode: {debug}")

    app.run(host='0.0.0.0', port=port, debug=debug)
