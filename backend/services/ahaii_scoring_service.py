"""
AHAII Scoring Service
African Health AI Infrastructure Index scoring algorithm and methodology
"""

import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
import statistics
from datetime import datetime, date

@dataclass
class AHAIIWeights:
    """AHAII scoring methodology weights and configuration"""
    
    # Pillar weights (total = 100%)
    HUMAN_CAPITAL: float = 0.30
    PHYSICAL_INFRASTRUCTURE: float = 0.30  
    REGULATORY_INFRASTRUCTURE: float = 0.25
    ECONOMIC_MARKET: float = 0.15
    
    # Sub-pillar weights within each pillar
    HUMAN_CAPITAL_SUB = {
        'clinical_literacy': 0.50,  # 15% of total
        'informatics_capacity': 0.33,  # 10% of total
        'workforce_pipeline': 0.17   # 5% of total
    }
    
    PHYSICAL_INFRASTRUCTURE_SUB = {
        'digitization_level': 0.50,  # 15% of total
        'computational_capacity': 0.33,  # 10% of total
        'connectivity_reliability': 0.17  # 5% of total
    }
    
    REGULATORY_INFRASTRUCTURE_SUB = {
        'approval_pathways': 0.40,  # 10% of total
        'data_governance': 0.40,    # 10% of total
        'market_access': 0.20       # 5% of total
    }
    
    ECONOMIC_MARKET_SUB = {
        'market_maturity': 0.40,    # 6% of total
        'financial_sustainability': 0.33,  # 5% of total
        'research_funding': 0.27    # 4% of total
    }

@dataclass
class IndicatorDefinition:
    """Definition of a specific infrastructure indicator"""
    name: str
    pillar: str
    sub_pillar: str
    unit: str
    weight: float
    target_value: float  # Ideal/maximum value for scoring
    minimum_value: float = 0.0
    calculation_method: str = 'linear'  # 'linear', 'logarithmic', 'threshold'
    data_sources: List[str] = None
    validation_requirements: str = None

