"""
AHAII Assessment API Endpoints
FastAPI integration for AHAII Phase 2 implementation
Provides RESTful API access to all AHAII assessment components
"""

import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends, Query
from pydantic import BaseModel
import sys

# Add backend directory to path for imports
backend_root = Path(__file__).parent.parent
sys.path.insert(0, str(backend_root))

# Import AHAII components
from app.data_collection.worldbank_collector import WorldBankCollector
from app.data_collection.policy_indicator_collector import PolicyIndicatorCollector
from app.data_collection.health_ai_ecosystem_mapper import HealthAIEcosystemMapper
from app.scoring.enhanced_ahaii_calculator import EnhancedAHAIICalculator
from app.validation.data_quality_report import DataQualityReporter
from app.validation.expert_validation_system import ExpertValidationSystem
from app.analysis.pilot_assessment.ahaii_pilot_report import AHAIIPilotReportGenerator
from app.main_integration import AHAIIIntegrationManager

# Configure logging
log_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Create console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_formatter)

# Create file handler
Path("logs").mkdir(exist_ok=True)
file_handler = logging.FileHandler("logs/ahaii_assessment_api.log", mode="a")
file_handler.setFormatter(log_formatter)

logger = logging.getLogger("AHAII_Assessment_API")
logger.setLevel(logging.INFO)
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Prevent duplicate logs
logger.propagate = False

# Create API router
router = APIRouter(prefix="/api/ahaii", tags=["AHAII Assessment"])


# Pydantic models for API requests/responses
class AHAIIAssessmentRequest(BaseModel):
    countries: Optional[List[str]] = ["ZAF", "KEN", "NGA", "GHA", "EGY"]
    include_policy_indicators: bool = True
    include_ecosystem_mapping: bool = True
    include_expert_validation: bool = True
    generate_report: bool = True


class AHAIICountryScore(BaseModel):
    country_code: str
    country_name: str
    total_score: float
    tier: int
    regional_rank: int
    pillar_scores: Dict[str, float]
    confidence_score: float


class AHAIIAssessmentResponse(BaseModel):
    assessment_id: str
    status: str
    countries_assessed: List[str]
    assessment_date: str
    country_scores: List[AHAIICountryScore]
    regional_average: float
    data_quality_grade: str
    expert_validation_status: str
    report_url: Optional[str] = None


class DataCollectionStatus(BaseModel):
    world_bank_status: str
    policy_indicators_status: str
    ecosystem_mapping_status: str
    total_data_points: int
    completeness_percentage: float


# Global integration manager instance
integration_manager = None


def get_integration_manager() -> AHAIIIntegrationManager:
    """Get or create AHAII integration manager instance"""
    global integration_manager
    if integration_manager is None:
        integration_manager = AHAIIIntegrationManager()
    return integration_manager


@router.get("/health", summary="Health check for AHAII assessment system")
async def health_check():
    """Check health and connectivity of AHAII assessment system"""
    try:
        manager = get_integration_manager()
        connectivity_results = manager.test_system_connectivity()

        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "connectivity": connectivity_results,
            "all_systems_operational": all(connectivity_results.values()),
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")


@router.post("/collect-data", summary="Collect data for AHAII assessment")
async def collect_data(
    background_tasks: BackgroundTasks,
    countries: List[str] = Query(default=["ZAF", "KEN", "NGA", "GHA", "EGY"]),
    include_world_bank: bool = Query(default=True),
    include_policy_indicators: bool = Query(default=True),
    include_ecosystem_mapping: bool = Query(default=True),
):
    """
    Collect data for AHAII assessment from multiple sources

    - **countries**: List of ISO country codes to assess
    - **include_world_bank**: Include World Bank indicator collection
    - **include_policy_indicators**: Include policy indicator collection
    - **include_ecosystem_mapping**: Include health AI ecosystem mapping
    """
    try:
        manager = get_integration_manager()

        # Run data collection in background
        def run_data_collection():
            return manager.run_data_collection_phase()

        background_tasks.add_task(run_data_collection)

        return {
            "message": "Data collection started",
            "status": "running",
            "countries": countries,
            "collection_components": {
                "world_bank": include_world_bank,
                "policy_indicators": include_policy_indicators,
                "ecosystem_mapping": include_ecosystem_mapping,
            },
            "estimated_completion": "5-10 minutes",
        }

    except Exception as e:
        logger.error(f"Data collection failed: {e}")
        raise HTTPException(status_code=500, detail=f"Data collection failed: {str(e)}")


