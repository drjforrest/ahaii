"""
AHAII Database Service
Handles database operations for AHAII quantitative assessment data
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import json

from config.database import get_db, supabase
from models.ahaii_models import (
    AHAIIAssessment, AHAIICountryScore, AHAIIPillarScore, 
    AHAIIIndicatorValue, DataCollectionRun, ExpertValidationResult,
    AHAIIAssessmentRequest, AHAIIAssessmentResponse, AHAIICountryScoreResponse
)

logger = logging.getLogger(__name__)

class AHAIIDatabaseService:
    """Service for AHAII database operations"""
    
    def __init__(self):
        self.supabase = supabase
    
    # Assessment Management
    
    def create_assessment(self, countries: List[str], methodology_version: str = "1.0") -> str:
        """
        Create a new AHAII assessment record
        
        Args:
            countries: List of country codes to assess
            methodology_version: Version of AHAII methodology
            
        Returns:
            Assessment ID
        """
        assessment_id = f"ahaii_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        try:
            assessment_data = {
                "assessment_id": assessment_id,
                "methodology_version": methodology_version,
                "countries_assessed": countries,
                "total_countries": len(countries),
                "assessment_date": datetime.utcnow().isoformat()
            }
            
            result = self.supabase.table("ahaii_assessments").insert(assessment_data).execute()
            
            if result.data:
                logger.info(f"Created assessment {assessment_id} for {len(countries)} countries")
                return assessment_id
            else:
                raise Exception("Failed to create assessment record")
                
        except Exception as e:
            logger.error(f"Error creating assessment: {e}")
            raise
    
    def update_assessment_status(self, assessment_id: str, **status_updates) -> bool:
        """
        Update assessment status fields
        
        Args:
            assessment_id: Assessment ID
            **status_updates: Status fields to update
            
        Returns:
            Success status
        """
        try:
            result = self.supabase.table("ahaii_assessments").update(
                status_updates
            ).eq("assessment_id", assessment_id).execute()
            
            return len(result.data) > 0
            
        except Exception as e:
            logger.error(f"Error updating assessment status: {e}")
            return False
    
    def get_assessment(self, assessment_id: str) -> Optional[Dict]:
        """Get assessment by ID"""
        try:
            result = self.supabase.table("ahaii_assessments").select("*").eq(
                "assessment_id", assessment_id
            ).execute()
            
            return result.data[0] if result.data else None
            
        except Exception as e:
            logger.error(f"Error getting assessment: {e}")
            return None
    
    def get_latest_assessment(self) -> Optional[Dict]:
        """Get the most recent completed assessment"""
        try:
            result = self.supabase.table("ahaii_assessments").select("*").eq(
                "data_collection_status", "completed"
            ).eq(
                "scoring_status", "completed"
            ).order("assessment_date", desc=True).limit(1).execute()
            
            return result.data[0] if result.data else None
            
        except Exception as e:
            logger.error(f"Error getting latest assessment: {e}")
            return None
    
    # Country Scores
    
    def save_country_score(self, assessment_id: str, country_score_data: Dict) -> int:
        """
        Save country score data
        
        Args:
            assessment_id: Assessment ID
            country_score_data: Country score information
            
        Returns:
            Country score ID
        """
        try:
            score_data = {
                "assessment_id": assessment_id,
                **country_score_data,
                "calculation_date": datetime.utcnow().isoformat()
            }
            
            result = self.supabase.table("ahaii_country_scores").insert(score_data).execute()
            
            if result.data:
                country_score_id = result.data[0]["id"]
                logger.info(f"Saved country score for {country_score_data.get('country_name')}")
                return country_score_id
            else:
                raise Exception("Failed to save country score")
                
        except Exception as e:
            logger.error(f"Error saving country score: {e}")
            raise
    
    def get_country_scores(self, assessment_id: str) -> List[Dict]:
        """Get all country scores for an assessment"""
        try:
            result = self.supabase.table("ahaii_country_scores").select("*").eq(
                "assessment_id", assessment_id
            ).order("total_score", desc=True).execute()
            
            return result.data or []
            
        except Exception as e:
            logger.error(f"Error getting country scores: {e}")
            return []
    
    def get_country_score_history(self, country_code: str, limit: int = 10) -> List[Dict]:
        """Get score history for a specific country"""
        try:
            result = self.supabase.table("ahaii_country_scores").select(
                "*, ahaii_assessments(assessment_date, methodology_version)"
            ).eq("country_code", country_code).order(
                "calculation_date", desc=True
            ).limit(limit).execute()
            
            return result.data or []
            
        except Exception as e:
            logger.error(f"Error getting country score history: {e}")
            return []
    
    # Pillar Scores
    
    def save_pillar_scores(self, country_score_id: int, pillar_scores: List[Dict]) -> bool:
        """Save pillar scores for a country"""
        try:
            pillar_data = []
            for pillar_score in pillar_scores:
                pillar_data.append({
                    "country_score_id": country_score_id,
                    **pillar_score
                })
            
            result = self.supabase.table("ahaii_pillar_scores").insert(pillar_data).execute()
            
            return len(result.data) == len(pillar_scores)
            
        except Exception as e:
            logger.error(f"Error saving pillar scores: {e}")
            return False
    
    def get_pillar_scores(self, country_score_id: int) -> List[Dict]:
        """Get pillar scores for a country"""
        try:
            result = self.supabase.table("ahaii_pillar_scores").select("*").eq(
                "country_score_id", country_score_id
            ).execute()
            
            return result.data or []
            
        except Exception as e:
            logger.error(f"Error getting pillar scores: {e}")
            return []
    
    # Indicator Values
    
    def save_indicator_values(self, country_score_id: int, indicators: List[Dict]) -> bool:
        """Save indicator values for a country"""
        try:
            indicator_data = []
            for indicator in indicators:
                indicator_data.append({
                    "country_score_id": country_score_id,
                    **indicator
                })
            
            result = self.supabase.table("ahaii_indicator_values").insert(indicator_data).execute()
            
            return len(result.data) == len(indicators)
            
        except Exception as e:
            logger.error(f"Error saving indicator values: {e}")
            return False
    
    def get_indicator_values(self, country_score_id: int) -> List[Dict]:
        """Get indicator values for a country"""
        try:
            result = self.supabase.table("ahaii_indicator_values").select("*").eq(
                "country_score_id", country_score_id
            ).order("pillar_name", "indicator_name").execute()
            
            return result.data or []
            
        except Exception as e:
            logger.error(f"Error getting indicator values: {e}")
            return []
    
    def get_indicators_by_pillar(self, assessment_id: str, pillar_name: str) -> List[Dict]:
        """Get all indicators for a specific pillar across countries"""
        try:
            result = self.supabase.table("ahaii_indicator_values").select(
                "*, ahaii_country_scores(country_code, country_name)"
            ).eq("pillar_name", pillar_name).in_(
                "country_score_id", 
                self.supabase.table("ahaii_country_scores").select("id").eq(
                    "assessment_id", assessment_id
                )
            ).execute()
            
            return result.data or []
            
        except Exception as e:
            logger.error(f"Error getting indicators by pillar: {e}")
            return []
    
    # Data Collection Tracking
    
    def create_data_collection_run(self, assessment_id: str) -> str:
        """Create a new data collection run"""
        run_id = f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        try:
            run_data = {
                "assessment_id": assessment_id,
                "run_id": run_id,
                "start_time": datetime.utcnow().isoformat(),
                "status": "running"
            }
            
            result = self.supabase.table("data_collection_runs").insert(run_data).execute()
            
            if result.data:
                return run_id
            else:
                raise Exception("Failed to create data collection run")
                
        except Exception as e:
            logger.error(f"Error creating data collection run: {e}")
            raise
    
    def update_collection_run_status(self, run_id: str, **updates) -> bool:
        """Update data collection run status"""
        try:
            if "status" in updates and updates["status"] in ["completed", "failed"]:
                updates["end_time"] = datetime.utcnow().isoformat()
            
            result = self.supabase.table("data_collection_runs").update(
                updates
            ).eq("run_id", run_id).execute()
            
            return len(result.data) > 0
            
        except Exception as e:
            logger.error(f"Error updating collection run status: {e}")
            return False
    
    def get_collection_run_status(self, run_id: str) -> Optional[Dict]:
        """Get data collection run status"""
        try:
            result = self.supabase.table("data_collection_runs").select("*").eq(
                "run_id", run_id
            ).execute()
            
            return result.data[0] if result.data else None
            
        except Exception as e:
            logger.error(f"Error getting collection run status: {e}")
            return None
    
    # Expert Validation
    
    def save_validation_result(self, validation_data: Dict) -> bool:
        """Save expert validation result"""
        try:
            result = self.supabase.table("expert_validation_results").insert(
                validation_data
            ).execute()
            
            return len(result.data) > 0
            
        except Exception as e:
            logger.error(f"Error saving validation result: {e}")
            return False
    
    def get_validation_results(self, assessment_id: str) -> List[Dict]:
        """Get validation results for an assessment"""
        try:
            # Get country codes for this assessment
            country_result = self.supabase.table("ahaii_country_scores").select(
                "country_code"
            ).eq("assessment_id", assessment_id).execute()
            
            if not country_result.data:
                return []
            
            country_codes = [row["country_code"] for row in country_result.data]
            
            result = self.supabase.table("expert_validation_results").select("*").in_(
                "country_code", country_codes
            ).execute()
            
            return result.data or []
            
        except Exception as e:
            logger.error(f"Error getting validation results: {e}")
            return []
    
    # Analytics and Reporting
    
    def get_regional_rankings(self, assessment_id: str) -> List[Dict]:
        """Get regional rankings for an assessment"""
        try:
            result = self.supabase.table("ahaii_country_rankings").select("*").eq(
                "assessment_id", assessment_id
            ).execute()
            
            return result.data or []
            
        except Exception as e:
            logger.error(f"Error getting regional rankings: {e}")
            return []
    
    def get_pillar_performance_summary(self, assessment_id: str) -> Dict[str, Any]:
        """Get pillar performance summary across all countries"""
        try:
            # Get all pillar scores for this assessment
            result = self.supabase.table("ahaii_pillar_summary").select("*").eq(
                "assessment_id", assessment_id
            ).execute()
            
            if not result.data:
                return {}
            
            pillar_data = {}
            for row in result.data:
                pillar_name = row["pillar_name"]
                if pillar_name not in pillar_data:
                    pillar_data[pillar_name] = {
                        "scores": [],
                        "confidences": [],
                        "countries": []
                    }
                
                pillar_data[pillar_name]["scores"].append(row["score"])
                pillar_data[pillar_name]["confidences"].append(row["confidence"])
                pillar_data[pillar_name]["countries"].append({
                    "code": row["country_code"],
                    "name": row["country_name"],
                    "score": row["score"]
                })
            
            # Calculate summary statistics
            summary = {}
            for pillar_name, data in pillar_data.items():
                scores = data["scores"]
                summary[pillar_name] = {
                    "mean_score": sum(scores) / len(scores),
                    "min_score": min(scores),
                    "max_score": max(scores),
                    "country_count": len(scores),
                    "top_performer": max(data["countries"], key=lambda c: c["score"]),
                    "countries": data["countries"]
                }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error getting pillar performance summary: {e}")
            return {}
    
    def get_data_quality_summary(self, assessment_id: str) -> Dict[str, Any]:
        """Get data quality summary for an assessment"""
        try:
            result = self.supabase.table("ahaii_data_quality_summary").select("*").eq(
                "assessment_id", assessment_id
            ).execute()
            
            if not result.data:
                return {}
            
            total_indicators = sum(row["total_indicators"] or 0 for row in result.data)
            validated_indicators = sum(row["validated_indicators"] or 0 for row in result.data)
            proxy_indicators = sum(row["proxy_indicators"] or 0 for row in result.data)
            
            return {
                "total_indicators": total_indicators,
                "validated_indicators": validated_indicators,
                "proxy_indicators": proxy_indicators,
                "validation_rate": validated_indicators / total_indicators if total_indicators > 0 else 0,
                "proxy_rate": proxy_indicators / total_indicators if total_indicators > 0 else 0,
                "countries": result.data
            }
            
        except Exception as e:
            logger.error(f"Error getting data quality summary: {e}")
            return {}
    
    # Utility methods
    
    def health_check(self) -> Dict[str, Any]:
        """Check database connectivity and basic functionality"""
        try:
            # Test basic connection
            result = self.supabase.table("ahaii_assessments").select("id").limit(1).execute()
            
            # Count records in key tables
            assessments_count = len(self.supabase.table("ahaii_assessments").select("id").execute().data or [])
            scores_count = len(self.supabase.table("ahaii_country_scores").select("id").execute().data or [])
            
            return {
                "status": "healthy",
                "connection": "ok",
                "assessments_count": assessments_count,
                "country_scores_count": scores_count,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "connection": "failed",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    # Bulk operations for efficiency
    
    def save_complete_assessment_data(self, assessment_id: str, assessment_data: Dict) -> bool:
        """
        Save complete assessment data in a single transaction-like operation
        
        Args:
            assessment_id: Assessment ID
            assessment_data: Complete assessment data structure
            
        Returns:
            Success status
        """
        try:
            success_count = 0
            total_operations = 0
            
            # Save country scores and related data
            for country_data in assessment_data.get("countries", []):
                total_operations += 1
                
                # Save country score
                country_score_id = self.save_country_score(assessment_id, {
                    "country_code": country_data["country_code"],
                    "country_name": country_data["country_name"],
                    "total_score": country_data["total_score"],
                    "overall_confidence": country_data["overall_confidence"],
                    "tier_classification": country_data["tier_classification"],
                    "regional_rank": country_data.get("regional_rank"),
                    "confidence_interval_lower": country_data.get("confidence_interval", [None, None])[0],
                    "confidence_interval_upper": country_data.get("confidence_interval", [None, None])[1],
                    "data_quality_grade": country_data.get("data_quality_grade"),
                    "data_completeness_pct": country_data.get("data_completeness_pct"),
                    "expert_validation_status": country_data.get("expert_validation_status")
                })
                
                if country_score_id:
                    # Save pillar scores
                    if "pillar_scores" in country_data:
                        self.save_pillar_scores(country_score_id, country_data["pillar_scores"])
                    
                    # Save indicators
                    if "indicators" in country_data:
                        self.save_indicator_values(country_score_id, country_data["indicators"])
                    
                    success_count += 1
            
            # Update assessment status
            self.update_assessment_status(assessment_id,
                scoring_status="completed",
                regional_average_score=assessment_data.get("regional_average_score")
            )
            
            logger.info(f"Saved complete assessment data: {success_count}/{total_operations} countries")
            return success_count == total_operations
            
        except Exception as e:
            logger.error(f"Error saving complete assessment data: {e}")
            return False


# Global instance
ahaii_db = AHAIIDatabaseService()

def get_ahaii_db() -> AHAIIDatabaseService:
    """Get AHAII database service instance"""
    return ahaii_db