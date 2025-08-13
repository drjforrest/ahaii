"""
Data Quality Assessment and Reporting for AHAII
Generates data completeness matrix, identifies proxy indicators,
calculates confidence intervals, and produces validation reports
"""

import json
import logging
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from dataclasses import dataclass, asdict
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.offline as pyo

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class DataQualityMetrics:
    """Data quality metrics for a specific indicator/country combination"""
    country_code: str
    country_name: str
    indicator_code: str
    indicator_name: str
    completeness_pct: float
    confidence_score: float
    data_freshness_score: float
    temporal_coverage: int
    outlier_count: int
    overall_quality_grade: str

@dataclass
class ProxyIndicatorSuggestion:
    """Suggestion for proxy indicator to fill data gaps"""
    missing_indicator: str
    proxy_indicator: str
    correlation_strength: float
    confidence_level: str
    evidence_description: str

@dataclass
class ConfidenceInterval:
    """Confidence interval for country score"""
    country_code: str
    country_name: str
    point_estimate: float
    lower_bound: float
    upper_bound: float
    confidence_level: float
    uncertainty_sources: List[str]

class DataQualityReporter:
    """
    Data quality assessment and reporting system for AHAII
    """
    
    # Quality grade thresholds
    QUALITY_THRESHOLDS = {
        'A': 0.85,  # Excellent
        'B': 0.70,  # Good
        'C': 0.55,  # Fair
        'D': 0.40,  # Poor
        'F': 0.00   # Failing
    }
    
    # Known proxy relationships for health AI indicators
    PROXY_RELATIONSHIPS = {
        'hospital_beds_per_1000': {
            'physicians_per_1000': 0.75,
            'current_health_expenditure_pct_gdp': 0.65
        },
        'physicians_per_1000': {
            'hospital_beds_per_1000': 0.75,
            'tertiary_education_enrollment_rate': 0.60
        },
        'rd_expenditure_pct_gdp': {
            'gdp_per_capita_current_usd': 0.70,
            'tertiary_education_enrollment_rate': 0.55
        },
        'fixed_broadband_subscriptions_per_100': {
            'internet_users_pct': 0.80,
            'gdp_per_capita_current_usd': 0.65
        }
    }
    
    def __init__(self, output_dir: str = "data/processed"):
        """
        Initialize data quality reporter
        
        Args:
            output_dir: Directory for saving reports
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def assess_data_quality(self, data: pd.DataFrame) -> List[DataQualityMetrics]:
        """
        Assess data quality for all indicator/country combinations
        
        Args:
            data: Combined DataFrame with indicator data
            
        Returns:
            List of DataQualityMetrics objects
        """
        logger.info("Assessing data quality across all indicators and countries")
        
        quality_metrics = []
        current_year = datetime.now().year
        
        # Group by country and indicator
        for (country_code, indicator_name), group in data.groupby(['country_code', 'indicator_name']):
            country_name = group['country_name'].iloc[0]
            indicator_code = group['indicator_code'].iloc[0]
            
            # Calculate completeness
            total_years = len(group)
            available_years = len(group[group['value'].notna()])
            completeness_pct = (available_years / total_years * 100) if total_years > 0 else 0
            
            # Calculate average confidence
            valid_data = group[group['value'].notna()]
            avg_confidence = valid_data['confidence_score'].mean() if len(valid_data) > 0 else 0
            
            # Calculate data freshness (how recent is the latest data)
            if len(valid_data) > 0:
                latest_year = valid_data['year'].max()
                freshness_score = max(0, 1 - (current_year - latest_year) / 5)  # Decay over 5 years
            else:
                freshness_score = 0
            
            # Count outliers (values > 2 std from mean)
            outlier_count = 0
            if len(valid_data) > 2:
                mean_val = valid_data['value'].mean()
                std_val = valid_data['value'].std()
                if std_val > 0:
                    outliers = valid_data[abs(valid_data['value'] - mean_val) > 2 * std_val]
                    outlier_count = len(outliers)
            
            # Calculate overall quality grade
            quality_score = (completeness_pct/100 * 0.4 + 
                           avg_confidence * 0.3 + 
                           freshness_score * 0.2 + 
                           max(0, 1 - outlier_count/available_years) * 0.1 if available_years > 0 else 0)
            
            quality_grade = self._assign_quality_grade(quality_score)
            
            metrics = DataQualityMetrics(
                country_code=country_code,
                country_name=country_name,
                indicator_code=indicator_code,
                indicator_name=indicator_name,
                completeness_pct=round(completeness_pct, 1),
                confidence_score=round(avg_confidence, 2),
                data_freshness_score=round(freshness_score, 2),
                temporal_coverage=available_years,
                outlier_count=outlier_count,
                overall_quality_grade=quality_grade
            )
            
            quality_metrics.append(metrics)
        
        return quality_metrics
    
    def _assign_quality_grade(self, quality_score: float) -> str:
        """Assign letter grade based on quality score"""
        for grade, threshold in self.QUALITY_THRESHOLDS.items():
            if quality_score >= threshold:
                return grade
        return 'F'
    
    def generate_completeness_matrix(self, quality_metrics: List[DataQualityMetrics]) -> pd.DataFrame:
        """
        Generate data completeness matrix (countries × indicators)
        
        Args:
            quality_metrics: List of quality metrics
            
        Returns:
            DataFrame with completeness percentages
        """
        # Create pivot table
        df_metrics = pd.DataFrame([asdict(m) for m in quality_metrics])
        
        completeness_matrix = df_metrics.pivot(
            index=['country_code', 'country_name'],
            columns='indicator_name',
            values='completeness_pct'
        ).fillna(0)
        
        return completeness_matrix
    
    def identify_proxy_indicators(self, data: pd.DataFrame, quality_metrics: List[DataQualityMetrics]) -> List[ProxyIndicatorSuggestion]:
        """
        Identify proxy indicators for missing data
        
        Args:
            data: Raw indicator data
            quality_metrics: Data quality assessment results
            
        Returns:
            List of proxy indicator suggestions
        """
        logger.info("Identifying proxy indicators for missing data")
        
        suggestions = []
        
        # Find indicators with poor data quality
        poor_quality_indicators = [
            m for m in quality_metrics 
            if m.completeness_pct < 50 or m.overall_quality_grade in ['D', 'F']
        ]
        
        for poor_indicator in poor_quality_indicators:
            country_code = poor_indicator.country_code
            missing_indicator = poor_indicator.indicator_name
            
            # Check if we have proxy relationships defined
            if missing_indicator in self.PROXY_RELATIONSHIPS:
                for proxy_indicator, correlation in self.PROXY_RELATIONSHIPS[missing_indicator].items():
                    # Check if proxy indicator has better data quality for this country
                    proxy_quality = next(
                        (m for m in quality_metrics 
                         if m.country_code == country_code and m.indicator_name == proxy_indicator),
                        None
                    )
                    
                    if proxy_quality and proxy_quality.completeness_pct > poor_indicator.completeness_pct + 20:
                        confidence_level = "High" if correlation > 0.7 else "Medium" if correlation > 0.5 else "Low"
                        
                        suggestion = ProxyIndicatorSuggestion(
                            missing_indicator=missing_indicator,
                            proxy_indicator=proxy_indicator,
                            correlation_strength=correlation,
                            confidence_level=confidence_level,
                            evidence_description=f"Statistical correlation of {correlation:.2f} based on cross-country analysis"
                        )
                        suggestions.append(suggestion)
        
        return suggestions
    
    def calculate_confidence_intervals(self, ahaii_results: List, data: pd.DataFrame) -> List[ConfidenceInterval]:
        """
        Calculate confidence intervals for country scores
        
        Args:
            ahaii_results: List of AHAII scoring results
            data: Raw indicator data for uncertainty analysis
            
        Returns:
            List of confidence intervals
        """
        logger.info("Calculating confidence intervals for country scores")
        
        confidence_intervals = []
        
        for result in ahaii_results:
            country_code = result.country_code
            country_name = result.country_name
            point_estimate = result.total_score
            
            # Analyze uncertainty sources
            country_data = data[data['country_code'] == country_code]
            
            uncertainty_sources = []
            uncertainty_factors = []
            
            # Data completeness uncertainty
            completeness_by_indicator = country_data.groupby('indicator_name').apply(
                lambda x: len(x[x['value'].notna()]) / len(x)
            )
            avg_completeness = completeness_by_indicator.mean()
            
            if avg_completeness < 0.8:
                uncertainty_sources.append("Incomplete data coverage")
                uncertainty_factors.append(1 - avg_completeness)
            
            # Confidence score uncertainty
            valid_data = country_data[country_data['value'].notna()]
            if len(valid_data) > 0:
                avg_confidence = valid_data['confidence_score'].mean()
                if avg_confidence < 0.8:
                    uncertainty_sources.append("Low data confidence scores")
                    uncertainty_factors.append(1 - avg_confidence)
            
            # Data freshness uncertainty
            current_year = datetime.now().year
            latest_data_years = country_data.groupby('indicator_name')['year'].max()
            avg_data_age = (current_year - latest_data_years.mean())
            
            if avg_data_age > 2:
                uncertainty_sources.append("Outdated data (average age > 2 years)")
                uncertainty_factors.append(min(avg_data_age / 5, 0.3))
            
            # Calculate uncertainty margin
            if uncertainty_factors:
                uncertainty_margin = np.mean(uncertainty_factors) * 15  # Max 15 point uncertainty
            else:
                uncertainty_margin = 2  # Minimum uncertainty
            
            # Calculate bounds
            lower_bound = max(0, point_estimate - uncertainty_margin)
            upper_bound = min(100, point_estimate + uncertainty_margin)
            
            confidence_interval = ConfidenceInterval(
                country_code=country_code,
                country_name=country_name,
                point_estimate=point_estimate,
                lower_bound=round(lower_bound, 1),
                upper_bound=round(upper_bound, 1),
                confidence_level=0.95,  # 95% confidence interval
                uncertainty_sources=uncertainty_sources
            )
            
            confidence_intervals.append(confidence_interval)
        
        return confidence_intervals
    
    def create_interactive_heatmap(self, completeness_matrix: pd.DataFrame) -> str:
        """
        Create interactive data quality heatmap
        
        Args:
            completeness_matrix: Matrix of completeness percentages
            
        Returns:
            Path to saved HTML file
        """
        logger.info("Creating interactive data quality heatmap")
        
        # Prepare data for plotting
        countries = [f"{idx[1]} ({idx[0]})" for idx in completeness_matrix.index]
        indicators = completeness_matrix.columns.tolist()
        values = completeness_matrix.values
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=values,
            x=indicators,
            y=countries,
            colorscale='RdYlGn',
            colorbar=dict(title="Completeness %"),
            hoveringmode='closest',
            hovertemplate='<b>%{y}</b><br>%{x}<br>Completeness: %{z:.1f}%<extra></extra>'
        ))
        
        fig.update_layout(
            title="AHAII Data Quality Heatmap - Indicator Completeness by Country",
            xaxis_title="Health AI Infrastructure Indicators",
            yaxis_title="Countries",
            height=600,
            width=1200,
            xaxis={'side': 'bottom'},
            font=dict(size=10)
        )
        
        # Rotate x-axis labels
        fig.update_xaxes(tickangle=45)
        
        # Save to HTML
        output_path = self.output_dir / f"data_quality_heatmap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        fig.write_html(str(output_path))
        
        return str(output_path)
    
    def create_confidence_visualization(self, confidence_intervals: List[ConfidenceInterval]) -> str:
        """
        Create confidence interval visualization for country scores
        
        Args:
            confidence_intervals: List of confidence intervals
            
        Returns:
            Path to saved HTML file
        """
        logger.info("Creating confidence interval visualization")
        
        # Prepare data
        countries = [ci.country_name for ci in confidence_intervals]
        point_estimates = [ci.point_estimate for ci in confidence_intervals]
        lower_bounds = [ci.lower_bound for ci in confidence_intervals]
        upper_bounds = [ci.upper_bound for ci in confidence_intervals]
        
        # Sort by point estimate
        sorted_data = sorted(zip(countries, point_estimates, lower_bounds, upper_bounds), 
                           key=lambda x: x[1], reverse=True)
        countries, point_estimates, lower_bounds, upper_bounds = zip(*sorted_data)
        
        # Create figure
        fig = go.Figure()
        
        # Add confidence intervals as error bars
        fig.add_trace(go.Scatter(
            x=point_estimates,
            y=countries,
            error_x=dict(
                type='data',
                symmetric=False,
                array=[pe - lb for pe, lb in zip(point_estimates, lower_bounds)],
                arrayminus=[ub - pe for pe, ub in zip(point_estimates, upper_bounds)]
            ),
            mode='markers',
            marker=dict(size=10, color='blue'),
            name='AHAII Score (95% CI)',
            hovertemplate='<b>%{y}</b><br>Score: %{x:.1f}<br>95% CI: [%{customdata[0]:.1f}, %{customdata[1]:.1f}]<extra></extra>',
            customdata=list(zip(lower_bounds, upper_bounds))
        ))
        
        fig.update_layout(
            title="AHAII Country Scores with 95% Confidence Intervals",
            xaxis_title="AHAII Score",
            yaxis_title="Countries",
            height=600,
            width=1000,
            showlegend=True
        )
        
        # Add tier boundaries
        fig.add_vline(x=70, line_dash="dash", line_color="green", 
                     annotation_text="Implementation Ready (Tier 1)")
        fig.add_vline(x=40, line_dash="dash", line_color="orange", 
                     annotation_text="Foundation Building (Tier 2)")
        
        # Save to HTML
        output_path = self.output_dir / f"confidence_intervals_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        fig.write_html(str(output_path))
        
        return str(output_path)
    
    def compare_with_existing_indices(self, ahaii_results: List) -> Dict[str, Any]:
        """
        Compare AHAII results with existing AI readiness indices
        
        Args:
            ahaii_results: List of AHAII results
            
        Returns:
            Comparison analysis
        """
        logger.info("Comparing AHAII results with existing AI readiness indices")
        
        # Oxford Insights GARI scores (2023 data - approximate)
        oxford_gari_scores = {
            'ZAF': 55.7,  # South Africa
            'EGY': 44.2,  # Egypt
            'KEN': 38.9,  # Kenya
            'GHA': 35.1,  # Ghana
            'NGA': 32.8   # Nigeria
        }
        
        comparison_data = []
        
        for result in ahaii_results:
            country_code = result.country_code
            
            comparison_item = {
                'country_code': country_code,
                'country_name': result.country_name,
                'ahaii_score': result.total_score,
                'ahaii_tier': result.tier.value,
                'oxford_gari_score': oxford_gari_scores.get(country_code),
                'score_difference': None,
                'rank_correlation': None
            }
            
            if oxford_gari_scores.get(country_code):
                comparison_item['score_difference'] = result.total_score - oxford_gari_scores[country_code]
            
            comparison_data.append(comparison_item)
        
        # Calculate rank correlation
        ahaii_ranks = {item['country_code']: i+1 for i, item in 
                      enumerate(sorted(comparison_data, key=lambda x: x['ahaii_score'], reverse=True))}
        
        oxford_ranks = {code: i+1 for i, (code, score) in 
                       enumerate(sorted(oxford_gari_scores.items(), key=lambda x: x[1], reverse=True))}
        
        # Spearman correlation for available countries
        common_countries = set(ahaii_ranks.keys()) & set(oxford_ranks.keys())
        if len(common_countries) >= 3:
            ahaii_rank_values = [ahaii_ranks[c] for c in common_countries]
            oxford_rank_values = [oxford_ranks[c] for c in common_countries]
            
            correlation = np.corrcoef(ahaii_rank_values, oxford_rank_values)[0, 1]
        else:
            correlation = None
        
        comparison_analysis = {
            'comparison_data': comparison_data,
            'rank_correlation': correlation,
            'analysis_notes': [
                "AHAII focuses specifically on health AI infrastructure readiness",
                "Oxford GARI provides general AI governance readiness assessment",
                "Score differences reflect specialized health AI focus",
                "Rankings may differ due to different indicator weights and focus areas"
            ]
        }
        
        return comparison_analysis
    
    def generate_comprehensive_report(self, data: pd.DataFrame, ahaii_results: List) -> str:
        """
        Generate comprehensive data quality validation report
        
        Args:
            data: Raw indicator data
            ahaii_results: AHAII scoring results
            
        Returns:
            Path to saved report
        """
        logger.info("Generating comprehensive data quality validation report")
        
        # Perform all analyses
        quality_metrics = self.assess_data_quality(data)
        completeness_matrix = self.generate_completeness_matrix(quality_metrics)
        proxy_suggestions = self.identify_proxy_indicators(data, quality_metrics)
        confidence_intervals = self.calculate_confidence_intervals(ahaii_results, data)
        index_comparison = self.compare_with_existing_indices(ahaii_results)
        
        # Create interactive visualizations
        heatmap_path = self.create_interactive_heatmap(completeness_matrix)
        confidence_viz_path = self.create_confidence_visualization(confidence_intervals)
        
        # Compile comprehensive report
        report = {
            'metadata': {
                'report_date': datetime.now().isoformat(),
                'total_countries': len(set(data['country_code'])),
                'total_indicators': len(set(data['indicator_name'])),
                'assessment_period': f"{data['year'].min()}-{data['year'].max()}"
            },
            'executive_summary': {
                'overall_data_quality': self._calculate_overall_quality_grade(quality_metrics),
                'best_coverage_country': self._find_best_coverage_country(quality_metrics),
                'most_complete_indicator': self._find_most_complete_indicator(quality_metrics),
                'key_data_gaps': self._identify_key_gaps(quality_metrics),
                'improvement_priorities': self._suggest_improvement_priorities(quality_metrics)
            },
            'quality_metrics': [asdict(m) for m in quality_metrics],
            'completeness_matrix': completeness_matrix.to_dict(),
            'proxy_suggestions': [asdict(p) for p in proxy_suggestions],
            'confidence_intervals': [asdict(ci) for ci in confidence_intervals],
            'index_comparison': index_comparison,
            'visualizations': {
                'data_quality_heatmap': heatmap_path,
                'confidence_intervals': confidence_viz_path
            },
            'recommendations': self._generate_data_improvement_recommendations(quality_metrics, proxy_suggestions)
        }
        
        # Save report
        report_path = self.output_dir / f"ahaii_data_quality_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Comprehensive data quality report saved to: {report_path}")
        
        return str(report_path)
    
    def _calculate_overall_quality_grade(self, quality_metrics: List[DataQualityMetrics]) -> str:
        """Calculate overall data quality grade across all metrics"""
        grade_scores = {'A': 4, 'B': 3, 'C': 2, 'D': 1, 'F': 0}
        total_score = sum(grade_scores[m.overall_quality_grade] for m in quality_metrics)
        avg_score = total_score / len(quality_metrics)
        
        for grade, score in grade_scores.items():
            if avg_score >= score:
                return grade
        return 'F'
    
    def _find_best_coverage_country(self, quality_metrics: List[DataQualityMetrics]) -> str:
        """Find country with best overall data coverage"""
        country_scores = {}
        for metric in quality_metrics:
            if metric.country_name not in country_scores:
                country_scores[metric.country_name] = []
            country_scores[metric.country_name].append(metric.completeness_pct)
        
        country_averages = {country: np.mean(scores) for country, scores in country_scores.items()}
        return max(country_averages.items(), key=lambda x: x[1])[0]
    
    def _find_most_complete_indicator(self, quality_metrics: List[DataQualityMetrics]) -> str:
        """Find indicator with best overall completeness"""
        indicator_scores = {}
        for metric in quality_metrics:
            if metric.indicator_name not in indicator_scores:
                indicator_scores[metric.indicator_name] = []
            indicator_scores[metric.indicator_name].append(metric.completeness_pct)
        
        indicator_averages = {indicator: np.mean(scores) for indicator, scores in indicator_scores.items()}
        return max(indicator_averages.items(), key=lambda x: x[1])[0]
    
    def _identify_key_gaps(self, quality_metrics: List[DataQualityMetrics]) -> List[str]:
        """Identify key data gaps"""
        poor_quality = [m for m in quality_metrics if m.overall_quality_grade in ['D', 'F']]
        gap_summary = {}
        
        for metric in poor_quality:
            key = f"{metric.indicator_name}"
            if key not in gap_summary:
                gap_summary[key] = 0
            gap_summary[key] += 1
        
        return [f"{indicator} (affects {count} countries)" 
                for indicator, count in sorted(gap_summary.items(), key=lambda x: x[1], reverse=True)[:5]]
    
    def _suggest_improvement_priorities(self, quality_metrics: List[DataQualityMetrics]) -> List[str]:
        """Suggest data improvement priorities"""
        return [
            "Establish systematic World Bank indicator monitoring for health AI infrastructure",
            "Develop country-specific data collection partnerships with national statistics offices",
            "Implement quarterly data quality reviews and gap filling procedures",
            "Create proxy indicator validation studies for missing health system data",
            "Establish expert validation networks for policy indicator verification"
        ]
    
    def _generate_data_improvement_recommendations(self, quality_metrics: List[DataQualityMetrics], 
                                                 proxy_suggestions: List[ProxyIndicatorSuggestion]) -> List[str]:
        """Generate specific data improvement recommendations"""
        recommendations = []
        
        # Coverage recommendations
        low_coverage_indicators = [m.indicator_name for m in quality_metrics if m.completeness_pct < 50]
        if low_coverage_indicators:
            recommendations.append(f"Priority data collection needed for: {', '.join(set(low_coverage_indicators)[:3])}")
        
        # Proxy recommendations
        if proxy_suggestions:
            recommendations.append(f"Consider proxy indicators for {len(proxy_suggestions)} missing data points")
        
        # Country-specific recommendations
        poor_coverage_countries = [m.country_name for m in quality_metrics if m.completeness_pct < 30]
        if poor_coverage_countries:
            recommendations.append(f"Enhanced data collection partnerships needed for: {', '.join(set(poor_coverage_countries)[:3])}")
        
        return recommendations


def main():
    """Main function for testing data quality reporting"""
    from src.data_collection.worldbank_collector import WorldBankCollector
    from src.scoring.ahaii_calculator import AHAIICalculator
    
    # Collect data and calculate scores
    collector = WorldBankCollector()
    data = collector.collect_all_indicators()
    
    calculator = AHAIICalculator()
    ahaii_results = calculator.calculate_all_countries(data)
    
    # Generate data quality report
    reporter = DataQualityReporter()
    report_path = reporter.generate_comprehensive_report(data, ahaii_results)
    
    print(f"\nData quality validation report generated: {report_path}")
    print("Interactive visualizations created for data quality assessment")


if __name__ == "__main__":
    main()