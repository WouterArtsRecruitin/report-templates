#!/usr/bin/env python3
"""
META CAMPAIGN AUTOMATION SERVICE
================================
Automated campaign creation and management for kandidatentekort.nl

Features:
- Pre-built audience segments (HR Directors, Operations, Retargeting)
- Campaign templates for different objectives
- Budget management and optimization
- A/B testing setup
- Performance monitoring

Campaign Structure:
- Campaign 1: Cold - HR Directors
- Campaign 2: Cold - Operations/COO
- Campaign 3: Retargeting (Website Visitors)
"""

import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from enum import Enum

from meta_api_client import (
    MetaApiClient,
    CampaignObjective,
    OptimizationGoal,
    MetaApiError
)
from pixel_tracking import ConversionAPI, UserData, CustomData

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ==============================================================================
# CONFIGURATION
# ==============================================================================

class CampaignConfig:
    """Campaign Configuration for kandidatentekort.nl"""
    # Budget tiers (in EUR cents)
    BUDGET_TIER_1 = 2500  # €25/day (€175/week)
    BUDGET_TIER_2 = 5000  # €50/day (€350/week)
    BUDGET_TIER_3 = 7500  # €75/day (€500/week)

    # Default settings
    DEFAULT_BID_STRATEGY = 'LOWEST_COST_WITH_BID_CAP'
    DEFAULT_STATUS = 'PAUSED'  # Start paused for review

    # Special ad categories
    SPECIAL_AD_CATEGORIES = []  # Not employment/housing/credit ads


# ==============================================================================
# AUDIENCE SEGMENTS
# ==============================================================================

class AudienceSegment(Enum):
    """Pre-defined audience segments"""
    HR_DIRECTORS = 'hr_directors'
    HR_MANAGERS = 'hr_managers'
    OPERATIONS_COO = 'operations_coo'
    RECRUITMENT_AGENCIES = 'recruitment_agencies'
    SME_OWNERS = 'sme_owners'
    TECH_SECTOR = 'tech_sector'
    INDUSTRY_MANUFACTURING = 'industry_manufacturing'
    HEALTHCARE = 'healthcare'
    RETARGETING_7D = 'retargeting_7d'
    RETARGETING_30D = 'retargeting_30d'
    RETARGETING_60D = 'retargeting_60d'
    LOOKALIKE_LEADS = 'lookalike_leads'
    LOOKALIKE_CUSTOMERS = 'lookalike_customers'
    ENGAGED_FB_IG = 'engaged_fb_ig'
    VIDEO_VIEWERS = 'video_viewers'


@dataclass
class AudienceDefinition:
    """Audience segment definition"""
    name: str
    description: str
    segment: AudienceSegment
    targeting: Dict[str, Any]
    estimated_reach: str
    recommended_budget: int  # Daily budget in cents


# ==============================================================================
# AUDIENCE BUILDER
# ==============================================================================

