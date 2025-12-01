#!/usr/bin/env python3
"""
LEONARDO AI + CANVA WORKFLOW
============================
Automatiseer het genereren van Meta campagne visuals via Leonardo AI
en push ze naar Canva templates.

Workflow:
1. Genereer images via Leonardo AI API
2. Download gegenereerde images
3. Upload naar Canva via API
4. Update campagne templates

Vereisten:
- LEONARDO_API_KEY: Leonardo AI API key
- CANVA_ACCESS_TOKEN: Canva API access token
"""

import os
import json
import time
import logging
import requests
from datetime import datetime
from typing import Dict, Any, List, Optional
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

class Config:
    """API Configuration"""
    LEONARDO_API_KEY = os.getenv('LEONARDO_API_KEY')
    LEONARDO_BASE_URL = 'https://cloud.leonardo.ai/api/rest/v1'

    CANVA_ACCESS_TOKEN = os.getenv('CANVA_ACCESS_TOKEN')
    CANVA_BASE_URL = 'https://api.canva.com/rest/v1'

    # Output directory for generated images
    OUTPUT_DIR = os.getenv('IMAGE_OUTPUT_DIR', './generated_images')


class AspectRatio(Enum):
    """Standard aspect ratios for Meta ads"""
    FACEBOOK_FEED = "16:9"      # 1200x675
    INSTAGRAM_SQUARE = "1:1"    # 1080x1080
    INSTAGRAM_STORY = "9:16"    # 1080x1920
    LINKEDIN = "1.91:1"         # 1200x628


class LeonardoModel(Enum):
    """Leonardo AI Models"""
    LEONARDO_DIFFUSION_XL = "1e60896f-3c26-4296-8ecc-53e2afecc132"
    LEONARDO_VISION_XL = "5c232a9e-9061-4777-980a-ddc8e65647c6"
    PHOTOREAL = "aa77f04e-3eec-4034-9c07-d0f619684628"


# ==============================================================================
# CAMPAIGN PROMPTS FOR KANDIDATENTEKORT.NL
# ==============================================================================

CAMPAIGN_PROMPTS = {
    "voor_na_vergelijking": {
        "name": "Voor/Na Vacature Vergelijking",
        "prompts": {
            "primary": """Professional Dutch office environment, modern laptop on clean desk showing split screen comparison, left side displays poorly written job posting with amateur layout, right side shows professionally optimized job posting with clean design and kandidatentekort.nl branding, orange accent colors (#FF6B35), Dutch business person in professional attire reviewing the comparison, satisfied expression, bright office lighting, photorealistic style, high quality""",
            "mobile": """Close-up shot of hands holding smartphone showing kandidatentekort.nl mobile interface, before and after job posting comparison visible on screen, orange UI elements prominent, Dutch office background slightly blurred, professional manicured hands, modern iPhone or Samsung device, natural lighting, commercial photography style, mobile-first composition"""
        },
        "text_overlays": {
            "headline": "180% meer sollicitaties na optimalisatie",
            "subheading": "Van onzichtbaar naar onmisbaar",
            "cta": "Gratis Vacature Check"
        }
    },
    "professional_recruiter": {
        "name": "Professional Dutch Recruiter",
        "prompts": {
            "female": """Professional Dutch woman, 30-40 years old, confident business attire, standing in modern Amsterdam office, holding tablet showing kandidatentekort.nl analytics dashboard with positive metrics, warm smile, orange corporate colors visible on screen, floor-to-ceiling windows with Dutch cityscape background, natural lighting, corporate photography style, authentic Dutch professional appearance""",
            "male": """Professional Dutch man in modern business casual attire, seated at contemporary office desk, laptop open displaying kandidatentekort.nl interface with success metrics, looking directly at camera with confident expression, Dutch corporate environment, kandidatentekort.nl branding visible on screen, warm office lighting, authentic business photography"""
        },
        "text_overlays": {
            "headline": "50+ Nederlandse bedrijven",
            "subheading": "Gemiddeld 180% meer reacties",
            "cta": "Start Gratis"
        }
    },
    "industrie_techniek": {
        "name": "Industrie & Techniek Sector",
        "prompts": {
            "automotive": """Dutch automotive workshop or manufacturing facility, professional mechanic or technician using tablet showing kandidatentekort.nl interface, technical job posting analysis visible on screen, industrial background with modern equipment, orange safety gear and UI elements, authentic Dutch industrial workplace, professional work lighting, realistic manufacturing environment""",
            "construction": """Dutch construction site office, project manager reviewing job postings on laptop showing kandidatentekort.nl platform, construction equipment visible through windows, hard hat on desk, orange high-visibility clothing elements matching UI colors, professional construction environment, natural daylight, authentic Dutch building sector setting"""
        },
        "text_overlays": {
            "headline": "67% technici vindt vacatures onduidelijk",
            "subheading": "Schrijf vacatures die monteurs begrijpen",
            "cta": "Gratis Analyse"
        }
    },
    "roi_kostenbesparing": {
        "name": "ROI & Kostenbesparing",
        "prompts": {
            "executive": """Dutch business executive in premium office setting, large monitor displaying kandidatentekort.nl cost analysis dashboard, charts showing recruitment savings and ROI improvements, orange chart elements and UI components, professional business environment, executive reviewing financial data, satisfied expression, high-end corporate photography style""",
            "sme_owner": """Dutch small business owner in practical office environment, computer showing kandidatentekort.nl savings calculator, realistic SME setting, orange branding elements visible, person calculating recruitment cost reductions, authentic small business atmosphere, natural office lighting, approachable professional appearance"""
        },
        "text_overlays": {
            "headline": "€27.500 bespaard per jaar",
            "subheading": "65% minder recruitment kosten",
            "cta": "Bereken Je Besparing"
        }
    },
    "mobile_quick_check": {
        "name": "Mobile-First Quick Check",
        "prompts": {
            "commuter": """Professional Dutch person using smartphone on modern Dutch train or in contemporary coffee shop, phone screen clearly showing kandidatentekort.nl mobile interface with vacancy analysis in progress, orange UI elements prominent, satisfied user expression, authentic mobile usage scenario, natural lighting, lifestyle photography approach""",
            "office_break": """Dutch professional taking coffee break in modern office kitchen, casually using phone showing kandidatentekort.nl quick analysis, orange UI colors visible, relaxed professional atmosphere, natural behavior, authentic workplace environment, lifestyle commercial photography"""
        },
        "text_overlays": {
            "headline": "2-minuten vacature check",
            "subheading": "Ook onderweg optimaliseren",
            "cta": "Check Nu"
        }
    }
}

