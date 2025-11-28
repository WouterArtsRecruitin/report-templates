#!/usr/bin/env python3
"""
META LEAD ADS WEBHOOK HANDLER
=============================
Process incoming leads from Meta Lead Ads and route to Slack, Pipedrive, and email.

Features:
- Webhook verification for Meta
- Lead data extraction and validation
- Slack notification to #high-priority-intakes
- Pipedrive deal creation
- Email notification to team
- Zapier webhook forwarding

Webhook URL: https://your-domain.com/webhook/meta-leads
"""

import os
import json
import hmac
import hashlib
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from flask import Flask, request, jsonify
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ==============================================================================
# CONFIGURATION
# ==============================================================================

class LeadAdsConfig:
    """Lead Ads Configuration"""
    # Meta App credentials
    APP_SECRET = os.getenv('META_APP_SECRET')
    ACCESS_TOKEN = os.getenv('META_ACCESS_TOKEN')
    VERIFY_TOKEN = os.getenv('META_WEBHOOK_VERIFY_TOKEN', 'kandidatentekort_verify_2024')
    PAGE_ID = os.getenv('META_PAGE_ID')

    # Slack configuration
    SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL')
    SLACK_CHANNEL = os.getenv('SLACK_CHANNEL', '#high-priority-intakes')

    # Pipedrive configuration
    PIPEDRIVE_API_TOKEN = os.getenv('PIPEDRIVE_API_TOKEN')
    PIPEDRIVE_BASE_URL = 'https://api.pipedrive.com/v1'
    PIPEDRIVE_PIPELINE_ID = int(os.getenv('PIPEDRIVE_PIPELINE_ID', '3'))  # Kandidatentekort pipeline
    PIPEDRIVE_STAGE_ID = int(os.getenv('PIPEDRIVE_STAGE_ID', '15'))  # New leads stage

    # Email configuration
    SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    SMTP_USER = os.getenv('SMTP_USER', 'artsrecruitin@gmail.com')
    SMTP_PASS = os.getenv('SMTP_PASS')
    NOTIFICATION_EMAIL = os.getenv('NOTIFICATION_EMAIL', 'warts@recruitin.nl')

    # Zapier webhook (optional)
    ZAPIER_WEBHOOK_URL = os.getenv('ZAPIER_WEBHOOK_URL')


@dataclass
class LeadData:
    """Extracted lead data from Meta Lead Ads"""
    lead_id: str
    form_id: str
    page_id: str
    ad_id: Optional[str]
    adset_id: Optional[str]
    campaign_id: Optional[str]
    created_time: str

    # Contact info
    email: Optional[str] = None
    phone: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None

    # Company info
    company_name: Optional[str] = None
    job_title: Optional[str] = None

    # Custom fields
    custom_fields: Dict[str, Any] = None


# ==============================================================================
# WEBHOOK HANDLERS
# ==============================================================================