class AudienceBuilder:
    """
    Build targeting specifications for different audience segments

    Usage:
        builder = AudienceBuilder()
        targeting = builder.get_targeting(AudienceSegment.HR_DIRECTORS)
    """

    def __init__(self, pixel_id: str = None):
        self.pixel_id = pixel_id or os.getenv('META_PIXEL_ID', '1443564313411457')

    def get_targeting(self, segment: AudienceSegment) -> Dict[str, Any]:
        """Get targeting specification for a segment"""
        targeting_map = {
            AudienceSegment.HR_DIRECTORS: self._hr_directors_targeting(),
            AudienceSegment.HR_MANAGERS: self._hr_managers_targeting(),
            AudienceSegment.OPERATIONS_COO: self._operations_coo_targeting(),
            AudienceSegment.RECRUITMENT_AGENCIES: self._recruitment_agencies_targeting(),
            AudienceSegment.SME_OWNERS: self._sme_owners_targeting(),
            AudienceSegment.TECH_SECTOR: self._tech_sector_targeting(),
            AudienceSegment.INDUSTRY_MANUFACTURING: self._industry_manufacturing_targeting(),
            AudienceSegment.HEALTHCARE: self._healthcare_targeting(),
            AudienceSegment.RETARGETING_7D: self._retargeting_targeting(7),
            AudienceSegment.RETARGETING_30D: self._retargeting_targeting(30),
            AudienceSegment.RETARGETING_60D: self._retargeting_targeting(60),
        }

        return targeting_map.get(segment, self._default_targeting())

    def get_all_segments(self) -> List[AudienceDefinition]:
        """Get all pre-defined audience segments with their definitions"""
        return [
            AudienceDefinition(
                name="HR Directors Netherlands",
                description="Senior HR decision makers in the Netherlands",
                segment=AudienceSegment.HR_DIRECTORS,
                targeting=self._hr_directors_targeting(),
                estimated_reach="15,000-25,000",
                recommended_budget=3500
            ),
            AudienceDefinition(
                name="HR Managers Netherlands",
                description="HR Managers and HR Business Partners",
                segment=AudienceSegment.HR_MANAGERS,
                targeting=self._hr_managers_targeting(),
                estimated_reach="40,000-60,000",
                recommended_budget=2500
            ),
            AudienceDefinition(
                name="Operations & COO",
                description="Operations leaders who handle hiring",
                segment=AudienceSegment.OPERATIONS_COO,
                targeting=self._operations_coo_targeting(),
                estimated_reach="20,000-35,000",
                recommended_budget=3000
            ),
            AudienceDefinition(
                name="Recruitment Agency Owners",
                description="Recruitment bureau owners and directors",
                segment=AudienceSegment.RECRUITMENT_AGENCIES,
                targeting=self._recruitment_agencies_targeting(),
                estimated_reach="5,000-10,000",
                recommended_budget=2500
            ),
            AudienceDefinition(
                name="SME Business Owners",
                description="Small to medium business owners who do hiring",
                segment=AudienceSegment.SME_OWNERS,
                targeting=self._sme_owners_targeting(),
                estimated_reach="80,000-120,000",
                recommended_budget=2500
            ),
            AudienceDefinition(
                name="Tech Sector HR",
                description="HR professionals in tech/IT companies",
                segment=AudienceSegment.TECH_SECTOR,
                targeting=self._tech_sector_targeting(),
                estimated_reach="10,000-18,000",
                recommended_budget=3000
            ),
            AudienceDefinition(
                name="Industry & Manufacturing HR",
                description="HR in industrial and manufacturing sector",
                segment=AudienceSegment.INDUSTRY_MANUFACTURING,
                targeting=self._industry_manufacturing_targeting(),
                estimated_reach="12,000-20,000",
                recommended_budget=2500
            ),
            AudienceDefinition(
                name="Healthcare HR",
                description="HR professionals in healthcare sector",
                segment=AudienceSegment.HEALTHCARE,
                targeting=self._healthcare_targeting(),
                estimated_reach="8,000-15,000",
                recommended_budget=3000
            ),
            AudienceDefinition(
                name="Website Visitors (7 days)",
                description="Recent website visitors for hot retargeting",
                segment=AudienceSegment.RETARGETING_7D,
                targeting=self._retargeting_targeting(7),
                estimated_reach="500-2,000",
                recommended_budget=1500
            ),
            AudienceDefinition(
                name="Website Visitors (30 days)",
                description="Website visitors for warm retargeting",
                segment=AudienceSegment.RETARGETING_30D,
                targeting=self._retargeting_targeting(30),
                estimated_reach="1,500-5,000",
                recommended_budget=2000
            ),
            AudienceDefinition(
                name="Website Visitors (60 days)",
                description="Extended retargeting pool",
                segment=AudienceSegment.RETARGETING_60D,
                targeting=self._retargeting_targeting(60),
                estimated_reach="3,000-10,000",
                recommended_budget=2000
            ),
        ]

    # ==========================================================================
    # TARGETING SPECIFICATIONS
    # ==========================================================================

    def _default_targeting(self) -> Dict[str, Any]:
        """Default Netherlands B2B targeting"""
        return {
            'geo_locations': {
                'countries': ['NL'],
                'location_types': ['home', 'recent']
            },
            'age_min': 25,
            'age_max': 60,
            'publisher_platforms': ['facebook', 'instagram'],
            'facebook_positions': ['feed', 'instant_article', 'instream_video'],
            'instagram_positions': ['stream', 'story', 'explore']
        }

    def _hr_directors_targeting(self) -> Dict[str, Any]:
        """HR Directors targeting specification"""
        base = self._default_targeting()
        base.update({
            'age_min': 30,
            'age_max': 58,
            'work_positions': [
                {'id': '107756515917549', 'name': 'HR Director'},
                {'id': '113371672019222', 'name': 'Chief Human Resources Officer'},
                {'id': '106159722750611', 'name': 'VP Human Resources'},
                {'id': '112445598771543', 'name': 'Head of HR'},
                {'id': '108076792556090', 'name': 'Hoofd HR'},
                {'id': '110841058935139', 'name': 'Directeur HR'},
                {'id': '108461929183051', 'name': 'Directeur P&O'},
                {'id': '109482319069234', 'name': 'Head of People'},
                {'id': '107438579285201', 'name': 'Chief People Officer'}
            ],
            'targeting_optimization': 'none',
            'flexible_spec': [{
                'interests': [
                    {'id': '6003156392553', 'name': 'Human resource management'},
                    {'id': '6003017432648', 'name': 'Recruitment'},
                    {'id': '6003366859849', 'name': 'Talent management'}
                ]
            }]
        })
        return base

    def _hr_managers_targeting(self) -> Dict[str, Any]:
        """HR Managers targeting specification"""
        base = self._default_targeting()
        base.update({
            'age_min': 28,
            'age_max': 55,
            'work_positions': [
                {'id': '108147285880481', 'name': 'HR Manager'},
                {'id': '106186806071543', 'name': 'HR Business Partner'},
                {'id': '108395165880234', 'name': 'Senior HR Manager'},
                {'id': '107534452615234', 'name': 'HR Specialist'},
                {'id': '109234567890123', 'name': 'P&O Manager'},
                {'id': '110345678901234', 'name': 'HR Adviseur'}
            ],
            'flexible_spec': [{
                'interests': [
                    {'id': '6003156392553', 'name': 'Human resource management'},
                    {'id': '6003017432648', 'name': 'Recruitment'}
                ]
            }]
        })
        return base

    def _operations_coo_targeting(self) -> Dict[str, Any]:
        """Operations/COO targeting specification"""
        base = self._default_targeting()
        base.update({
            'age_min': 32,
            'age_max': 58,
            'work_positions': [
                {'id': '108447645850630', 'name': 'COO'},
                {'id': '105645139469143', 'name': 'Chief Operating Officer'},
                {'id': '107911055909073', 'name': 'Operations Director'},
                {'id': '110182412348619', 'name': 'Operations Manager'},
                {'id': '106077216087688', 'name': 'VP Operations'},
                {'id': '108234567890234', 'name': 'Directeur Operaties'},
                {'id': '109345678901345', 'name': 'Hoofd Operations'}
            ],
            'flexible_spec': [{
                'interests': [
                    {'id': '6003223996963', 'name': 'Business operations'},
                    {'id': '6003139166621', 'name': 'Management'}
                ]
            }]
        })
        return base

    def _recruitment_agencies_targeting(self) -> Dict[str, Any]:
        """Recruitment agency owners targeting"""
        base = self._default_targeting()
        base.update({
            'age_min': 28,
            'age_max': 55,
            'work_positions': [
                {'id': '107823456789012', 'name': 'Recruitment Consultant'},
                {'id': '108934567890123', 'name': 'Managing Director'},
                {'id': '109045678901234', 'name': 'Director'},
                {'id': '110156789012345', 'name': 'Owner'}
            ],
            'work_employers': [
                {'id': '108246789012345', 'name': 'Recruitment'},
                {'id': '109357890123456', 'name': 'Staffing'},
                {'id': '110468901234567', 'name': 'Headhunting'}
            ],
            'flexible_spec': [{
                'interests': [
                    {'id': '6003017432648', 'name': 'Recruitment'},
                    {'id': '6003156392553', 'name': 'Human resource management'},
                    {'id': '6003445678901', 'name': 'Staffing agency'}
                ]
            }]
        })
        return base

    def _sme_owners_targeting(self) -> Dict[str, Any]:
        """SME business owners targeting"""
        base = self._default_targeting()
        base.update({
            'age_min': 30,
            'age_max': 60,
            'work_positions': [
                {'id': '110156789012345', 'name': 'Owner'},
                {'id': '107234567890123', 'name': 'Founder'},
                {'id': '108345678901234', 'name': 'CEO'},
                {'id': '109456789012345', 'name': 'Managing Director'},
                {'id': '110567890123456', 'name': 'Directeur'},
                {'id': '111678901234567', 'name': 'Eigenaar'},
                {'id': '112789012345678', 'name': 'DGA'}
            ],
            'behaviors': [
                {'id': '6002714895372', 'name': 'Small business owners'}
            ],
            'flexible_spec': [{
                'interests': [
                    {'id': '6003139166621', 'name': 'Management'},
                    {'id': '6003017432648', 'name': 'Recruitment'},
                    {'id': '6003556789012', 'name': 'Entrepreneurship'}
                ]
            }]
        })
        return base

    def _tech_sector_targeting(self) -> Dict[str, Any]:
        """Tech sector HR targeting"""
        base = self._hr_managers_targeting()
        base.update({
            'industries': [
                {'id': '6003456789012', 'name': 'Information Technology'},
                {'id': '6003567890123', 'name': 'Software'},
                {'id': '6003678901234', 'name': 'Technology'}
            ],
            'flexible_spec': [{
                'interests': [
                    {'id': '6003156392553', 'name': 'Human resource management'},
                    {'id': '6003017432648', 'name': 'Recruitment'},
                    {'id': '6003789012345', 'name': 'Technology recruiting'}
                ]
            }]
        })
        return base

    def _industry_manufacturing_targeting(self) -> Dict[str, Any]:
        """Industry/Manufacturing HR targeting"""
        base = self._hr_managers_targeting()
        base.update({
            'industries': [
                {'id': '6003890123456', 'name': 'Manufacturing'},
                {'id': '6003901234567', 'name': 'Industrial'},
                {'id': '6003012345678', 'name': 'Engineering'},
                {'id': '6003123456789', 'name': 'Automotive'}
            ],
            'flexible_spec': [{
                'interests': [
                    {'id': '6003156392553', 'name': 'Human resource management'},
                    {'id': '6003234567890', 'name': 'Manufacturing'},
                    {'id': '6003345678901', 'name': 'Industrial'}
                ]
            }]
        })
        return base

    def _healthcare_targeting(self) -> Dict[str, Any]:
        """Healthcare HR targeting"""
        base = self._hr_managers_targeting()
        base.update({
            'industries': [
                {'id': '6003456789012', 'name': 'Healthcare'},
                {'id': '6003567890123', 'name': 'Medical'},
                {'id': '6003678901234', 'name': 'Hospital'},
                {'id': '6003789012345', 'name': 'Zorg'}
            ],
            'flexible_spec': [{
                'interests': [
                    {'id': '6003156392553', 'name': 'Human resource management'},
                    {'id': '6003890123456', 'name': 'Healthcare'},
                    {'id': '6003901234567', 'name': 'Healthcare recruiting'}
                ]
            }]
        })
        return base

    def _retargeting_targeting(self, days: int) -> Dict[str, Any]:
        """Retargeting based on pixel data"""
        return {
            'geo_locations': {
                'countries': ['NL'],
                'location_types': ['home', 'recent']
            },
            'age_min': 25,
            'age_max': 60,
            'custom_audiences': [{
                'id': f'website_visitors_{days}d',
                'name': f'Website Visitors {days} Days'
            }],
            'excluded_custom_audiences': [{
                'id': 'converted_leads',
                'name': 'Converted Leads'
            }]
        }