NEGATIVE_PROMPT = "low quality, blurry, cartoon, anime, drawing, fake interface, stock photo look, overly posed, unrealistic lighting, poor composition, watermark, text, logo"


# ==============================================================================
# LEONARDO AI CLIENT
# ==============================================================================

class LeonardoClient:
    """
    Leonardo AI API Client

    Usage:
        client = LeonardoClient()
        generation_id = client.generate_image(prompt, aspect_ratio="16:9")
        images = client.get_generation(generation_id)
    """

    def __init__(self, api_key: str = None):
        self.api_key = api_key or Config.LEONARDO_API_KEY
        if not self.api_key:
            raise ValueError("LEONARDO_API_KEY environment variable is required")

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def generate_image(
        self,
        prompt: str,
        negative_prompt: str = NEGATIVE_PROMPT,
        model_id: str = LeonardoModel.PHOTOREAL.value,
        width: int = 1024,
        height: int = 576,
        num_images: int = 4,
        guidance_scale: float = 7.0,
        preset_style: str = "PHOTOGRAPHY"
    ) -> str:
        """
        Generate images from prompt

        Returns:
            generation_id: ID to poll for results
        """
        payload = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "modelId": model_id,
            "width": width,
            "height": height,
            "num_images": num_images,
            "guidance_scale": guidance_scale,
            "presetStyle": preset_style,
            "photoReal": True,
            "photoRealVersion": "v2"
        }

        response = requests.post(
            f"{Config.LEONARDO_BASE_URL}/generations",
            headers=self.headers,
            json=payload,
            timeout=60
        )

        if response.status_code != 200:
            logger.error(f"Leonardo API error: {response.text}")
            raise Exception(f"Leonardo API error: {response.status_code}")

        result = response.json()
        generation_id = result.get("sdGenerationJob", {}).get("generationId")

        logger.info(f"Generation started: {generation_id}")
        return generation_id

    def get_generation(self, generation_id: str, max_wait: int = 120) -> List[Dict]:
        """
        Poll for generation results

        Args:
            generation_id: ID from generate_image
            max_wait: Maximum seconds to wait

        Returns:
            List of generated image data
        """
        start_time = time.time()

        while time.time() - start_time < max_wait:
            response = requests.get(
                f"{Config.LEONARDO_BASE_URL}/generations/{generation_id}",
                headers=self.headers,
                timeout=30
            )

            if response.status_code != 200:
                raise Exception(f"Failed to get generation: {response.status_code}")

            result = response.json()
            generation = result.get("generations_by_pk", {})
            status = generation.get("status")

            if status == "COMPLETE":
                images = generation.get("generated_images", [])
                logger.info(f"Generation complete: {len(images)} images")
                return images

            elif status == "FAILED":
                raise Exception("Generation failed")

            logger.info(f"Generation status: {status}, waiting...")
            time.sleep(5)

        raise TimeoutError("Generation timed out")

    def download_image(self, image_url: str, output_path: str) -> str:
        """Download generated image to local file"""
        response = requests.get(image_url, timeout=60)

        if response.status_code != 200:
            raise Exception(f"Failed to download image: {response.status_code}")

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'wb') as f:
            f.write(response.content)

        logger.info(f"Image saved: {output_path}")
        return output_path

    def get_dimensions_for_ratio(self, ratio: AspectRatio) -> tuple:
        """Get width x height for aspect ratio"""
        dimensions = {
            AspectRatio.FACEBOOK_FEED: (1344, 768),
            AspectRatio.INSTAGRAM_SQUARE: (1024, 1024),
            AspectRatio.INSTAGRAM_STORY: (768, 1344),
            AspectRatio.LINKEDIN: (1344, 704)
        }
        return dimensions.get(ratio, (1024, 1024))