class LeadAdsWebhookHandler:
    """
    Handle Meta Lead Ads webhooks

    Usage:
        handler = LeadAdsWebhookHandler()

        # In Flask route
        @app.route('/webhook/meta-leads', methods=['GET', 'POST'])
        def meta_leads_webhook():
            if request.method == 'GET':
                return handler.verify_webhook(request)
            return handler.process_webhook(request)
    """

    def __init__(self):
        self.app_secret = LeadAdsConfig.APP_SECRET
        self.access_token = LeadAdsConfig.ACCESS_TOKEN
        self.verify_token = LeadAdsConfig.VERIFY_TOKEN

    def verify_webhook(self, req) -> tuple:
        """
        Verify webhook subscription (GET request from Meta)

        Meta sends these parameters:
        - hub.mode: should be 'subscribe'
        - hub.verify_token: should match our verify token
        - hub.challenge: we return this to verify
        """
        mode = req.args.get('hub.mode')
        token = req.args.get('hub.verify_token')
        challenge = req.args.get('hub.challenge')

        if mode == 'subscribe' and token == self.verify_token:
            logger.info("Webhook verified successfully")
            return challenge, 200
        else:
            logger.warning(f"Webhook verification failed: mode={mode}, token={token}")
            return 'Forbidden', 403

    def verify_signature(self, payload: bytes, signature: str) -> bool:
        """
        Verify webhook signature from Meta

        Args:
            payload: Raw request body
            signature: X-Hub-Signature-256 header value
        """
        if not self.app_secret:
            logger.warning("APP_SECRET not set, skipping signature verification")
            return True

        if not signature:
            return False

        expected_signature = 'sha256=' + hmac.new(
            self.app_secret.encode('utf-8'),
            payload,
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(expected_signature, signature)

    def process_webhook(self, req) -> tuple:
        """
        Process incoming webhook (POST request from Meta)
        """
        try:
            # Verify signature
            signature = req.headers.get('X-Hub-Signature-256')
            payload = req.get_data()

            if not self.verify_signature(payload, signature):
                logger.warning("Invalid webhook signature")
                return jsonify({'error': 'Invalid signature'}), 403

            # Parse data
            data = req.get_json(force=True, silent=True)
            if not data:
                return jsonify({'error': 'No JSON data'}), 400

            logger.info(f"Received webhook: {json.dumps(data, indent=2)[:500]}")

            # Process each entry
            entries = data.get('entry', [])
            processed_leads = []

            for entry in entries:
                changes = entry.get('changes', [])
                for change in changes:
                    if change.get('field') == 'leadgen':
                        lead_gen_id = change.get('value', {}).get('leadgen_id')
                        if lead_gen_id:
                            lead_data = self.fetch_lead_data(lead_gen_id)
                            if lead_data:
                                self.process_lead(lead_data)
                                processed_leads.append(lead_data.lead_id)

            return jsonify({
                'status': 'success',
                'processed_leads': processed_leads
            }), 200

        except Exception as e:
            logger.error(f"Webhook processing error: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500

    def fetch_lead_data(self, lead_id: str) -> Optional[LeadData]:
        """
        Fetch lead details from Meta Graph API

        Args:
            lead_id: Lead gen ID from webhook
        """
        if not self.access_token:
            logger.error("ACCESS_TOKEN not set, cannot fetch lead data")
            return None

        url = f"https://graph.facebook.com/v18.0/{lead_id}"
        params = {
            'access_token': self.access_token,
            'fields': 'id,created_time,field_data,ad_id,adset_id,campaign_id,form_id,page_id'
        }

        try:
            response = requests.get(url, params=params, timeout=30)
            result = response.json()

            if 'error' in result:
                logger.error(f"Graph API error: {result['error']}")
                return None

            # Extract field data
            field_data = {}
            for field in result.get('field_data', []):
                name = field.get('name', '').lower()
                values = field.get('values', [])
                value = values[0] if values else None
                field_data[name] = value

            # Create LeadData object
            lead_data = LeadData(
                lead_id=result.get('id'),
                form_id=result.get('form_id'),
                page_id=result.get('page_id'),
                ad_id=result.get('ad_id'),
                adset_id=result.get('adset_id'),
                campaign_id=result.get('campaign_id'),
                created_time=result.get('created_time'),
                email=field_data.get('email'),
                phone=field_data.get('phone_number') or field_data.get('phone'),
                first_name=field_data.get('first_name'),
                last_name=field_data.get('last_name'),
                full_name=field_data.get('full_name'),
                company_name=field_data.get('company_name') or field_data.get('company'),
                job_title=field_data.get('job_title'),
                custom_fields=field_data
            )

            logger.info(f"Fetched lead data: {lead_data.email}")
            return lead_data

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch lead data: {str(e)}")
            return None

    def process_lead(self, lead: LeadData) -> bool:
        """
        Process a lead through all integrations

        1. Send Slack notification
        2. Create Pipedrive deal
        3. Forward to Zapier
        4. Send email notification
        """
        success = True

        # 1. Slack notification
        try:
            self.send_slack_notification(lead)
        except Exception as e:
            logger.error(f"Slack notification failed: {str(e)}")
            success = False

        # 2. Pipedrive deal
        try:
            self.create_pipedrive_deal(lead)
        except Exception as e:
            logger.error(f"Pipedrive deal creation failed: {str(e)}")
            success = False

        # 3. Zapier webhook
        try:
            self.forward_to_zapier(lead)
        except Exception as e:
            logger.error(f"Zapier forwarding failed: {str(e)}")
            success = False

        # 4. Email notification
        try:
            self.send_email_notification(lead)
        except Exception as e:
            logger.error(f"Email notification failed: {str(e)}")
            success = False

        return success


# ==============================================================================
# SLACK INTEGRATION
# ==============================================================================

    def send_slack_notification(self, lead: LeadData) -> bool:
        """
        Send lead notification to Slack #high-priority-intakes channel
        """
        if not LeadAdsConfig.SLACK_WEBHOOK_URL:
            logger.warning("SLACK_WEBHOOK_URL not set, skipping notification")
            return False

        # Format lead info
        name = lead.full_name or f"{lead.first_name or ''} {lead.last_name or ''}".strip() or 'Unknown'

        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "🔥 Nieuwe Meta Lead Ad Lead!",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Naam:*\n{name}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Bedrijf:*\n{lead.company_name or 'Niet opgegeven'}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Email:*\n{lead.email or 'Niet opgegeven'}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Telefoon:*\n{lead.phone or 'Niet opgegeven'}"
                    }
                ]
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Functie:*\n{lead.job_title or 'Niet opgegeven'}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Tijd:*\n{lead.created_time}"
                    }
                ]
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"Campaign: {lead.campaign_id or 'N/A'} | Ad Set: {lead.adset_id or 'N/A'} | Lead ID: {lead.lead_id}"
                    }
                ]
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "📞 Bel Nu",
                            "emoji": True
                        },
                        "url": f"tel:{lead.phone}" if lead.phone else "https://kandidatentekort.nl",
                        "style": "primary"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "📧 Email",
                            "emoji": True
                        },
                        "url": f"mailto:{lead.email}" if lead.email else "https://kandidatentekort.nl"
                    }
                ]
            }
        ]

        payload = {
            "channel": LeadAdsConfig.SLACK_CHANNEL,
            "blocks": blocks,
            "text": f"Nieuwe Meta Lead: {name} ({lead.company_name or 'Unknown'})"
        }

        try:
            response = requests.post(
                LeadAdsConfig.SLACK_WEBHOOK_URL,
                json=payload,
                timeout=10
            )

            if response.status_code == 200:
                logger.info(f"Slack notification sent for lead {lead.lead_id}")
                return True
            else:
                logger.error(f"Slack notification failed: {response.status_code}")
                return False

        except requests.exceptions.RequestException as e:
            logger.error(f"Slack request failed: {str(e)}")
            return False


