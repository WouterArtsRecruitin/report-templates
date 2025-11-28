#!/usr/bin/env python3
"""
META PIXEL TRACKING MODULE
==========================
Client-side pixel code generation and server-side Conversion API integration.

Features:
- Generate Meta Pixel installation code for kandidatentekort.nl
- Server-side Conversion API for accurate tracking
- Event tracking (Lead, InitiateCheckout, ViewContent, etc.)
- User data hashing for privacy compliance

Pixel ID: 1443564313411457
Website: kandidatentekort.nl
"""

import os
import json
import time
import hashlib
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from enum import Enum
import requests
import uuid

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ==============================================================================
# CONFIGURATION
# ==============================================================================

class PixelConfig:
    """Meta Pixel Configuration for kandidatentekort.nl"""
    PIXEL_ID = os.getenv('META_PIXEL_ID', '1443564313411457')
    ACCESS_TOKEN = os.getenv('META_ACCESS_TOKEN')
    API_VERSION = 'v18.0'
    CONVERSION_API_URL = f'https://graph.facebook.com/{API_VERSION}/{PIXEL_ID}/events'

    # Test event code for debugging (set in Events Manager)
    TEST_EVENT_CODE = os.getenv('META_TEST_EVENT_CODE')


class StandardEvent(Enum):
    """Meta Standard Events"""
    PAGE_VIEW = 'PageView'
    VIEW_CONTENT = 'ViewContent'
    SEARCH = 'Search'
    ADD_TO_CART = 'AddToCart'
    ADD_TO_WISHLIST = 'AddToWishlist'
    INITIATE_CHECKOUT = 'InitiateCheckout'
    ADD_PAYMENT_INFO = 'AddPaymentInfo'
    PURCHASE = 'Purchase'
    LEAD = 'Lead'
    COMPLETE_REGISTRATION = 'CompleteRegistration'
    CONTACT = 'Contact'
    CUSTOMIZE_PRODUCT = 'CustomizeProduct'
    DONATE = 'Donate'
    FIND_LOCATION = 'FindLocation'
    SCHEDULE = 'Schedule'
    START_TRIAL = 'StartTrial'
    SUBMIT_APPLICATION = 'SubmitApplication'
    SUBSCRIBE = 'Subscribe'


class ActionSource(Enum):
    """Event action sources"""
    WEBSITE = 'website'
    EMAIL = 'email'
    APP = 'app'
    PHONE_CALL = 'phone_call'
    CHAT = 'chat'
    PHYSICAL_STORE = 'physical_store'
    SYSTEM_GENERATED = 'system_generated'
    OTHER = 'other'


@dataclass
class UserData:
    """User data for event tracking (will be hashed)"""
    email: Optional[str] = None
    phone: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    zip_code: Optional[str] = None
    client_ip_address: Optional[str] = None
    client_user_agent: Optional[str] = None
    fbc: Optional[str] = None  # Facebook click ID cookie
    fbp: Optional[str] = None  # Facebook browser ID cookie
    external_id: Optional[str] = None


@dataclass
class CustomData:
    """Custom data for event tracking"""
    content_name: Optional[str] = None
    content_category: Optional[str] = None
    content_ids: Optional[List[str]] = None
    content_type: Optional[str] = None
    value: Optional[float] = None
    currency: Optional[str] = None
    num_items: Optional[int] = None
    predicted_ltv: Optional[float] = None
    status: Optional[str] = None
    search_string: Optional[str] = None


# ==============================================================================
# CLIENT-SIDE PIXEL CODE GENERATOR
# ==============================================================================

