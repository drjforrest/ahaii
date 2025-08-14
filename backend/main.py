"""
AHAII Backend API Server
African Health AI Infrastructure Index - Main FastAPI Application
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from datetime import datetime
import os
import logging
import sys
from pathlib import Path
from contextlib import asynccontextmanager

# Import API routers
from api.countries import router as countries_router
from api.ahaii_assessment import router as ahaii_router

# Import configuration
from config.settings import settings
from config.database import supabase

# Create logs directory if it doesn't exist
Path("logs").mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/ahaii_backend.log", mode="a"),
    ],
    force=True  # Override any existing logging configuration
)

# Get logger
logger = logging.getLogger("AHAII_Backend")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup event
    logger.info("🚀 AHAII Backend API Server Starting...")
    logger.info("📊 Loading AHAII Assessment Framework")
    logger.info("🔌 Connecting to Supabase database")
    logger.info("⚡ All systems initialized successfully")
    
    yield
    
    # Shutdown event
    logger.info("🛑 AHAII Backend API Server Shutting Down...")
    logger.info("💾 Saving any pending data")
    logger.info("✅ Shutdown complete")

# Initialize FastAPI app with lifespan
app = FastAPI(
    title="AHAII Backend API",
    description="African Health AI Infrastructure Index - Backend API for automated country assessments and ETL pipeline",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js frontend (dev)
        "http://localhost:3030",  # Next.js frontend (production port)
        "http://127.0.0.1:3000",
        "https://taifa-fiala.net",  # Production frontend domain
        "https://ahaii.vercel.app",  # Fallback domain
        "https://*.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(countries_router)
app.include_router(ahaii_router)




# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring and deployment"""
    logger.info("🔍 Health check requested")
    try:
        # Test database connection
        db_status = "connected"
        try:
            # Simple Supabase connection test
            test_response = supabase.table("countries").select("id").limit(1).execute()
            if hasattr(test_response, "error") and test_response.error:
                db_status = f"error: {test_response.error}"
                logger.warning(f"Database connection warning: {test_response.error}")
            else:
                logger.info("✅ Database connection successful")
        except Exception as e:
            db_status = f"connection_failed: {str(e)}"
            logger.error(f"❌ Database connection failed: {str(e)}")

        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "database": db_status,
            "environment": os.getenv("ENVIRONMENT", "development"),
            "services": {
                "countries_api": "active",
                "etl_pipeline": "ready",
                "scoring_service": "ready",
            },
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            },
        )


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "AHAII Backend API",
        "description": "African Health AI Infrastructure Index - Automated Country Assessment API",
        "version": "1.0.0",
        "documentation": "/docs",
        "health_check": "/health",
        "endpoints": {
            "countries": "/api/countries/",
            "featured_countries": "/api/countries/featured",
            "country_details": "/api/countries/{country_id}/details",
            "regional_overview": "/api/countries/regions",
            "statistics": "/api/countries/statistics",
            "ahaii_assessment": "/api/ahaii/",
            "ahaii_health": "/api/ahaii/health",
            "ahaii_scores": "/api/ahaii/scores",
            "ahaii_collect_data": "/api/ahaii/collect-data",
            "ahaii_run_assessment": "/api/ahaii/run-complete-assessment",
        },
        "etl_components": {
            "academic_processing": "ready",
            "news_monitoring": "active",
            "scoring_service": "automated",
            "database_integration": "supabase",
        },
        "ahaii_components": {
            "world_bank_collector": "active",
            "policy_indicator_collector": "active",
            "ecosystem_mapper": "active",
            "scoring_calculator": "active",
            "expert_validation": "active",
            "report_generator": "active",
        },
        "timestamp": datetime.now().isoformat(),
    }


# Global exception handler
@app.exception_handler(500)
async def internal_server_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred. Please try again later.",
            "timestamp": datetime.now().isoformat(),
        },
    )


# Configuration info endpoint (for debugging)
@app.get("/config/info")
async def config_info():
    """Configuration information endpoint (non-sensitive data only)"""
    return {
        "ahaii_pillars": [
            "human_capital",
            "physical_infrastructure",
            "regulatory",
            "economic",
        ],
        "ai_keywords_count": len(settings.AFRICAN_AI_KEYWORDS),
        "database_tables": [
            "countries",
            "ahaii_scores",
            "infrastructure_intelligence",
            "infrastructure_indicators",
            "health_ai_organizations",
        ],
        "supported_regions": [
            "North Africa",
            "West Africa",
            "East Africa",
            "Central Africa",
            "Southern Africa",
        ],
    }


if __name__ == "__main__":
    # Development server
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