# ==============================================================================
# CAMPAIGN TEMPLATES
# ==============================================================================

@dataclass
class CampaignTemplate:
    """Campaign template definition"""
    name: str
    objective: CampaignObjective
    optimization_goal: OptimizationGoal
    audience_segments: List[AudienceSegment]
    daily_budget: int
    ad_copy_variants: List[Dict[str, str]]
    description: str


class CampaignTemplates:
    """Pre-defined campaign templates for kandidatentekort.nl"""

    @staticmethod
    def cold_hr_directors() -> CampaignTemplate:
        """Campaign targeting HR Directors"""
        return CampaignTemplate(
            name="Kandidatentekort - Cold HR Directors",
            objective=CampaignObjective.OUTCOME_LEADS,
            optimization_goal=OptimizationGoal.LEAD_GENERATION,
            audience_segments=[AudienceSegment.HR_DIRECTORS],
            daily_budget=3500,  # €35/day
            ad_copy_variants=[
                {
                    "headline": "180% meer sollicitaties?",
                    "primary_text": "Ontdek waarom jouw vacatures niet converteren. Gratis vacature-analyse in 2 minuten.",
                    "cta": "LEARN_MORE"
                },
                {
                    "headline": "Vacatures die niet werken?",
                    "primary_text": "67% van vacatures mist cruciale elementen. Check nu gratis hoe jouw vacatures scoren.",
                    "cta": "SIGN_UP"
                },
                {
                    "headline": "Kandidatentekort oplossen",
                    "primary_text": "Stop met zoeken, start met vinden. AI-analyse toont exact wat je vacatures missen.",
                    "cta": "GET_QUOTE"
                }
            ],
            description="Cold acquisition campaign targeting HR Directors in the Netherlands"
        )

    @staticmethod
    def cold_operations() -> CampaignTemplate:
        """Campaign targeting Operations/COO"""
        return CampaignTemplate(
            name="Kandidatentekort - Cold Operations",
            objective=CampaignObjective.OUTCOME_LEADS,
            optimization_goal=OptimizationGoal.LEAD_GENERATION,
            audience_segments=[AudienceSegment.OPERATIONS_COO, AudienceSegment.SME_OWNERS],
            daily_budget=2500,  # €25/day
            ad_copy_variants=[
                {
                    "headline": "Openstaande vacatures kosten geld",
                    "primary_text": "Elke dag zonder de juiste medewerker kost productiviteit. Optimaliseer je vacatures met AI.",
                    "cta": "LEARN_MORE"
                },
                {
                    "headline": "Te weinig sollicitanten?",
                    "primary_text": "Je vacaturetekst is het probleem. Ontdek in 2 minuten wat er mist.",
                    "cta": "GET_QUOTE"
                }
            ],
            description="Cold acquisition campaign targeting Operations leaders and business owners"
        )

    @staticmethod
    def retargeting() -> CampaignTemplate:
        """Retargeting campaign for website visitors"""
        return CampaignTemplate(
            name="Kandidatentekort - Retargeting",
            objective=CampaignObjective.OUTCOME_LEADS,
            optimization_goal=OptimizationGoal.CONVERSIONS,
            audience_segments=[AudienceSegment.RETARGETING_7D, AudienceSegment.RETARGETING_30D],
            daily_budget=1500,  # €15/day
            ad_copy_variants=[
                {
                    "headline": "Nog niet geanalyseerd?",
                    "primary_text": "Je was bijna klaar. Rond je gratis vacature-analyse af en ontvang direct je rapport.",
                    "cta": "SIGN_UP"
                },
                {
                    "headline": "Kom terug voor je resultaat",
                    "primary_text": "Wist je dat je vacature 3 kritieke verbeterpunten heeft? Check het nu.",
                    "cta": "LEARN_MORE"
                }
            ],
            description="Retargeting campaign for website visitors who didn't convert"
        )

    @staticmethod
    def awareness() -> CampaignTemplate:
        """Brand awareness campaign"""
        return CampaignTemplate(
            name="Kandidatentekort - Awareness",
            objective=CampaignObjective.OUTCOME_AWARENESS,
            optimization_goal=OptimizationGoal.REACH,
            audience_segments=[AudienceSegment.HR_MANAGERS, AudienceSegment.RECRUITMENT_AGENCIES],
            daily_budget=2000,  # €20/day
            ad_copy_variants=[
                {
                    "headline": "De #1 vacature-analyzer",
                    "primary_text": "50+ Nederlandse bedrijven verbeteren hun vacatures met kandidatentekort.nl",
                    "cta": "LEARN_MORE"
                }
            ],
            description="Brand awareness campaign for HR professionals"
        )

    @staticmethod
    def get_all_templates() -> List[CampaignTemplate]:
        """Get all available campaign templates"""
        return [
            CampaignTemplates.cold_hr_directors(),
            CampaignTemplates.cold_operations(),
            CampaignTemplates.retargeting(),
            CampaignTemplates.awareness()
        ]