class PixelCodeGenerator:
    """
    Generate Meta Pixel installation code for kandidatentekort.nl

    Usage:
        generator = PixelCodeGenerator()
        head_code = generator.get_base_pixel_code()
        event_code = generator.get_event_code('Lead', {'value': 50, 'currency': 'EUR'})
    """

    def __init__(self, pixel_id: str = None):
        self.pixel_id = pixel_id or PixelConfig.PIXEL_ID

    def get_base_pixel_code(self) -> str:
        """
        Get the base Meta Pixel code to install in <head> section

        Returns:
            HTML/JavaScript code string
        """
        return f'''<!-- Meta Pixel Code for kandidatentekort.nl -->
<script>
!function(f,b,e,v,n,t,s)
{{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)}};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '{self.pixel_id}');
fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id={self.pixel_id}&ev=PageView&noscript=1"
/></noscript>
<!-- End Meta Pixel Code -->'''

    def get_event_code(
        self,
        event_name: str,
        custom_data: Dict[str, Any] = None
    ) -> str:
        """
        Get JavaScript code for tracking a specific event

        Args:
            event_name: Standard event name or custom event
            custom_data: Additional event parameters

        Returns:
            JavaScript code string
        """
        if custom_data:
            data_json = json.dumps(custom_data)
            return f"fbq('track', '{event_name}', {data_json});"
        return f"fbq('track', '{event_name}');"

    def get_lead_event_code(
        self,
        content_name: str = 'Vacature Analyse',
        value: float = 0,
        currency: str = 'EUR'
    ) -> str:
        """Get Lead event tracking code"""
        return self.get_event_code('Lead', {
            'content_name': content_name,
            'value': value,
            'currency': currency
        })

    def get_initiate_checkout_event_code(
        self,
        content_name: str = 'Assessment Start',
        value: float = 0,
        currency: str = 'EUR'
    ) -> str:
        """Get InitiateCheckout event tracking code (for assessment start)"""
        return self.get_event_code('InitiateCheckout', {
            'content_name': content_name,
            'value': value,
            'currency': currency
        })

    def get_view_content_event_code(
        self,
        content_name: str,
        content_category: str = 'vacancy'
    ) -> str:
        """Get ViewContent event tracking code"""
        return self.get_event_code('ViewContent', {
            'content_name': content_name,
            'content_category': content_category
        })

    def get_complete_registration_event_code(
        self,
        content_name: str = 'Assessment Completed',
        status: str = 'completed'
    ) -> str:
        """Get CompleteRegistration event tracking code"""
        return self.get_event_code('CompleteRegistration', {
            'content_name': content_name,
            'status': status
        })

    def get_netlify_integration_code(self) -> str:
        """
        Get complete Netlify-ready pixel integration code

        This includes:
        - Base pixel code
        - Common event tracking
        - Form submission tracking
        """
        return f'''<!-- =================================================== -->
<!-- META PIXEL INTEGRATION FOR KANDIDATENTEKORT.NL     -->
<!-- Deploy via Netlify: kandidatentekortv2             -->
<!-- Pixel ID: {self.pixel_id}                          -->
<!-- =================================================== -->

<!-- Base Meta Pixel Code - Add to <head> section -->
{self.get_base_pixel_code()}

<!-- Event Tracking Script - Add before </body> -->
<script>
(function() {{
    // Track page-specific events based on URL
    const path = window.location.pathname;

    // Vacancy analysis page view
    if (path.includes('/analyse') || path.includes('/check')) {{
        fbq('track', 'ViewContent', {{
            content_name: 'Vacature Analyse Pagina',
            content_category: 'tool'
        }});
    }}

    // Pricing/checkout page
    if (path.includes('/prijzen') || path.includes('/pricing')) {{
        fbq('track', 'InitiateCheckout', {{
            content_name: 'Pricing Page',
            currency: 'EUR'
        }});
    }}

    // Form submission tracking
    document.addEventListener('DOMContentLoaded', function() {{
        // Track Typeform submissions
        const typeformIframes = document.querySelectorAll('iframe[src*="typeform"]');
        typeformIframes.forEach(function(iframe) {{
            iframe.addEventListener('load', function() {{
                console.log('[Meta Pixel] Typeform loaded');
            }});
        }});

        // Track form submissions
        const forms = document.querySelectorAll('form');
        forms.forEach(function(form) {{
            form.addEventListener('submit', function(e) {{
                fbq('track', 'Lead', {{
                    content_name: form.getAttribute('data-form-name') || 'Form Submission',
                    content_category: 'form'
                }});
            }});
        }});

        // Track CTA button clicks
        const ctaButtons = document.querySelectorAll('[data-track-cta]');
        ctaButtons.forEach(function(btn) {{
            btn.addEventListener('click', function() {{
                const ctaName = btn.getAttribute('data-track-cta');
                fbq('trackCustom', 'CTAClick', {{
                    cta_name: ctaName,
                    page: window.location.pathname
                }});
            }});
        }});
    }});

    // Track scroll depth
    let scrollDepths = [25, 50, 75, 100];
    let trackedDepths = [];

    window.addEventListener('scroll', function() {{
        const scrollPercent = Math.round(
            (window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100
        );

        scrollDepths.forEach(function(depth) {{
            if (scrollPercent >= depth && !trackedDepths.includes(depth)) {{
                trackedDepths.push(depth);
                fbq('trackCustom', 'ScrollDepth', {{ depth: depth }});
            }}
        }});
    }});
}})();
</script>
<!-- End Meta Pixel Event Tracking -->'''

    def get_typeform_embed_with_tracking(self, typeform_id: str) -> str:
        """Get Typeform embed code with pixel tracking"""
        return f'''<!-- Typeform with Meta Pixel Tracking -->
<div data-tf-widget="{typeform_id}" data-tf-opacity="100" data-tf-iframe-props="title=Kandidatentekort Assessment" data-tf-transitive-search-params data-tf-medium="snippet" style="width:100%;height:500px;"></div>
<script src="//embed.typeform.com/next/embed.js"></script>
<script>
// Track Typeform events
window.addEventListener('message', function(event) {{
    if (event.data && event.data.type) {{
        // Typeform started
        if (event.data.type === 'form-start') {{
            fbq('track', 'InitiateCheckout', {{
                content_name: 'Assessment Started',
                content_category: 'assessment'
            }});
        }}
        // Typeform submitted
        if (event.data.type === 'form-submit') {{
            fbq('track', 'Lead', {{
                content_name: 'Assessment Completed',
                content_category: 'assessment',
                value: 50,
                currency: 'EUR'
            }});
            fbq('track', 'CompleteRegistration', {{
                content_name: 'Assessment Registration',
                status: 'completed'
            }});
        }}
    }}
}});
</script>'''


