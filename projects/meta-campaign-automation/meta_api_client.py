#!/usr/bin/env python3
"""
META FACEBOOK API CLIENT
========================
OAuth token management and Graph API integration for Meta campaigns.

Features:
- OAuth 2.0 token management with auto-refresh
- Graph API wrapper for ads, audiences, and insights
- Lead Ads webhook processing
- Conversion API for server-side tracking

Required Environment Variables:
- META_APP_ID: Facebook App ID
- META_APP_SECRET: Facebook App Secret
- META_ACCESS_TOKEN: Long-lived access token
- META_AD_ACCOUNT_ID: Ad Account ID (format: act_XXXXXXXXX)
- META_PIXEL_ID: Pixel ID for conversion tracking
"""

import os
import json
import time
import hmac
import hashlib
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import requests
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ==============================================================================
# CONFIGURATION
# ==============================================================================

class MetaConfig:
    """Meta API Configuration"""
    APP_ID = os.getenv('META_APP_ID')
    APP_SECRET = os.getenv('META_APP_SECRET')
    ACCESS_TOKEN = os.getenv('META_ACCESS_TOKEN')
    AD_ACCOUNT_ID = os.getenv('META_AD_ACCOUNT_ID')  # Format: act_XXXXXXXXX
    PIXEL_ID = os.getenv('META_PIXEL_ID', '1443564313411457')

    # API Settings
    API_VERSION = 'v18.0'
    BASE_URL = f'https://graph.facebook.com/{API_VERSION}'

    # Token refresh threshold (7 days before expiry)
    TOKEN_REFRESH_THRESHOLD_DAYS = 7


class CampaignObjective(Enum):
    """Meta Campaign Objectives"""
    OUTCOME_AWARENESS = 'OUTCOME_AWARENESS'
    OUTCOME_ENGAGEMENT = 'OUTCOME_ENGAGEMENT'
    OUTCOME_TRAFFIC = 'OUTCOME_TRAFFIC'
    OUTCOME_LEADS = 'OUTCOME_LEADS'
    OUTCOME_APP_PROMOTION = 'OUTCOME_APP_PROMOTION'
    OUTCOME_SALES = 'OUTCOME_SALES'


class OptimizationGoal(Enum):
    """Ad Set Optimization Goals"""
    LEAD_GENERATION = 'LEAD_GENERATION'
    LINK_CLICKS = 'LINK_CLICKS'
    LANDING_PAGE_VIEWS = 'LANDING_PAGE_VIEWS'
    IMPRESSIONS = 'IMPRESSIONS'
    REACH = 'REACH'
    CONVERSIONS = 'CONVERSIONS'
    VALUE = 'VALUE'


@dataclass
class TokenInfo:
    """OAuth Token Information"""
    access_token: str
    token_type: str
    expires_at: datetime
    scopes: List[str]


# ==============================================================================
# META API CLIENT
# ==============================================================================