# ==============================================================================
# PIPEDRIVE INTEGRATION
# ==============================================================================

    def create_pipedrive_deal(self, lead: LeadData) -> Optional[Dict]:
        """
        Create a Pipedrive deal from the lead
        """
        if not LeadAdsConfig.PIPEDRIVE_API_TOKEN:
            logger.warning("PIPEDRIVE_API_TOKEN not set, skipping deal creation")
            return None

        base_url = LeadAdsConfig.PIPEDRIVE_BASE_URL
        api_token = LeadAdsConfig.PIPEDRIVE_API_TOKEN

        try:
            # 1. Find or create person
            name = lead.full_name or f"{lead.first_name or ''} {lead.last_name or ''}".strip()
            person_id = None

            if lead.email:
                # Search for existing person
                search_url = f"{base_url}/persons/search"
                search_response = requests.get(
                    search_url,
                    params={
                        'api_token': api_token,
                        'term': lead.email,
                        'fields': 'email'
                    },
                    timeout=30
                )
                search_result = search_response.json()

                if search_result.get('success'):
                    items = search_result.get('data', {}).get('items', [])
                    if items:
                        person_id = items[0].get('item', {}).get('id')
                        logger.info(f"Found existing person: {person_id}")

            if not person_id:
                # Create new person
                person_data = {
                    'name': name or lead.email.split('@')[0] if lead.email else 'Unknown Lead'
                }
                if lead.email:
                    person_data['email'] = [{'value': lead.email, 'primary': True}]
                if lead.phone:
                    person_data['phone'] = [{'value': lead.phone, 'primary': True}]

                create_url = f"{base_url}/persons"
                create_response = requests.post(
                    create_url,
                    params={'api_token': api_token},
                    json=person_data,
                    timeout=30
                )
                create_result = create_response.json()

                if create_result.get('success'):
                    person_id = create_result.get('data', {}).get('id')
                    logger.info(f"Created new person: {person_id}")

            # 2. Find or create organization
            org_id = None
            if lead.company_name:
                # Search for existing org
                search_url = f"{base_url}/organizations/search"
                search_response = requests.get(
                    search_url,
                    params={
                        'api_token': api_token,
                        'term': lead.company_name
                    },
                    timeout=30
                )
                search_result = search_response.json()

                if search_result.get('success'):
                    items = search_result.get('data', {}).get('items', [])
                    if items:
                        org_id = items[0].get('item', {}).get('id')

                if not org_id:
                    # Create new organization
                    create_url = f"{base_url}/organizations"
                    create_response = requests.post(
                        create_url,
                        params={'api_token': api_token},
                        json={'name': lead.company_name},
                        timeout=30
                    )
                    create_result = create_response.json()

                    if create_result.get('success'):
                        org_id = create_result.get('data', {}).get('id')

            # 3. Create deal
            deal_title = f"Meta Lead - {lead.company_name or name or 'Unknown'}"
            deal_data = {
                'title': deal_title,
                'pipeline_id': LeadAdsConfig.PIPEDRIVE_PIPELINE_ID,
                'stage_id': LeadAdsConfig.PIPEDRIVE_STAGE_ID,
                'person_id': person_id
            }

            if org_id:
                deal_data['org_id'] = org_id

            # Add custom fields if available (you can customize these field keys)
            # deal_data['your_custom_field_key'] = lead.job_title

            create_url = f"{base_url}/deals"
            create_response = requests.post(
                create_url,
                params={'api_token': api_token},
                json=deal_data,
                timeout=30
            )
            create_result = create_response.json()

            if create_result.get('success'):
                deal = create_result.get('data', {})
                logger.info(f"Created Pipedrive deal: {deal.get('id')}")
                return deal
            else:
                logger.error(f"Failed to create deal: {create_result}")
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Pipedrive API error: {str(e)}")
            return None