# ==============================================================================
# SERVER-SIDE CONVERSION API
# ==============================================================================

class ConversionAPI:
    """
    Meta Conversion API for server-side event tracking

    Usage:
        api = ConversionAPI()
        api.send_lead_event(
            user_data=UserData(email='test@example.com'),
            custom_data=CustomData(content_name='Vacature Analyse', value=50)
        )
    """

    def __init__(self, pixel_id: str = None, access_token: str = None):
        self.pixel_id = pixel_id or PixelConfig.PIXEL_ID
        self.access_token = access_token or PixelConfig.ACCESS_TOKEN
        self.api_url = f'https://graph.facebook.com/{PixelConfig.API_VERSION}/{self.pixel_id}/events'

        if not self.access_token:
            logger.warning("META_ACCESS_TOKEN not set - Conversion API will not work")

    def _hash_value(self, value: str) -> str:
        """Hash a value using SHA256 (as required by Meta)"""
        if not value:
            return None
        normalized = value.lower().strip()
        return hashlib.sha256(normalized.encode('utf-8')).hexdigest()

    def _hash_phone(self, phone: str) -> str:
        """Hash phone number with proper formatting"""
        if not phone:
            return None
        # Remove non-digits
        digits = ''.join(filter(str.isdigit, phone))
        # Add Netherlands country code if missing
        if not digits.startswith('31'):
            digits = '31' + digits.lstrip('0')
        return hashlib.sha256(digits.encode('utf-8')).hexdigest()

    def _prepare_user_data(self, user_data: UserData) -> Dict[str, Any]:
        """Prepare and hash user data for API"""
        data = {}

        if user_data.email:
            data['em'] = [self._hash_value(user_data.email)]
        if user_data.phone:
            data['ph'] = [self._hash_phone(user_data.phone)]
        if user_data.first_name:
            data['fn'] = [self._hash_value(user_data.first_name)]
        if user_data.last_name:
            data['ln'] = [self._hash_value(user_data.last_name)]
        if user_data.city:
            data['ct'] = [self._hash_value(user_data.city)]
        if user_data.state:
            data['st'] = [self._hash_value(user_data.state)]
        if user_data.country:
            data['country'] = [self._hash_value(user_data.country)]
        if user_data.zip_code:
            data['zp'] = [self._hash_value(user_data.zip_code)]
        if user_data.client_ip_address:
            data['client_ip_address'] = user_data.client_ip_address
        if user_data.client_user_agent:
            data['client_user_agent'] = user_data.client_user_agent
        if user_data.fbc:
            data['fbc'] = user_data.fbc
        if user_data.fbp:
            data['fbp'] = user_data.fbp
        if user_data.external_id:
            data['external_id'] = [self._hash_value(user_data.external_id)]

        return data

    def _prepare_custom_data(self, custom_data: CustomData) -> Dict[str, Any]:
        """Prepare custom data for API"""
        data = {}

        if custom_data.content_name:
            data['content_name'] = custom_data.content_name
        if custom_data.content_category:
            data['content_category'] = custom_data.content_category
        if custom_data.content_ids:
            data['content_ids'] = custom_data.content_ids
        if custom_data.content_type:
            data['content_type'] = custom_data.content_type
        if custom_data.value is not None:
            data['value'] = custom_data.value
        if custom_data.currency:
            data['currency'] = custom_data.currency
        if custom_data.num_items is not None:
            data['num_items'] = custom_data.num_items
        if custom_data.predicted_ltv is not None:
            data['predicted_ltv'] = custom_data.predicted_ltv
        if custom_data.status:
            data['status'] = custom_data.status
        if custom_data.search_string:
            data['search_string'] = custom_data.search_string

        return data

    def send_event(
        self,
        event_name: str,
        user_data: UserData = None,
        custom_data: CustomData = None,
        event_source_url: str = None,
        action_source: ActionSource = ActionSource.WEBSITE,
        event_id: str = None
    ) -> Dict[str, Any]:
        """
        Send an event to Meta Conversion API

        Args:
            event_name: Standard or custom event name
            user_data: User data for matching
            custom_data: Custom event data
            event_source_url: URL where event occurred
            action_source: Where the event originated
            event_id: Unique event ID for deduplication

        Returns:
            API response dict
        """
        if not self.access_token:
            logger.error("Cannot send event: META_ACCESS_TOKEN not set")
            return {'error': 'No access token'}

        event = {
            'event_name': event_name,
            'event_time': int(time.time()),
            'action_source': action_source.value,
            'event_id': event_id or str(uuid.uuid4())
        }

        if event_source_url:
            event['event_source_url'] = event_source_url

        if user_data:
            event['user_data'] = self._prepare_user_data(user_data)

        if custom_data:
            event['custom_data'] = self._prepare_custom_data(custom_data)

        payload = {
            'data': [event],
            'access_token': self.access_token
        }

        # Add test event code if configured
        if PixelConfig.TEST_EVENT_CODE:
            payload['test_event_code'] = PixelConfig.TEST_EVENT_CODE

        try:
            response = requests.post(
                self.api_url,
                json=payload,
                timeout=30
            )

            result = response.json()

            if 'error' in result:
                logger.error(f"Conversion API error: {result['error']}")
            else:
                logger.info(f"Event sent successfully: {event_name} (id: {event['event_id']})")

            return result

        except requests.exceptions.RequestException as e:
            logger.error(f"Conversion API request failed: {str(e)}")
            return {'error': str(e)}

    # ==========================================================================
    # CONVENIENCE METHODS FOR KANDIDATENTEKORT.NL
    # ==========================================================================

    def send_lead_event(
        self,
        user_data: UserData,
        content_name: str = 'Kandidatentekort Lead',
        value: float = 50,
        event_source_url: str = 'https://kandidatentekort.nl'
    ) -> Dict[str, Any]:
        """Send Lead event when form is submitted"""
        return self.send_event(
            event_name=StandardEvent.LEAD.value,
            user_data=user_data,
            custom_data=CustomData(
                content_name=content_name,
                value=value,
                currency='EUR'
            ),
            event_source_url=event_source_url
        )

    def send_assessment_start_event(
        self,
        user_data: UserData = None,
        event_source_url: str = 'https://kandidatentekort.nl/assessment'
    ) -> Dict[str, Any]:
        """Send InitiateCheckout event when assessment starts"""
        return self.send_event(
            event_name=StandardEvent.INITIATE_CHECKOUT.value,
            user_data=user_data,
            custom_data=CustomData(
                content_name='Vacature Assessment Start',
                content_category='assessment'
            ),
            event_source_url=event_source_url
        )

    def send_assessment_complete_event(
        self,
        user_data: UserData,
        score: int = None,
        event_source_url: str = 'https://kandidatentekort.nl/assessment'
    ) -> Dict[str, Any]:
        """Send CompleteRegistration event when assessment is completed"""
        custom_data = CustomData(
            content_name='Vacature Assessment Complete',
            content_category='assessment',
            status='completed',
            value=float(score) if score else None
        )

        return self.send_event(
            event_name=StandardEvent.COMPLETE_REGISTRATION.value,
            user_data=user_data,
            custom_data=custom_data,
            event_source_url=event_source_url
        )

    def send_page_view_event(
        self,
        user_data: UserData = None,
        page_name: str = None,
        event_source_url: str = None
    ) -> Dict[str, Any]:
        """Send PageView event"""
        return self.send_event(
            event_name=StandardEvent.PAGE_VIEW.value,
            user_data=user_data,
            custom_data=CustomData(content_name=page_name) if page_name else None,
            event_source_url=event_source_url
        )

    def send_contact_event(
        self,
        user_data: UserData,
        event_source_url: str = 'https://kandidatentekort.nl/contact'
    ) -> Dict[str, Any]:
        """Send Contact event"""
        return self.send_event(
            event_name=StandardEvent.CONTACT.value,
            user_data=user_data,
            custom_data=CustomData(
                content_name='Contact Form',
                content_category='contact'
            ),
            event_source_url=event_source_url
        )