# ==============================================================================
# CAMPAIGN AUTOMATION SERVICE
# ==============================================================================

class CampaignAutomationService:
    """
    Automate campaign creation and management

    Usage:
        service = CampaignAutomationService()

        # Create all campaigns from templates
        campaigns = service.create_all_campaigns()

        # Get performance report
        report = service.get_performance_report()
    """

    def __init__(self, api_client: MetaApiClient = None):
        self.api_client = api_client or MetaApiClient()
        self.audience_builder = AudienceBuilder()
        self.conversion_api = ConversionAPI()

    def create_campaign_from_template(
        self,
        template: CampaignTemplate,
        status: str = 'PAUSED'
    ) -> Dict[str, Any]:
        """
        Create a campaign from a template

        Args:
            template: CampaignTemplate to use
            status: Initial campaign status

        Returns:
            Created campaign data
        """
        try:
            # Create campaign
            campaign = self.api_client.create_campaign(
                name=template.name,
                objective=template.objective,
                status=status,
                daily_budget=template.daily_budget,
                special_ad_categories=CampaignConfig.SPECIAL_AD_CATEGORIES
            )

            campaign_id = campaign.get('id')
            logger.info(f"Created campaign: {campaign_id} ({template.name})")

            # Create ad sets for each audience segment
            ad_sets = []
            for segment in template.audience_segments:
                targeting = self.audience_builder.get_targeting(segment)

                ad_set = self.api_client.create_ad_set(
                    name=f"{template.name} - {segment.value}",
                    campaign_id=campaign_id,
                    daily_budget=template.daily_budget // len(template.audience_segments),
                    targeting=targeting,
                    optimization_goal=template.optimization_goal,
                    status=status
                )

                ad_sets.append(ad_set)
                logger.info(f"Created ad set: {ad_set.get('id')}")

            return {
                'campaign': campaign,
                'ad_sets': ad_sets,
                'template': template.name
            }

        except MetaApiError as e:
            logger.error(f"Failed to create campaign: {e.message}")
            raise

    def create_all_campaigns(self, status: str = 'PAUSED') -> List[Dict]:
        """Create all campaigns from templates"""
        results = []

        for template in CampaignTemplates.get_all_templates():
            try:
                result = self.create_campaign_from_template(template, status)
                results.append(result)
            except MetaApiError as e:
                logger.error(f"Skipping template {template.name}: {e.message}")
                results.append({
                    'template': template.name,
                    'error': e.message
                })

        return results

    def get_performance_report(self, days: int = 7) -> Dict[str, Any]:
        """
        Get performance report for all campaigns

        Args:
            days: Number of days to report on
        """
        try:
            campaigns = self.api_client.get_campaigns()

            report = {
                'period': f'last_{days}d',
                'generated_at': datetime.now().isoformat(),
                'campaigns': [],
                'totals': {
                    'spend': 0,
                    'impressions': 0,
                    'clicks': 0,
                    'leads': 0
                }
            }

            for campaign in campaigns:
                insights = self.api_client.get_campaign_insights(
                    campaign['id'],
                    date_preset=f'last_{days}d'
                )

                campaign_data = {
                    'id': campaign['id'],
                    'name': campaign['name'],
                    'status': campaign['status'],
                    'spend': float(insights.get('spend', 0)),
                    'impressions': int(insights.get('impressions', 0)),
                    'clicks': int(insights.get('clicks', 0)),
                    'cpc': float(insights.get('cpc', 0)),
                    'cpm': float(insights.get('cpm', 0)),
                    'ctr': float(insights.get('ctr', 0))
                }

                # Extract leads from actions
                actions = insights.get('actions', [])
                leads = next(
                    (a.get('value', 0) for a in actions if a.get('action_type') == 'lead'),
                    0
                )
                campaign_data['leads'] = int(leads)

                report['campaigns'].append(campaign_data)

                # Update totals
                report['totals']['spend'] += campaign_data['spend']
                report['totals']['impressions'] += campaign_data['impressions']
                report['totals']['clicks'] += campaign_data['clicks']
                report['totals']['leads'] += campaign_data['leads']

            # Calculate overall metrics
            if report['totals']['clicks'] > 0:
                report['totals']['cpc'] = report['totals']['spend'] / report['totals']['clicks']
            if report['totals']['impressions'] > 0:
                report['totals']['cpm'] = (report['totals']['spend'] / report['totals']['impressions']) * 1000
                report['totals']['ctr'] = (report['totals']['clicks'] / report['totals']['impressions']) * 100
            if report['totals']['leads'] > 0:
                report['totals']['cpl'] = report['totals']['spend'] / report['totals']['leads']

            return report

        except MetaApiError as e:
            logger.error(f"Failed to generate report: {e.message}")
            return {'error': e.message}

    def optimize_budgets(self, target_cpl: float = 25.0) -> Dict[str, Any]:
        """
        Optimize campaign budgets based on performance

        Args:
            target_cpl: Target cost per lead in EUR
        """
        report = self.get_performance_report(7)
        recommendations = []

        for campaign in report.get('campaigns', []):
            if campaign.get('leads', 0) > 0:
                cpl = campaign['spend'] / campaign['leads']

                if cpl < target_cpl * 0.8:
                    # Performing well, increase budget
                    recommendations.append({
                        'campaign_id': campaign['id'],
                        'campaign_name': campaign['name'],
                        'action': 'INCREASE_BUDGET',
                        'reason': f'CPL ({cpl:.2f}€) below target ({target_cpl}€)',
                        'current_cpl': cpl
                    })
                elif cpl > target_cpl * 1.5:
                    # Underperforming, decrease budget
                    recommendations.append({
                        'campaign_id': campaign['id'],
                        'campaign_name': campaign['name'],
                        'action': 'DECREASE_BUDGET',
                        'reason': f'CPL ({cpl:.2f}€) above target ({target_cpl}€)',
                        'current_cpl': cpl
                    })
            elif campaign['spend'] > 50 and campaign['leads'] == 0:
                # Spending without leads
                recommendations.append({
                    'campaign_id': campaign['id'],
                    'campaign_name': campaign['name'],
                    'action': 'REVIEW_TARGETING',
                    'reason': f'Spent {campaign["spend"]:.2f}€ with 0 leads'
                })

        return {
            'target_cpl': target_cpl,
            'recommendations': recommendations
        }


# ==============================================================================
# MAIN (for testing)
# ==============================================================================

if __name__ == '__main__':
    # Display available audience segments
    builder = AudienceBuilder()
    segments = builder.get_all_segments()

    print("=" * 60)
    print("AVAILABLE AUDIENCE SEGMENTS")
    print("=" * 60)

    for segment in segments:
        print(f"\n{segment.name}")
        print(f"  Description: {segment.description}")
        print(f"  Estimated Reach: {segment.estimated_reach}")
        print(f"  Recommended Budget: €{segment.recommended_budget / 100:.2f}/day")

    print("\n" + "=" * 60)
    print("CAMPAIGN TEMPLATES")
    print("=" * 60)

    for template in CampaignTemplates.get_all_templates():
        print(f"\n{template.name}")
        print(f"  Objective: {template.objective.value}")
        print(f"  Budget: €{template.daily_budget / 100:.2f}/day")
        print(f"  Segments: {[s.value for s in template.audience_segments]}")
        print(f"  Ad Variants: {len(template.ad_copy_variants)}")
