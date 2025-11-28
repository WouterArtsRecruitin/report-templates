#!/usr/bin/env python3
"""
COMPLETE META CAMPAIGN AUTOMATION FLOW
======================================
Volledige pipeline: Leonardo AI → Canva → Facebook/Instagram/LinkedIn

Flow:
1. Genereer images via Leonardo AI (MCP server of direct API)
2. Upload naar Canva en voeg tekst/branding toe
3. Publiceer naar Meta (Facebook/Instagram) via Ads API

Dependencies:
- LEONARDO_API_KEY: Leonardo AI API key
- CANVA_ACCESS_TOKEN: Canva API access token
- META_ACCESS_TOKEN: Meta/Facebook access token
- META_AD_ACCOUNT_ID: Ad account (act_XXXXXXX)
- META_PAGE_ID: Facebook Page ID
"""

import os
import json
import time
import asyncio
import logging
import hashlib
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import requests
import httpx

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ==============================================================================
# CONFIGURATION
# ==============================================================================

class Config:
    """API Configuration"""
    # Leonardo AI
    LEONARDO_API_KEY = os.getenv('LEONARDO_API_KEY')
    LEONARDO_BASE_URL = 'https://cloud.leonardo.ai/api/rest/v1'

    # Canva
    CANVA_ACCESS_TOKEN = os.getenv('CANVA_ACCESS_TOKEN')
    CANVA_BASE_URL = 'https://api.canva.com/rest/v1'

    # Meta/Facebook
    META_ACCESS_TOKEN = os.getenv('META_ACCESS_TOKEN')
    META_AD_ACCOUNT_ID = os.getenv('META_AD_ACCOUNT_ID')  # act_XXXXXXX
    META_PAGE_ID = os.getenv('META_PAGE_ID')
    META_PIXEL_ID = os.getenv('META_PIXEL_ID', '1443564313411457')
    META_API_VERSION = 'v18.0'
    META_BASE_URL = f'https://graph.facebook.com/{META_API_VERSION}'

    # Output
    OUTPUT_DIR = os.getenv('IMAGE_OUTPUT_DIR', './generated_campaigns')


class Platform(Enum):
    """Target platforms"""
    FACEBOOK_FEED = "facebook_feed"
    INSTAGRAM_FEED = "instagram_feed"
    INSTAGRAM_STORY = "instagram_story"
    LINKEDIN = "linkedin"


class AdObjective(Enum):
    """Meta Ad objectives"""
    LEADS = "OUTCOME_LEADS"
    TRAFFIC = "OUTCOME_TRAFFIC"
    AWARENESS = "OUTCOME_AWARENESS"
    ENGAGEMENT = "OUTCOME_ENGAGEMENT"


# ==============================================================================
# KANDIDATENTEKORT.NL CAMPAIGN CONTENT
# ==============================================================================