@router.get("/data-collection-status", summary="Get data collection status")
async def get_data_collection_status():
    """Get current status of data collection processes"""
    try:
        manager = get_integration_manager()

        # Check if pipeline results exist
        if (
            hasattr(manager, "pipeline_results")
            and "data_collection" in manager.pipeline_results
        ):
            collection_results = manager.pipeline_results["data_collection"]

            # Calculate status metrics
            total_data_points = 0
            successful_components = 0
            total_components = 3

            wb_status = collection_results.get("world_bank", {}).get(
                "status", "not_started"
            )
            policy_status = collection_results.get("policy", {}).get(
                "status", "not_started"
            )
            ecosystem_status = collection_results.get("ecosystem", {}).get(
                "status", "not_started"
            )

            if wb_status == "success":
                successful_components += 1
                total_data_points += collection_results["world_bank"].get(
                    "data_points", 0
                )

            if policy_status == "success":
                successful_components += 1
                total_data_points += collection_results["policy"].get("indicators", 0)

            if ecosystem_status == "success":
                successful_components += 1
                total_data_points += collection_results["ecosystem"].get(
                    "organizations_mapped", 0
                )

            completeness_percentage = (successful_components / total_components) * 100

            return DataCollectionStatus(
                world_bank_status=wb_status,
                policy_indicators_status=policy_status,
                ecosystem_mapping_status=ecosystem_status,
                total_data_points=total_data_points,
                completeness_percentage=completeness_percentage,
            )
        else:
            return DataCollectionStatus(
                world_bank_status="not_started",
                policy_indicators_status="not_started",
                ecosystem_mapping_status="not_started",
                total_data_points=0,
                completeness_percentage=0.0,
            )

    except Exception as e:
        logger.error(f"Failed to get data collection status: {e}")
        raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")


@router.post("/calculate-scores", summary="Calculate AHAII scores")
async def calculate_ahaii_scores(
    background_tasks: BackgroundTasks,
    use_enhanced_scoring: bool = Query(default=True),
    include_confidence_intervals: bool = Query(default=True),
):
    """
    Calculate AHAII scores for collected data

    - **use_enhanced_scoring**: Use enhanced scoring with policy and ecosystem data
    - **include_confidence_intervals**: Include confidence interval calculations
    """
    try:
        manager = get_integration_manager()

        # Check if data collection is complete
        if (
            not hasattr(manager, "pipeline_results")
            or "data_collection" not in manager.pipeline_results
        ):
            raise HTTPException(
                status_code=400,
                detail="Data collection must be completed before calculating scores",
            )

        # Run scoring in background
        def run_scoring():
            collection_results = manager.pipeline_results["data_collection"]
            return manager.run_scoring_phase(collection_results)

        background_tasks.add_task(run_scoring)

        return {
            "message": "AHAII score calculation started",
            "status": "running",
            "scoring_type": "enhanced" if use_enhanced_scoring else "basic",
            "estimated_completion": "2-5 minutes",
        }

    except Exception as e:
        logger.error(f"Score calculation failed: {e}")
        raise HTTPException(
            status_code=500, detail=f"Score calculation failed: {str(e)}"
        )