# ==============================================================================
# ZAPIER INTEGRATION
# ==============================================================================

    def forward_to_zapier(self, lead: LeadData) -> bool:
        """
        Forward lead data to Zapier webhook for additional automations
        """
        if not LeadAdsConfig.ZAPIER_WEBHOOK_URL:
            logger.info("ZAPIER_WEBHOOK_URL not set, skipping")
            return False

        payload = {
            'lead_id': lead.lead_id,
            'form_id': lead.form_id,
            'page_id': lead.page_id,
            'campaign_id': lead.campaign_id,
            'adset_id': lead.adset_id,
            'ad_id': lead.ad_id,
            'created_time': lead.created_time,
            'email': lead.email,
            'phone': lead.phone,
            'first_name': lead.first_name,
            'last_name': lead.last_name,
            'full_name': lead.full_name,
            'company_name': lead.company_name,
            'job_title': lead.job_title,
            'custom_fields': lead.custom_fields,
            'source': 'meta_lead_ads',
            'processed_at': datetime.now().isoformat()
        }

        try:
            response = requests.post(
                LeadAdsConfig.ZAPIER_WEBHOOK_URL,
                json=payload,
                timeout=10
            )

            if response.status_code == 200:
                logger.info(f"Forwarded lead to Zapier: {lead.lead_id}")
                return True
            else:
                logger.error(f"Zapier forwarding failed: {response.status_code}")
                return False

        except requests.exceptions.RequestException as e:
            logger.error(f"Zapier request failed: {str(e)}")
            return False


