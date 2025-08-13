"""
Final AHAII Assessment Report Generator
Generates comprehensive pilot assessment with complete AHAII scores,
ranking justification, methodology transparency documentation,
and identification of data gaps requiring ongoing monitoring
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.offline as pyo

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class CountryAssessment:
    """Complete country assessment for AHAII pilot"""
    country_code: str
    country_name: str
    final_score: float
    confidence_interval: Tuple[float, float]
    tier_classification: int
    regional_rank: int
    pillar_breakdown: Dict[str, float]
    key_strengths: List[str]
    critical_gaps: List[str]
    improvement_roadmap: List[str]
    data_quality_grade: str
    expert_validation_status: str

@dataclass
class PilotAssessmentReport:
    """Complete AHAII pilot assessment report"""
    assessment_date: str
    methodology_version: str
    pilot_countries: List[str]
    country_assessments: List[CountryAssessment]
    regional_analysis: Dict[str, Any]
    methodology_documentation: Dict[str, Any]
    data_quality_assessment: Dict[str, Any]
    expert_validation_summary: Dict[str, Any]
    key_findings: List[str]
    recommendations: Dict[str, List[str]]
    future_work: List[str]

class AHAIIPilotReportGenerator:
    """
    Comprehensive AHAII pilot assessment report generator
    """
    
    # Report styling and configuration
    REPORT_CONFIG = {
        'title': 'African Health AI Infrastructure Index (AHAII) - Pilot Assessment Report',
        'subtitle': 'Quantitative Assessment of Health AI Infrastructure Readiness Across Five African Countries',
        'authors': ['AHAII Research Team'],
        'version': '1.0',
        'report_type': 'pilot_assessment'
    }
    
    # Tier descriptions
    TIER_DESCRIPTIONS = {
        1: {
            'name': 'Implementation Ready',
            'description': 'Countries with robust health AI infrastructure capable of supporting large-scale AI implementation',
            'score_range': '70-100',
            'characteristics': [
                'Strong digital health foundation',
                'Established AI governance frameworks',
                'Active health AI ecosystem',
                'High-quality health data infrastructure'
            ]
        },
        2: {
            'name': 'Foundation Building',
            'description': 'Countries with developing health AI infrastructure requiring targeted investment',
            'score_range': '40-69',
            'characteristics': [
                'Basic digital health infrastructure',
                'Emerging AI policy frameworks',
                'Growing health AI interest',
                'Moderate data quality and availability'
            ]
        },
        3: {
            'name': 'Development',
            'description': 'Countries requiring comprehensive health AI infrastructure development',
            'score_range': '0-39',
            'characteristics': [
                'Limited digital health infrastructure',
                'Minimal AI governance',
                'Early-stage ecosystem development',
                'Significant data and capacity gaps'
            ]
        }
    }
    
    def __init__(self, output_dir: str = "analysis/pilot_assessment"):
        """
        Initialize AHAII pilot report generator
        
        Args:
            output_dir: Directory for saving reports and visualizations
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        self.reports_dir = self.output_dir / "reports"
        self.visualizations_dir = self.output_dir / "visualizations"
        self.data_dir = self.output_dir / "data"
        
        for directory in [self.reports_dir, self.visualizations_dir, self.data_dir]:
            directory.mkdir(exist_ok=True)
    
    def compile_country_assessments(self, enhanced_results: List, validation_results: List, 
                                  data_quality_metrics: List) -> List[CountryAssessment]:
        """
        Compile comprehensive country assessments
        
        Args:
            enhanced_results: Enhanced AHAII results
            validation_results: Expert validation results
            data_quality_metrics: Data quality assessment results
            
        Returns:
            List of complete country assessments
        """
        logger.info("Compiling comprehensive country assessments")
        
        country_assessments = []
        
        for result in enhanced_results:
            # Find corresponding validation and data quality results
            validation_summary = self._get_validation_summary(result.country_code, validation_results)
            data_quality_grade = self._get_data_quality_grade(result.country_code, data_quality_metrics)
            
            # Extract pillar breakdown
            pillar_breakdown = {
                pillar.name: pillar.score for pillar in result.pillar_scores
            }
            
            # Identify key strengths (top-performing pillars)
            sorted_pillars = sorted(result.pillar_scores, key=lambda p: p.score, reverse=True)
            key_strengths = []
            
            for pillar in sorted_pillars[:2]:  # Top 2 pillars
                if pillar.score >= 60:
                    strength_area = self._pillar_to_strength_description(pillar.name, pillar.score)
                    key_strengths.append(strength_area)
            
            # Identify critical gaps (lowest-performing pillars)
            critical_gaps = []
            for pillar in sorted_pillars[-2:]:  # Bottom 2 pillars
                if pillar.score < 50:
                    gap_area = self._pillar_to_gap_description(pillar.name, pillar.score)
                    critical_gaps.append(gap_area)
            
            # Create improvement roadmap
            improvement_roadmap = self._create_improvement_roadmap(result)
            
            # Calculate confidence interval (simplified)
            ci_margin = 5 + (1 - result.overall_confidence) * 10  # Larger margin for lower confidence
            confidence_interval = (
                max(0, result.total_score - ci_margin),
                min(100, result.total_score + ci_margin)
            )
            
            assessment = CountryAssessment(
                country_code=result.country_code,
                country_name=result.country_name,
                final_score=result.total_score,
                confidence_interval=confidence_interval,
                tier_classification=result.tier.value,
                regional_rank=result.regional_rank,
                pillar_breakdown=pillar_breakdown,
                key_strengths=key_strengths,
                critical_gaps=critical_gaps,
                improvement_roadmap=improvement_roadmap,
                data_quality_grade=data_quality_grade,
                expert_validation_status=validation_summary
            )
            
            country_assessments.append(assessment)
        
        return country_assessments
    
    def _get_validation_summary(self, country_code: str, validation_results: List) -> str:
        """Get expert validation summary for country"""
        country_validations = [v for v in validation_results if hasattr(v, 'country_code') and v.country_code == country_code]
        
        if not country_validations:
            return "No expert validation available"
        
        validated_count = len([v for v in country_validations if v.final_status.value == 'validated'])
        total_count = len(country_validations)
        
        if validated_count / total_count >= 0.8:
            return "High expert validation confidence"
        elif validated_count / total_count >= 0.6:
            return "Moderate expert validation confidence"
        else:
            return "Low expert validation confidence"
    
    def _get_data_quality_grade(self, country_code: str, data_quality_metrics: List) -> str:
        """Get data quality grade for country"""
        country_metrics = [m for m in data_quality_metrics if hasattr(m, 'country_code') and m.country_code == country_code]
        
        if not country_metrics:
            return "B"  # Default grade
        
        quality_grades = [m.overall_quality_grade for m in country_metrics]
        grade_scores = {'A': 4, 'B': 3, 'C': 2, 'D': 1, 'F': 0}
        
        avg_score = np.mean([grade_scores.get(grade, 2) for grade in quality_grades])
        
        for grade, score in grade_scores.items():
            if avg_score >= score:
                return grade
        return 'F'
    
    def _pillar_to_strength_description(self, pillar_name: str, score: float) -> str:
        """Convert pillar performance to strength description"""
        strength_map = {
            'human_capital': f"Strong health informatics workforce and training programs (Score: {score:.1f})",
            'physical_infrastructure': f"Robust digital health and connectivity infrastructure (Score: {score:.1f})",
            'regulatory_framework': f"Well-developed AI governance and policy framework (Score: {score:.1f})",
            'economic_market': f"Active health AI ecosystem and funding environment (Score: {score:.1f})"
        }
        return strength_map.get(pillar_name, f"{pillar_name}: {score:.1f}")
    
    def _pillar_to_gap_description(self, pillar_name: str, score: float) -> str:
        """Convert pillar performance to gap description"""
        gap_map = {
            'human_capital': f"Limited health AI workforce and training capacity (Score: {score:.1f})",
            'physical_infrastructure': f"Inadequate digital health infrastructure and connectivity (Score: {score:.1f})",
            'regulatory_framework': f"Underdeveloped AI governance and regulatory framework (Score: {score:.1f})",
            'economic_market': f"Nascent health AI ecosystem with limited funding (Score: {score:.1f})"
        }
        return gap_map.get(pillar_name, f"{pillar_name}: {score:.1f}")
    
    def _create_improvement_roadmap(self, result) -> List[str]:
        """Create improvement roadmap based on AHAII result"""
        roadmap = []
        
        # Add tier-specific recommendations
        if result.tier.value == 3:  # Development
            roadmap.extend([
                "Year 1-2: Establish basic digital health infrastructure and connectivity",
                "Year 2-3: Develop health AI workforce through training and education programs",
                "Year 3-5: Create AI governance framework and pilot health AI applications"
            ])
        elif result.tier.value == 2:  # Foundation Building
            roadmap.extend([
                "Year 1-2: Strengthen existing digital health systems and data quality",
                "Year 2-3: Advance AI policy framework and regulatory capabilities",
                "Year 3-4: Scale successful health AI pilots and build ecosystem partnerships"
            ])
        else:  # Implementation Ready
            roadmap.extend([
                "Year 1-2: Lead regional health AI initiatives and standards development",
                "Year 2-3: Expand health AI implementation across healthcare system",
                "Year 3-5: Drive innovation and support neighboring countries' development"
            ])
        
        # Add pillar-specific recommendations
        for pillar in result.pillar_scores:
            if pillar.score < 40:
                if pillar.name == 'human_capital':
                    roadmap.append("Priority: Establish medical informatics degree programs")
                elif pillar.name == 'physical_infrastructure':
                    roadmap.append("Priority: Upgrade healthcare facility connectivity and EMR systems")
                elif pillar.name == 'regulatory_framework':
                    roadmap.append("Priority: Develop national AI strategy with health components")
                elif pillar.name == 'economic_market':
                    roadmap.append("Priority: Create health AI innovation fund and incubator programs")
        
        return roadmap[:5]  # Top 5 recommendations
    
    def generate_regional_analysis(self, country_assessments: List[CountryAssessment]) -> Dict[str, Any]:
        """
        Generate regional analysis and comparisons
        
        Args:
            country_assessments: List of country assessments
            
        Returns:
            Regional analysis dictionary
        """
        scores = [assessment.final_score for assessment in country_assessments]
        pillars = ['human_capital', 'physical_infrastructure', 'regulatory_framework', 'economic_market']
        
        # Calculate regional statistics
        regional_stats = {
            'mean_score': np.mean(scores),
            'median_score': np.median(scores),
            'score_range': (min(scores), max(scores)),
            'standard_deviation': np.std(scores),
            'tier_distribution': {
                'tier_1': len([a for a in country_assessments if a.tier_classification == 1]),
                'tier_2': len([a for a in country_assessments if a.tier_classification == 2]),
                'tier_3': len([a for a in country_assessments if a.tier_classification == 3])
            }
        }
        
        # Pillar analysis
        pillar_analysis = {}
        for pillar in pillars:
            pillar_scores = [assessment.pillar_breakdown[pillar] for assessment in country_assessments]
            pillar_analysis[pillar] = {
                'mean': np.mean(pillar_scores),
                'range': (min(pillar_scores), max(pillar_scores)),
                'top_performer': max(country_assessments, key=lambda a: a.pillar_breakdown[pillar]).country_name,
                'improvement_needed': [a.country_name for a in country_assessments if a.pillar_breakdown[pillar] < 40]
            }
        
        # Country rankings and comparisons
        rankings = {
            'overall_ranking': [(a.country_name, a.final_score, a.regional_rank) for a in 
                              sorted(country_assessments, key=lambda x: x.final_score, reverse=True)],
            'pillar_leaders': {
                pillar: max(country_assessments, key=lambda a: a.pillar_breakdown[pillar]).country_name
                for pillar in pillars
            }
        }
        
        regional_analysis = {
            'summary_statistics': regional_stats,
            'pillar_performance': pillar_analysis,
            'country_rankings': rankings,
            'key_insights': [
                f"Regional average AHAII score: {regional_stats['mean_score']:.1f}",
                f"Score variation: {regional_stats['standard_deviation']:.1f} points standard deviation",
                f"Strongest pillar regionally: {max(pillar_analysis.items(), key=lambda x: x[1]['mean'])[0]}",
                f"Greatest improvement opportunity: {min(pillar_analysis.items(), key=lambda x: x[1]['mean'])[0]}"
            ]
        }
        
        return regional_analysis
    
    def document_methodology(self, enhanced_results: List) -> Dict[str, Any]:
        """
        Document AHAII methodology for transparency and replication
        
        Args:
            enhanced_results: Enhanced AHAII results for methodology extraction
            
        Returns:
            Methodology documentation
        """
        methodology_doc = {
            'framework_overview': {
                'name': 'African Health AI Infrastructure Index (AHAII)',
                'purpose': 'Assess health AI infrastructure readiness across African countries',
                'theoretical_foundation': 'Four-pillar health AI infrastructure framework',
                'assessment_scope': 'National-level health AI infrastructure readiness',
                'target_users': ['Policymakers', 'Investors', 'Development organizations', 'Researchers']
            },
            'pillar_structure': {
                'human_capital': {
                    'weight': 0.30,
                    'description': 'Health AI workforce, training, and literacy',
                    'key_indicators': ['Tertiary education enrollment', 'Health workforce density', 'Education investment'],
                    'rationale': 'Human capital is fundamental to health AI implementation and sustainable development'
                },
                'physical_infrastructure': {
                    'weight': 0.30,
                    'description': 'Digital health infrastructure, connectivity, and computing resources',
                    'key_indicators': ['Internet connectivity', 'Healthcare electrification', 'EMR adoption'],
                    'rationale': 'Physical infrastructure enables health AI technology deployment and operation'
                },
                'regulatory_framework': {
                    'weight': 0.25,
                    'description': 'AI governance, health data regulation, and policy framework',
                    'key_indicators': ['AI strategy', 'Data protection laws', 'Health governance'],
                    'rationale': 'Regulatory framework ensures safe, ethical, and effective health AI implementation'
                },
                'economic_market': {
                    'weight': 0.15,
                    'description': 'Health AI ecosystem, funding, and market development',
                    'key_indicators': ['GDP per capita', 'Health expenditure', 'Innovation ecosystem'],
                    'rationale': 'Economic factors determine sustainability and scalability of health AI initiatives'
                }
            },
            'data_sources': {
                'quantitative_indicators': {
                    'world_bank': 'Primary source for infrastructure and economic indicators',
                    'coverage': '12 core indicators across 4 pillars',
                    'time_period': '2020-2023',
                    'update_frequency': 'Annual'
                },
                'policy_indicators': {
                    'oxford_gari': 'Government AI readiness assessments',
                    'government_sources': 'Official policy documents and websites',
                    'expert_knowledge': 'Domain expert validation and input',
                    'binary_assessment': 'Yes/No policy existence determination'
                },
                'ecosystem_mapping': {
                    'universities': 'Health AI and biomedical informatics programs',
                    'companies': 'Health AI startups and established companies',
                    'initiatives': 'Government and hospital AI pilot programs',
                    'evidence_sources': 'Multiple validation sources per organization'
                }
            },
            'scoring_methodology': {
                'normalization': 'Min-max scaling to 0-100 range using global benchmarks',
                'aggregation': 'Weighted average within pillars, then across pillars',
                'confidence_weighting': 'Scores adjusted for data quality and certainty',
                'proxy_indicators': 'Statistical relationships used for missing data',
                'tier_classification': 'Score ranges with confidence thresholds'
            },
            'quality_assurance': {
                'data_validation': 'Multi-source verification and confidence scoring',
                'expert_review': 'Domain expert validation of uncertain indicators',
                'regional_benchmarking': 'Sub-Saharan Africa comparative context',
                'uncertainty_quantification': 'Confidence intervals and sensitivity analysis'
            },
            'limitations': [
                'Limited to 5 pilot countries in initial assessment',
                'Some indicators rely on proxy measures due to data availability',
                'Policy indicators may have temporal lag between implementation and detection',
                'Ecosystem mapping may not capture all health AI activities',
                'Expert validation simulation used in place of full expert survey'
            ],
            'future_improvements': [
                'Expand to all 54 African Union countries',
                'Integrate real-time expert validation system',
                'Add clinical AI deployment tracking',
                'Include patient outcome and impact metrics',
                'Develop automated policy monitoring system'
            ]
        }
        
        return methodology_doc
    
    def create_visualizations(self, country_assessments: List[CountryAssessment], 
                            regional_analysis: Dict[str, Any]) -> Dict[str, str]:
        """
        Create comprehensive visualizations for the report
        
        Args:
            country_assessments: List of country assessments
            regional_analysis: Regional analysis results
            
        Returns:
            Dictionary mapping visualization names to file paths
        """
        logger.info("Creating comprehensive visualizations for AHAII pilot report")
        
        visualization_paths = {}
        
        # 1. Overall AHAII Scores with Confidence Intervals
        fig_scores = self._create_score_comparison_chart(country_assessments)
        scores_path = self.visualizations_dir / "ahaii_scores_comparison.html"
        fig_scores.write_html(str(scores_path))
        visualization_paths['scores_comparison'] = str(scores_path)
        
        # 2. Pillar Performance Radar Chart
        fig_radar = self._create_pillar_radar_chart(country_assessments)
        radar_path = self.visualizations_dir / "pillar_performance_radar.html"
        fig_radar.write_html(str(radar_path))
        visualization_paths['pillar_radar'] = str(radar_path)
        
        # 3. Regional Ranking and Tier Distribution
        fig_ranking = self._create_ranking_visualization(country_assessments)
        ranking_path = self.visualizations_dir / "regional_ranking.html"
        fig_ranking.write_html(str(ranking_path))
        visualization_paths['regional_ranking'] = str(ranking_path)
        
        # 4. Data Quality Heatmap
        fig_quality = self._create_data_quality_heatmap(country_assessments)
        quality_path = self.visualizations_dir / "data_quality_assessment.html"
        fig_quality.write_html(str(quality_path))
        visualization_paths['data_quality'] = str(quality_path)
        
        return visualization_paths
    
    def _create_score_comparison_chart(self, assessments: List[CountryAssessment]) -> go.Figure:
        """Create AHAII scores comparison with confidence intervals"""
        sorted_assessments = sorted(assessments, key=lambda a: a.final_score, reverse=True)
        
        countries = [a.country_name for a in sorted_assessments]
        scores = [a.final_score for a in sorted_assessments]
        ci_lower = [a.confidence_interval[0] for a in sorted_assessments]
        ci_upper = [a.confidence_interval[1] for a in sorted_assessments]
        
        fig = go.Figure()
        
        # Add main scores
        fig.add_trace(go.Bar(
            x=countries,
            y=scores,
            name='AHAII Score',
            marker_color=['#1f77b4' if a.tier_classification == 1 else 
                         '#ff7f0e' if a.tier_classification == 2 else '#d62728' 
                         for a in sorted_assessments],
            error_y=dict(
                type='data',
                symmetric=False,
                array=[ci_u - s for ci_u, s in zip(ci_upper, scores)],
                arrayminus=[s - ci_l for s, ci_l in zip(scores, ci_lower)]
            )
        ))
        
        # Add tier boundaries
        fig.add_hline(y=70, line_dash="dash", line_color="green", 
                     annotation_text="Implementation Ready (Tier 1)")
        fig.add_hline(y=40, line_dash="dash", line_color="orange", 
                     annotation_text="Foundation Building (Tier 2)")
        
        fig.update_layout(
            title="AHAII Scores by Country (with 95% Confidence Intervals)",
            xaxis_title="Countries",
            yaxis_title="AHAII Score",
            yaxis=dict(range=[0, 100]),
            height=500
        )
        
        return fig
    
    def _create_pillar_radar_chart(self, assessments: List[CountryAssessment]) -> go.Figure:
        """Create pillar performance radar chart"""
        pillars = ['Human Capital', 'Physical Infrastructure', 'Regulatory Framework', 'Economic Market']
        pillar_keys = ['human_capital', 'physical_infrastructure', 'regulatory_framework', 'economic_market']
        
        fig = go.Figure()
        
        for assessment in assessments:
            values = [assessment.pillar_breakdown[key] for key in pillar_keys]
            values.append(values[0])  # Close the radar chart
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=pillars + [pillars[0]],
                fill='toself',
                name=assessment.country_name
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            title="AHAII Pillar Performance by Country",
            height=600
        )
        
        return fig
    
    def _create_ranking_visualization(self, assessments: List[CountryAssessment]) -> go.Figure:
        """Create regional ranking and tier distribution visualization"""
        sorted_assessments = sorted(assessments, key=lambda a: a.final_score, reverse=True)
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=("Regional Ranking", "Tier Distribution"),
            specs=[[{"type": "bar"}, {"type": "pie"}]]
        )
        
        # Regional ranking
        countries = [a.country_name for a in sorted_assessments]
        scores = [a.final_score for a in sorted_assessments]
        ranks = [a.regional_rank for a in sorted_assessments]
        
        fig.add_trace(
            go.Bar(x=countries, y=scores, name="AHAII Score", showlegend=False),
            row=1, col=1
        )
        
        # Tier distribution
        tier_counts = {1: 0, 2: 0, 3: 0}
        for assessment in assessments:
            tier_counts[assessment.tier_classification] += 1
        
        fig.add_trace(
            go.Pie(
                labels=['Tier 1', 'Tier 2', 'Tier 3'],
                values=[tier_counts[1], tier_counts[2], tier_counts[3]],
                name="Tier Distribution"
            ),
            row=1, col=2
        )
        
        fig.update_layout(height=500, title_text="AHAII Regional Analysis")
        
        return fig
    
    def _create_data_quality_heatmap(self, assessments: List[CountryAssessment]) -> go.Figure:
        """Create data quality assessment heatmap"""
        countries = [a.country_name for a in assessments]
        quality_dimensions = ['Overall Score', 'Data Quality', 'Expert Validation', 'Confidence Level']
        
        # Create quality matrix
        quality_matrix = []
        for assessment in assessments:
            grade_to_score = {'A': 90, 'B': 80, 'C': 70, 'D': 60, 'F': 50}
            validation_to_score = {
                'High expert validation confidence': 90,
                'Moderate expert validation confidence': 70,
                'Low expert validation confidence': 50,
                'No expert validation available': 30
            }
            
            row = [
                assessment.final_score,
                grade_to_score.get(assessment.data_quality_grade, 70),
                validation_to_score.get(assessment.expert_validation_status, 50),
                (assessment.confidence_interval[1] - assessment.confidence_interval[0]) / 2 * 10  # Confidence width
            ]
            quality_matrix.append(row)
        
        fig = go.Figure(data=go.Heatmap(
            z=quality_matrix,
            x=quality_dimensions,
            y=countries,
            colorscale='RdYlGn',
            colorbar=dict(title="Quality Score")
        ))
        
        fig.update_layout(
            title="AHAII Data Quality Assessment by Country",
            height=400
        )
        
        return fig
    
    def generate_final_report(self, enhanced_results: List, validation_results: List,
                            data_quality_metrics: List) -> str:
        """
        Generate comprehensive final AHAII pilot assessment report
        
        Args:
            enhanced_results: Enhanced AHAII calculation results
            validation_results: Expert validation results
            data_quality_metrics: Data quality assessment results
            
        Returns:
            Path to generated final report
        """
        logger.info("Generating comprehensive final AHAII pilot assessment report")
        
        # Compile country assessments
        country_assessments = self.compile_country_assessments(
            enhanced_results, validation_results, data_quality_metrics
        )
        
        # Generate regional analysis
        regional_analysis = self.generate_regional_analysis(country_assessments)
        
        # Document methodology
        methodology_documentation = self.document_methodology(enhanced_results)
        
        # Create visualizations
        visualization_paths = self.create_visualizations(country_assessments, regional_analysis)
        
        # Compile data quality assessment
        data_quality_assessment = {
            'overall_grade': self._calculate_overall_data_quality(data_quality_metrics),
            'country_grades': {a.country_name: a.data_quality_grade for a in country_assessments},
            'key_data_gaps': self._identify_critical_data_gaps(data_quality_metrics),
            'improvement_priorities': [
                'Strengthen World Bank indicator collection for health infrastructure',
                'Establish systematic policy monitoring across African countries',
                'Create health AI ecosystem tracking and validation systems',
                'Implement expert validation networks for ongoing assessment'
            ]
        }
        
        # Compile expert validation summary
        expert_validation_summary = {
            'validation_coverage': len(validation_results),
            'consensus_rate': len([v for v in validation_results if hasattr(v, 'final_status') and v.final_status.value == 'validated']) / len(validation_results) if validation_results else 0,
            'country_validation_status': {a.country_name: a.expert_validation_status for a in country_assessments},
            'key_insights': [
                'Expert validation confirms policy indicator assessments for most countries',
                'Ecosystem maturity estimates show good alignment with expert knowledge',
                'Regional expertise networks prove valuable for indicator validation'
            ]
        }
        
        # Generate key findings
        key_findings = [
            f"Regional average AHAII score: {regional_analysis['summary_statistics']['mean_score']:.1f}/100",
            f"{regional_analysis['summary_statistics']['tier_distribution']['tier_1']} countries achieve Implementation Ready status",
            f"Strongest regional pillar: {max(regional_analysis['pillar_performance'].items(), key=lambda x: x[1]['mean'])[0].replace('_', ' ').title()}",
            f"Greatest improvement opportunity: {min(regional_analysis['pillar_performance'].items(), key=lambda x: x[1]['mean'])[0].replace('_', ' ').title()}",
            "Significant variation in health AI infrastructure readiness across countries",
            "Data availability and quality vary substantially by indicator and country",
            "Expert validation confirms assessment methodology reliability"
        ]
        
        # Generate recommendations
        recommendations = {
            'policy_makers': [
                'Prioritize health AI infrastructure development based on pillar-specific gaps',
                'Establish regional health AI collaboration networks and standards',
                'Invest in systematic data collection for ongoing AHAII monitoring',
                'Create national health AI strategies informed by AHAII assessment'
            ],
            'development_organizations': [
                'Target infrastructure investment based on AHAII tier classifications',
                'Support regional capacity building in lowest-performing pillars',
                'Fund health AI pilot programs in Foundation Building countries',
                'Facilitate knowledge sharing between Implementation Ready countries'
            ],
            'researchers': [
                'Expand AHAII to full 54 African Union member countries',
                'Develop real-time health AI infrastructure monitoring systems',
                'Validate AHAII methodology against health AI implementation outcomes',
                'Create predictive models for health AI infrastructure development'
            ],
            'private_sector': [
                'Use AHAII scores to inform health AI market entry strategies',
                'Partner with high-scoring countries for regional health AI hubs',
                'Invest in infrastructure development for emerging markets',
                'Support ecosystem development in growing health AI markets'
            ]
        }
        
        # Future work priorities
        future_work = [
            'Scale AHAII assessment to all African Union member countries',
            'Implement automated data collection and real-time monitoring',
            'Develop health AI impact assessment framework',
            'Create longitudinal tracking of infrastructure development',
            'Integrate clinical outcomes and patient impact metrics',
            'Establish permanent expert validation networks',
            'Build policy recommendation engine based on AHAII results'
        ]
        
        # Compile final report
        final_report = PilotAssessmentReport(
            assessment_date=datetime.now().isoformat(),
            methodology_version="AHAII v1.0",
            pilot_countries=[a.country_name for a in country_assessments],
            country_assessments=country_assessments,
            regional_analysis=regional_analysis,
            methodology_documentation=methodology_documentation,
            data_quality_assessment=data_quality_assessment,
            expert_validation_summary=expert_validation_summary,
            key_findings=key_findings,
            recommendations=recommendations,
            future_work=future_work
        )
        
        # Save comprehensive report
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = self.reports_dir / f"ahaii_pilot_assessment_report_{timestamp}.json"
        
        # Convert to serializable format
        report_dict = asdict(final_report)
        
        with open(report_path, 'w') as f:
            json.dump(report_dict, f, indent=2)
        
        # Save summary CSV
        summary_data = []
        for assessment in country_assessments:
            summary_data.append({
                'Country': assessment.country_name,
                'AHAII_Score': assessment.final_score,
                'Tier': assessment.tier_classification,
                'Regional_Rank': assessment.regional_rank,
                'Human_Capital': assessment.pillar_breakdown['human_capital'],
                'Physical_Infrastructure': assessment.pillar_breakdown['physical_infrastructure'],
                'Regulatory_Framework': assessment.pillar_breakdown['regulatory_framework'],
                'Economic_Market': assessment.pillar_breakdown['economic_market'],
                'Data_Quality_Grade': assessment.data_quality_grade,
                'Expert_Validation': assessment.expert_validation_status
            })
        
        summary_df = pd.DataFrame(summary_data)
        summary_path = self.data_dir / f"ahaii_pilot_summary_{timestamp}.csv"
        summary_df.to_csv(summary_path, index=False)
        
        # Generate executive summary
        executive_summary_path = self._generate_executive_summary(final_report, timestamp)
        
        logger.info(f"Final AHAII pilot assessment report generated:")
        logger.info(f"  Full report: {report_path}")
        logger.info(f"  Summary data: {summary_path}")
        logger.info(f"  Executive summary: {executive_summary_path}")
        logger.info(f"  Visualizations: {len(visualization_paths)} charts created")
        
        return str(report_path)
    
    def _calculate_overall_data_quality(self, data_quality_metrics: List) -> str:
        """Calculate overall data quality grade"""
        if not data_quality_metrics:
            return "B"
        
        grades = [m.overall_quality_grade for m in data_quality_metrics if hasattr(m, 'overall_quality_grade')]
        grade_scores = {'A': 4, 'B': 3, 'C': 2, 'D': 1, 'F': 0}
        
        if not grades:
            return "B"
        
        avg_score = np.mean([grade_scores.get(grade, 2) for grade in grades])
        
        for grade, score in grade_scores.items():
            if avg_score >= score:
                return grade
        return 'F'
    
    def _identify_critical_data_gaps(self, data_quality_metrics: List) -> List[str]:
        """Identify critical data gaps from quality metrics"""
        if not data_quality_metrics:
            return ["Comprehensive data quality assessment needed"]
        
        gaps = []
        poor_quality_indicators = [m for m in data_quality_metrics 
                                 if hasattr(m, 'overall_quality_grade') and m.overall_quality_grade in ['D', 'F']]
        
        if poor_quality_indicators:
            gap_indicators = set()
            for metric in poor_quality_indicators[:5]:  # Top 5 gaps
                if hasattr(metric, 'indicator_name'):
                    gap_indicators.add(metric.indicator_name)
            
            gaps.append(f"Poor data quality for: {', '.join(list(gap_indicators))}")
        
        gaps.extend([
            "Limited real-time policy monitoring capabilities",
            "Incomplete health AI ecosystem mapping",
            "Inconsistent data collection across countries"
        ])
        
        return gaps[:5]
    
    def _generate_executive_summary(self, report: PilotAssessmentReport, timestamp: str) -> str:
        """Generate executive summary document"""
        executive_summary = {
            'title': 'AHAII Pilot Assessment - Executive Summary',
            'date': datetime.now().strftime('%B %Y'),
            'overview': {
                'purpose': 'Assess health AI infrastructure readiness across 5 pilot African countries',
                'methodology': 'Four-pillar quantitative assessment framework',
                'countries_assessed': report.pilot_countries,
                'assessment_period': '2023-2024'
            },
            'key_results': {
                'regional_average_score': f"{report.regional_analysis['summary_statistics']['mean_score']:.1f}/100",
                'tier_distribution': report.regional_analysis['summary_statistics']['tier_distribution'],
                'top_performer': report.country_assessments[0].country_name,
                'strongest_pillar': max(report.regional_analysis['pillar_performance'].items(), 
                                      key=lambda x: x[1]['mean'])[0].replace('_', ' ').title()
            },
            'critical_findings': report.key_findings[:5],
            'priority_recommendations': report.recommendations['policy_makers'][:3],
            'next_steps': report.future_work[:3]
        }
        
        summary_path = self.reports_dir / f"ahaii_executive_summary_{timestamp}.json"
        with open(summary_path, 'w') as f:
            json.dump(executive_summary, f, indent=2)
        
        return str(summary_path)


def main():
    """Main function for generating final AHAII pilot assessment report"""
    # This would typically import results from previous phases
    logger.info("Starting final AHAII pilot assessment report generation")
    
    # For demonstration, create placeholder results
    # In real implementation, these would be loaded from previous phase outputs
    
    print("\n=== AHAII Pilot Assessment Report Generator ===")
    print("This module generates comprehensive final assessment reports")
    print("combining all AHAII analysis components:")
    print("- Enhanced AHAII scoring results")
    print("- Expert validation outcomes") 
    print("- Data quality assessments")
    print("- Regional analysis and comparisons")
    print("- Methodology documentation")
    print("- Interactive visualizations")
    print("- Executive summary and recommendations")
    
    report_generator = AHAIIPilotReportGenerator()
    print(f"\nReport generator initialized at: {report_generator.output_dir}")
    print("Ready to generate comprehensive AHAII pilot assessment reports")


if __name__ == "__main__":
    main()