CAMPAIGN_CONTENT = {
    "voor_na_vergelijking": {
        "name": "Voor/Na Vacature Vergelijking",
        "leonardo_prompt": """Professional Dutch office environment, modern laptop on clean desk showing split screen comparison, left side displays poorly written job posting with amateur layout, right side shows professionally optimized job posting with clean design and kandidatentekort.nl branding, orange accent colors (#FF6B35), Dutch business person in professional attire reviewing the comparison, satisfied expression, bright office lighting, photorealistic style, high quality, ultra-realistic photography, shot with Canon EOS R5, 85mm lens, perfect lighting""",
        "headline": "180% meer sollicitaties",
        "primary_text": "Ontdek waarom jouw vacatures niet converteren. Onze AI analyseert in 2 minuten wat er mist en hoe je het oplost.",
        "description": "Gratis vacature-analyse",
        "cta": "LEARN_MORE",
        "link": "https://kandidatentekort.nl/analyse"
    },
    "professional_recruiter": {
        "name": "Professional Dutch Recruiter",
        "leonardo_prompt": """Professional Dutch woman, 30-40 years old, confident business attire, standing in modern Amsterdam office, holding tablet showing kandidatentekort.nl analytics dashboard with positive metrics, warm smile, orange corporate colors visible on screen, floor-to-ceiling windows with Dutch cityscape background, natural lighting, corporate photography style, authentic Dutch professional appearance, ultra-realistic photography, shot with Canon EOS R5, 85mm lens, perfect lighting""",
        "headline": "50+ bedrijven gingen je voor",
        "primary_text": "Nederlandse HR professionals vertrouwen op kandidatentekort.nl voor betere vacatureteksten. Gemiddeld 180% meer reacties.",
        "description": "Gratis voor altijd",
        "cta": "SIGN_UP",
        "link": "https://kandidatentekort.nl/start"
    },
    "industrie_techniek": {
        "name": "Industrie & Techniek",
        "leonardo_prompt": """Dutch automotive workshop or manufacturing facility, professional mechanic or technician using tablet showing kandidatentekort.nl interface, technical job posting analysis visible on screen, industrial background with modern equipment, orange safety gear and UI elements, authentic Dutch industrial workplace, professional work lighting, realistic manufacturing environment, ultra-realistic photography, shot with Canon EOS R5, 85mm lens, perfect lighting""",
        "headline": "Technici begrijpen je vacature niet",
        "primary_text": "67% van technici vindt vacatures onduidelijk. Laat onze AI je vacature analyseren en verbeteren voor technisch personeel.",
        "description": "Specifiek voor technische sectoren",
        "cta": "GET_QUOTE",
        "link": "https://kandidatentekort.nl/techniek"
    },
    "roi_kostenbesparing": {
        "name": "ROI & Kostenbesparing",
        "leonardo_prompt": """Dutch business executive in premium office setting, large monitor displaying kandidatentekort.nl cost analysis dashboard, charts showing recruitment savings and ROI improvements, orange chart elements and UI components, professional business environment, executive reviewing financial data, satisfied expression, high-end corporate photography style, ultra-realistic photography, shot with Canon EOS R5, 85mm lens, perfect lighting""",
        "headline": "€27.500 per jaar besparen",
        "primary_text": "Betere vacatures = minder externe bureaus nodig. Bereken hoeveel jij kunt besparen met geoptimaliseerde vacatureteksten.",
        "description": "65% minder recruitment kosten",
        "cta": "LEARN_MORE",
        "link": "https://kandidatentekort.nl/roi"
    },
    "mobile_quick_check": {
        "name": "Mobile Quick Check",
        "leonardo_prompt": """Professional Dutch person using smartphone on modern Dutch train or in contemporary coffee shop, phone screen clearly showing kandidatentekort.nl mobile interface with vacancy analysis in progress, orange UI elements prominent, satisfied user expression, authentic mobile usage scenario, natural lighting, lifestyle photography approach, ultra-realistic photography, shot with Canon EOS R5, 85mm lens, perfect lighting""",
        "headline": "2-minuten vacature check",
        "primary_text": "Ook onderweg je vacatures optimaliseren. Direct resultaat op je telefoon, waar je ook bent.",
        "description": "Gratis & instant",
        "cta": "LEARN_MORE",
        "link": "https://kandidatentekort.nl/check"
    }
}

PLATFORM_DIMENSIONS = {
    Platform.FACEBOOK_FEED: (1200, 628),
    Platform.INSTAGRAM_FEED: (1080, 1080),
    Platform.INSTAGRAM_STORY: (1080, 1920),
    Platform.LINKEDIN: (1200, 628),
}

NEGATIVE_PROMPT = "blur, blurry, low quality, pixelated, cartoon, animated, text overlay, watermark, distorted face, extra limbs"


# ==============================================================================
# LEONARDO AI CLIENT
# ==============================================================================