class AHAIIScoringService:
    """
    AHAII Scoring Service
    Implements the comprehensive scoring methodology for health AI infrastructure assessment
    """
    
    def __init__(self):
        self.weights = AHAIIWeights()
        self.indicator_definitions = self._initialize_indicator_definitions()
    
    def _initialize_indicator_definitions(self) -> Dict[str, IndicatorDefinition]:
        """Initialize the comprehensive indicator definitions"""
        
        indicators = {
            # Human Capital - Clinical AI Literacy (15% total weight)
            'ai_trained_clinicians_per_100k': IndicatorDefinition(
                name='AI-trained clinicians per 100,000 population',
                pillar='human_capital',
                sub_pillar='clinical_literacy',
                unit='per_100k_population',
                weight=0.35,  # 35% of clinical literacy
                target_value=50.0,  # Target: 50 AI-trained clinicians per 100k
                data_sources=['health_ministry', 'medical_associations', 'training_institutions']
            ),
            'healthcare_admin_ai_competency_rate': IndicatorDefinition(
                name='Healthcare administrator AI competency rate',
                pillar='human_capital', 
                sub_pillar='clinical_literacy',
                unit='percentage',
                weight=0.25,
                target_value=30.0,  # Target: 30% of healthcare administrators
                data_sources=['hospital_associations', 'health_informatics_surveys']
            ),
            'clinical_ai_certification_programs': IndicatorDefinition(
                name='Clinical AI certification programs available',
                pillar='human_capital',
                sub_pillar='clinical_literacy', 
                unit='count',
                weight=0.40,
                target_value=10.0,  # Target: 10+ certification programs
                calculation_method='logarithmic',
                data_sources=['medical_education_bodies', 'professional_associations']
            ),
            
            # Human Capital - Biomedical Informatics Capacity (10% total weight)  
            'medical_informatics_programs_per_million': IndicatorDefinition(
                name='Medical informatics degree programs per million population',
                pillar='human_capital',
                sub_pillar='informatics_capacity',
                unit='per_million_population', 
                weight=0.40,
                target_value=2.0,  # Target: 2 programs per million people
                data_sources=['universities', 'higher_education_ministries']
            ),
            'health_ai_publications_annual': IndicatorDefinition(
                name='Health AI publications by local authors (annual)',
                pillar='human_capital',
                sub_pillar='informatics_capacity',
                unit='count',
                weight=0.35,
                target_value=100.0,  # Target: 100+ publications annually
                calculation_method='logarithmic',
                data_sources=['pubmed', 'academic_databases', 'research_institutions']
            ),
            'clinical_ai_research_centers': IndicatorDefinition(
                name='Clinical AI research centers',
                pillar='human_capital',
                sub_pillar='informatics_capacity', 
                unit='count',
                weight=0.25,
                target_value=5.0,  # Target: 5+ research centers
                calculation_method='logarithmic',
                data_sources=['research_institutions', 'universities']
            ),
            
            # Human Capital - Technical Workforce Pipeline (5% total weight)
            'health_it_professionals_per_1000_beds': IndicatorDefinition(
                name='Healthcare IT professionals per 1,000 hospital beds',
                pillar='human_capital',
                sub_pillar='workforce_pipeline',
                unit='per_1000_beds',
                weight=0.50,
                target_value=20.0,  # Target: 20 IT professionals per 1000 beds
                data_sources=['hospital_associations', 'it_professional_bodies']
            ),
            'health_informatics_brain_drain_rate': IndicatorDefinition(
                name='Health informatics brain drain rate (inverted)',
                pillar='human_capital',
                sub_pillar='workforce_pipeline',
                unit='percentage',
                weight=0.30,
                target_value=90.0,  # Target: 90% retention (10% brain drain)
                data_sources=['professional_associations', 'migration_studies']
            ),
            'health_data_science_graduates_annual': IndicatorDefinition(
                name='Health data science graduates annually per million population',
                pillar='human_capital',
                sub_pillar='workforce_pipeline',
                unit='per_million_population',
                weight=0.20,
                target_value=10.0,  # Target: 10 graduates per million annually
                data_sources=['universities', 'graduation_statistics']
            ),
            
            # Physical Infrastructure - Hospital Digitization Level (15% total weight)
            'emr_adoption_rate': IndicatorDefinition(
                name='Electronic Medical Record (EMR) adoption rate',
                pillar='physical_infrastructure',
                sub_pillar='digitization_level',
                unit='percentage',
                weight=0.40,
                target_value=80.0,  # Target: 80% EMR adoption
                data_sources=['hospital_surveys', 'health_ministry', 'emr_vendors']
            ),
            'medical_device_connectivity_rate': IndicatorDefinition(
                name='Medical device connectivity and integration rate',
                pillar='physical_infrastructure',
                sub_pillar='digitization_level',
                unit='percentage', 
                weight=0.35,
                target_value=60.0,  # Target: 60% device connectivity
                data_sources=['hospital_assessments', 'medical_device_manufacturers']
            ),
            'interoperability_standards_implementation': IndicatorDefinition(
                name='Healthcare interoperability standards implementation rate',
                pillar='physical_infrastructure',
                sub_pillar='digitization_level',
                unit='percentage',
                weight=0.25,
                target_value=50.0,  # Target: 50% interoperability compliance
                data_sources=['health_informatics_associations', 'standards_bodies']
            ),
            
            # Physical Infrastructure - Computational Health Infrastructure (10% total weight)
            'medical_grade_data_centers_per_capita': IndicatorDefinition(
                name='Medical-grade data centers per million population',
                pillar='physical_infrastructure',
                sub_pillar='computational_capacity',
                unit='per_million_population',
                weight=0.35,
                target_value=1.0,  # Target: 1 data center per million people
                calculation_method='logarithmic',
                data_sources=['data_center_operators', 'health_ministry']
            ),
            'gpu_clusters_medical_imaging': IndicatorDefinition(
                name='GPU clusters dedicated to medical imaging',
                pillar='physical_infrastructure',
                sub_pillar='computational_capacity',
                unit='count',
                weight=0.30,
                target_value=20.0,  # Target: 20+ GPU clusters
                calculation_method='logarithmic', 
                data_sources=['hospitals', 'research_institutions', 'cloud_providers']
            ),
            'real_time_clinical_processing_capacity': IndicatorDefinition(
                name='Real-time clinical decision support processing capacity',
                pillar='physical_infrastructure',
                sub_pillar='computational_capacity',
                unit='percentage',
                weight=0.35,
                target_value=70.0,  # Target: 70% of major hospitals
                data_sources=['hospital_surveys', 'health_it_vendors']
            ),
            
            # Physical Infrastructure - Power and Connectivity Reliability (5% total weight)
            'healthcare_power_reliability': IndicatorDefinition(
                name='Healthcare facility power reliability (uptime %)',
                pillar='physical_infrastructure',
                sub_pillar='connectivity_reliability', 
                unit='percentage',
                weight=0.40,
                target_value=99.5,  # Target: 99.5% uptime
                data_sources=['utility_companies', 'hospital_surveys']
            ),
            'medical_internet_connectivity_rate': IndicatorDefinition(
                name='Medical-grade internet connectivity rate',
                pillar='physical_infrastructure',
                sub_pillar='connectivity_reliability',
                unit='percentage',
                weight=0.35,
                target_value=95.0,  # Target: 95% connectivity
                data_sources=['telecom_operators', 'hospital_surveys']
            ),
            'backup_power_coverage_rate': IndicatorDefinition(
                name='Hospital backup power system coverage rate',
                pillar='physical_infrastructure',
                sub_pillar='connectivity_reliability',
                unit='percentage',
                weight=0.25,
                target_value=90.0,  # Target: 90% backup power coverage
                data_sources=['hospital_assessments', 'energy_ministry']
            )
            
            # Additional indicators would be defined here for regulatory and economic pillars...
            # For brevity, I'll add a few key ones
        }
        
        # Add key regulatory indicators
        indicators.update({
            'medical_ai_approval_pathway_maturity': IndicatorDefinition(
                name='Medical AI approval pathway maturity score',
                pillar='regulatory_infrastructure',
                sub_pillar='approval_pathways',
                unit='score_0_to_10',
                weight=0.50,
                target_value=8.0,
                data_sources=['regulatory_authorities', 'medical_device_agencies']
            ),
            'health_data_privacy_framework_score': IndicatorDefinition(
                name='Health data privacy framework implementation score',
                pillar='regulatory_infrastructure', 
                sub_pillar='data_governance',
                unit='score_0_to_10',
                weight=0.60,
                target_value=8.0,
                data_sources=['data_protection_authorities', 'health_ministries']
            ),
            'ai_reimbursement_policy_coverage': IndicatorDefinition(
                name='AI diagnostic/treatment reimbursement policy coverage',
                pillar='regulatory_infrastructure',
                sub_pillar='market_access',
                unit='percentage', 
                weight=0.70,
                target_value=50.0,
                data_sources=['health_insurance_authorities', 'reimbursement_agencies']
            )
        })
        
        # Add key economic indicators  
        indicators.update({
            'health_ai_startups_per_million': IndicatorDefinition(
                name='Health AI startups per million population',
                pillar='economic_market',
                sub_pillar='market_maturity',
                unit='per_million_population',
                weight=0.40,
                target_value=2.0,
                calculation_method='logarithmic',
                data_sources=['startup_databases', 'venture_capital_reports']
            ),
            'health_ai_venture_capital_annual': IndicatorDefinition(
                name='Health AI venture capital investment (annual, per capita)',
                pillar='economic_market',
                sub_pillar='market_maturity', 
                unit='usd_per_capita',
                weight=0.35,
                target_value=5.0,
                calculation_method='logarithmic',
                data_sources=['venture_capital_databases', 'investment_reports']
            ),
            'health_ministry_ai_budget_percentage': IndicatorDefinition(
                name='Health ministry AI budget as % of digital health budget',
                pillar='economic_market',
                sub_pillar='financial_sustainability',
                unit='percentage',
                weight=0.60,
                target_value=15.0,
                data_sources=['health_ministries', 'government_budgets']
            ),
            'clinical_ai_research_funding_per_capita': IndicatorDefinition(
                name='Clinical AI research funding per capita (annual)',
                pillar='economic_market',
                sub_pillar='research_funding',
                unit='usd_per_capita',
                weight=0.50,
                target_value=2.0,
                calculation_method='logarithmic', 
                data_sources=['research_councils', 'university_budgets']
            )
        })
        
        return indicators
    
    def calculate_indicator_score(self, value: float, indicator: IndicatorDefinition) -> float:
        """Calculate normalized score (0-100) for a specific indicator value"""
        
        if value is None or value < indicator.minimum_value:
            return 0.0
            
        if indicator.calculation_method == 'linear':
            # Linear scaling to target value
            score = min(100.0, (value / indicator.target_value) * 100.0)
            
        elif indicator.calculation_method == 'logarithmic':
            # Logarithmic scaling for indicators with diminishing returns
            import math
            if value <= 0:
                return 0.0
            score = min(100.0, (math.log(1 + value) / math.log(1 + indicator.target_value)) * 100.0)
            
        elif indicator.calculation_method == 'threshold':
            # Threshold-based scoring
            score = 100.0 if value >= indicator.target_value else (value / indicator.target_value) * 100.0
            
        else:
            score = 0.0
            
        return round(float(score), 2)
    
    def calculate_sub_pillar_score(self, indicators_data: Dict[str, float], 
                                  sub_pillar: str, pillar: str) -> Tuple[float, Dict]:
        """Calculate weighted score for a sub-pillar"""
        
        relevant_indicators = {
            name: definition for name, definition in self.indicator_definitions.items()
            if definition.pillar == pillar and definition.sub_pillar == sub_pillar
        }
        
        if not relevant_indicators:
            return 0.0, {}
        
        weighted_scores = []
        indicator_scores = {}
        total_weight = 0.0
        
        for indicator_name, definition in relevant_indicators.items():
            if indicator_name in indicators_data:
                raw_value = indicators_data[indicator_name]
                indicator_score = self.calculate_indicator_score(raw_value, definition)
                
                weighted_scores.append(indicator_score * definition.weight)
                indicator_scores[indicator_name] = {
                    'raw_value': raw_value,
                    'normalized_score': indicator_score,
                    'weight': definition.weight,
                    'weighted_contribution': indicator_score * definition.weight
                }
                total_weight += definition.weight
        
        if total_weight == 0:
            return 0.0, indicator_scores
            
        # Calculate weighted average
        sub_pillar_score = sum(weighted_scores) / total_weight
        
        return round(sub_pillar_score, 2), indicator_scores
    
    def calculate_pillar_score(self, indicators_data: Dict[str, float], pillar: str) -> Tuple[float, Dict]:
        """Calculate weighted score for an entire pillar"""
        
        # Get sub-pillar weights for this pillar
        if pillar == 'human_capital':
            sub_pillar_weights = self.weights.HUMAN_CAPITAL_SUB
        elif pillar == 'physical_infrastructure':
            sub_pillar_weights = self.weights.PHYSICAL_INFRASTRUCTURE_SUB  
        elif pillar == 'regulatory_infrastructure':
            sub_pillar_weights = self.weights.REGULATORY_INFRASTRUCTURE_SUB
        elif pillar == 'economic_market':
            sub_pillar_weights = self.weights.ECONOMIC_MARKET_SUB
        else:
            return 0.0, {}
        
        pillar_weighted_scores = []
        sub_pillar_results = {}
        total_weight = 0.0
        
        for sub_pillar, weight in sub_pillar_weights.items():
            sub_pillar_score, indicator_details = self.calculate_sub_pillar_score(
                indicators_data, sub_pillar, pillar
            )
            
            if sub_pillar_score > 0:  # Only include sub-pillars with data
                pillar_weighted_scores.append(sub_pillar_score * weight)
                sub_pillar_results[sub_pillar] = {
                    'score': sub_pillar_score,
                    'weight': weight,
                    'weighted_contribution': sub_pillar_score * weight,
                    'indicators': indicator_details
                }
                total_weight += weight
        
        if total_weight == 0:
            return 0.0, sub_pillar_results
            
        pillar_score = sum(pillar_weighted_scores) / total_weight
        
        return round(pillar_score, 2), sub_pillar_results
    
    def calculate_ahaii_score(self, indicators_data: Dict[str, float], 
                             country_id: str, assessment_year: int) -> Dict:
        """
        Calculate complete AHAII score for a country
        
        Returns comprehensive scoring breakdown with confidence metrics
        """
        
        # Calculate each pillar score
        pillars = ['human_capital', 'physical_infrastructure', 'regulatory_infrastructure', 'economic_market']
        pillar_weights = {
            'human_capital': self.weights.HUMAN_CAPITAL,
            'physical_infrastructure': self.weights.PHYSICAL_INFRASTRUCTURE,
            'regulatory_infrastructure': self.weights.REGULATORY_INFRASTRUCTURE,
            'economic_market': self.weights.ECONOMIC_MARKET
        }
        
        pillar_scores = {}
        pillar_details = {}
        total_weighted_score = 0.0
        data_availability_count = 0
        total_indicators_count = len(self.indicator_definitions)
        
        for pillar in pillars:
            pillar_score, pillar_breakdown = self.calculate_pillar_score(indicators_data, pillar)
            pillar_scores[f'{pillar}_score'] = pillar_score
            pillar_details[pillar] = pillar_breakdown
            
            total_weighted_score += pillar_score * pillar_weights[pillar]
            
            # Count indicators with data for this pillar
            pillar_indicators_with_data = sum(
                1 for sub_pillar_data in pillar_breakdown.values() 
                for indicator in sub_pillar_data.get('indicators', {}).keys()
                if indicator in indicators_data
            )
            data_availability_count += pillar_indicators_with_data
        
        # Calculate overall AHAII score
        total_score = round(total_weighted_score, 2)
        
        # Determine readiness tier
        readiness_tier = self._determine_readiness_tier(total_score, pillar_scores)
        
        # Calculate confidence and completeness metrics
        data_completeness_percentage = (data_availability_count / total_indicators_count) * 100
        confidence_score = self._calculate_confidence_score(data_completeness_percentage, pillar_scores)
        
        # Generate tier justification
        tier_justification = self._generate_tier_justification(total_score, pillar_scores, readiness_tier)
        
        # Identify key strengths and improvement areas
        key_strengths = self._identify_key_strengths(pillar_scores)
        priority_improvement_areas = self._identify_improvement_areas(pillar_scores)
        
        return {
            'country_id': country_id,
            'assessment_year': assessment_year,
            'assessment_quarter': None,  # Can be specified separately
            'total_score': total_score,
            'readiness_tier': readiness_tier,
            'tier_justification': tier_justification,
            
            # Pillar scores
            'human_capital_score': pillar_scores['human_capital_score'],
            'physical_infrastructure_score': pillar_scores['physical_infrastructure_score'], 
            'regulatory_infrastructure_score': pillar_scores['regulatory_infrastructure_score'],
            'economic_market_score': pillar_scores['economic_market_score'],
            
            # Quality metrics
            'overall_confidence_score': confidence_score,
            'data_completeness_percentage': round(data_completeness_percentage, 2),
            'expert_validation_score': None,  # To be filled by expert review
            'peer_review_status': 'pending',
            
            # Analysis
            'key_strengths': key_strengths,
            'priority_improvement_areas': priority_improvement_areas,
            'development_trajectory': None,  # To be determined by trend analysis
            
            # Methodology metadata
            'assessment_methodology_version': '1.0',
            'indicator_weights_used': {
                'pillar_weights': pillar_weights,
                'sub_pillar_weights': {
                    'human_capital': self.weights.HUMAN_CAPITAL_SUB,
                    'physical_infrastructure': self.weights.PHYSICAL_INFRASTRUCTURE_SUB,
                    'regulatory_infrastructure': self.weights.REGULATORY_INFRASTRUCTURE_SUB,
                    'economic_market': self.weights.ECONOMIC_MARKET_SUB
                }
            },
            
            # Detailed breakdown for analysis
            'pillar_breakdown': pillar_details,
            'indicators_processed': list(indicators_data.keys()),
            'indicators_missing': [
                name for name in self.indicator_definitions.keys() 
                if name not in indicators_data
            ]
        }
    
    def _determine_readiness_tier(self, total_score: float, pillar_scores: Dict) -> int:
        """Determine AHAII readiness tier based on total score and pillar balance"""
        
        if total_score >= 70.0:
            # Tier 1: Implementation Ready
            # Must have strong performance across all pillars
            weak_pillars = sum(1 for score in pillar_scores.values() if score < 60.0)
            if weak_pillars <= 1:
                return 1
            else:
                return 2  # High score but imbalanced
        
        elif total_score >= 40.0:
            # Tier 2: Foundation Building
            return 2
            
        else:
            # Tier 3: Readiness Development
            return 3
    
    def _calculate_confidence_score(self, data_completeness: float, pillar_scores: Dict) -> float:
        """Calculate overall confidence score based on data availability and consistency"""
        
        # Base confidence from data completeness
        completeness_confidence = min(1.0, data_completeness / 80.0)  # 80% completeness = full confidence
        
        # Consistency confidence - lower if pillar scores vary wildly
        pillar_values = list(pillar_scores.values())
        if len(pillar_values) > 1:
            pillar_std = statistics.stdev(pillar_values)
            consistency_confidence = max(0.5, 1.0 - (pillar_std / 50.0))  # Penalize high variation
        else:
            consistency_confidence = 1.0
        
        # Combined confidence score
        confidence_score = (completeness_confidence * 0.7) + (consistency_confidence * 0.3)
        
        return round(min(1.0, confidence_score), 2)
    
    def _generate_tier_justification(self, total_score: float, pillar_scores: Dict, tier: int) -> str:
        """Generate human-readable justification for tier classification"""
        
        if tier == 1:
            strongest_pillar = max(pillar_scores.keys(), key=lambda k: pillar_scores[k])
            return (f"Tier 1 (Implementation Ready): Total score of {total_score} with strong "
                   f"performance across all infrastructure pillars. Particular strength in "
                   f"{strongest_pillar.replace('_', ' ')} ({pillar_scores[strongest_pillar]:.1f}).")
        
        elif tier == 2:
            strongest_pillar = max(pillar_scores.keys(), key=lambda k: pillar_scores[k])
            weakest_pillar = min(pillar_scores.keys(), key=lambda k: pillar_scores[k])
            return (f"Tier 2 (Foundation Building): Total score of {total_score} demonstrates solid "
                   f"foundation with strength in {strongest_pillar.replace('_', ' ')} "
                   f"({pillar_scores[strongest_pillar]:.1f}) but gaps in "
                   f"{weakest_pillar.replace('_', ' ')} ({pillar_scores[weakest_pillar]:.1f}).")
        
        else:
            return (f"Tier 3 (Readiness Development): Total score of {total_score} indicates "
                   f"early-stage infrastructure development requiring comprehensive capacity "
                   f"building across multiple pillars.")
    
    def _identify_key_strengths(self, pillar_scores: Dict) -> List[str]:
        """Identify key infrastructure strengths based on pillar performance"""
        
        strengths = []
        
        for pillar, score in pillar_scores.items():
            pillar_name = pillar.replace('_score', '').replace('_', ' ').title()
            
            if score >= 75.0:
                strengths.append(f"Excellent {pillar_name} infrastructure ({score:.1f}/100)")
            elif score >= 60.0:
                strengths.append(f"Strong {pillar_name} foundation ({score:.1f}/100)")
        
        # If no strong pillars, identify relative strengths
        if not strengths:
            best_pillar = max(pillar_scores.keys(), key=lambda k: pillar_scores[k])
            best_score = pillar_scores[best_pillar]
            pillar_name = best_pillar.replace('_score', '').replace('_', ' ').title()
            strengths.append(f"Relative strength in {pillar_name} ({best_score:.1f}/100)")
        
        return strengths
    
    def _identify_improvement_areas(self, pillar_scores: Dict) -> List[str]:
        """Identify priority improvement areas based on pillar weaknesses"""
        
        improvement_areas = []
        
        # Sort pillars by score to prioritize improvements
        sorted_pillars = sorted(pillar_scores.items(), key=lambda x: x[1])
        
        for pillar, score in sorted_pillars:
            pillar_name = pillar.replace('_score', '').replace('_', ' ').title()
            
            if score < 40.0:
                improvement_areas.append(f"Critical gap in {pillar_name} ({score:.1f}/100) - requires immediate attention")
            elif score < 60.0:
                improvement_areas.append(f"{pillar_name} development needed ({score:.1f}/100)")
        
        # Limit to top 3 priority areas to keep actionable
        return improvement_areas[:3]