class MetaApiClient:
    """
    Meta Graph API Client for Facebook Ads Management

    Usage:
        client = MetaApiClient()

        # Check token status
        if not client.is_token_valid():
            client.refresh_long_lived_token()

        # Create campaign
        campaign = client.create_campaign(
            name="Kandidatentekort - HR Directors",
            objective=CampaignObjective.OUTCOME_LEADS
        )
    """

    def __init__(self, access_token: str = None):
        self.access_token = access_token or MetaConfig.ACCESS_TOKEN
        self.ad_account_id = MetaConfig.AD_ACCOUNT_ID
        self.pixel_id = MetaConfig.PIXEL_ID
        self._token_info: Optional[TokenInfo] = None

        if not self.access_token:
            raise ValueError("META_ACCESS_TOKEN environment variable is required")

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Dict = None,
        data: Dict = None
    ) -> Dict[str, Any]:
        """Make authenticated request to Meta Graph API"""
        url = f"{MetaConfig.BASE_URL}/{endpoint}"

        params = params or {}
        params['access_token'] = self.access_token

        try:
            if method == 'GET':
                response = requests.get(url, params=params, timeout=30)
            elif method == 'POST':
                response = requests.post(url, params=params, json=data, timeout=30)
            elif method == 'DELETE':
                response = requests.delete(url, params=params, timeout=30)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            result = response.json()

            if 'error' in result:
                error = result['error']
                logger.error(f"Meta API Error: {error.get('message')} (code: {error.get('code')})")
                raise MetaApiError(
                    message=error.get('message'),
                    code=error.get('code'),
                    error_subcode=error.get('error_subcode')
                )

            return result

        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            raise MetaApiError(message=str(e))

    # ==========================================================================
    # TOKEN MANAGEMENT
    # ==========================================================================

    def get_token_info(self) -> TokenInfo:
        """Get information about the current access token"""
        result = self._make_request(
            'GET',
            'debug_token',
            params={'input_token': self.access_token}
        )

        data = result.get('data', {})
        expires_at = datetime.fromtimestamp(data.get('expires_at', 0))

        self._token_info = TokenInfo(
            access_token=self.access_token,
            token_type=data.get('type', 'unknown'),
            expires_at=expires_at,
            scopes=data.get('scopes', [])
        )

        return self._token_info

    def is_token_valid(self) -> bool:
        """Check if the current token is valid and not expiring soon"""
        try:
            token_info = self.get_token_info()
            threshold = datetime.now() + timedelta(days=MetaConfig.TOKEN_REFRESH_THRESHOLD_DAYS)
            return token_info.expires_at > threshold
        except MetaApiError:
            return False

    def exchange_for_long_lived_token(self, short_lived_token: str) -> str:
        """Exchange a short-lived token for a long-lived token (60 days)"""
        if not MetaConfig.APP_ID or not MetaConfig.APP_SECRET:
            raise ValueError("META_APP_ID and META_APP_SECRET required for token exchange")

        params = {
            'grant_type': 'fb_exchange_token',
            'client_id': MetaConfig.APP_ID,
            'client_secret': MetaConfig.APP_SECRET,
            'fb_exchange_token': short_lived_token
        }

        response = requests.get(
            f"{MetaConfig.BASE_URL}/oauth/access_token",
            params=params,
            timeout=30
        )

        result = response.json()

        if 'error' in result:
            raise MetaApiError(message=result['error'].get('message'))

        new_token = result.get('access_token')
        logger.info("Successfully exchanged for long-lived token")

        return new_token

    def refresh_long_lived_token(self) -> str:
        """Refresh the long-lived token (requires app permissions)"""
        return self.exchange_for_long_lived_token(self.access_token)

    def get_required_permissions(self) -> List[str]:
        """Return list of required permissions for full functionality"""
        return [
            'ads_read',
            'ads_management',
            'business_management',
            'leads_retrieval',
            'pages_read_engagement',
            'pages_manage_ads'
        ]

    # ==========================================================================
    # CAMPAIGN MANAGEMENT
    # ==========================================================================

    def create_campaign(
        self,
        name: str,
        objective: CampaignObjective = CampaignObjective.OUTCOME_LEADS,
        status: str = 'PAUSED',
        daily_budget: int = None,
        lifetime_budget: int = None,
        special_ad_categories: List[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new ad campaign

        Args:
            name: Campaign name
            objective: Campaign objective
            status: ACTIVE, PAUSED, DELETED, ARCHIVED
            daily_budget: Daily budget in cents
            lifetime_budget: Lifetime budget in cents
            special_ad_categories: List of special ad categories (EMPLOYMENT, HOUSING, CREDIT)

        Returns:
            Created campaign data including ID
        """
        data = {
            'name': name,
            'objective': objective.value,
            'status': status,
            'special_ad_categories': special_ad_categories or []
        }

        if daily_budget:
            data['daily_budget'] = daily_budget
        if lifetime_budget:
            data['lifetime_budget'] = lifetime_budget

        result = self._make_request(
            'POST',
            f'{self.ad_account_id}/campaigns',
            data=data
        )

        logger.info(f"Created campaign: {result.get('id')}")
        return result

    def get_campaign(self, campaign_id: str) -> Dict[str, Any]:
        """Get campaign details"""
        return self._make_request(
            'GET',
            campaign_id,
            params={'fields': 'id,name,objective,status,daily_budget,lifetime_budget,created_time'}
        )

    def update_campaign(self, campaign_id: str, **updates) -> Dict[str, Any]:
        """Update campaign settings"""
        return self._make_request('POST', campaign_id, data=updates)

    def get_campaigns(self, status_filter: str = None) -> List[Dict]:
        """List all campaigns in the ad account"""
        params = {
            'fields': 'id,name,objective,status,daily_budget,lifetime_budget,created_time,insights{spend,impressions,clicks}'
        }

        if status_filter:
            params['filtering'] = json.dumps([{
                'field': 'effective_status',
                'operator': 'IN',
                'value': [status_filter]
            }])

        result = self._make_request('GET', f'{self.ad_account_id}/campaigns', params=params)
        return result.get('data', [])

    # ==========================================================================
    # AD SET MANAGEMENT
    # ==========================================================================

    def create_ad_set(
        self,
        name: str,
        campaign_id: str,
        daily_budget: int,
        targeting: Dict,
        optimization_goal: OptimizationGoal = OptimizationGoal.LEAD_GENERATION,
        billing_event: str = 'IMPRESSIONS',
        bid_amount: int = None,
        status: str = 'PAUSED',
        start_time: datetime = None,
        end_time: datetime = None
    ) -> Dict[str, Any]:
        """
        Create a new ad set within a campaign

        Args:
            name: Ad set name
            campaign_id: Parent campaign ID
            daily_budget: Daily budget in cents
            targeting: Targeting specification dict
            optimization_goal: What to optimize for
            billing_event: IMPRESSIONS, LINK_CLICKS, etc.
            bid_amount: Bid amount in cents (optional)
            status: ACTIVE, PAUSED, etc.
            start_time: When to start running
            end_time: When to stop running
        """
        data = {
            'name': name,
            'campaign_id': campaign_id,
            'daily_budget': daily_budget,
            'targeting': json.dumps(targeting),
            'optimization_goal': optimization_goal.value,
            'billing_event': billing_event,
            'status': status
        }

        if bid_amount:
            data['bid_amount'] = bid_amount
        if start_time:
            data['start_time'] = start_time.isoformat()
        if end_time:
            data['end_time'] = end_time.isoformat()

        result = self._make_request(
            'POST',
            f'{self.ad_account_id}/adsets',
            data=data
        )

        logger.info(f"Created ad set: {result.get('id')}")
        return result

    # ==========================================================================
    # CUSTOM AUDIENCES
    # ==========================================================================

    def create_custom_audience(
        self,
        name: str,
        description: str = '',
        subtype: str = 'CUSTOM',
        customer_file_source: str = None
    ) -> Dict[str, Any]:
        """Create a custom audience for targeting"""
        data = {
            'name': name,
            'description': description,
            'subtype': subtype
        }

        if customer_file_source:
            data['customer_file_source'] = customer_file_source

        result = self._make_request(
            'POST',
            f'{self.ad_account_id}/customaudiences',
            data=data
        )

        logger.info(f"Created custom audience: {result.get('id')}")
        return result

    def create_lookalike_audience(
        self,
        name: str,
        origin_audience_id: str,
        country: str = 'NL',
        ratio: float = 0.01  # 1% lookalike
    ) -> Dict[str, Any]:
        """Create a lookalike audience based on existing audience"""
        data = {
            'name': name,
            'subtype': 'LOOKALIKE',
            'origin_audience_id': origin_audience_id,
            'lookalike_spec': json.dumps({
                'country': country,
                'ratio': ratio,
                'type': 'similarity'
            })
        }

        return self._make_request(
            'POST',
            f'{self.ad_account_id}/customaudiences',
            data=data
        )

    def get_custom_audiences(self) -> List[Dict]:
        """List all custom audiences"""
        result = self._make_request(
            'GET',
            f'{self.ad_account_id}/customaudiences',
            params={'fields': 'id,name,description,subtype,approximate_count'}
        )
        return result.get('data', [])

    # ==========================================================================
    # TARGETING TEMPLATES
    # ==========================================================================

    def build_hr_directors_targeting(self) -> Dict:
        """Build targeting spec for HR Directors in Netherlands"""
        return {
            'geo_locations': {
                'countries': ['NL'],
                'location_types': ['home', 'recent']
            },
            'age_min': 28,
            'age_max': 60,
            'genders': [1, 2],  # All genders
            'targeting_optimization': 'none',
            'work_positions': [
                {'id': '107756515917549', 'name': 'HR Director'},
                {'id': '108147285880481', 'name': 'HR Manager'},
                {'id': '112445598771543', 'name': 'Head of HR'},
                {'id': '113371672019222', 'name': 'Chief Human Resources Officer'},
                {'id': '106159722750611', 'name': 'VP Human Resources'},
                {'id': '108076792556090', 'name': 'Hoofd HR'},
                {'id': '110841058935139', 'name': 'Directeur HR'}
            ],
            'interests': [
                {'id': '6003156392553', 'name': 'Human resource management'},
                {'id': '6003017432648', 'name': 'Recruitment'}
            ]
        }

    def build_operations_targeting(self) -> Dict:
        """Build targeting spec for Operations/COO in Netherlands"""
        return {
            'geo_locations': {
                'countries': ['NL'],
                'location_types': ['home', 'recent']
            },
            'age_min': 30,
            'age_max': 60,
            'genders': [1, 2],
            'targeting_optimization': 'none',
            'work_positions': [
                {'id': '108447645850630', 'name': 'COO'},
                {'id': '107911055909073', 'name': 'Operations Director'},
                {'id': '110182412348619', 'name': 'Operations Manager'},
                {'id': '105645139469143', 'name': 'Chief Operating Officer'},
                {'id': '106077216087688', 'name': 'VP Operations'}
            ],
            'interests': [
                {'id': '6003223996963', 'name': 'Business operations'},
                {'id': '6003017432648', 'name': 'Recruitment'}
            ]
        }

    def build_retargeting_spec(self, pixel_id: str = None, retention_days: int = 30) -> Dict:
        """Build retargeting spec for website visitors"""
        return {
            'geo_locations': {
                'countries': ['NL']
            },
            'custom_audiences': [{
                'id': f'PIXEL_{pixel_id or self.pixel_id}',
                'name': f'Website Visitors {retention_days}d'
            }]
        }

    # ==========================================================================
    # INSIGHTS & REPORTING
    # ==========================================================================

    def get_campaign_insights(
        self,
        campaign_id: str,
        date_preset: str = 'last_7d',
        fields: List[str] = None
    ) -> Dict[str, Any]:
        """Get performance insights for a campaign"""
        default_fields = [
            'impressions', 'clicks', 'spend', 'reach',
            'cpc', 'cpm', 'ctr', 'actions', 'cost_per_action_type'
        ]

        result = self._make_request(
            'GET',
            f'{campaign_id}/insights',
            params={
                'fields': ','.join(fields or default_fields),
                'date_preset': date_preset
            }
        )

        return result.get('data', [{}])[0] if result.get('data') else {}

    def get_account_insights(self, date_preset: str = 'last_30d') -> Dict[str, Any]:
        """Get performance insights for the entire ad account"""
        fields = [
            'account_id', 'account_name', 'spend', 'impressions',
            'clicks', 'reach', 'cpc', 'cpm', 'ctr'
        ]

        result = self._make_request(
            'GET',
            f'{self.ad_account_id}/insights',
            params={
                'fields': ','.join(fields),
                'date_preset': date_preset
            }
        )

        return result.get('data', [{}])[0] if result.get('data') else {}


# ==============================================================================
# EXCEPTIONS
# ==============================================================================

class MetaApiError(Exception):
    """Custom exception for Meta API errors"""

    def __init__(self, message: str, code: int = None, error_subcode: int = None):
        self.message = message
        self.code = code
        self.error_subcode = error_subcode
        super().__init__(self.message)

    def is_token_expired(self) -> bool:
        """Check if error is due to expired token"""
        return self.code == 190

    def is_rate_limited(self) -> bool:
        """Check if error is due to rate limiting"""
        return self.code == 17 or self.code == 4

    def is_permission_error(self) -> bool:
        """Check if error is due to missing permissions"""
        return self.code in [10, 200, 294]


# ==============================================================================
# STANDALONE FUNCTIONS
# ==============================================================================

def verify_webhook_signature(payload: bytes, signature: str, app_secret: str) -> bool:
    """
    Verify Meta webhook signature

    Args:
        payload: Raw request body
        signature: X-Hub-Signature-256 header value
        app_secret: Facebook App Secret

    Returns:
        True if signature is valid
    """
    expected_signature = hmac.new(
        app_secret.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(f'sha256={expected_signature}', signature)


def hash_user_data(value: str, data_type: str = 'email') -> str:
    """
    Hash user data for Conversion API

    Args:
        value: Value to hash
        data_type: Type of data (email, phone, etc.)

    Returns:
        SHA256 hashed and lowercase value
    """
    normalized = value.lower().strip()

    if data_type == 'phone':
        # Remove non-digits
        normalized = ''.join(filter(str.isdigit, normalized))
        # Add country code if missing
        if not normalized.startswith('31'):
            normalized = '31' + normalized.lstrip('0')

    return hashlib.sha256(normalized.encode('utf-8')).hexdigest()


# ==============================================================================
# MAIN (for testing)
# ==============================================================================

if __name__ == '__main__':
    # Test token validation
    client = MetaApiClient()

    try:
        token_info = client.get_token_info()
        print(f"Token type: {token_info.token_type}")
        print(f"Expires at: {token_info.expires_at}")
        print(f"Scopes: {token_info.scopes}")
        print(f"Token valid: {client.is_token_valid()}")
    except MetaApiError as e:
        print(f"Error: {e.message}")
        if e.is_token_expired():
            print("Token has expired - please generate a new one")
