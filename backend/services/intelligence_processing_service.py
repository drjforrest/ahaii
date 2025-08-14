"""
AHAII Intelligence Processing Service
Automated extraction of infrastructure indicators from intelligence sources
and real-time updating of country AHAII scores
"""

import asyncio
import json
import re
from datetime import datetime, date
from typing import Any, Dict, List, Optional, Tuple
from uuid import uuid4

from loguru import logger
from pydantic import BaseModel

from config.database import get_supabase
from services.ahaii_scoring_service import AHAIIScoringService


class InfrastructureSignal(BaseModel):
    """Extracted infrastructure signal from intelligence source"""

    signal_id: str
    source_type: str  # 'academic_paper', 'news_article', 'government_report'
    source_url: str
    source_title: str
    country_iso_code: Optional[str]

    # Extracted indicator information
    indicator_name: str
    indicator_value: float
    indicator_unit: str
    pillar: str  # 'human_capital', 'physical_infrastructure', 'regulatory', 'economic'

    # Quality metrics
    confidence_score: float  # 0-1 AI confidence in extraction
    extraction_method: str  # 'keyword_pattern', 'ai_nlp', 'structured_data'
    extracted_text: str  # Source text that led to extraction

    # Processing metadata
    processed_at: datetime
    verification_status: str = "pending"  # 'pending', 'verified', 'disputed'


class CountryIntelligenceMatcher:
    """Matches intelligence content to African countries"""

    def __init__(self):
        self.country_patterns = self._build_country_patterns()

    def _build_country_patterns(self) -> Dict[str, List[str]]:
        """Build country detection patterns including variations and cities"""

        patterns = {
            # Major countries with cities and variations
            "ZAF": [
                "south africa",
                "south african",
                "johannesburg",
                "cape town",
                "durban",
                "pretoria",
            ],
            "KEN": ["kenya", "kenyan", "nairobi", "mombasa", "kenyatta"],
            "NGA": ["nigeria", "nigerian", "lagos", "abuja", "kano", "ibadan"],
            "EGY": ["egypt", "egyptian", "cairo", "alexandria", "giza"],
            "MAR": ["morocco", "moroccan", "rabat", "casablanca", "marrakech"],
            "GHA": ["ghana", "ghanaian", "accra", "kumasi", "tamale"],
            "ETH": ["ethiopia", "ethiopian", "addis ababa", "dire dawa"],
            "TUN": ["tunisia", "tunisian", "tunis", "sfax"],
            "UGA": ["uganda", "ugandan", "kampala", "gulu"],
            "TZA": ["tanzania", "tanzanian", "dar es salaam", "dodoma", "arusha"],
            "RWA": ["rwanda", "rwandan", "kigali"],
            "BWA": ["botswana", "gaborone"],
            "SEN": ["senegal", "senegalese", "dakar"],
            "ZWE": ["zimbabwe", "zimbabwean", "harare", "bulawayo"],
        }

        return patterns

    def detect_country(self, text: str) -> Optional[str]:
        """Detect country from text content"""
        text_lower = text.lower()

        # Score each country based on pattern matches
        country_scores = {}

        for iso_code, patterns in self.country_patterns.items():
            score = 0
            for pattern in patterns:
                if pattern in text_lower:
                    # Weight capital cities and country names higher
                    if pattern in ["south africa", "kenya", "nigeria", "egypt"]:
                        score += 10
                    elif "capital" in pattern or len(pattern.split()) == 1:
                        score += 5
                    else:
                        score += 3

            if score > 0:
                country_scores[iso_code] = score

        # Return country with highest score, minimum threshold of 5
        if country_scores:
            best_country = max(country_scores.keys(), key=lambda k: country_scores[k])
            if country_scores[best_country] >= 5:
                return best_country

        return None