# ==============================================================================
# INTEGRATION HELPER
# ==============================================================================

def create_netlify_pixel_file() -> str:
    """
    Generate the complete pixel integration file for Netlify deployment

    Returns:
        File content string for _headers or netlify.toml
    """
    generator = PixelCodeGenerator()
    return generator.get_netlify_integration_code()


def get_pixel_verification_code() -> str:
    """Get code snippet to verify pixel is working"""
    return f'''<!-- Pixel Verification Script -->
<script>
// Check if Meta Pixel is loaded
if (typeof fbq !== 'undefined') {{
    console.log('[Meta Pixel] ✅ Pixel loaded successfully');
    console.log('[Meta Pixel] Pixel ID: {PixelConfig.PIXEL_ID}');

    // Test tracking
    fbq('track', 'PageView');
    console.log('[Meta Pixel] ✅ PageView event sent');
}} else {{
    console.error('[Meta Pixel] ❌ Pixel not loaded');
}}
</script>'''


# ==============================================================================
# MAIN (for testing)
# ==============================================================================

if __name__ == '__main__':
    # Generate pixel code
    generator = PixelCodeGenerator()
    print("=" * 60)
    print("META PIXEL CODE FOR KANDIDATENTEKORT.NL")
    print("=" * 60)
    print("\n1. BASE PIXEL CODE (add to <head>):\n")
    print(generator.get_base_pixel_code())

    print("\n2. LEAD EVENT CODE:\n")
    print(generator.get_lead_event_code())

    print("\n3. COMPLETE NETLIFY INTEGRATION:\n")
    print(generator.get_netlify_integration_code())

    # Test Conversion API (if token is set)
    if PixelConfig.ACCESS_TOKEN:
        print("\n" + "=" * 60)
        print("TESTING CONVERSION API")
        print("=" * 60)

        api = ConversionAPI()
        result = api.send_page_view_event(
            page_name='Test Page',
            event_source_url='https://kandidatentekort.nl/test'
        )
        print(f"API Response: {result}")
