"""
AHAII Scoring Algorithm for African Health AI Infrastructure Index
Implements transparent scoring methodology with min-max normalization
Weighted aggregation by pillar with confidence-weighted scoring
Generates tier classifications and improvement recommendations
"""

import json
import logging
import numpy as np
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AHAIITier(Enum):
    """AHAII Infrastructure Readiness Tiers"""

    IMPLEMENTATION_READY = 1  # 70+ points
    FOUNDATION_BUILDING = 2  # 40-69 points
    DEVELOPMENT = 3  # 0-39 points


@dataclass
class PillarScore:
    """Individual pillar score with breakdown"""

    name: str
    score: float
    confidence: float
    sub_components: Dict[str, float]
    weight: float
    normalized_indicators: Dict[str, float]


@dataclass
class AHAIIResult:
    """Complete AHAII assessment result"""

    country_code: str
    country_name: str
    assessment_date: str
    total_score: float
    overall_confidence: float
    tier: AHAIITier
    pillar_scores: List[PillarScore]
    improvement_recommendations: List[str]
    data_quality_issues: List[str]
    regional_rank: Optional[int] = None


class AHAIICalculator:
    """
    AHAII scoring calculation engine
    Implements four-pillar health AI infrastructure assessment
    """

    # Pillar weights based on AHAII framework
    PILLAR_WEIGHTS = {
        "human_capital": 0.30,  # Human Capital: AI literacy, training
        "physical_infrastructure": 0.30,  # Physical: Connectivity, computing, EMR
        "regulatory_framework": 0.25,  # Regulatory: Governance, standards
        "economic_market": 0.15,  # Economic: Funding, market maturity
    }

    # Indicator mapping to pillars
    INDICATOR_PILLAR_MAPPING = {
        # Human Capital (30%)
        "tertiary_education_enrollment_rate": "human_capital",
        "government_expenditure_on_education_pct_gdp": "human_capital",
        "physicians_per_1000": "human_capital",
        # Physical Infrastructure (30%)
        "electricity_access_pct": "physical_infrastructure",
        "internet_users_pct": "physical_infrastructure",
        "mobile_subscriptions_per_100": "physical_infrastructure",
        "fixed_broadband_subscriptions_per_100": "physical_infrastructure",
        "hospital_beds_per_1000": "physical_infrastructure",
        # Regulatory Framework (25%) - Will be enhanced with policy indicators
        "rd_expenditure_pct_gdp": "regulatory_framework",
        # Economic/Market (15%)
        "gdp_per_capita_current_usd": "economic_market",
        "current_health_expenditure_pct_gdp": "economic_market",
        "total_population": "economic_market",  # Market size proxy
    }

    # Global min/max values for normalization (based on World Bank global data)
    NORMALIZATION_BOUNDS = {
        "electricity_access_pct": (0, 100),
        "mobile_subscriptions_per_100": (0, 200),
        "internet_users_pct": (0, 100),
        "rd_expenditure_pct_gdp": (0, 5),
        "hospital_beds_per_1000": (0, 15),
        "current_health_expenditure_pct_gdp": (0, 20),
        "tertiary_education_enrollment_rate": (0, 100),
        "fixed_broadband_subscriptions_per_100": (0, 50),
        "physicians_per_1000": (0, 10),
        "gdp_per_capita_current_usd": (0, 100000),
        "government_expenditure_on_education_pct_gdp": (0, 10),
        "total_population": (100000, 1400000000),  # Log scale for population
    }

    # Confidence thresholds for tier classification
    TIER_CONFIDENCE_THRESHOLDS = {
        AHAIITier.IMPLEMENTATION_READY: 0.8,
        AHAIITier.FOUNDATION_BUILDING: 0.6,
        AHAIITier.DEVELOPMENT: 0.4,
    }

    def __init__(self, output_dir: str = "data/indicators"):
        """
        Initialize AHAII calculator

        Args:
            output_dir: Directory for saving calculated scores
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def normalize_indicator(
        self, value: float, indicator_name: str, confidence: float = 1.0
    ) -> Tuple[float, float]:
        """
        Normalize indicator value to 0-100 scale using min-max normalization

        Args:
            value: Raw indicator value
            indicator_name: Name of the indicator
            confidence: Confidence score for the value

        Returns:
            Tuple of (normalized_value, adjusted_confidence)
        """
        if pd.isna(value) or value is None:
            return 0.0, 0.0

        if indicator_name not in self.NORMALIZATION_BOUNDS:
            logger.warning(
                f"No normalization bounds for {indicator_name}, using value as-is"
            )
            return min(max(value, 0), 100), confidence

        min_val, max_val = self.NORMALIZATION_BOUNDS[indicator_name]

        # Special handling for population (log scale)
        if indicator_name == "total_population":
            value = np.log10(max(value, min_val))
            min_val = np.log10(min_val)
            max_val = np.log10(max_val)

        # Min-max normalization to 0-100 scale
        normalized = ((value - min_val) / (max_val - min_val)) * 100
        normalized = max(0, min(100, normalized))  # Clamp to 0-100

        return normalized, confidence

    def calculate_pillar_score(
        self, country_data: pd.DataFrame, pillar_name: str
    ) -> PillarScore:
        """
        Calculate score for individual pillar

        Args:
            country_data: DataFrame with country's indicator data
            pillar_name: Name of the pillar to calculate

        Returns:
            PillarScore object with detailed breakdown
        """
        # Get indicators for this pillar
        pillar_indicators = {
            indicator: name
            for indicator, name in self.INDICATOR_PILLAR_MAPPING.items()
            if name == pillar_name
        }

        if not pillar_indicators:
            logger.warning(f"No indicators found for pillar: {pillar_name}")
            return PillarScore(
                name=pillar_name,
                score=0.0,
                confidence=0.0,
                sub_components={},
                weight=self.PILLAR_WEIGHTS.get(pillar_name, 0.0),
                normalized_indicators={},
            )

        normalized_values = {}
        confidences = []
        sub_components = {}

        for indicator in pillar_indicators:
            # Get most recent data for this indicator
            indicator_data = country_data[country_data["indicator_name"] == indicator]

            if len(indicator_data) == 0:
                logger.warning(f"No data found for indicator: {indicator}")
                normalized_values[indicator] = 0.0
                confidences.append(0.0)
                sub_components[indicator] = 0.0
                continue

            # Use most recent year with data
            latest_data = (
                indicator_data.dropna(subset=["value"]).sort_values("year").tail(1)
            )

            if len(latest_data) == 0:
                logger.warning(f"No valid data for indicator: {indicator}")
                normalized_values[indicator] = 0.0
                confidences.append(0.0)
                sub_components[indicator] = 0.0
                continue

            raw_value = latest_data["value"].iloc[0]
            raw_confidence = latest_data["confidence_score"].iloc[0]

            # Normalize the value
            normalized_value, adjusted_confidence = self.normalize_indicator(
                raw_value, indicator, raw_confidence
            )

            normalized_values[indicator] = normalized_value
            confidences.append(adjusted_confidence)
            sub_components[indicator] = normalized_value

        # Calculate weighted average (equal weights within pillar for now)
        if normalized_values:
            pillar_score = np.mean(list(normalized_values.values()))
            pillar_confidence = np.mean(confidences) if confidences else 0.0
        else:
            pillar_score = 0.0
            pillar_confidence = 0.0

        return PillarScore(
            name=pillar_name,
            score=pillar_score,
            confidence=pillar_confidence,
            sub_components=sub_components,
            weight=self.PILLAR_WEIGHTS.get(pillar_name, 0.0),
            normalized_indicators=normalized_values,
        )

    def generate_tier_classification(
        self, total_score: float, confidence: float
    ) -> AHAIITier:
        """
        Generate tier classification based on total score and confidence

        Args:
            total_score: Overall AHAII score (0-100)
            confidence: Overall confidence score (0-1)

        Returns:
            AHAIITier classification
        """
        # Adjust score based on confidence
        confidence_adjusted_score = total_score * confidence

        if (
            confidence_adjusted_score >= 70
            and confidence
            >= self.TIER_CONFIDENCE_THRESHOLDS[AHAIITier.IMPLEMENTATION_READY]
        ):
            return AHAIITier.IMPLEMENTATION_READY
        elif (
            confidence_adjusted_score >= 40
            and confidence
            >= self.TIER_CONFIDENCE_THRESHOLDS[AHAIITier.FOUNDATION_BUILDING]
        ):
            return AHAIITier.FOUNDATION_BUILDING
        else:
            return AHAIITier.DEVELOPMENT

    def generate_improvement_recommendations(
        self, pillar_scores: List[PillarScore], tier: AHAIITier
    ) -> List[str]:
        """
        Generate specific improvement recommendations based on pillar scores

        Args:
            pillar_scores: List of calculated pillar scores
            tier: Current tier classification

        Returns:
            List of improvement recommendations
        """
        recommendations = []

        # Sort pillars by score to identify weakest areas
        sorted_pillars = sorted(pillar_scores, key=lambda p: p.score)

        for pillar in sorted_pillars:
            if pillar.score < 50:  # Focus on pillars scoring below 50
                if pillar.name == "human_capital":
                    recommendations.extend(
                        [
                            "Invest in health informatics training programs for healthcare professionals",
                            "Establish medical AI and biomedical informatics curricula in universities",
                            "Create continuous professional development programs for clinical AI literacy",
                        ]
                    )

                elif pillar.name == "physical_infrastructure":
                    recommendations.extend(
                        [
                            "Accelerate electronic medical record (EMR) implementation in healthcare facilities",
                            "Improve healthcare connectivity and broadband infrastructure",
                            "Upgrade medical imaging and diagnostic equipment with AI capabilities",
                        ]
                    )

                elif pillar.name == "regulatory_framework":
                    recommendations.extend(
                        [
                            "Develop national AI strategy with health AI components",
                            "Establish medical AI regulatory approval pathways",
                            "Create health data governance and privacy frameworks",
                        ]
                    )

                elif pillar.name == "economic_market":
                    recommendations.extend(
                        [
                            "Increase health AI research and development funding",
                            "Support health AI startup ecosystem development",
                            "Establish health AI innovation hubs and incubators",
                        ]
                    )

        # Add tier-specific recommendations
        if tier == AHAIITier.DEVELOPMENT:
            recommendations.insert(
                0,
                "Focus on basic digital health infrastructure and workforce development",
            )
        elif tier == AHAIITier.FOUNDATION_BUILDING:
            recommendations.insert(
                0,
                "Prioritize regulatory framework development and pilot AI implementations",
            )

        return recommendations[:5]  # Return top 5 recommendations

    def identify_data_quality_issues(self, country_data: pd.DataFrame) -> List[str]:
        """
        Identify data quality issues that may affect scoring accuracy

        Args:
            country_data: DataFrame with country's indicator data

        Returns:
            List of data quality issues
        """
        issues = []

        # Check for missing indicators
        expected_indicators = set(self.INDICATOR_PILLAR_MAPPING.keys())
        available_indicators = set(country_data["indicator_name"].unique())
        missing_indicators = expected_indicators - available_indicators

        if missing_indicators:
            issues.append(
                f"Missing data for {len(missing_indicators)} key indicators: {', '.join(list(missing_indicators)[:3])}"
            )

        # Check for low confidence data
        low_confidence_data = country_data[country_data["confidence_score"] < 0.5]
        if len(low_confidence_data) > 0:
            issues.append(
                f"{len(low_confidence_data)} data points have low confidence scores"
            )

        # Check for outdated data (older than 3 years)
        current_year = datetime.now().year
        old_data = country_data[country_data["year"] < (current_year - 3)]
        if len(old_data) > 0:
            issues.append(f"{len(old_data)} data points are more than 3 years old")

        # Check for incomplete time series
        for indicator in available_indicators:
            indicator_data = country_data[country_data["indicator_name"] == indicator]
            years_with_data = len(indicator_data[indicator_data["value"].notna()])
            total_years = len(indicator_data)

            if years_with_data < total_years * 0.5:
                issues.append(
                    f"Incomplete time series for {indicator} ({years_with_data}/{total_years} years)"
                )

        return issues

    def calculate_ahaii_score(
        self, country_data: pd.DataFrame, country_code: str, country_name: str
    ) -> AHAIIResult:
        """
        Calculate complete AHAII score for a country

        Args:
            country_data: DataFrame with country's indicator data
            country_code: ISO country code
            country_name: Country name

        Returns:
            Complete AHAIIResult object
        """
        logger.info(f"Calculating AHAII score for {country_name} ({country_code})")

        # Calculate pillar scores
        pillar_scores = []
        total_weighted_score = 0.0
        total_weighted_confidence = 0.0

        for pillar_name in self.PILLAR_WEIGHTS.keys():
            pillar_score = self.calculate_pillar_score(country_data, pillar_name)
            pillar_scores.append(pillar_score)

            # Add to weighted totals
            weight = pillar_score.weight
            total_weighted_score += pillar_score.score * weight
            total_weighted_confidence += pillar_score.confidence * weight

        # Calculate overall scores
        total_score = total_weighted_score  # Already weighted
        overall_confidence = total_weighted_confidence  # Already weighted

        # Generate tier classification
        tier = self.generate_tier_classification(total_score, overall_confidence)

        # Generate recommendations and identify issues
        recommendations = self.generate_improvement_recommendations(pillar_scores, tier)
        data_quality_issues = self.identify_data_quality_issues(country_data)

        result = AHAIIResult(
            country_code=country_code,
            country_name=country_name,
            assessment_date=datetime.now().isoformat(),
            total_score=round(total_score, 2),
            overall_confidence=round(overall_confidence, 2),
            tier=tier,
            pillar_scores=pillar_scores,
            improvement_recommendations=recommendations,
            data_quality_issues=data_quality_issues,
        )

        logger.info(
            f"AHAII Score for {country_name}: {total_score:.1f} (Tier {tier.value})"
        )

        return result

    def calculate_all_countries(self, data: pd.DataFrame) -> List[AHAIIResult]:
        """
        Calculate AHAII scores for all countries in dataset

        Args:
            data: Combined DataFrame with all countries' data

        Returns:
            List of AHAIIResult objects for all countries
        """
        results = []

        countries = data.groupby(["country_code", "country_name"])

        for (country_code, country_name), country_data in countries:
            try:
                result = self.calculate_ahaii_score(
                    country_data, country_code, country_name
                )
                results.append(result)
            except Exception as e:
                logger.error(f"Error calculating score for {country_name}: {e}")
                continue

        # Add regional rankings
        results.sort(key=lambda r: r.total_score, reverse=True)
        for i, result in enumerate(results):
            result.regional_rank = i + 1

        return results

    def export_results(self, results: List[AHAIIResult], format: str = "json") -> str:
        """
        Export AHAII results to file

        Args:
            results: List of AHAIIResult objects
            format: Export format ('json', 'csv', or 'dashboard')

        Returns:
            Path to exported file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if format == "json":
            output_path = self.output_dir / f"ahaii_scores_{timestamp}.json"

            # Convert to serializable format
            serializable_results = []
            for result in results:
                result_dict = asdict(result)
                result_dict["tier"] = result.tier.value
                serializable_results.append(result_dict)

            with open(output_path, "w") as f:
                json.dump(serializable_results, f, indent=2)

        elif format == "csv":
            output_path = self.output_dir / f"ahaii_scores_{timestamp}.csv"

            # Create DataFrame for CSV export
            csv_data = []
            for result in results:
                row = {
                    "country_code": result.country_code,
                    "country_name": result.country_name,
                    "total_score": result.total_score,
                    "overall_confidence": result.overall_confidence,
                    "tier": result.tier.value,
                    "regional_rank": result.regional_rank,
                    "assessment_date": result.assessment_date,
                }

                # Add pillar scores
                for pillar in result.pillar_scores:
                    row[f"{pillar.name}_score"] = pillar.score
                    row[f"{pillar.name}_confidence"] = pillar.confidence

                csv_data.append(row)

            df = pd.DataFrame(csv_data)
            df.to_csv(output_path, index=False)

        elif format == "dashboard":
            output_path = self.output_dir / f"ahaii_dashboard_{timestamp}.json"

            # Create dashboard-ready format
            dashboard_data = {
                "last_updated": datetime.now().isoformat(),
                "countries": [],
            }

            for result in results:
                country_data = {
                    "country_code": result.country_code,
                    "country_name": result.country_name,
                    "total_score": result.total_score,
                    "tier": result.tier.value,
                    "rank": result.regional_rank,
                    "pillars": {
                        pillar.name: {
                            "score": pillar.score,
                            "confidence": pillar.confidence,
                        }
                        for pillar in result.pillar_scores
                    },
                }
                dashboard_data["countries"].append(country_data)

            with open(output_path, "w") as f:
                json.dump(dashboard_data, f, indent=2)

        logger.info(f"Results exported to: {output_path}")
        return str(output_path)


def main():
    """Main function for testing the AHAII calculator"""
    from src.data_collection.worldbank_collector import WorldBankCollector

    # Collect World Bank data
    logger.info("Collecting World Bank data...")
    collector = WorldBankCollector()
    data = collector.collect_all_indicators()

    # Calculate AHAII scores
    logger.info("Calculating AHAII scores...")
    calculator = AHAIICalculator()
    results = calculator.calculate_all_countries(data)

    # Export results in multiple formats
    calculator.export_results(results, "json")
    calculator.export_results(results, "csv")
    calculator.export_results(results, "dashboard")

    # Print summary
    print("\n=== AHAII Scoring Results ===")
    for result in results:
        print(
            f"{result.country_name}: {result.total_score:.1f} (Tier {result.tier.value}, Rank {result.regional_rank})"
        )


if __name__ == "__main__":
    main()