class IndicatorExtractor:
    """Extracts infrastructure indicators from text using AI and pattern matching"""

    def __init__(self):
        self.scoring_service = AHAIIScoringService()
        self.indicator_patterns = self._build_extraction_patterns()

    def _build_extraction_patterns(self) -> Dict[str, List[Dict]]:
        """Build regex patterns for indicator extraction"""

        patterns = {
            # Human Capital Indicators
            "ai_trained_clinicians_per_100k": [
                {
                    "pattern": r"(\d+(?:\.\d+)?)\s*(?:percent|%)\s*(?:of\s+)?(?:doctors|physicians|clinicians)\s*(?:have|received|completed|trained)\s*(?:AI|artificial intelligence|machine learning)\s*(?:training|certification)",
                    "value_group": 1,
                    "confidence": 0.8,
                    "unit": "percentage",
                }
            ],
            "emr_adoption_rate": [
                {
                    "pattern": r"(\d+(?:\.\d+)?)\s*(?:percent|%)\s*(?:of\s+)?(?:hospitals|facilities|clinics)\s*(?:have|use|implemented|adopted)\s*(?:EMR|electronic medical record|electronic health record)",
                    "value_group": 1,
                    "confidence": 0.9,
                    "unit": "percentage",
                },
                {
                    "pattern": r"EMR\s*(?:adoption|implementation)\s*(?:rate|level)\s*(?:of|at)\s*(\d+(?:\.\d+)?)\s*(?:percent|%)",
                    "value_group": 1,
                    "confidence": 0.9,
                    "unit": "percentage",
                },
            ],
            "clinical_ai_certification_programs": [
                {
                    "pattern": r"(\d+)\s*(?:new\s+)?(?:AI|artificial intelligence)\s*(?:training|certification|education)\s*programs?\s*(?:launched|established|available)",
                    "value_group": 1,
                    "confidence": 0.7,
                    "unit": "count",
                }
            ],
            "telemedicine_capability": [
                {
                    "pattern": r"(\d+(?:\.\d+)?)\s*(?:percent|%)\s*(?:of\s+)?(?:hospitals|facilities)\s*(?:have|offer|provide)\s*(?:telemedicine|telehealth|remote consultation)",
                    "value_group": 1,
                    "confidence": 0.8,
                    "unit": "percentage",
                }
            ],
            "health_ai_startups_per_million": [
                {
                    "pattern": r"(\d+)\s*(?:new\s+)?(?:health|medical)\s*(?:AI|artificial intelligence)\s*(?:startups|companies)\s*(?:launched|established|founded)",
                    "value_group": 1,
                    "confidence": 0.6,
                    "unit": "count",
                }
            ],
        }

        return patterns

    def extract_indicators(
        self, text: str, country_iso: str
    ) -> List[InfrastructureSignal]:
        """Extract infrastructure indicators from text"""
        signals = []

        for indicator_name, pattern_configs in self.indicator_patterns.items():
            for pattern_config in pattern_configs:
                matches = re.finditer(pattern_config["pattern"], text, re.IGNORECASE)

                for match in matches:
                    try:
                        value = float(match.group(pattern_config["value_group"]))

                        # Determine pillar based on indicator
                        pillar = self._get_indicator_pillar(indicator_name)

                        signal = InfrastructureSignal(
                            signal_id=str(uuid4()),
                            source_type="intelligence_extraction",
                            source_url="",  # Will be filled by caller
                            source_title="",  # Will be filled by caller
                            country_iso_code=country_iso,
                            indicator_name=indicator_name,
                            indicator_value=value,
                            indicator_unit=pattern_config["unit"],
                            pillar=pillar,
                            confidence_score=pattern_config["confidence"],
                            extraction_method="keyword_pattern",
                            extracted_text=match.group(0),
                            processed_at=datetime.now(),
                        )

                        signals.append(signal)

                    except (ValueError, IndexError) as e:
                        logger.warning(
                            f"Error extracting value from pattern match: {e}"
                        )
                        continue

        return signals

    def _get_indicator_pillar(self, indicator_name: str) -> str:
        """Map indicator to AHAII pillar"""
        pillar_mapping = {
            "ai_trained_clinicians_per_100k": "human_capital",
            "healthcare_admin_ai_competency_rate": "human_capital",
            "clinical_ai_certification_programs": "human_capital",
            "medical_informatics_programs_per_million": "human_capital",
            "emr_adoption_rate": "physical_infrastructure",
            "medical_device_connectivity_rate": "physical_infrastructure",
            "telemedicine_capability": "physical_infrastructure",
            "healthcare_power_reliability": "physical_infrastructure",
            "medical_ai_approval_pathway_maturity": "regulatory_infrastructure",
            "health_data_privacy_framework_score": "regulatory_infrastructure",
            "ai_reimbursement_policy_coverage": "regulatory_infrastructure",
            "health_ai_startups_per_million": "economic_market",
            "health_ministry_ai_budget_percentage": "economic_market",
            "clinical_ai_research_funding_per_capita": "economic_market",
        }

        return pillar_mapping.get(indicator_name, "physical_infrastructure")


