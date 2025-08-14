#!/usr/bin/env python3
"""
AHAII ETL Orchestration System
Coordinates all data collection pipelines with scheduling, monitoring, and error handling
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum

from loguru import logger

# Import our ETL components
from .news.rss_monitor import monitor_rss_feeds
from .academic.unified_academic_processor import (
    UnifiedAcademicProcessor,
    HealthAIInfrastructureExtractor,
)
from services.database_service import DatabaseService
from services.ahaii_scoring_service import AHAIIScoringService
from services.vector_service import VectorService
from .snowball_sampler import HealthAISnowballSampler, SamplingConfig
from config.database import supabase


class PipelineStatus(Enum):
    """Pipeline execution status"""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class PipelineRun:
    """Represents a single ETL pipeline execution"""

    pipeline_name: str
    status: PipelineStatus
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    records_processed: int = 0
    records_created: int = 0
    records_updated: int = 0
    records_failed: int = 0
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class AHAIIETLOrchestrator:
    """Main ETL orchestrator for AHAII data pipelines"""

    def __init__(self):
        self.db_service = DatabaseService()
        self.scoring_service = AHAIIScoringService()
        self.vector_service = VectorService()
        self.infrastructure_extractor = HealthAIInfrastructureExtractor()

        # Initialize snowball sampler with conservative settings
        snowball_config = SamplingConfig(
            max_depth=3,
            max_citations_per_batch=15,
            delay_between_requests=5.0,
            government_domains_allowed={
                "who.int",
                "afro.who.int",
                "africa.who.int",
            },  # International only
        )
        self.snowball_sampler = HealthAISnowballSampler(snowball_config)

        # Pipeline configurations
        self.pipeline_configs = {
            "news_monitoring": {
                "enabled": True,
                "frequency_hours": 6,  # Run every 6 hours
                "max_runtime_minutes": 30,
                "retry_attempts": 3,
                "description": "Monitor health AI infrastructure news from RSS feeds",
            },
            "academic_processing": {
                "enabled": True,
                "frequency_hours": 24,  # Run daily
                "max_runtime_minutes": 120,
                "retry_attempts": 2,
                "description": "Process academic papers and extract infrastructure indicators",
            },
            "score_calculation": {
                "enabled": True,
                "frequency_hours": 12,  # Run twice daily
                "max_runtime_minutes": 60,
                "retry_attempts": 3,
                "description": "Calculate and update AHAII scores based on latest data",
            },
            "snowball_sampling": {
                "enabled": True,
                "frequency_hours": 8,  # Run every 8 hours
                "max_runtime_minutes": 45,
                "retry_attempts": 2,
                "description": "Discover new health AI resources through reference extraction",
            },
            "data_quality_check": {
                "enabled": True,
                "frequency_hours": 4,  # Run every 4 hours
                "max_runtime_minutes": 15,
                "retry_attempts": 1,
                "description": "Validate data quality and identify issues",
            },
        }

        # Execution tracking
        self.current_runs: Dict[str, PipelineRun] = {}
        self.run_history: List[PipelineRun] = []

    async def run_full_pipeline(self) -> Dict[str, PipelineRun]:
        """Execute the complete ETL pipeline with proper orchestration"""
        logger.info("🚀 Starting Complete AHAII ETL Pipeline...")

        results = {}

        # 1. News Monitoring Pipeline
        if self.pipeline_configs["news_monitoring"]["enabled"]:
            results["news_monitoring"] = await self.run_news_monitoring_pipeline()

        # 2. Academic Processing Pipeline
        if self.pipeline_configs["academic_processing"]["enabled"]:
            results["academic_processing"] = (
                await self.run_academic_processing_pipeline()
            )

        # 3. Score Calculation Pipeline
        if self.pipeline_configs["score_calculation"]["enabled"]:
            results["score_calculation"] = await self.run_scoring_pipeline()

        # 4. Snowball Sampling Pipeline
        if self.pipeline_configs.get("snowball_sampling", {}).get("enabled", True):
            results["snowball_sampling"] = await self.run_snowball_sampling_pipeline()

        # 5. Data Quality Check
        if self.pipeline_configs["data_quality_check"]["enabled"]:
            results["data_quality_check"] = await self.run_data_quality_pipeline()

        # Generate comprehensive report
        await self.generate_pipeline_report(results)

        logger.info("🎉 Complete AHAII ETL Pipeline Finished!")
        return results

    async def run_news_monitoring_pipeline(self) -> PipelineRun:
        """Execute news monitoring pipeline with error handling"""
        pipeline_name = "news_monitoring"
        run = PipelineRun(pipeline_name=pipeline_name, status=PipelineStatus.PENDING)
        run.started_at = datetime.now()

        self.current_runs[pipeline_name] = run

        try:
            logger.info("📰 Starting News Monitoring Pipeline...")
            run.status = PipelineStatus.RUNNING

            # Monitor RSS feeds for last 24 hours
            articles = await monitor_rss_feeds(hours_back=24)

            run.records_processed = len(articles)

            # Process and store articles
            stored_articles = []
            infrastructure_intelligence_records = []

            for article in articles:
                try:
                    # Store article as infrastructure intelligence
                    intelligence_data = {
                        "report_type": "news_monitoring",
                        "report_title": article.title,
                        "report_summary": (
                            article.summary or article.content[:500]
                            if article.content
                            else ""
                        ),
                        "key_findings": {
                            "health_ai_relevance_score": article.health_ai_relevance_score,
                            "african_relevance_score": article.african_relevance_score,
                            "infrastructure_pillar": article.infrastructure_pillar,
                            "mentioned_countries": article.mentioned_countries,
                            "infrastructure_indicators": article.infrastructure_indicators,
                            "health_organizations": article.mentioned_health_organizations,
                            "regulatory_signals": article.regulatory_signals,
                            "funding_mentions": article.funding_mentions,
                        },
                        "source_type": "news_article",
                        "source_url": str(article.url),
                        "source_publication": article.source,
                        "publication_date": article.published_date,
                        "affects_human_capital": article.infrastructure_pillar
                        == "human_capital",
                        "affects_physical_infrastructure": article.infrastructure_pillar
                        == "physical_infrastructure",
                        "affects_regulatory_framework": article.infrastructure_pillar
                        == "regulatory",
                        "affects_economic_market": article.infrastructure_pillar
                        == "economic",
                        "impact_significance": (
                            "high"
                            if article.health_ai_relevance_score > 0.7
                            else (
                                "medium"
                                if article.health_ai_relevance_score > 0.4
                                else "low"
                            )
                        ),
                        "confidence_score": max(
                            article.health_ai_relevance_score,
                            article.african_relevance_score,
                        ),
                        "verification_status": "auto_processed",
                    }

                    # Determine country association
                    if article.mentioned_countries:
                        for country_name in article.mentioned_countries:
                            # Look up country ID
                            country_result = (
                                await supabase.table("countries")
                                .select("id")
                                .ilike("name", f"%{country_name}%")
                                .execute()
                            )
                            if country_result.data:
                                intelligence_data["country_id"] = country_result.data[
                                    0
                                ]["id"]
                                break

                    stored_record = (
                        await self.db_service.insert_infrastructure_intelligence(
                            intelligence_data
                        )
                    )
                    if stored_record:
                        stored_articles.append(stored_record)
                        infrastructure_intelligence_records.append(stored_record)
                        run.records_created += 1
                    else:
                        run.records_failed += 1

                    # Extract and store infrastructure indicators
                    for indicator in article.infrastructure_indicators:
                        if article.mentioned_countries:
                            for country_name in article.mentioned_countries:
                                country_result = (
                                    await supabase.table("countries")
                                    .select("id")
                                    .ilike("name", f"%{country_name}%")
                                    .execute()
                                )
                                if country_result.data:
                                    indicator_data = {
                                        "country_id": country_result.data[0]["id"],
                                        "pillar": self._map_pillar_to_ahaii(
                                            article.infrastructure_pillar
                                        ),
                                        "indicator_name": indicator.get(
                                            "indicator_name", "news_signal"
                                        ),
                                        "indicator_value": indicator.get("value", 1.0),
                                        "indicator_unit": indicator.get(
                                            "value_type", "signal"
                                        ),
                                        "data_year": (
                                            article.published_date.year
                                            if article.published_date
                                            else datetime.now().year
                                        ),
                                        "data_source": article.source,
                                        "data_source_type": "news_media",
                                        "data_collection_method": "automated_rss_monitoring",
                                        "verification_status": "auto_extracted",
                                        "confidence_level": "medium",
                                        "confidence_score": indicator.get(
                                            "confidence", 0.6
                                        ),
                                        "validation_notes": f"Extracted from news article: {article.title}",
                                    }

                                    await self.db_service.insert_infrastructure_indicator(
                                        indicator_data
                                    )
                                    break

                except Exception as e:
                    logger.error(f"Error processing article {article.title}: {e}")
                    run.records_failed += 1
                    continue

            run.metadata = {
                "articles_monitored": len(articles),
                "intelligence_records_created": len(
                    infrastructure_intelligence_records
                ),
                "sources_processed": len(set(article.source for article in articles)),
                "countries_mentioned": len(
                    set(
                        country
                        for article in articles
                        for country in article.mentioned_countries
                    )
                ),
                "avg_health_ai_relevance": (
                    sum(article.health_ai_relevance_score for article in articles)
                    / len(articles)
                    if articles
                    else 0
                ),
                "avg_african_relevance": (
                    sum(article.african_relevance_score for article in articles)
                    / len(articles)
                    if articles
                    else 0
                ),
            }

            run.status = PipelineStatus.COMPLETED
            run.completed_at = datetime.now()

            logger.info(
                f"✅ News Monitoring Pipeline Completed: {run.records_created} records created, {run.records_failed} failed"
            )

        except Exception as e:
            run.status = PipelineStatus.FAILED
            run.error_message = str(e)
            run.completed_at = datetime.now()
            logger.error(f"❌ News Monitoring Pipeline Failed: {e}")

        self.run_history.append(run)
        return run

    async def run_academic_processing_pipeline(self) -> PipelineRun:
        """Execute academic processing pipeline"""
        pipeline_name = "academic_processing"
        run = PipelineRun(pipeline_name=pipeline_name, status=PipelineStatus.PENDING)
        run.started_at = datetime.now()

        self.current_runs[pipeline_name] = run

        try:
            logger.info("📚 Starting Academic Processing Pipeline...")
            run.status = PipelineStatus.RUNNING

            # Run unified academic processor
            processor = UnifiedAcademicProcessor()
            papers = await processor.collect_all_academic_data(
                max_results_per_source=100
            )

            run.records_processed = len(papers)

            # Process and store academic papers
            for paper in papers:
                try:
                    # Extract infrastructure indicators from paper
                    indicators = (
                        self.infrastructure_extractor.extract_infrastructure_indicators(
                            paper
                        )
                    )

                    # Store indicators in database
                    for indicator in indicators:
                        # Find associated country
                        country_id = None
                        if paper.get("african_entities"):
                            for entity in paper["african_entities"]:
                                country_result = (
                                    await supabase.table("countries")
                                    .select("id")
                                    .ilike("name", f"%{entity}%")
                                    .execute()
                                )
                                if country_result.data:
                                    country_id = country_result.data[0]["id"]
                                    break

                        if country_id:
                            indicator["country_id"] = country_id
                            indicator["data_year"] = paper.get(
                                "year", datetime.now().year
                            )

                            stored_indicator = (
                                await self.db_service.insert_infrastructure_indicator(
                                    indicator
                                )
                            )
                            if stored_indicator:
                                run.records_created += 1
                            else:
                                run.records_failed += 1

                    # Store paper as infrastructure intelligence
                    intelligence_data = {
                        "report_type": "academic_scan",
                        "country_id": country_id,
                        "report_title": paper["title"],
                        "report_summary": paper.get("abstract", "")[:500],
                        "key_findings": {
                            "african_relevance_score": paper.get(
                                "african_relevance_score", 0.0
                            ),
                            "ai_relevance_score": paper.get("ai_relevance_score", 0.0),
                            "african_entities": paper.get("african_entities", []),
                            "keywords": paper.get("keywords", []),
                            "citation_count": paper.get("citation_count", 0),
                            "infrastructure_indicators_count": len(indicators),
                        },
                        "source_type": "academic_paper",
                        "source_url": paper.get("url", ""),
                        "source_publication": paper.get("journal", ""),
                        "publication_date": paper.get("publication_date"),
                        "confidence_score": (
                            paper.get("african_relevance_score", 0)
                            + paper.get("ai_relevance_score", 0)
                        )
                        / 2,
                        "verification_status": (
                            "peer_reviewed"
                            if paper.get("source") in ["pubmed", "systematic_review"]
                            else "auto_processed"
                        ),
                    }

                    await self.db_service.insert_infrastructure_intelligence(
                        intelligence_data
                    )

                except Exception as e:
                    logger.error(
                        f"Error processing paper {paper.get('title', 'Unknown')}: {e}"
                    )
                    run.records_failed += 1
                    continue

            run.metadata = {
                "papers_processed": len(papers),
                "source_distribution": processor.source_statistics,
                "avg_african_relevance": (
                    sum(p.get("african_relevance_score", 0) for p in papers)
                    / len(papers)
                    if papers
                    else 0
                ),
                "avg_ai_relevance": (
                    sum(p.get("ai_relevance_score", 0) for p in papers) / len(papers)
                    if papers
                    else 0
                ),
            }

            run.status = PipelineStatus.COMPLETED
            run.completed_at = datetime.now()

            logger.info(
                f"✅ Academic Processing Pipeline Completed: {run.records_created} indicators created"
            )

        except Exception as e:
            run.status = PipelineStatus.FAILED
            run.error_message = str(e)
            run.completed_at = datetime.now()
            logger.error(f"❌ Academic Processing Pipeline Failed: {e}")

        self.run_history.append(run)
        return run

    async def run_scoring_pipeline(self) -> PipelineRun:
        """Execute AHAII scoring pipeline"""
        pipeline_name = "score_calculation"
        run = PipelineRun(pipeline_name=pipeline_name, status=PipelineStatus.PENDING)
        run.started_at = datetime.now()

        self.current_runs[pipeline_name] = run

        try:
            logger.info("🏆 Starting AHAII Scoring Pipeline...")
            run.status = PipelineStatus.RUNNING

            # Get all African countries
            countries_result = (
                await supabase.table("countries")
                .select("*")
                .eq("continent", "Africa")
                .execute()
            )
            countries = countries_result.data if countries_result.data else []

            run.records_processed = len(countries)

            for country in countries:
                try:
                    # Calculate AHAII scores for this country
                    scores = (
                        await self.scoring_service.calculate_comprehensive_ahaii_score(
                            country_id=country["id"],
                            assessment_year=datetime.now().year,
                            assessment_quarter=(datetime.now().month - 1) // 3 + 1,
                        )
                    )

                    if scores:
                        # Update scores in database
                        stored_scores = await self.db_service.update_ahaii_scores(
                            country["id"], scores
                        )
                        if stored_scores:
                            run.records_created += 1
                        else:
                            run.records_failed += 1
                    else:
                        run.records_failed += 1

                except Exception as e:
                    logger.error(
                        f"Error calculating scores for {country.get('name', 'Unknown')}: {e}"
                    )
                    run.records_failed += 1
                    continue

            run.metadata = {
                "countries_scored": run.records_created,
                "scoring_year": datetime.now().year,
                "scoring_quarter": (datetime.now().month - 1) // 3 + 1,
            }

            run.status = PipelineStatus.COMPLETED
            run.completed_at = datetime.now()

            logger.info(
                f"✅ Scoring Pipeline Completed: {run.records_created} countries scored"
            )

        except Exception as e:
            run.status = PipelineStatus.FAILED
            run.error_message = str(e)
            run.completed_at = datetime.now()
            logger.error(f"❌ Scoring Pipeline Failed: {e}")

        self.run_history.append(run)
        return run

    async def run_snowball_sampling_pipeline(self) -> PipelineRun:
        """Execute snowball sampling pipeline for reference discovery"""
        pipeline_name = "snowball_sampling"
        run = PipelineRun(pipeline_name=pipeline_name, status=PipelineStatus.PENDING)
        run.started_at = datetime.now()

        self.current_runs[pipeline_name] = run

        try:
            logger.info("🔬 Starting Snowball Sampling Pipeline...")
            run.status = PipelineStatus.RUNNING

            # Run snowball sampling session
            session_results = await self.snowball_sampler.run_sampling_session()

            # Update run statistics
            run.records_processed = session_results.get("citations_processed", 0)
            run.records_created = session_results.get("health_ai_discoveries", 0)
            run.records_failed = session_results.get("failed_extractions", 0)

            run.metadata = {
                "session_id": session_results.get("session_id"),
                "reference_links_extracted": session_results.get(
                    "reference_links_extracted", 0
                ),
                "government_docs_processed": session_results.get(
                    "government_docs_processed", 0
                ),
                "african_relevant_findings": session_results.get(
                    "african_relevant_findings", 0
                ),
                "depth_reached": session_results.get("depth_reached", 0),
                "average_quality": session_results.get("average_quality", 0.0),
                "pillar_distribution": session_results.get("pillar_distribution", {}),
                "discoveries_by_depth": session_results.get("discoveries_by_depth", {}),
            }

            run.status = PipelineStatus.COMPLETED
            run.completed_at = datetime.now()

            logger.info(
                f"✅ Snowball Sampling Pipeline Completed: {run.records_created} discoveries, {run.metadata['reference_links_extracted']} references"
            )

        except Exception as e:
            run.status = PipelineStatus.FAILED
            run.error_message = str(e)
            run.completed_at = datetime.now()
            logger.error(f"❌ Snowball Sampling Pipeline Failed: {e}")

        self.run_history.append(run)
        return run

    async def run_data_quality_pipeline(self) -> PipelineRun:
        """Execute data quality validation pipeline"""
        pipeline_name = "data_quality_check"
        run = PipelineRun(pipeline_name=pipeline_name, status=PipelineStatus.PENDING)
        run.started_at = datetime.now()

        self.current_runs[pipeline_name] = run

        try:
            logger.info("🔍 Starting Data Quality Pipeline...")
            run.status = PipelineStatus.RUNNING

            quality_checks = {
                "duplicate_intelligence_records": 0,
                "missing_country_associations": 0,
                "outdated_indicators": 0,
                "low_confidence_scores": 0,
                "unverified_records": 0,
            }

            # Check for duplicate intelligence records
            duplicates_result = await supabase.rpc(
                "check_duplicate_intelligence"
            ).execute()
            if duplicates_result.data:
                quality_checks["duplicate_intelligence_records"] = (
                    duplicates_result.data[0].get("count", 0)
                )

            # Check for missing country associations
            missing_country_result = (
                await supabase.table("infrastructure_intelligence")
                .select("id")
                .is_("country_id", "null")
                .execute()
            )
            if missing_country_result.data:
                quality_checks["missing_country_associations"] = len(
                    missing_country_result.data
                )

            # Check for outdated indicators (older than 2 years)
            cutoff_year = datetime.now().year - 2
            outdated_result = (
                await supabase.table("infrastructure_indicators")
                .select("id")
                .lt("data_year", cutoff_year)
                .execute()
            )
            if outdated_result.data:
                quality_checks["outdated_indicators"] = len(outdated_result.data)

            # Check for low confidence scores
            low_confidence_result = (
                await supabase.table("infrastructure_indicators")
                .select("id")
                .lt("confidence_score", 0.3)
                .execute()
            )
            if low_confidence_result.data:
                quality_checks["low_confidence_scores"] = len(
                    low_confidence_result.data
                )

            # Check for unverified records
            unverified_result = (
                await supabase.table("infrastructure_intelligence")
                .select("id")
                .eq("verification_status", "pending")
                .execute()
            )
            if unverified_result.data:
                quality_checks["unverified_records"] = len(unverified_result.data)

            run.records_processed = sum(quality_checks.values())
            run.metadata = {
                "quality_checks": quality_checks,
                "overall_quality_score": max(
                    0, 1.0 - (sum(quality_checks.values()) / 1000)
                ),  # Simple quality metric
            }

            run.status = PipelineStatus.COMPLETED
            run.completed_at = datetime.now()

            logger.info(
                f"✅ Data Quality Pipeline Completed: {run.records_processed} issues identified"
            )

        except Exception as e:
            run.status = PipelineStatus.FAILED
            run.error_message = str(e)
            run.completed_at = datetime.now()
            logger.error(f"❌ Data Quality Pipeline Failed: {e}")

        self.run_history.append(run)
        return run

    async def generate_pipeline_report(
        self, results: Dict[str, PipelineRun]
    ) -> Dict[str, Any]:
        """Generate comprehensive pipeline execution report"""
        report = {
            "execution_timestamp": datetime.now().isoformat(),
            "pipeline_results": {},
            "overall_summary": {
                "total_pipelines": len(results),
                "successful_pipelines": 0,
                "failed_pipelines": 0,
                "total_records_processed": 0,
                "total_records_created": 0,
                "total_records_failed": 0,
            },
            "data_statistics": await self.db_service.get_ahaii_statistics(),
            "recommendations": [],
        }

        for pipeline_name, run in results.items():
            report["pipeline_results"][pipeline_name] = {
                "status": run.status.value,
                "duration_seconds": (
                    (run.completed_at - run.started_at).total_seconds()
                    if run.completed_at and run.started_at
                    else 0
                ),
                "records_processed": run.records_processed,
                "records_created": run.records_created,
                "records_failed": run.records_failed,
                "error_message": run.error_message,
                "metadata": run.metadata,
            }

            # Update overall summary
            if run.status == PipelineStatus.COMPLETED:
                report["overall_summary"]["successful_pipelines"] += 1
            elif run.status == PipelineStatus.FAILED:
                report["overall_summary"]["failed_pipelines"] += 1

            report["overall_summary"][
                "total_records_processed"
            ] += run.records_processed
            report["overall_summary"]["total_records_created"] += run.records_created
            report["overall_summary"]["total_records_failed"] += run.records_failed

        # Generate recommendations
        if report["overall_summary"]["failed_pipelines"] > 0:
            report["recommendations"].append(
                "Review failed pipelines and implement error handling improvements"
            )

        if (
            report["overall_summary"]["total_records_failed"]
            > report["overall_summary"]["total_records_created"] * 0.1
        ):
            report["recommendations"].append(
                "High failure rate detected - review data validation logic"
            )

        logger.info("📊 Pipeline Execution Report Generated")
        logger.info(
            f"   Successful Pipelines: {report['overall_summary']['successful_pipelines']}/{report['overall_summary']['total_pipelines']}"
        )
        logger.info(
            f"   Records Created: {report['overall_summary']['total_records_created']}"
        )
        logger.info(
            f"   Records Failed: {report['overall_summary']['total_records_failed']}"
        )

        return report

    def _map_pillar_to_ahaii(self, pillar: Optional[str]) -> str:
        """Map infrastructure pillar to AHAII pillar naming"""
        mapping = {
            "human_capital": "human_capital",
            "physical_infrastructure": "physical_infrastructure",
            "regulatory": "regulatory_framework",
            "economic": "economic_market",
        }
        return mapping.get(pillar, "unknown")


async def run_etl_orchestrator():
    """Main entry point for ETL orchestration"""
    orchestrator = AHAIIETLOrchestrator()
    results = await orchestrator.run_full_pipeline()
    return results


if __name__ == "__main__":
    # Run the complete ETL pipeline
    results = asyncio.run(run_etl_orchestrator())
    print(f"\n🎉 ETL Pipeline Execution Complete!")
    print(
        f"Results: {json.dumps({k: v.status.value for k, v in results.items()}, indent=2)}"
    )