class LeonardoClient:
    """Leonardo AI API Client"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or Config.LEONARDO_API_KEY
        if not self.api_key:
            raise ValueError("LEONARDO_API_KEY is required")

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def generate_and_wait(
        self,
        prompt: str,
        width: int = 1024,
        height: int = 1024,
        model: str = "lucid_origin",
        max_wait: int = 120
    ) -> Dict[str, Any]:
        """Generate image and wait for completion"""
        model_ids = {
            "lucid_origin": "7b592283-e8a7-4c5a-9ba6-d18c31f258b9",
            "phoenix": "de7d3faf-762f-48e0-b3b7-9d0ac3a3fcf3",
            "lucid_realism": "05ce0082-2d80-4a2d-8653-4d1c85e2418e",
        }

        payload = {
            "prompt": prompt,
            "negative_prompt": NEGATIVE_PROMPT,
            "modelId": model_ids.get(model, model),
            "width": width,
            "height": height,
            "num_images": 4,
            "guidance_scale": 7.0,
            "enhancePrompt": True,
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            # Start generation
            response = await client.post(
                f"{Config.LEONARDO_BASE_URL}/generations",
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            result = response.json()

            generation_id = result.get("sdGenerationJob", {}).get("generationId")
            if not generation_id:
                return {"error": "No generation ID returned"}

            logger.info(f"Leonardo generation started: {generation_id}")

            # Poll for completion
            start_time = time.time()
            while time.time() - start_time < max_wait:
                status_response = await client.get(
                    f"{Config.LEONARDO_BASE_URL}/generations/{generation_id}",
                    headers=self.headers
                )
                status_data = status_response.json()
                status = status_data.get("generations_by_pk", {}).get("status")

                if status == "COMPLETE":
                    images = status_data.get("generations_by_pk", {}).get("generated_images", [])
                    return {
                        "success": True,
                        "generation_id": generation_id,
                        "images": [img.get("url") for img in images],
                        "status": "COMPLETE"
                    }
                elif status == "FAILED":
                    return {"error": "Generation failed", "generation_id": generation_id}

                await asyncio.sleep(3)

            return {"error": f"Timeout after {max_wait}s", "generation_id": generation_id}

    async def download_image(self, url: str, output_path: str) -> str:
        """Download image to local file"""
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.get(url)
            response.raise_for_status()

            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'wb') as f:
                f.write(response.content)

            logger.info(f"Image downloaded: {output_path}")
            return output_path


# ==============================================================================
# CANVA CLIENT
# ==============================================================================

class CanvaClient:
    """Canva API Client for design creation and asset upload"""

    def __init__(self, access_token: str = None):
        self.access_token = access_token or Config.CANVA_ACCESS_TOKEN
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        } if self.access_token else {}

    def upload_asset(self, file_path: str, name: str) -> Optional[str]:
        """Upload image to Canva as asset"""
        if not self.access_token:
            logger.warning("Canva access token not configured")
            return None

        # Get upload URL
        response = requests.post(
            f"{Config.CANVA_BASE_URL}/assets",
            headers=self.headers,
            json={"name": name}
        )

        if response.status_code != 200:
            logger.error(f"Canva upload failed: {response.text}")
            return None

        upload_data = response.json()
        upload_url = upload_data.get("upload_url")
        asset_id = upload_data.get("id")

        # Upload file
        with open(file_path, 'rb') as f:
            upload_response = requests.put(
                upload_url,
                data=f.read(),
                headers={"Content-Type": "image/png"}
            )

        if upload_response.status_code in [200, 201]:
            logger.info(f"Uploaded to Canva: {asset_id}")
            return asset_id

        return None

    def create_design_with_text(
        self,
        asset_id: str,
        headline: str,
        description: str,
        width: int = 1200,
        height: int = 628
    ) -> Optional[str]:
        """Create Canva design with text overlay"""
        if not self.access_token:
            return None

        # This would use Canva's design API to create a design with text overlay
        # For now, return the asset_id as the design reference
        logger.info(f"Design created with asset {asset_id}")
        return asset_id


# ==============================================================================
# META/FACEBOOK CLIENT
# ==============================================================================

class MetaAdsClient:
    """Meta Ads API Client for campaign creation"""

    def __init__(self, access_token: str = None, ad_account_id: str = None):
        self.access_token = access_token or Config.META_ACCESS_TOKEN
        self.ad_account_id = ad_account_id or Config.META_AD_ACCOUNT_ID
        self.page_id = Config.META_PAGE_ID

        if not self.access_token:
            logger.warning("META_ACCESS_TOKEN not configured")

    def _request(self, method: str, endpoint: str, data: Dict = None) -> Dict:
        """Make authenticated request to Meta API"""
        url = f"{Config.META_BASE_URL}/{endpoint}"
        params = {"access_token": self.access_token}

        if method == "GET":
            response = requests.get(url, params=params, timeout=30)
        elif method == "POST":
            response = requests.post(url, params=params, json=data, timeout=30)
        else:
            raise ValueError(f"Unsupported method: {method}")

        result = response.json()
        if "error" in result:
            logger.error(f"Meta API error: {result['error']}")
        return result

    def upload_image(self, image_path: str) -> Optional[str]:
        """Upload image to Meta ad account"""
        if not self.access_token or not self.ad_account_id:
            return None

        url = f"{Config.META_BASE_URL}/{self.ad_account_id}/adimages"

        with open(image_path, 'rb') as f:
            files = {'filename': f}
            response = requests.post(
                url,
                params={"access_token": self.access_token},
                files=files,
                timeout=120
            )

        result = response.json()
        if "images" in result:
            image_hash = list(result["images"].values())[0].get("hash")
            logger.info(f"Image uploaded to Meta: {image_hash}")
            return image_hash

        logger.error(f"Meta image upload failed: {result}")
        return None

    def create_campaign(
        self,
        name: str,
        objective: AdObjective = AdObjective.LEADS,
        daily_budget: int = 2500,  # €25 in cents
        status: str = "PAUSED"
    ) -> Optional[str]:
        """Create ad campaign"""
        if not self.ad_account_id:
            return None

        data = {
            "name": name,
            "objective": objective.value,
            "status": status,
            "special_ad_categories": []
        }

        result = self._request("POST", f"{self.ad_account_id}/campaigns", data)
        campaign_id = result.get("id")
        if campaign_id:
            logger.info(f"Campaign created: {campaign_id}")
        return campaign_id

    def create_adset(
        self,
        campaign_id: str,
        name: str,
        targeting: Dict,
        daily_budget: int = 2500,
        optimization_goal: str = "LEAD_GENERATION",
        status: str = "PAUSED"
    ) -> Optional[str]:
        """Create ad set within campaign"""
        if not self.ad_account_id:
            return None

        data = {
            "name": name,
            "campaign_id": campaign_id,
            "daily_budget": daily_budget,
            "billing_event": "IMPRESSIONS",
            "optimization_goal": optimization_goal,
            "targeting": json.dumps(targeting),
            "status": status
        }

        result = self._request("POST", f"{self.ad_account_id}/adsets", data)
        return result.get("id")

    def create_ad(
        self,
        adset_id: str,
        name: str,
        image_hash: str,
        headline: str,
        primary_text: str,
        link_url: str,
        cta: str = "LEARN_MORE",
        status: str = "PAUSED"
    ) -> Optional[str]:
        """Create ad creative and ad"""
        if not self.ad_account_id or not self.page_id:
            return None

        # Create ad creative
        creative_data = {
            "name": f"Creative - {name}",
            "object_story_spec": {
                "page_id": self.page_id,
                "link_data": {
                    "image_hash": image_hash,
                    "link": link_url,
                    "message": primary_text,
                    "name": headline,
                    "call_to_action": {"type": cta}
                }
            }
        }

        creative_result = self._request("POST", f"{self.ad_account_id}/adcreatives", creative_data)
        creative_id = creative_result.get("id")

        if not creative_id:
            return None

        # Create ad
        ad_data = {
            "name": name,
            "adset_id": adset_id,
            "creative": {"creative_id": creative_id},
            "status": status
        }

        ad_result = self._request("POST", f"{self.ad_account_id}/ads", ad_data)
        ad_id = ad_result.get("id")

        if ad_id:
            logger.info(f"Ad created: {ad_id}")
        return ad_id

    def get_hr_directors_targeting(self) -> Dict:
        """Get targeting for HR Directors in Netherlands"""
        return {
            "geo_locations": {
                "countries": ["NL"],
                "location_types": ["home", "recent"]
            },
            "age_min": 28,
            "age_max": 58,
            "publisher_platforms": ["facebook", "instagram"],
            "facebook_positions": ["feed"],
            "instagram_positions": ["stream"]
        }


# ==============================================================================
# COMPLETE AUTOMATION FLOW
# ==============================================================================

class MetaCampaignAutomation:
    """
    Complete automation flow: Leonardo → Canva → Facebook

    Usage:
        automation = MetaCampaignAutomation()
        result = await automation.run_campaign_flow("voor_na_vergelijking", Platform.FACEBOOK_FEED)
    """

    def __init__(self):
        self.leonardo = LeonardoClient() if Config.LEONARDO_API_KEY else None
        self.canva = CanvaClient() if Config.CANVA_ACCESS_TOKEN else None
        self.meta = MetaAdsClient() if Config.META_ACCESS_TOKEN else None
        self.output_dir = Config.OUTPUT_DIR

    async def run_campaign_flow(
        self,
        campaign_key: str,
        platform: Platform = Platform.FACEBOOK_FEED,
        create_meta_campaign: bool = False
    ) -> Dict[str, Any]:
        """
        Run complete campaign flow

        1. Generate images with Leonardo AI
        2. Upload to Canva (optional)
        3. Create Meta campaign (optional)
        """
        if campaign_key not in CAMPAIGN_CONTENT:
            return {"error": f"Unknown campaign: {campaign_key}"}

        campaign = CAMPAIGN_CONTENT[campaign_key]
        width, height = PLATFORM_DIMENSIONS[platform]

        result = {
            "campaign": campaign["name"],
            "platform": platform.value,
            "timestamp": datetime.now().isoformat(),
            "steps": []
        }

        # Step 1: Generate images with Leonardo AI
        logger.info(f"Step 1: Generating images for {campaign['name']}")
        if self.leonardo:
            try:
                gen_result = await self.leonardo.generate_and_wait(
                    prompt=campaign["leonardo_prompt"],
                    width=width,
                    height=height
                )

                result["steps"].append({
                    "step": "leonardo_generation",
                    "status": "success" if gen_result.get("success") else "failed",
                    "images": gen_result.get("images", []),
                    "generation_id": gen_result.get("generation_id")
                })

                # Download first image
                if gen_result.get("images"):
                    image_url = gen_result["images"][0]
                    local_path = os.path.join(
                        self.output_dir,
                        campaign_key,
                        f"{platform.value}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    )
                    await self.leonardo.download_image(image_url, local_path)
                    result["local_image_path"] = local_path

            except Exception as e:
                result["steps"].append({
                    "step": "leonardo_generation",
                    "status": "error",
                    "error": str(e)
                })
        else:
            result["steps"].append({
                "step": "leonardo_generation",
                "status": "skipped",
                "reason": "LEONARDO_API_KEY not configured"
            })

        # Step 2: Upload to Canva
        logger.info(f"Step 2: Uploading to Canva")
        if self.canva and result.get("local_image_path"):
            try:
                asset_id = self.canva.upload_asset(
                    result["local_image_path"],
                    f"{campaign['name']} - {platform.value}"
                )
                result["steps"].append({
                    "step": "canva_upload",
                    "status": "success" if asset_id else "failed",
                    "asset_id": asset_id
                })
                result["canva_asset_id"] = asset_id
            except Exception as e:
                result["steps"].append({
                    "step": "canva_upload",
                    "status": "error",
                    "error": str(e)
                })
        else:
            result["steps"].append({
                "step": "canva_upload",
                "status": "skipped",
                "reason": "CANVA_ACCESS_TOKEN not configured or no image"
            })

        # Step 3: Create Meta Campaign (optional)
        if create_meta_campaign and self.meta and result.get("local_image_path"):
            logger.info(f"Step 3: Creating Meta campaign")
            try:
                # Upload image to Meta
                image_hash = self.meta.upload_image(result["local_image_path"])

                if image_hash:
                    # Create campaign
                    campaign_id = self.meta.create_campaign(
                        name=f"Kandidatentekort - {campaign['name']}",
                        objective=AdObjective.LEADS,
                        status="PAUSED"
                    )

                    if campaign_id:
                        # Create ad set
                        adset_id = self.meta.create_adset(
                            campaign_id=campaign_id,
                            name=f"{campaign['name']} - {platform.value}",
                            targeting=self.meta.get_hr_directors_targeting(),
                            daily_budget=2500
                        )

                        if adset_id:
                            # Create ad
                            ad_id = self.meta.create_ad(
                                adset_id=adset_id,
                                name=f"Ad - {campaign['name']}",
                                image_hash=image_hash,
                                headline=campaign["headline"],
                                primary_text=campaign["primary_text"],
                                link_url=campaign["link"],
                                cta=campaign["cta"]
                            )

                            result["steps"].append({
                                "step": "meta_campaign",
                                "status": "success",
                                "campaign_id": campaign_id,
                                "adset_id": adset_id,
                                "ad_id": ad_id,
                                "image_hash": image_hash
                            })
                            result["meta_campaign_id"] = campaign_id

            except Exception as e:
                result["steps"].append({
                    "step": "meta_campaign",
                    "status": "error",
                    "error": str(e)
                })
        else:
            result["steps"].append({
                "step": "meta_campaign",
                "status": "skipped",
                "reason": "create_meta_campaign=False or missing config"
            })

        return result

    async def run_all_campaigns(
        self,
        platforms: List[Platform] = None,
        create_meta_campaigns: bool = False
    ) -> Dict[str, Any]:
        """Run flow for all campaigns"""
        if platforms is None:
            platforms = [Platform.FACEBOOK_FEED]

        all_results = {
            "started_at": datetime.now().isoformat(),
            "campaigns": {}
        }

        for campaign_key in CAMPAIGN_CONTENT.keys():
            campaign_results = []
            for platform in platforms:
                result = await self.run_campaign_flow(
                    campaign_key,
                    platform,
                    create_meta_campaigns
                )
                campaign_results.append(result)
            all_results["campaigns"][campaign_key] = campaign_results

        all_results["completed_at"] = datetime.now().isoformat()
        return all_results


# ==============================================================================
# CLI
# ==============================================================================

async def main():
    """Command line interface"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Meta Campaign Automation: Leonardo → Canva → Facebook"
    )
    parser.add_argument(
        "--campaign",
        choices=list(CAMPAIGN_CONTENT.keys()) + ["all"],
        default="all",
        help="Campaign to run"
    )
    parser.add_argument(
        "--platform",
        choices=["facebook", "instagram", "instagram_story", "linkedin"],
        default="facebook",
        help="Target platform"
    )
    parser.add_argument(
        "--create-meta-campaign",
        action="store_true",
        help="Actually create campaign in Meta Ads Manager"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available campaigns"
    )

    args = parser.parse_args()

    if args.list:
        print("\nAvailable Campaigns:")
        print("=" * 60)
        for key, campaign in CAMPAIGN_CONTENT.items():
            print(f"\n{key}:")
            print(f"  Name: {campaign['name']}")
            print(f"  Headline: {campaign['headline']}")
            print(f"  CTA: {campaign['cta']}")
            print(f"  Link: {campaign['link']}")
        return

    # Map platform
    platform_map = {
        "facebook": Platform.FACEBOOK_FEED,
        "instagram": Platform.INSTAGRAM_FEED,
        "instagram_story": Platform.INSTAGRAM_STORY,
        "linkedin": Platform.LINKEDIN
    }
    platform = platform_map.get(args.platform, Platform.FACEBOOK_FEED)

    automation = MetaCampaignAutomation()

    if args.campaign == "all":
        print("\nRunning all campaigns...")
        results = await automation.run_all_campaigns(
            platforms=[platform],
            create_meta_campaigns=args.create_meta_campaign
        )
    else:
        print(f"\nRunning {args.campaign}...")
        results = await automation.run_campaign_flow(
            args.campaign,
            platform,
            args.create_meta_campaign
        )

    # Save results
    output_file = os.path.join(
        Config.OUTPUT_DIR,
        f"flow_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to: {output_file}")
    print(f"Images saved to: {Config.OUTPUT_DIR}")


if __name__ == "__main__":
    asyncio.run(main())