# ==============================================================================
# CANVA CLIENT
# ==============================================================================

class CanvaClient:
    """
    Canva API Client for uploading assets and managing designs

    Usage:
        client = CanvaClient()
        asset_id = client.upload_asset(image_path, "Campaign Image")
    """

    def __init__(self, access_token: str = None):
        self.access_token = access_token or Config.CANVA_ACCESS_TOKEN
        if not self.access_token:
            logger.warning("CANVA_ACCESS_TOKEN not set - Canva features disabled")

        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def upload_asset(self, file_path: str, name: str) -> Optional[str]:
        """
        Upload an image asset to Canva

        Returns:
            asset_id: Canva asset ID
        """
        if not self.access_token:
            logger.warning("Canva upload skipped - no access token")
            return None

        # First, get upload URL
        response = requests.post(
            f"{Config.CANVA_BASE_URL}/assets/upload",
            headers=self.headers,
            json={
                "name": name,
                "type": "IMAGE"
            },
            timeout=30
        )

        if response.status_code != 200:
            logger.error(f"Canva upload init error: {response.text}")
            return None

        upload_data = response.json()
        upload_url = upload_data.get("upload_url")
        asset_id = upload_data.get("asset_id")

        # Upload the file
        with open(file_path, 'rb') as f:
            upload_response = requests.put(
                upload_url,
                data=f.read(),
                headers={"Content-Type": "image/png"},
                timeout=120
            )

        if upload_response.status_code not in [200, 201]:
            logger.error(f"Canva file upload error: {upload_response.status_code}")
            return None

        logger.info(f"Uploaded to Canva: {asset_id}")
        return asset_id

    def list_designs(self, query: str = None) -> List[Dict]:
        """List Canva designs"""
        if not self.access_token:
            return []

        params = {}
        if query:
            params["query"] = query

        response = requests.get(
            f"{Config.CANVA_BASE_URL}/designs",
            headers=self.headers,
            params=params,
            timeout=30
        )

        if response.status_code != 200:
            return []

        return response.json().get("designs", [])


# ==============================================================================
# WORKFLOW ORCHESTRATOR
# ==============================================================================