class IntelligenceProcessingService:
    """Main service for processing intelligence and updating AHAII scores"""

    def __init__(self):
        self.country_matcher = CountryIntelligenceMatcher()
        self.indicator_extractor = IndicatorExtractor()
        self.scoring_service = AHAIIScoringService()
        self.supabase = get_supabase()

    async def process_intelligence_report(
        self, report_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process an intelligence report and extract infrastructure signals"""

        report_title = report_data.get("title", "")
        report_content = report_data.get("content", "")
        report_url = report_data.get("url", "")
        source_type = report_data.get("source_type", "unknown")

        # Detect country
        country_iso = self.country_matcher.detect_country(
            f"{report_title} {report_content}"
        )

        if not country_iso:
            logger.info(f"No African country detected in report: {report_title}")
            return {"signals_extracted": 0, "country": None}

        # Extract infrastructure signals
        signals = self.indicator_extractor.extract_indicators(
            f"{report_title} {report_content}", country_iso
        )

        # Update signals with source information
        for signal in signals:
            signal.source_url = report_url
            signal.source_title = report_title
            signal.source_type = source_type

        # Store signals and update scores
        updated_scores = None
        if signals:
            await self._store_infrastructure_signals(signals)
            updated_scores = await self._update_country_scores(country_iso)

        result = {
            "country": country_iso,
            "signals_extracted": len(signals),
            "signals": [signal.dict() for signal in signals],
            "updated_scores": updated_scores,
        }

        logger.info(
            f"Processed intelligence for {country_iso}: {len(signals)} signals extracted"
        )

        return result

    async def _store_infrastructure_signals(self, signals: List[InfrastructureSignal]):
        """Store extracted signals in the database"""

        for signal in signals:
            try:
                # Get country ID
                country_result = (
                    self.supabase.table("countries")
                    .select("id")
                    .eq("iso_code_alpha3", signal.country_iso_code)
                    .execute()
                )

                if not country_result.data:
                    logger.warning(f"Country not found: {signal.country_iso_code}")
                    continue

                country_id = country_result.data[0]["id"]

                # Insert infrastructure indicator
                indicator_data = {
                    "country_id": country_id,
                    "pillar": signal.pillar,
                    "indicator_name": signal.indicator_name,
                    "indicator_value": signal.indicator_value,
                    "indicator_unit": signal.indicator_unit,
                    "data_year": datetime.now().year,
                    "data_source": signal.source_title,
                    "data_source_type": "ai_extracted",
                    "confidence_score": signal.confidence_score,
                    "verification_status": signal.verification_status,
                    "created_at": signal.processed_at.isoformat(),
                }

                result = (
                    self.supabase.table("infrastructure_indicators")
                    .insert(indicator_data)
                    .execute()
                )

                if result.data:
                    logger.info(
                        f"Stored indicator {signal.indicator_name} for {signal.country_iso_code}"
                    )
                else:
                    logger.error(f"Failed to store indicator: {result}")

                # Store in intelligence reports table
                intelligence_data = {
                    "report_type": "indicator_extraction",
                    "country_id": country_id,
                    "report_title": signal.source_title,
                    "source_type": signal.source_type,
                    "source_url": signal.source_url,
                    "key_findings": {
                        "extracted_indicators": [
                            {
                                "indicator_name": signal.indicator_name,
                                "indicator_value": signal.indicator_value,
                                "confidence": signal.confidence_score,
                                "extracted_text": signal.extracted_text,
                            }
                        ]
                    },
                    "affects_human_capital": signal.pillar == "human_capital",
                    "affects_physical_infrastructure": signal.pillar
                    == "physical_infrastructure",
                    "affects_regulatory_framework": signal.pillar
                    == "regulatory_infrastructure",
                    "affects_economic_market": signal.pillar == "economic_market",
                    "impact_significance": (
                        "medium" if signal.confidence_score > 0.7 else "low"
                    ),
                    "confidence_score": signal.confidence_score,
                    "processed_by_ai": True,
                }

                self.supabase.table("infrastructure_intelligence").insert(
                    intelligence_data
                ).execute()

            except Exception as e:
                logger.error(f"Error storing signal {signal.signal_id}: {e}")
                continue

    async def _update_country_scores(self, country_iso: str) -> Optional[Dict]:
        """Recalculate and update AHAII scores for a country"""

        try:
            # Get country ID
            country_result = (
                self.supabase.table("countries")
                .select("id, name")
                .eq("iso_code_alpha3", country_iso)
                .execute()
            )

            if not country_result.data:
                logger.warning(f"Country not found: {country_iso}")
                return None

            country_id = country_result.data[0]["id"]
            country_name = country_result.data[0]["name"]

            # Fetch current indicators for this country
            indicators_result = (
                self.supabase.table("infrastructure_indicators")
                .select("*")
                .eq("country_id", country_id)
                .execute()
            )

            if not indicators_result.data:
                logger.info(f"No indicators found for {country_name}")
                return None

            # Build indicators dictionary for scoring
            indicators_data = {}
            for indicator in indicators_result.data:
                indicator_name = indicator["indicator_name"]
                indicator_value = float(indicator["indicator_value"])

                # Use most recent value if multiple exist
                if indicator_name not in indicators_data:
                    indicators_data[indicator_name] = indicator_value
                else:
                    # Compare dates and use most recent
                    current_date = datetime.fromisoformat(
                        indicator["created_at"].replace("Z", "+00:00")
                    )
                    # For simplicity, just overwrite with latest processing
                    indicators_data[indicator_name] = indicator_value

            # Calculate new AHAII scores
            current_year = datetime.now().year
            new_scores = self.scoring_service.calculate_ahaii_score(
                indicators_data, country_id, current_year
            )

            # Store updated scores
            scores_data = {
                "country_id": country_id,
                "assessment_year": current_year,
                "total_score": new_scores["total_score"],
                "human_capital_score": new_scores["human_capital_score"],
                "physical_infrastructure_score": new_scores[
                    "physical_infrastructure_score"
                ],
                "regulatory_infrastructure_score": new_scores[
                    "regulatory_infrastructure_score"
                ],
                "economic_market_score": new_scores["economic_market_score"],
                "readiness_tier": new_scores["readiness_tier"],
                "tier_justification": new_scores["tier_justification"],
                "overall_confidence_score": new_scores["overall_confidence_score"],
                "data_completeness_percentage": new_scores[
                    "data_completeness_percentage"
                ],
                "key_strengths": new_scores["key_strengths"],
                "priority_improvement_areas": new_scores["priority_improvement_areas"],
                "assessment_methodology_version": new_scores[
                    "assessment_methodology_version"
                ],
                "indicator_weights_used": new_scores["indicator_weights_used"],
            }

            # Upsert scores (insert or update)
            upsert_result = (
                self.supabase.table("ahaii_scores")
                .upsert(scores_data, on_conflict="country_id,assessment_year")
                .execute()
            )

            if upsert_result.data:
                logger.info(
                    f"Updated AHAII scores for {country_name}: {new_scores['total_score']:.1f} (Tier {new_scores['readiness_tier']})"
                )
                return {
                    "country": country_name,
                    "country_iso": country_iso,
                    "previous_score": None,  # Could be fetched from history
                    "new_score": new_scores["total_score"],
                    "tier": new_scores["readiness_tier"],
                    "updated_pillars": {
                        "human_capital": new_scores["human_capital_score"],
                        "physical_infrastructure": new_scores[
                            "physical_infrastructure_score"
                        ],
                        "regulatory_infrastructure": new_scores[
                            "regulatory_infrastructure_score"
                        ],
                        "economic_market": new_scores["economic_market_score"],
                    },
                }
            else:
                logger.error(f"Failed to update scores for {country_name}")
                return None

        except Exception as e:
            logger.error(f"Error updating scores for {country_iso}: {e}")
            return None


# Example usage function
async def process_sample_intelligence():
    """Example of how intelligence processing works"""

    # Sample intelligence report
    sample_report = {
        "title": "Kenya Health Ministry Announces EMR Rollout to 200 Hospitals",
        "content": """
        The Kenyan Ministry of Health announced today that 85% of public hospitals 
        have successfully implemented electronic medical record systems. The initiative, 
        launched in partnership with local tech companies, aims to digitize healthcare 
        across all major facilities by 2025.
        
        Additionally, 12 new AI training programs for clinical staff have been 
        established in partnership with University of Nairobi Medical School.
        """,
        "url": "https://health.go.ke/news/emr-implementation-update",
        "source_type": "government_report",
    }

    # Process the report
    service = IntelligenceProcessingService()
    result = await service.process_intelligence_report(sample_report)

    print("Intelligence Processing Result:")
    print(json.dumps(result, indent=2, default=str))

    return result


if __name__ == "__main__":
    # Test the intelligence processing
    asyncio.run(process_sample_intelligence())