def get_indicator_definitions_summary() -> Dict:
    """Get summary of all AHAII indicator definitions for reference"""
    
    service = AHAIIScoringService()
    
    summary = {
        'total_indicators': len(service.indicator_definitions),
        'by_pillar': {},
        'weights': {
            'human_capital': service.weights.HUMAN_CAPITAL,
            'physical_infrastructure': service.weights.PHYSICAL_INFRASTRUCTURE,
            'regulatory_infrastructure': service.weights.REGULATORY_INFRASTRUCTURE,
            'economic_market': service.weights.ECONOMIC_MARKET
        }
    }
    
    for pillar in ['human_capital', 'physical_infrastructure', 'regulatory_infrastructure', 'economic_market']:
        pillar_indicators = [
            name for name, defn in service.indicator_definitions.items() 
            if defn.pillar == pillar
        ]
        summary['by_pillar'][pillar] = {
            'count': len(pillar_indicators),
            'indicators': pillar_indicators
        }
    
    return summary


if __name__ == "__main__":
    # Test the scoring service with sample data
    scoring_service = AHAIIScoringService()
    
    # Sample indicator data for Kenya (pilot country)
    sample_data = {
        'ai_trained_clinicians_per_100k': 12.0,
        'healthcare_admin_ai_competency_rate': 15.0,
        'clinical_ai_certification_programs': 3.0,
        'medical_informatics_programs_per_million': 0.8,
        'health_ai_publications_annual': 25.0,
        'clinical_ai_research_centers': 2.0,
        'emr_adoption_rate': 35.0,
        'medical_device_connectivity_rate': 20.0,
        'healthcare_power_reliability': 85.0,
        'medical_ai_approval_pathway_maturity': 4.0,
        'health_data_privacy_framework_score': 5.0,
        'health_ai_startups_per_million': 0.5,
        'health_ministry_ai_budget_percentage': 3.0
    }
    
    result = scoring_service.calculate_ahaii_score(sample_data, 'kenya_test', 2024)
    
    print("AHAII Scoring Test Results:")
    print(f"Total Score: {result['total_score']}")
    print(f"Readiness Tier: {result['readiness_tier']}")
    print(f"Human Capital: {result['human_capital_score']}")
    print(f"Physical Infrastructure: {result['physical_infrastructure_score']}")
    print(f"Regulatory Infrastructure: {result['regulatory_infrastructure_score']}")
    print(f"Economic Market: {result['economic_market_score']}")
    print(f"Data Completeness: {result['data_completeness_percentage']}%")
    print(f"Confidence Score: {result['overall_confidence_score']}")
    print(f"\nTier Justification: {result['tier_justification']}")
    print(f"\nKey Strengths: {result['key_strengths']}")
    print(f"Priority Improvements: {result['priority_improvement_areas']}")