class CampaignImageWorkflow:
    """
    Orchestrate the complete workflow:
    Leonardo AI generation → Download → Canva upload

    Usage:
        workflow = CampaignImageWorkflow()
        results = workflow.generate_campaign_images("voor_na_vergelijking")
    """

    def __init__(self):
        self.leonardo = LeonardoClient() if Config.LEONARDO_API_KEY else None
        self.canva = CanvaClient() if Config.CANVA_ACCESS_TOKEN else None
        self.output_dir = Config.OUTPUT_DIR

    def generate_campaign_images(
        self,
        campaign_key: str,
        aspect_ratio: AspectRatio = AspectRatio.FACEBOOK_FEED,
        upload_to_canva: bool = True
    ) -> Dict[str, Any]:
        """
        Generate all images for a campaign

        Args:
            campaign_key: Key from CAMPAIGN_PROMPTS
            aspect_ratio: Target aspect ratio
            upload_to_canva: Whether to upload to Canva

        Returns:
            Results dict with generated images and Canva IDs
        """
        if not self.leonardo:
            raise ValueError("Leonardo API key not configured")

        campaign = CAMPAIGN_PROMPTS.get(campaign_key)
        if not campaign:
            raise ValueError(f"Unknown campaign: {campaign_key}")

        results = {
            "campaign": campaign["name"],
            "timestamp": datetime.now().isoformat(),
            "aspect_ratio": aspect_ratio.value,
            "images": []
        }

        width, height = self.leonardo.get_dimensions_for_ratio(aspect_ratio)

        for variant_name, prompt in campaign["prompts"].items():
            logger.info(f"Generating {campaign['name']} - {variant_name}")

            try:
                # Generate images
                generation_id = self.leonardo.generate_image(
                    prompt=prompt,
                    width=width,
                    height=height,
                    num_images=4
                )

                # Wait for completion
                generated_images = self.leonardo.get_generation(generation_id)

                for i, img_data in enumerate(generated_images):
                    image_url = img_data.get("url")
                    if not image_url:
                        continue

                    # Download image
                    filename = f"{campaign_key}_{variant_name}_{i+1}.png"
                    output_path = os.path.join(
                        self.output_dir,
                        campaign_key,
                        filename
                    )

                    local_path = self.leonardo.download_image(image_url, output_path)

                    image_result = {
                        "variant": variant_name,
                        "index": i + 1,
                        "local_path": local_path,
                        "leonardo_url": image_url,
                        "canva_asset_id": None
                    }

                    # Upload to Canva
                    if upload_to_canva and self.canva:
                        asset_name = f"{campaign['name']} - {variant_name} #{i+1}"
                        canva_id = self.canva.upload_asset(local_path, asset_name)
                        image_result["canva_asset_id"] = canva_id

                    results["images"].append(image_result)

            except Exception as e:
                logger.error(f"Error generating {variant_name}: {str(e)}")
                results["images"].append({
                    "variant": variant_name,
                    "error": str(e)
                })

        return results

    def generate_all_campaigns(
        self,
        aspect_ratios: List[AspectRatio] = None
    ) -> Dict[str, Any]:
        """Generate images for all campaigns"""
        if aspect_ratios is None:
            aspect_ratios = [AspectRatio.FACEBOOK_FEED]

        all_results = {
            "generated_at": datetime.now().isoformat(),
            "campaigns": {}
        }

        for campaign_key in CAMPAIGN_PROMPTS.keys():
            campaign_results = []

            for ratio in aspect_ratios:
                try:
                    result = self.generate_campaign_images(
                        campaign_key,
                        aspect_ratio=ratio
                    )
                    campaign_results.append(result)
                except Exception as e:
                    logger.error(f"Failed {campaign_key} ({ratio}): {str(e)}")
                    campaign_results.append({
                        "aspect_ratio": ratio.value,
                        "error": str(e)
                    })

            all_results["campaigns"][campaign_key] = campaign_results

        return all_results


# ==============================================================================
# CLI INTERFACE
# ==============================================================================

def main():
    """Command line interface"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate Meta campaign images for kandidatentekort.nl"
    )
    parser.add_argument(
        "--campaign",
        choices=list(CAMPAIGN_PROMPTS.keys()) + ["all"],
        default="all",
        help="Campaign to generate"
    )
    parser.add_argument(
        "--ratio",
        choices=["16:9", "1:1", "9:16", "1.91:1"],
        default="16:9",
        help="Aspect ratio"
    )
    parser.add_argument(
        "--no-canva",
        action="store_true",
        help="Skip Canva upload"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available campaigns"
    )

    args = parser.parse_args()

    if args.list:
        print("\nAvailable Campaigns:")
        print("=" * 50)
        for key, campaign in CAMPAIGN_PROMPTS.items():
            print(f"\n{key}:")
            print(f"  Name: {campaign['name']}")
            print(f"  Variants: {', '.join(campaign['prompts'].keys())}")
            print(f"  Headline: {campaign['text_overlays']['headline']}")
        return

    # Map ratio string to enum
    ratio_map = {
        "16:9": AspectRatio.FACEBOOK_FEED,
        "1:1": AspectRatio.INSTAGRAM_SQUARE,
        "9:16": AspectRatio.INSTAGRAM_STORY,
        "1.91:1": AspectRatio.LINKEDIN
    }
    aspect_ratio = ratio_map.get(args.ratio, AspectRatio.FACEBOOK_FEED)

    workflow = CampaignImageWorkflow()

    if args.campaign == "all":
        print("\nGenerating all campaigns...")
        results = workflow.generate_all_campaigns([aspect_ratio])
    else:
        print(f"\nGenerating {args.campaign}...")
        results = workflow.generate_campaign_images(
            args.campaign,
            aspect_ratio=aspect_ratio,
            upload_to_canva=not args.no_canva
        )

    # Save results
    output_file = os.path.join(
        Config.OUTPUT_DIR,
        f"generation_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to: {output_file}")
    print(f"Images saved to: {Config.OUTPUT_DIR}")


if __name__ == "__main__":
    main()