# ==============================================================================
# EMAIL NOTIFICATION
# ==============================================================================

    def send_email_notification(self, lead: LeadData) -> bool:
        """
        Send email notification about new lead
        """
        if not LeadAdsConfig.SMTP_PASS:
            logger.warning("SMTP_PASS not set, skipping email notification")
            return False

        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        name = lead.full_name or f"{lead.first_name or ''} {lead.last_name or ''}".strip() or 'Unknown'

        html_content = f"""
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
    <div style="background-color: #1E3A8A; padding: 20px; text-align: center; border-radius: 8px 8px 0 0;">
        <h1 style="color: white; margin: 0;">🔥 Nieuwe Meta Lead!</h1>
    </div>

    <div style="background-color: #f9fafb; padding: 20px; border: 1px solid #e5e7eb; border-top: none;">
        <table width="100%" cellpadding="10">
            <tr>
                <td style="font-weight: bold; width: 30%;">Naam:</td>
                <td>{name}</td>
            </tr>
            <tr>
                <td style="font-weight: bold;">Bedrijf:</td>
                <td>{lead.company_name or 'Niet opgegeven'}</td>
            </tr>
            <tr>
                <td style="font-weight: bold;">Email:</td>
                <td><a href="mailto:{lead.email}">{lead.email or 'Niet opgegeven'}</a></td>
            </tr>
            <tr>
                <td style="font-weight: bold;">Telefoon:</td>
                <td><a href="tel:{lead.phone}">{lead.phone or 'Niet opgegeven'}</a></td>
            </tr>
            <tr>
                <td style="font-weight: bold;">Functie:</td>
                <td>{lead.job_title or 'Niet opgegeven'}</td>
            </tr>
            <tr>
                <td style="font-weight: bold;">Tijd:</td>
                <td>{lead.created_time}</td>
            </tr>
        </table>

        <div style="margin-top: 20px; padding: 15px; background-color: #fff; border-radius: 6px;">
            <p style="margin: 0; color: #6b7280; font-size: 12px;">
                Campaign: {lead.campaign_id or 'N/A'}<br>
                Ad Set: {lead.adset_id or 'N/A'}<br>
                Lead ID: {lead.lead_id}
            </p>
        </div>
    </div>

    <div style="background-color: #FF6B35; padding: 20px; text-align: center; border-radius: 0 0 8px 8px;">
        <a href="tel:{lead.phone}" style="color: white; text-decoration: none; font-weight: bold; font-size: 18px;">
            📞 Bel Direct
        </a>
    </div>
</body>
</html>
"""

        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"🔥 Nieuwe Meta Lead: {name} ({lead.company_name or 'Unknown'})"
            msg['From'] = LeadAdsConfig.SMTP_USER
            msg['To'] = LeadAdsConfig.NOTIFICATION_EMAIL

            msg.attach(MIMEText(html_content, 'html'))

            with smtplib.SMTP(LeadAdsConfig.SMTP_HOST, LeadAdsConfig.SMTP_PORT) as server:
                server.starttls()
                server.login(LeadAdsConfig.SMTP_USER, LeadAdsConfig.SMTP_PASS)
                server.send_message(msg)

            logger.info(f"Email notification sent for lead {lead.lead_id}")
            return True

        except Exception as e:
            logger.error(f"Email sending failed: {str(e)}")
            return False


# ==============================================================================
# FLASK APP (for standalone deployment)
# ==============================================================================

app = Flask(__name__)
handler = LeadAdsWebhookHandler()


@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'meta-lead-ads-webhook',
        'version': '1.0.0'
    })


@app.route('/webhook/meta-leads', methods=['GET', 'POST'])
def meta_leads_webhook():
    """Meta Lead Ads webhook endpoint"""
    if request.method == 'GET':
        return handler.verify_webhook(request)
    return handler.process_webhook(request)


@app.route('/test-lead', methods=['POST'])
def test_lead():
    """Test endpoint for manual lead processing"""
    try:
        data = request.get_json()

        lead = LeadData(
            lead_id=data.get('lead_id', 'test_123'),
            form_id=data.get('form_id', 'test_form'),
            page_id=data.get('page_id', 'test_page'),
            ad_id=data.get('ad_id'),
            adset_id=data.get('adset_id'),
            campaign_id=data.get('campaign_id'),
            created_time=datetime.now().isoformat(),
            email=data.get('email'),
            phone=data.get('phone'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            full_name=data.get('full_name'),
            company_name=data.get('company_name'),
            job_title=data.get('job_title'),
            custom_fields=data.get('custom_fields', {})
        )

        success = handler.process_lead(lead)

        return jsonify({
            'status': 'success' if success else 'partial',
            'lead_id': lead.lead_id
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
