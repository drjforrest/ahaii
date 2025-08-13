"""
Enhanced AHAII Calculator with Supplementary Data Integration
Integrates supplementary data into scoring algorithm including policy indicators,
proxy indicator logic, regional benchmarking, and detailed score explanations
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

# Import base calculator
from app.scoring.ahaii_calculator import AHAIICalculator, AHAIIResult, PillarScore, AHAIITier

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ProxyIndicatorApplication:
    """Details of proxy indicator usage in scoring"""
    original_indicator: str
    proxy_indicator: str
    proxy_value: float
    confidence_adjustment: float
    justification: str

@dataclass
class RegionalBenchmark:
    """Regional benchmarking context"""
    indicator_name: str
    country_value: float
    ssa_average: float
    ssa_median: float
    percentile_rank: float
    regional_tier: str

@dataclass
class EnhancedPillarScore(PillarScore):
    """Enhanced pillar score with additional analytics"""
    proxy_applications: List[ProxyIndicatorApplication] = None
    regional_benchmarks: List[RegionalBenchmark] = None
    improvement_potential: float = 0.0
    key_constraints: List[str] = None
    
    def __post_init__(self):
        if self.proxy_applications is None:
            self.proxy_applications = []
        if self.regional_benchmarks is None:
            self.regional_benchmarks = []
        if self.key_constraints is None:
            self.key_constraints = []

@dataclass
class EnhancedAHAIIResult(AHAIIResult):
    """Enhanced AHAII result with comprehensive analytics"""
    policy_indicators: Dict[str, bool] = None
    policy_confidence_scores: Dict[str, float] = None
    proxy_usage_summary: Dict[str, int] = None
    regional_comparison: Dict[str, float] = None
    detailed_recommendations: Dict[str, List[str]] = None
    methodology_notes: List[str] = None
    
    def __post_init__(self):
        if self.policy_indicators is None:
            self.policy_indicators = {}
        if self.policy_confidence_scores is None:
            self.policy_confidence_scores = {}
        if self.proxy_usage_summary is None:
            self.proxy_usage_summary = {}
        if self.regional_comparison is None:
            self.regional_comparison = {}
        if self.detailed_recommendations is None:
            self.detailed_recommendations = {}
        if self.methodology_notes is None:
            self.methodology_notes = []

class EnhancedAHAIICalculator(AHAIICalculator):
    """
    Enhanced AHAII scoring with comprehensive data integration
    """
    
    # Regional averages for Sub-Saharan Africa (estimated from World Bank data)
    SSA_REGIONAL_AVERAGES = {
        'electricity_access_pct': 48.0,
        'mobile_subscriptions_per_100': 89.0,
        'internet_users_pct': 28.0,
        'rd_expenditure_pct_gdp': 0.4,
        'hospital_beds_per_1000': 0.9,
        'current_health_expenditure_pct_gdp': 5.8,
        'tertiary_education_enrollment_rate': 8.5,
        'fixed_broadband_subscriptions_per_100': 0.4,
        'physicians_per_1000': 0.2,
        'gdp_per_capita_current_usd': 1800,
        'government_expenditure_on_education_pct_gdp': 4.5
    }
    
    # Enhanced proxy relationships with confidence factors
    ENHANCED_PROXY_RELATIONSHIPS = {
        'hospital_beds_per_1000': {
            'physicians_per_1000': {'correlation': 0.75, 'factor': 4.5, 'confidence_reduction': 0.15},
            'current_health_expenditure_pct_gdp': {'correlation': 0.65, 'factor': 0.15, 'confidence_reduction': 0.25}
        },
        'physicians_per_1000': {
            'hospital_beds_per_1000': {'correlation': 0.75, 'factor': 0.22, 'confidence_reduction': 0.15},
            'tertiary_education_enrollment_rate': {'correlation': 0.60, 'factor': 0.01, 'confidence_reduction': 0.30}
        },
        'fixed_broadband_subscriptions_per_100': {
            'internet_users_pct': {'correlation': 0.80, 'factor': 0.35, 'confidence_reduction': 0.10},
            'gdp_per_capita_current_usd': {'correlation': 0.65, 'factor': 0.002, 'confidence_reduction': 0.20}
        },
        'rd_expenditure_pct_gdp': {
            'gdp_per_capita_current_usd': {'correlation': 0.70, 'factor': 0.00003, 'confidence_reduction': 0.20},
            'tertiary_education_enrollment_rate': {'correlation': 0.55, 'factor': 0.03, 'confidence_reduction': 0.30}
        }
    }
    
    # Policy indicator weights within regulatory pillar
    POLICY_WEIGHTS = {
        'national_ai_strategy': 0.40,
        'data_protection_regulation': 0.25,
        'ai_ethics_guidelines': 0.20,
        'health_data_governance': 0.10,
        'digital_health_strategy': 0.05
    }
    
    def __init__(self, output_dir: str = "data/indicators"):
        """Initialize enhanced calculator"""
        super().__init__(output_dir)
        self.proxy_applications = {}  # Track proxy usage
    
    def apply_proxy_indicators(self, country_data: pd.DataFrame, country_code: str) -> pd.DataFrame:
        """
        Apply proxy indicator logic for missing health system data
        
        Args:
            country_data: DataFrame with country's indicator data
            country_code: ISO country code
            
        Returns:
            Enhanced DataFrame with proxy-derived indicators
        """
        enhanced_data = country_data.copy()
        proxy_applications = []
        
        available_indicators = set(country_data['indicator_name'].unique())
        
        for missing_indicator, proxy_options in self.ENHANCED_PROXY_RELATIONSHIPS.items():
            # Check if indicator is missing or has poor data quality
            indicator_data = country_data[country_data['indicator_name'] == missing_indicator]
            
            needs_proxy = (
                missing_indicator not in available_indicators or
                len(indicator_data[indicator_data['value'].notna()]) == 0 or
                indicator_data[indicator_data['value'].notna()]['confidence_score'].mean() < 0.5
            )
            
            if needs_proxy:
                # Find best available proxy
                best_proxy = None
                best_proxy_data = None
                
                for proxy_indicator, proxy_info in proxy_options.items():
                    if proxy_indicator in available_indicators:
                        proxy_data = country_data[country_data['indicator_name'] == proxy_indicator]
                        valid_proxy_data = proxy_data[proxy_data['value'].notna()]
                        
                        if len(valid_proxy_data) > 0 and valid_proxy_data['confidence_score'].mean() > 0.5:
                            best_proxy = proxy_indicator
                            best_proxy_data = valid_proxy_data
                            break
                
                if best_proxy and best_proxy_data is not None:
                    # Calculate proxy value
                    proxy_info = proxy_options[best_proxy]
                    latest_proxy_value = best_proxy_data.sort_values('year').tail(1)['value'].iloc[0]
                    proxy_derived_value = latest_proxy_value * proxy_info['factor']
                    
                    # Adjust confidence
                    original_confidence = best_proxy_data['confidence_score'].mean()
                    adjusted_confidence = original_confidence * (1 - proxy_info['confidence_reduction'])
                    
                    # Create proxy indicator record
                    proxy_record = {
                        'country_code': country_code,
                        'country_name': best_proxy_data['country_name'].iloc[0],
                        'indicator_code': f"PROXY_{missing_indicator}",
                        'indicator_name': missing_indicator,
                        'year': best_proxy_data.sort_values('year').tail(1)['year'].iloc[0],
                        'value': proxy_derived_value,
                        'confidence_score': adjusted_confidence,
                        'data_source': f"proxy_from_{best_proxy}"
                    }
                    
                    # Add to enhanced data
                    enhanced_data = pd.concat([enhanced_data, pd.DataFrame([proxy_record])], ignore_index=True)
                    
                    # Track proxy application
                    proxy_application = ProxyIndicatorApplication(
                        original_indicator=missing_indicator,
                        proxy_indicator=best_proxy,
                        proxy_value=proxy_derived_value,
                        confidence_adjustment=proxy_info['confidence_reduction'],
                        justification=f"Derived from {best_proxy} using correlation factor {proxy_info['correlation']:.2f}"
                    )
                    proxy_applications.append(proxy_application)
                    
                    logger.info(f"Applied proxy for {missing_indicator} using {best_proxy} -> {proxy_derived_value:.2f}")
        
        # Store proxy applications for this country
        self.proxy_applications[country_code] = proxy_applications
        
        return enhanced_data
    
    def calculate_regional_benchmarks(self, country_data: pd.DataFrame, country_code: str) -> List[RegionalBenchmark]:
        """
        Calculate regional benchmarking context for country indicators
        
        Args:
            country_data: DataFrame with country's indicator data
            country_code: ISO country code
            
        Returns:
            List of regional benchmark comparisons
        """
        benchmarks = []
        
        available_indicators = country_data['indicator_name'].unique()
        
        for indicator_name in available_indicators:
            if indicator_name in self.SSA_REGIONAL_AVERAGES:
                indicator_data = country_data[country_data['indicator_name'] == indicator_name]
                valid_data = indicator_data[indicator_data['value'].notna()]
                
                if len(valid_data) > 0:
                    # Use most recent value
                    country_value = valid_data.sort_values('year').tail(1)['value'].iloc[0]
                    ssa_average = self.SSA_REGIONAL_AVERAGES[indicator_name]
                    
                    # Estimate SSA median (roughly 85% of average for most indicators)
                    ssa_median = ssa_average * 0.85
                    
                    # Calculate percentile rank (simplified)
                    if country_value >= ssa_average:
                        percentile_rank = 75 + (min(country_value / ssa_average - 1, 1) * 25)
                    else:
                        percentile_rank = max(0, (country_value / ssa_average) * 75)
                    
                    # Determine regional tier
                    if percentile_rank >= 75:
                        regional_tier = "Top Quartile"
                    elif percentile_rank >= 50:
                        regional_tier = "Above Median"
                    elif percentile_rank >= 25:
                        regional_tier = "Below Median"
                    else:
                        regional_tier = "Bottom Quartile"
                    
                    benchmark = RegionalBenchmark(
                        indicator_name=indicator_name,
                        country_value=country_value,
                        ssa_average=ssa_average,
                        ssa_median=ssa_median,
                        percentile_rank=round(percentile_rank, 1),
                        regional_tier=regional_tier
                    )
                    benchmarks.append(benchmark)
        
        return benchmarks
    
    def integrate_policy_indicators(self, country_data: pd.DataFrame, policy_data: pd.DataFrame, 
                                  country_code: str) -> pd.DataFrame:
        """
        Integrate policy indicators into regulatory framework pillar
        
        Args:
            country_data: DataFrame with country's quantitative indicator data
            policy_data: DataFrame with policy indicators
            country_code: ISO country code
            
        Returns:
            Enhanced DataFrame with policy indicators integrated
        """
        enhanced_data = country_data.copy()
        
        # Get policy indicators for this country
        country_policies = policy_data[policy_data['country_code'] == country_code]
        
        if len(country_policies) == 0:
            logger.warning(f"No policy indicators found for {country_code}")
            return enhanced_data
        
        # Calculate weighted policy score for regulatory pillar
        policy_score = 0.0
        total_weight = 0.0
        policy_confidence = 0.0
        
        for _, policy_row in country_policies.iterrows():
            indicator_name = policy_row['indicator_name']
            indicator_value = policy_row['indicator_value']
            confidence = policy_row['confidence_score']
            
            if indicator_name in self.POLICY_WEIGHTS:
                weight = self.POLICY_WEIGHTS[indicator_name]
                policy_score += (100 if indicator_value else 0) * weight
                total_weight += weight
                policy_confidence += confidence * weight
        
        if total_weight > 0:
            policy_score = policy_score / total_weight  # Normalize to 0-100
            policy_confidence = policy_confidence / total_weight
            
            # Create synthetic policy indicator for regulatory pillar
            policy_record = {
                'country_code': country_code,
                'country_name': enhanced_data['country_name'].iloc[0] if len(enhanced_data) > 0 else country_code,
                'indicator_code': 'POLICY_COMPOSITE',
                'indicator_name': 'policy_framework_score',
                'year': datetime.now().year,
                'value': policy_score,
                'confidence_score': policy_confidence,
                'data_source': 'policy_indicator_integration'
            }
            
            enhanced_data = pd.concat([enhanced_data, pd.DataFrame([policy_record])], ignore_index=True)
            
            logger.info(f"Integrated policy indicators for {country_code}: score={policy_score:.1f}, confidence={policy_confidence:.2f}")
        
        return enhanced_data
    
    def calculate_enhanced_pillar_score(self, country_data: pd.DataFrame, pillar_name: str, 
                                      country_code: str) -> EnhancedPillarScore:
        """
        Calculate enhanced pillar score with additional analytics
        
        Args:
            country_data: DataFrame with country's indicator data
            pillar_name: Name of the pillar to calculate
            country_code: ISO country code
            
        Returns:
            Enhanced PillarScore object
        """
        # Get base pillar score
        base_score = self.calculate_pillar_score(country_data, pillar_name)
        
        # Get proxy applications for this country
        proxy_applications = self.proxy_applications.get(country_code, [])
        pillar_proxies = [p for p in proxy_applications 
                         if self.INDICATOR_PILLAR_MAPPING.get(p.original_indicator) == pillar_name]
        
        # Calculate regional benchmarks
        regional_benchmarks = self.calculate_regional_benchmarks(country_data, country_code)
        pillar_benchmarks = [b for b in regional_benchmarks 
                           if self.INDICATOR_PILLAR_MAPPING.get(b.indicator_name) == pillar_name]
        
        # Calculate improvement potential (how much room for growth)
        improvement_potential = max(0, 100 - base_score.score)
        
        # Identify key constraints
        key_constraints = []
        for indicator, value in base_score.normalized_indicators.items():
            if value < 30:  # Low-performing indicators
                key_constraints.append(f"Low {indicator.replace('_', ' ')}: {value:.1f}")
        
        # Add pillar-specific constraints
        if pillar_name == 'regulatory_framework' and base_score.score < 40:
            key_constraints.append("Limited policy framework development")
        elif pillar_name == 'physical_infrastructure' and base_score.score < 50:
            key_constraints.append("Basic infrastructure gaps")
        elif pillar_name == 'human_capital' and base_score.score < 40:
            key_constraints.append("Skills and capacity development needed")
        elif pillar_name == 'economic_market' and base_score.score < 35:
            key_constraints.append("Market size and funding limitations")
        
        enhanced_score = EnhancedPillarScore(
            name=base_score.name,
            score=base_score.score,
            confidence=base_score.confidence,
            sub_components=base_score.sub_components,
            weight=base_score.weight,
            normalized_indicators=base_score.normalized_indicators,
            proxy_applications=pillar_proxies,
            regional_benchmarks=pillar_benchmarks,
            improvement_potential=improvement_potential,
            key_constraints=key_constraints[:3]  # Top 3 constraints
        )
        
        return enhanced_score
    
    def generate_detailed_recommendations(self, pillar_scores: List[EnhancedPillarScore], 
                                        tier: AHAIITier, country_code: str) -> Dict[str, List[str]]:
        """
        Generate detailed improvement recommendations by pillar
        
        Args:
            pillar_scores: List of enhanced pillar scores
            tier: Current tier classification
            country_code: ISO country code
            
        Returns:
            Dictionary of recommendations by pillar
        """
        recommendations = {}
        
        for pillar in pillar_scores:
            pillar_recommendations = []
            
            # High-priority recommendations based on pillar performance
            if pillar.score < 40:  # Critical improvement needed
                if pillar.name == 'human_capital':
                    pillar_recommendations.extend([
                        "URGENT: Establish medical informatics training programs in medical schools",
                        "Create national health AI workforce development strategy",
                        "Partner with international institutions for clinical AI capacity building"
                    ])
                elif pillar.name == 'physical_infrastructure':
                    pillar_recommendations.extend([
                        "URGENT: Accelerate EMR implementation in public healthcare facilities",
                        "Upgrade healthcare connectivity infrastructure",
                        "Establish national health data center capabilities"
                    ])
                elif pillar.name == 'regulatory_framework':
                    pillar_recommendations.extend([
                        "URGENT: Develop national AI strategy with health AI components",
                        "Establish medical AI regulatory approval pathways",
                        "Create health data governance framework"
                    ])
                elif pillar.name == 'economic_market':
                    pillar_recommendations.extend([
                        "URGENT: Increase R&D investment in health AI technologies",
                        "Create health AI innovation funding mechanisms",
                        "Establish public-private partnerships for health AI development"
                    ])
            
            elif pillar.score < 60:  # Moderate improvement needed
                if pillar.name == 'human_capital':
                    pillar_recommendations.extend([
                        "Expand health informatics education programs",
                        "Create continuing education requirements for clinical AI"
                    ])
                elif pillar.name == 'physical_infrastructure':
                    pillar_recommendations.extend([
                        "Standardize EMR systems across healthcare facilities",
                        "Improve healthcare facility internet connectivity"
                    ])
                elif pillar.name == 'regulatory_framework':
                    pillar_recommendations.extend([
                        "Strengthen AI ethics guidelines implementation",
                        "Enhance health data privacy regulations"
                    ])
                elif pillar.name == 'economic_market':
                    pillar_recommendations.extend([
                        "Support health AI startup ecosystem development",
                        "Create health AI market incentives"
                    ])
            
            # Add constraint-specific recommendations
            for constraint in pillar.key_constraints:
                if "electricity_access" in constraint.lower():
                    pillar_recommendations.append("Prioritize healthcare facility electrification")
                elif "internet_users" in constraint.lower():
                    pillar_recommendations.append("Expand digital literacy and internet access programs")
                elif "hospital_beds" in constraint.lower():
                    pillar_recommendations.append("Increase healthcare infrastructure investment")
            
            # Add proxy-based recommendations
            for proxy_app in pillar.proxy_applications:
                pillar_recommendations.append(
                    f"Improve data collection for {proxy_app.original_indicator.replace('_', ' ')} "
                    f"(currently estimated from {proxy_app.proxy_indicator.replace('_', ' ')})"
                )
            
            recommendations[pillar.name] = pillar_recommendations[:5]  # Top 5 per pillar
        
        return recommendations
    
    def calculate_enhanced_ahaii_score(self, country_data: pd.DataFrame, policy_data: pd.DataFrame,
                                     country_code: str, country_name: str) -> EnhancedAHAIIResult:
        """
        Calculate enhanced AHAII score with comprehensive data integration
        
        Args:
            country_data: DataFrame with country's quantitative indicator data
            policy_data: DataFrame with policy indicators
            country_code: ISO country code
            country_name: Country name
            
        Returns:
            Enhanced AHAII result with comprehensive analytics
        """
        logger.info(f"Calculating enhanced AHAII score for {country_name} ({country_code})")
        
        # Apply proxy indicators
        enhanced_data = self.apply_proxy_indicators(country_data, country_code)
        
        # Integrate policy indicators
        enhanced_data = self.integrate_policy_indicators(enhanced_data, policy_data, country_code)
        
        # Update indicator-pillar mapping for policy indicators
        enhanced_mapping = self.INDICATOR_PILLAR_MAPPING.copy()
        enhanced_mapping['policy_framework_score'] = 'regulatory_framework'
        
        # Temporarily update mapping
        original_mapping = self.INDICATOR_PILLAR_MAPPING
        self.INDICATOR_PILLAR_MAPPING = enhanced_mapping
        
        # Calculate enhanced pillar scores
        enhanced_pillar_scores = []
        total_weighted_score = 0.0
        total_weighted_confidence = 0.0
        
        for pillar_name in self.PILLAR_WEIGHTS.keys():
            pillar_score = self.calculate_enhanced_pillar_score(enhanced_data, pillar_name, country_code)
            enhanced_pillar_scores.append(pillar_score)
            
            weight = pillar_score.weight
            total_weighted_score += pillar_score.score * weight
            total_weighted_confidence += pillar_score.confidence * weight
        
        # Restore original mapping
        self.INDICATOR_PILLAR_MAPPING = original_mapping
        
        # Calculate overall scores
        total_score = total_weighted_score
        overall_confidence = total_weighted_confidence
        
        # Generate tier classification
        tier = self.generate_tier_classification(total_score, overall_confidence)
        
        # Extract policy indicators
        country_policies = policy_data[policy_data['country_code'] == country_code]
        policy_indicators = dict(zip(country_policies['indicator_name'], country_policies['indicator_value']))
        policy_confidence_scores = dict(zip(country_policies['indicator_name'], country_policies['confidence_score']))
        
        # Generate proxy usage summary
        proxy_usage_summary = {}
        for pillar_score in enhanced_pillar_scores:
            for proxy_app in pillar_score.proxy_applications:
                if proxy_app.original_indicator not in proxy_usage_summary:
                    proxy_usage_summary[proxy_app.original_indicator] = 0
                proxy_usage_summary[proxy_app.original_indicator] += 1
        
        # Calculate regional comparison
        regional_benchmarks = self.calculate_regional_benchmarks(enhanced_data, country_code)
        regional_comparison = {}
        for benchmark in regional_benchmarks:
            regional_comparison[benchmark.indicator_name] = {
                'percentile_rank': benchmark.percentile_rank,
                'regional_tier': benchmark.regional_tier
            }
        
        # Generate detailed recommendations
        detailed_recommendations = self.generate_detailed_recommendations(
            enhanced_pillar_scores, tier, country_code
        )
        
        # Generate methodology notes
        methodology_notes = [
            f"Assessment incorporates {len(policy_indicators)} policy indicators",
            f"Applied {len(proxy_usage_summary)} proxy indicator estimations",
            f"Regional benchmarking against {len(self.SSA_REGIONAL_AVERAGES)} SSA indicators",
            "Confidence scores adjusted for data quality and proxy usage",
            "Tier classification includes confidence thresholds"
        ]
        
        # Basic recommendations for backward compatibility
        basic_recommendations = []
        for pillar_recs in detailed_recommendations.values():
            basic_recommendations.extend(pillar_recs[:2])  # Top 2 from each pillar
        
        result = EnhancedAHAIIResult(
            country_code=country_code,
            country_name=country_name,
            assessment_date=datetime.now().isoformat(),
            total_score=round(total_score, 2),
            overall_confidence=round(overall_confidence, 2),
            tier=tier,
            pillar_scores=enhanced_pillar_scores,
            improvement_recommendations=basic_recommendations[:5],
            data_quality_issues=self.identify_data_quality_issues(enhanced_data),
            policy_indicators=policy_indicators,
            policy_confidence_scores=policy_confidence_scores,
            proxy_usage_summary=proxy_usage_summary,
            regional_comparison=regional_comparison,
            detailed_recommendations=detailed_recommendations,
            methodology_notes=methodology_notes
        )
        
        logger.info(f"Enhanced AHAII Score for {country_name}: {total_score:.1f} (Tier {tier.value})")
        
        return result


def main():
    """Main function for testing enhanced AHAII calculator"""
    from app.data_collection.worldbank_collector import WorldBankCollector
    from app.data_collection.policy_indicator_collector import PolicyIndicatorCollector
    
    # Collect all data
    logger.info("Collecting World Bank data...")
    wb_collector = WorldBankCollector()
    wb_data = wb_collector.collect_all_indicators()
    
    logger.info("Collecting policy indicators...")
    policy_collector = PolicyIndicatorCollector()
    policy_data = policy_collector.collect_all_countries()
    
    # Calculate enhanced AHAII scores
    logger.info("Calculating enhanced AHAII scores...")
    calculator = EnhancedAHAIICalculator()
    
    enhanced_results = []
    pilot_countries = ['ZAF', 'KEN', 'NGA', 'GHA', 'EGY']
    country_names = {
        'ZAF': 'South Africa',
        'KEN': 'Kenya', 
        'NGA': 'Nigeria',
        'GHA': 'Ghana',
        'EGY': 'Egypt'
    }
    
    for country_code in pilot_countries:
        country_name = country_names[country_code]
        country_wb_data = wb_data[wb_data['country_code'] == country_code]
        
        if len(country_wb_data) > 0:
            result = calculator.calculate_enhanced_ahaii_score(
                country_wb_data, policy_data, country_code, country_name
            )
            enhanced_results.append(result)
    
    # Add regional rankings
    enhanced_results.sort(key=lambda r: r.total_score, reverse=True)
    for i, result in enumerate(enhanced_results):
        result.regional_rank = i + 1
    
    # Export enhanced results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_path = Path("data/indicators") / f"enhanced_ahaii_scores_{timestamp}.json"
    
    # Convert to serializable format
    serializable_results = []
    for result in enhanced_results:
        result_dict = asdict(result)
        result_dict['tier'] = result.tier.value
        serializable_results.append(result_dict)
    
    with open(output_path, 'w') as f:
        json.dump(serializable_results, f, indent=2)
    
    # Print enhanced summary
    print("\n=== Enhanced AHAII Scoring Results ===")
    for result in enhanced_results:
        print(f"\n{result.country_name}: {result.total_score:.1f} (Tier {result.tier.value}, Rank {result.regional_rank})")
        print(f"  Policy indicators: {sum(result.policy_indicators.values())}/{len(result.policy_indicators)}")
        print(f"  Proxy applications: {sum(result.proxy_usage_summary.values())}")
        print(f"  Top recommendation: {result.improvement_recommendations[0] if result.improvement_recommendations else 'None'}")
    
    print(f"\nDetailed results saved to: {output_path}")


if __name__ == "__main__":
    main()