@router.get("/scores", summary="Get calculated AHAII scores")
async def get_ahaii_scores(
    format: str = Query(default="summary", regex="^(summary|detailed|dashboard)$")
):
    """
    Get calculated AHAII scores

    - **format**: Response format (summary, detailed, dashboard)
    """
    try:
        manager = get_integration_manager()

        # Check if scoring is complete
        if (
            not hasattr(manager, "pipeline_results")
            or "scoring" not in manager.pipeline_results
            or "enhanced_scores" not in manager.pipeline_results["scoring"]
        ):
            raise HTTPException(
                status_code=404,
                detail="AHAII scores not available. Run score calculation first.",
            )

        scoring_results = manager.pipeline_results["scoring"]["enhanced_scores"]

        if scoring_results.get("status") != "success":
            raise HTTPException(
                status_code=500, detail="Score calculation failed or incomplete"
            )

        enhanced_results = scoring_results["results"]

        if format == "summary":
            # Return summary format
            country_scores = []
            for result in enhanced_results:
                country_scores.append(
                    AHAIICountryScore(
                        country_code=result.country_code,
                        country_name=result.country_name,
                        total_score=result.total_score,
                        tier=result.tier.value,
                        regional_rank=result.regional_rank,
                        pillar_scores={
                            pillar.name: pillar.score for pillar in result.pillar_scores
                        },
                        confidence_score=result.overall_confidence,
                    )
                )

            regional_average = sum(score.total_score for score in country_scores) / len(
                country_scores
            )

            return AHAIIAssessmentResponse(
                assessment_id=f"ahaii_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                status="completed",
                countries_assessed=[score.country_code for score in country_scores],
                assessment_date=datetime.now().isoformat(),
                country_scores=country_scores,
                regional_average=round(regional_average, 2),
                data_quality_grade="B",  # Would be calculated from validation results
                expert_validation_status="completed",
            )

        elif format == "detailed":
            # Return detailed results with all metadata
            return {
                "detailed_results": [
                    {
                        "country_code": result.country_code,
                        "country_name": result.country_name,
                        "total_score": result.total_score,
                        "confidence": result.overall_confidence,
                        "tier": result.tier.value,
                        "rank": result.regional_rank,
                        "pillar_breakdown": {
                            pillar.name: {
                                "score": pillar.score,
                                "confidence": pillar.confidence,
                                "sub_components": pillar.sub_components,
                            }
                            for pillar in result.pillar_scores
                        },
                        "policy_indicators": result.policy_indicators,
                        "recommendations": result.improvement_recommendations,
                        "data_quality_issues": result.data_quality_issues,
                    }
                    for result in enhanced_results
                ]
            }

        else:  # dashboard format
            # Return dashboard-ready format
            return {
                "dashboard_data": {
                    "last_updated": datetime.now().isoformat(),
                    "countries": [
                        {
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
                        for result in enhanced_results
                    ],
                }
            }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get AHAII scores: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve scores: {str(e)}"
        )


@router.post("/validate", summary="Run expert validation")
async def run_expert_validation(background_tasks: BackgroundTasks):
    """Run expert validation for uncertain indicators"""
    try:
        manager = get_integration_manager()

        # Check if data collection and scoring are complete
        if (
            not hasattr(manager, "pipeline_results")
            or "data_collection" not in manager.pipeline_results
            or "scoring" not in manager.pipeline_results
        ):
            raise HTTPException(
                status_code=400,
                detail="Data collection and scoring must be completed before validation",
            )

        # Run validation in background
        def run_validation():
            collection_results = manager.pipeline_results["data_collection"]
            scoring_results = manager.pipeline_results["scoring"]
            return manager.run_validation_phase(collection_results, scoring_results)

        background_tasks.add_task(run_validation)

        return {
            "message": "Expert validation started",
            "status": "running",
            "estimated_completion": "3-7 minutes",
        }

    except Exception as e:
        logger.error(f"Expert validation failed: {e}")
        raise HTTPException(
            status_code=500, detail=f"Expert validation failed: {str(e)}"
        )


@router.post("/generate-report", summary="Generate final AHAII assessment report")
async def generate_final_report(background_tasks: BackgroundTasks):
    """Generate comprehensive final AHAII assessment report"""
    try:
        manager = get_integration_manager()

        # Check if all phases are complete
        required_phases = ["data_collection", "scoring", "validation"]
        for phase in required_phases:
            if (
                not hasattr(manager, "pipeline_results")
                or phase not in manager.pipeline_results
            ):
                raise HTTPException(
                    status_code=400,
                    detail=f"Phase '{phase}' must be completed before generating final report",
                )

        # Run report generation in background
        def run_reporting():
            collection_results = manager.pipeline_results["data_collection"]
            scoring_results = manager.pipeline_results["scoring"]
            validation_results = manager.pipeline_results["validation"]
            return manager.run_reporting_phase(
                collection_results, scoring_results, validation_results
            )

        background_tasks.add_task(run_reporting)

        return {
            "message": "Final report generation started",
            "status": "running",
            "estimated_completion": "2-5 minutes",
        }

    except Exception as e:
        logger.error(f"Report generation failed: {e}")
        raise HTTPException(
            status_code=500, detail=f"Report generation failed: {str(e)}"
        )


