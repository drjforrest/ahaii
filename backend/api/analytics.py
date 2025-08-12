#!/usr/bin/env python3
"""
AHAII Analytics API Endpoints
API routes for dashboard analytics and metrics
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any, Optional
import asyncio

from services.analytics_service import (
    AHAIIAnalyticsService, 
    get_dashboard_analytics, 
    get_full_analytics
)
from services.database_service import DatabaseService

router = APIRouter()

# Cache for analytics data to avoid repeated expensive queries
_analytics_cache = {
    "summary": None,
    "full": None,
    "last_updated": None
}

CACHE_DURATION_MINUTES = 15  # Cache for 15 minutes


def _is_cache_expired() -> bool:
    """Check if analytics cache has expired"""
    if _analytics_cache["last_updated"] is None:
        return True
    
    from datetime import datetime, timedelta
    cache_age = datetime.now() - _analytics_cache["last_updated"]
    return cache_age > timedelta(minutes=CACHE_DURATION_MINUTES)


async def _refresh_cache():
    """Refresh the analytics cache in background"""
    global _analytics_cache
    
    try:
        service = AHAIIAnalyticsService()
        
        # Refresh both summary and full analytics
        summary = await service.get_dashboard_summary()
        full_metrics = await service.get_comprehensive_metrics()
        full_data = service.to_dict(full_metrics)
        
        _analytics_cache.update({
            "summary": summary,
            "full": full_data,
            "last_updated": datetime.now()
        })
        
    except Exception as e:
        # Log error but don't crash the cache refresh
        print(f"Cache refresh failed: {e}")


@router.get("/analytics/dashboard")
async def get_dashboard_summary(
    background_tasks: BackgroundTasks,
    force_refresh: bool = False
) -> Dict[str, Any]:
    """
    Get dashboard summary analytics - optimized for quick loading
    
    Returns headline stats, quality metrics, and top-level insights
    perfect for the main dashboard display.
    """
    
    # Use cache if available and not expired
    if not force_refresh and not _is_cache_expired() and _analytics_cache["summary"]:
        return _analytics_cache["summary"]
    
    try:
        # Refresh cache in background if expired
        if _is_cache_expired():
            background_tasks.add_task(_refresh_cache)
        
        # For immediate response, get fresh data if cache is empty
        if _analytics_cache["summary"] is None or force_refresh:
            summary = await get_dashboard_analytics()
            _analytics_cache["summary"] = summary
            from datetime import datetime
            _analytics_cache["last_updated"] = datetime.now()
            return summary
        
        return _analytics_cache["summary"]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get analytics: {str(e)}")


@router.get("/analytics/full")
async def get_comprehensive_analytics(
    background_tasks: BackgroundTasks,
    force_refresh: bool = False
) -> Dict[str, Any]:
    """
    Get comprehensive analytics - all available metrics
    
    Returns detailed breakdown of all system metrics, data sources,
    quality indicators, and temporal data.
    """
    
    # Use cache if available and not expired
    if not force_refresh and not _is_cache_expired() and _analytics_cache["full"]:
        return _analytics_cache["full"]
    
    try:
        # Refresh cache in background if expired  
        if _is_cache_expired():
            background_tasks.add_task(_refresh_cache)
        
        # For immediate response, get fresh data if cache is empty
        if _analytics_cache["full"] is None or force_refresh:
            full_data = await get_full_analytics()
            _analytics_cache["full"] = full_data
            from datetime import datetime
            _analytics_cache["last_updated"] = datetime.now()
            return full_data
        
        return _analytics_cache["full"]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get comprehensive analytics: {str(e)}")


@router.get("/analytics/time-series")
async def get_time_series(days: int = 30) -> Dict[str, Any]:
    """
    Get time-series data for charts and trend analysis
    
    Args:
        days: Number of days of historical data to return (default: 30)
    """
    
    if days < 1 or days > 365:
        raise HTTPException(status_code=400, detail="Days parameter must be between 1 and 365")
    
    try:
        service = AHAIIAnalyticsService()
        time_series = await service.get_time_series_data(days)
        return time_series
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get time series: {str(e)}")


@router.get("/analytics/domains")
async def get_domain_breakdown() -> Dict[str, Any]:
    """
    Get detailed breakdown of data sources by domain
    
    Returns domain distribution, source types, and collection metrics
    perfect for showing "Look how hard we're working!" stats
    """
    
    try:
        service = AHAIIAnalyticsService()
        metrics = await service.get_comprehensive_metrics()
        
        return {
            "domain_distribution": metrics.domain_distribution,
            "source_distribution": metrics.source_distribution,
            "total_domains": len(metrics.domain_distribution),
            "total_source_types": len(metrics.source_distribution),
            "government_docs_processed": metrics.government_docs_processed,
            "academic_papers": metrics.total_academic_papers,
            "news_articles": metrics.source_distribution.get("news_article", 0),
            "snowball_discoveries": metrics.snowball_discoveries
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get domain breakdown: {str(e)}")


@router.get("/analytics/quality")
async def get_quality_metrics() -> Dict[str, Any]:
    """
    Get data quality and verification metrics
    
    Shows verification status, confidence scores, and data reliability
    """
    
    try:
        service = AHAIIAnalyticsService()
        metrics = await service.get_comprehensive_metrics()
        
        total_records = metrics.total_infrastructure_intelligence
        
        return {
            "total_records": total_records,
            "verified_records": metrics.verified_records,
            "high_confidence_records": metrics.high_confidence_records,
            "peer_reviewed_sources": metrics.peer_reviewed_sources,
            "verification_rate": round((metrics.verified_records / total_records) * 100, 1) if total_records > 0 else 0,
            "high_confidence_rate": round((metrics.high_confidence_records / total_records) * 100, 1) if total_records > 0 else 0,
            "peer_reviewed_rate": round((metrics.peer_reviewed_sources / total_records) * 100, 1) if total_records > 0 else 0,
            "avg_african_relevance": round(metrics.african_relevance_avg * 100, 1),
            "avg_ai_relevance": round(metrics.ai_relevance_avg * 100, 1)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get quality metrics: {str(e)}")


@router.get("/analytics/activity")
async def get_activity_metrics() -> Dict[str, Any]:
    """
    Get recent activity and collection metrics
    
    Shows how actively the system is collecting and processing data
    """
    
    try:
        service = AHAIIAnalyticsService()
        metrics = await service.get_comprehensive_metrics()
        
        return {
            "records_last_24h": metrics.records_collected_last_24h,
            "records_last_7d": metrics.records_collected_last_7d,
            "records_last_30d": metrics.records_collected_last_30d,
            "avg_records_per_day": round(metrics.avg_records_per_day, 1),
            "days_operational": metrics.days_operational,
            "total_records": metrics.total_infrastructure_intelligence,
            "uptime_days": metrics.uptime_days,
            "successful_pipeline_runs": metrics.successful_pipeline_runs,
            "failed_pipeline_runs": metrics.failed_pipeline_runs,
            "success_rate": round((metrics.successful_pipeline_runs / (metrics.successful_pipeline_runs + metrics.failed_pipeline_runs)) * 100, 1) if (metrics.successful_pipeline_runs + metrics.failed_pipeline_runs) > 0 else 100
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get activity metrics: {str(e)}")


@router.get("/analytics/countries")
async def get_country_coverage() -> Dict[str, Any]:
    """
    Get country coverage and geographic distribution
    """
    
    try:
        service = AHAIIAnalyticsService()
        metrics = await service.get_comprehensive_metrics()
        
        return {
            "total_countries": metrics.total_countries,
            "countries_with_data": len(metrics.country_coverage),
            "coverage_rate": round((len(metrics.country_coverage) / metrics.total_countries) * 100, 1) if metrics.total_countries > 0 else 0,
            "country_distribution": metrics.country_coverage,
            "top_countries": dict(list(sorted(metrics.country_coverage.items(), key=lambda x: x[1], reverse=True))[:10]) if metrics.country_coverage else {}
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get country coverage: {str(e)}")


@router.post("/analytics/refresh")
async def refresh_analytics(background_tasks: BackgroundTasks) -> Dict[str, str]:
    """
    Manually trigger analytics cache refresh
    
    Useful for immediate updates after running ETL pipelines
    """
    
    try:
        background_tasks.add_task(_refresh_cache)
        return {"status": "refresh_triggered", "message": "Analytics cache refresh started in background"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to trigger refresh: {str(e)}")


@router.get("/analytics/health")
async def get_analytics_health() -> Dict[str, Any]:
    """
    Get analytics system health status
    """
    
    try:
        # Test database connection
        db_service = DatabaseService()
        countries = await db_service.get_countries()
        
        cache_status = "fresh" if not _is_cache_expired() and _analytics_cache["summary"] else "stale"
        
        return {
            "status": "healthy",
            "database_connection": "ok" if countries else "error",
            "cache_status": cache_status,
            "last_cache_update": _analytics_cache["last_updated"].isoformat() if _analytics_cache["last_updated"] else None,
            "cached_data_available": bool(_analytics_cache["summary"])
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "cache_status": "unknown",
            "database_connection": "error"
        }


# Add to main FastAPI app
def setup_analytics_routes(app):
    """Add analytics routes to FastAPI app"""
    app.include_router(router, prefix="/api", tags=["analytics"])