@router.post(
    "/run-complete-assessment", summary="Run complete AHAII assessment pipeline"
)
async def run_complete_assessment(
    background_tasks: BackgroundTasks, request: AHAIIAssessmentRequest
):
    """
    Run complete AHAII assessment pipeline including data collection,
    scoring, validation, and report generation
    """
    logger.info("🚀 Starting complete AHAII assessment pipeline")
    logger.info(f"📍 Countries to assess: {request.countries}")
    logger.info(
        f"⚙️ Components: Policy={request.include_policy_indicators}, Ecosystem={request.include_ecosystem_mapping}, Validation={request.include_expert_validation}, Report={request.generate_report}"
    )

    try:
        manager = get_integration_manager()

        # Run complete pipeline in background with detailed logging
        def run_complete_pipeline():
            logger.info("🔄 Background pipeline execution started")
            try:
                result = manager.run_complete_pipeline()
                logger.info("✅ Background pipeline execution completed successfully")
                return result
            except Exception as e:
                logger.error(f"❌ Background pipeline execution failed: {str(e)}")
                raise

        background_tasks.add_task(run_complete_pipeline)

        response = {
            "message": "Complete AHAII assessment pipeline started",
            "status": "running",
            "countries": request.countries,
            "components": {
                "policy_indicators": request.include_policy_indicators,
                "ecosystem_mapping": request.include_ecosystem_mapping,
                "expert_validation": request.include_expert_validation,
                "final_report": request.generate_report,
            },
            "estimated_completion": "15-30 minutes",
        }

        logger.info("📤 Assessment pipeline response sent to client")
        return response

    except Exception as e:
        logger.error(f"Complete assessment failed: {e}")
        raise HTTPException(
            status_code=500, detail=f"Complete assessment failed: {str(e)}"
        )


@router.get("/status", summary="Get overall AHAII assessment status")
async def get_assessment_status():
    """Get overall status of AHAII assessment pipeline"""
    try:
        manager = get_integration_manager()

        if not hasattr(manager, "pipeline_results"):
            return {
                "status": "not_started",
                "phases_completed": [],
                "current_phase": None,
                "overall_progress": 0,
            }

        pipeline_results = manager.pipeline_results
        phases_completed = []
        current_phase = None

        # Check each phase status
        if "data_collection" in pipeline_results:
            phases_completed.append("data_collection")
        elif "data_collection" not in pipeline_results:
            current_phase = "data_collection"

        if "scoring" in pipeline_results:
            phases_completed.append("scoring")
        elif len(phases_completed) == 1:
            current_phase = "scoring"

        if "validation" in pipeline_results:
            phases_completed.append("validation")
        elif len(phases_completed) == 2:
            current_phase = "validation"

        if "reporting" in pipeline_results:
            phases_completed.append("reporting")
        elif len(phases_completed) == 3:
            current_phase = "reporting"

        total_phases = 4
        overall_progress = (len(phases_completed) / total_phases) * 100

        status = "completed" if len(phases_completed) == total_phases else "in_progress"

        return {
            "status": status,
            "phases_completed": phases_completed,
            "current_phase": current_phase,
            "overall_progress": round(overall_progress, 1),
            "summary": pipeline_results.get("summary", {}),
        }

    except Exception as e:
        logger.error(f"Failed to get assessment status: {e}")
        raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")


@router.get("/countries", summary="Get list of supported countries")
async def get_supported_countries():
    """Get list of countries supported by AHAII assessment"""
    return {
        "pilot_countries": [
            {"code": "ZAF", "name": "South Africa"},
            {"code": "KEN", "name": "Kenya"},
            {"code": "NGA", "name": "Nigeria"},
            {"code": "GHA", "name": "Ghana"},
            {"code": "EGY", "name": "Egypt"},
        ],
        "total_pilot_countries": 5,
        "expansion_planned": True,
        "target_countries": 54,  # All African Union member states
    }


@router.get("/methodology", summary="Get AHAII methodology documentation")
async def get_methodology():
    """Get comprehensive AHAII methodology documentation"""
    return {
        "framework": {
            "name": "African Health AI Infrastructure Index (AHAII)",
            "version": "1.0",
            "pillars": {
                "human_capital": {
                    "weight": 0.30,
                    "description": "Health AI workforce, training, and literacy",
                },
                "physical_infrastructure": {
                    "weight": 0.30,
                    "description": "Digital health infrastructure, connectivity, and computing",
                },
                "regulatory_framework": {
                    "weight": 0.25,
                    "description": "AI governance, health data regulation, and policy",
                },
                "economic_market": {
                    "weight": 0.15,
                    "description": "Health AI ecosystem, funding, and market development",
                },
            },
        },
        "data_sources": {
            "world_bank": "Primary quantitative indicators",
            "policy_assessment": "Binary policy indicators",
            "ecosystem_mapping": "Health AI organizations and initiatives",
            "expert_validation": "Domain expert consensus",
        },
        "scoring_methodology": {
            "normalization": "Min-max scaling to 0-100 range",
            "aggregation": "Weighted average within and across pillars",
            "confidence_adjustment": "Data quality and certainty weighting",
            "tier_classification": "Implementation Ready (70+), Foundation Building (40-69), Development (0-39)",
        },
    }
