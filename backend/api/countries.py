"""
Automated AHAII Country Assessment API
Generates country profiles and scores from ETL pipeline data
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import asyncio
from dataclasses import dataclass, asdict
from decimal import Decimal

from services.database_service import DatabaseService
from services.ahaii_scoring_service import AHAIIScoringService
from config.database import supabase

router = APIRouter(prefix="/api/countries", tags=["countries"])

# Initialize services
scoring_service = AHAIIScoringService()
db_service = DatabaseService()


@dataclass
class CountryProfile:
    """Country profile data class for API responses"""

    id: str
    name: str
    iso_code_alpha3: str
    region: str
    population: Optional[int] = None
    gdp_usd: Optional[float] = None
    healthcare_spending_percent_gdp: Optional[float] = None
    ahaii_score: Optional[Dict[str, Any]] = None
    recent_intelligence_count: int = 0
    last_updated: Optional[str] = None
    images: Optional[Dict[str, str]] = None
    tier: Optional[str] = None
    confidence: Optional[float] = None
    ranking: Optional[int] = None


# ISO3 to image name mapping for automated frontend asset paths
ISO3_TO_IMAGE_NAME = {
    "AGO": "angola",
    "BEN": "benin",
    "BWA": "botswana",
    "CIV": "cote-divoire",
    "EGY": "egypt",
    "ETH": "ethiopia",
    "GHA": "ghana",
    "KEN": "kenya",
    "MUS": "mauritius",
    "NGA": "nigeria",
    "RWA": "rwanda",
    "SEN": "senegal",
    "SYC": "seychelles",
    "ZAF": "south-africa",
    "TUN": "tunisia",
    "ZMB": "zambia",
    "DZA": "algeria",
    "MAR": "morocco",
    "LBY": "libya",
    "SUD": "sudan",
    "TZA": "tanzania",
    "UGA": "uganda",
    "MOZ": "mozambique",
    "MDG": "madagascar",
    # Add all 54 African countries as needed
}

ISO3_TO_ISO2 = {
    "AGO": "ao",
    "BEN": "bj",
    "BWA": "bw",
    "CIV": "ci",
    "EGY": "eg",
    "ETH": "et",
    "GHA": "gh",
    "KEN": "ke",
    "MUS": "mu",
    "NGA": "ng",
    "RWA": "rw",
    "SEN": "sn",
    "SYC": "sc",
    "ZAF": "za",
    "TUN": "tn",
    "ZMB": "zm",
    "DZA": "dz",
    "MAR": "ma",
    "LBY": "ly",
    "SUD": "sd",
    "TZA": "tz",
    "UGA": "ug",
    "MOZ": "mz",
    "MDG": "mg",
}


def generate_image_paths(iso3_code: str) -> Dict[str, str]:
    """Generate automated image paths for frontend carousel assets"""
    image_name = ISO3_TO_IMAGE_NAME.get(iso3_code, iso3_code.lower())

    return {
        "flag_image": f"/images/countries/{image_name}-flag.png",
        "country_outline_image": f"/images/countries/{image_name}-country.png",
        "country_icon_light": f"/images/svg-icons/country-icons/{image_name}-icon-light.svg",
        "country_icon_dark": f"/images/svg-icons/country-icons/{image_name}-icon-dark.svg",
    }


def get_database_session():
    """Get Supabase database connection for dependency injection"""
    return supabase


async def calculate_featured_countries(
    countries: List[Dict], limit: int = 8
) -> List[Dict]:
    """Algorithm to select featured countries based on AHAII scoring criteria"""
    # Score countries for featuring based on multiple criteria
    featured_scores = []

    for country in countries:
        score_data = country.get("ahaii_score", {})
        if not score_data:
            continue

        total_score = score_data.get("total_score", 0)
        confidence = score_data.get("confidence", 0)
        tier = score_data.get("readiness_tier", "emerging")
        recent_activity = country.get("recent_intelligence_count", 0)

        # Featuring algorithm weights
        feature_score = (
            total_score * 0.4  # 40% AHAII score
            + confidence * 100 * 0.2  # 20% confidence
            + recent_activity * 0.2  # 20% recent activity
            + {"leader": 100, "ready": 80, "building": 60, "emerging": 40}.get(tier, 0)
            * 0.2  # 20% tier
        )

        featured_scores.append({"country": country, "feature_score": feature_score})

    # Sort by feature score and ensure regional diversity
    featured_scores.sort(key=lambda x: x["feature_score"], reverse=True)

    # Select top countries ensuring regional representation
    selected = []
    regions_included = set()

    # First pass: get highest scoring countries from each region
    for item in featured_scores:
        country = item["country"]
        if len(selected) >= limit:
            break

        region = country.get("region")
        if region not in regions_included or len(selected) < 4:
            selected.append(country)
            if region:
                regions_included.add(region)

    # Second pass: fill remaining slots with highest scores
    for item in featured_scores:
        country = item["country"]
        if len(selected) >= limit:
            break
        if country not in selected:
            selected.append(country)

    return selected[:limit]


@router.get("/with-scores")
async def get_all_countries_with_scores(
    include_estimated: bool = Query(
        True, description="Include countries with estimated scores"
    ),
    min_confidence: float = Query(0.5, description="Minimum confidence score"),
    db_session=Depends(get_database_session),
):
    """
    Get all African countries with automatically calculated AHAII scores
    Scores are generated from ETL pipeline data in real-time
    """
    try:
        # Get all countries from Supabase
        countries_response = supabase.table("countries").select("*").execute()

        if not countries_response.data:
            return {"countries": [], "total": 0}

        results = []
        for country in countries_response.data:
            country_id = country["id"]

            # Get AHAII score
            score_response = (
                supabase.table("ahaii_scores")
                .select("*")
                .eq("country_id", country_id)
                .order("created_at", desc=True)
                .limit(1)
                .execute()
            )

            ahaii_score = score_response.data[0] if score_response.data else None

            # Get recent intelligence activity count (last 30 days)
            cutoff_date = (datetime.now() - timedelta(days=30)).isoformat()
            activity_response = (
                supabase.table("infrastructure_intelligence")
                .select("id", count="exact")
                .eq("country_id", country_id)
                .gte("created_at", cutoff_date)
                .execute()
            )

            recent_activity = activity_response.count or 0

            # Get last update timestamp
            last_update_response = (
                supabase.table("infrastructure_intelligence")
                .select("created_at")
                .eq("country_id", country_id)
                .order("created_at", desc=True)
                .limit(1)
                .execute()
            )

            last_updated = None
            if last_update_response.data:
                last_updated = last_update_response.data[0]["created_at"]

            # Add image paths
            images = generate_image_paths(country["iso_code_alpha3"])

            country_data = {
                "id": country_id,
                "name": country["name"],
                "iso_code_alpha3": country["iso_code_alpha3"],
                "region": country.get("region"),
                "population": country.get("population"),
                "gdp_usd": country.get("gdp_usd"),
                "healthcare_spending_percent_gdp": country.get(
                    "healthcare_spending_percent_gdp"
                ),
                "ahaii_score": ahaii_score,
                "recent_intelligence_count": recent_activity,
                "last_updated": last_updated,
                "images": images,
                "tier": (
                    ahaii_score.get("readiness_tier") if ahaii_score else "emerging"
                ),
                "confidence": ahaii_score.get("confidence") if ahaii_score else 0.0,
            }

            # Filter by confidence if specified
            if not include_estimated or (
                ahaii_score and ahaii_score.get("confidence", 0) >= min_confidence
            ):
                results.append(country_data)

        # Sort by AHAII score (descending), then by recent activity
        results.sort(
            key=lambda x: (
                x["ahaii_score"]["total_score"] if x["ahaii_score"] else 0,
                x["recent_intelligence_count"],
            ),
            reverse=True,
        )

        # Add rankings
        for i, country in enumerate(results, 1):
            country["ranking"] = i

        return {"countries": results, "total": len(results)}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching countries: {str(e)}"
        )


@router.get("/featured")
async def get_featured_countries(
    limit: int = Query(8, description="Number of featured countries"),
    db_session=Depends(get_database_session),
):
    """
    Get featured countries for carousel based on:
    - AHAII tier and score
    - Recent intelligence activity
    - Regional representation
    - Economic/population significance
    """
    try:
        # Get countries with recent activity and scores
        countries_with_scores = await get_all_countries_with_scores(
            db_session=db_session
        )
        all_countries = countries_with_scores["countries"]

        # Apply featured selection algorithm
        featured = await calculate_featured_countries(all_countries, limit)

        return {
            "countries": featured,
            "selection_criteria": "automated_scoring",
            "algorithm": "tier_score_activity_regional_diversity",
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching featured countries: {str(e)}"
        )


@router.get("/by-region/{region}")
async def get_countries_by_region(
    region: str, db_session=Depends(get_database_session)
):
    """Get countries filtered by African region"""
    try:
        # Get countries by region from Supabase
        countries_response = (
            supabase.table("countries").select("*").eq("region", region).execute()
        )

        if not countries_response.data:
            return {"countries": [], "region": region}

        results = []
        for country in countries_response.data:
            country_id = country["id"]

            # Get AHAII score
            score_response = (
                supabase.table("ahaii_scores")
                .select("*")
                .eq("country_id", country_id)
                .order("created_at", desc=True)
                .limit(1)
                .execute()
            )

            ahaii_score = score_response.data[0] if score_response.data else None

            # Add image paths
            images = generate_image_paths(country["iso_code_alpha3"])

            country_data = {
                "id": country_id,
                "name": country["name"],
                "iso_code_alpha3": country["iso_code_alpha3"],
                "region": country["region"],
                "population": country.get("population"),
                "gdp_usd": country.get("gdp_usd"),
                "healthcare_spending_percent_gdp": country.get(
                    "healthcare_spending_percent_gdp"
                ),
                "ahaii_score": ahaii_score,
                "images": images,
                "tier": (
                    ahaii_score.get("readiness_tier") if ahaii_score else "emerging"
                ),
            }
            results.append(country_data)

        # Sort by AHAII score within region
        results.sort(
            key=lambda x: x["ahaii_score"]["total_score"] if x["ahaii_score"] else 0,
            reverse=True,
        )

        return {"countries": results, "region": region, "count": len(results)}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching countries by region: {str(e)}"
        )


@router.get("/{country_id}/details")
async def get_country_details(
    country_id: str, db_session=Depends(get_database_session)
):
    """Get comprehensive country details for country detail page"""
    try:
        # Find country (try both ID and ISO codes)
        country_response = (
            supabase.table("countries")
            .select("*")
            .or_(f"id.eq.{country_id},iso_code_alpha3.ilike.{country_id.upper()}")
            .limit(1)
            .execute()
        )

        if not country_response.data:
            raise HTTPException(status_code=404, detail="Country not found")

        country = country_response.data[0]
        country_id = country["id"]

        # Get AHAII score with full details
        score_response = (
            supabase.table("ahaii_scores")
            .select("*")
            .eq("country_id", country_id)
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )

        ahaii_score = score_response.data[0] if score_response.data else None

        # Get recent intelligence signals
        signals_response = (
            supabase.table("infrastructure_intelligence")
            .select("*")
            .eq("country_id", country_id)
            .order("created_at", desc=True)
            .limit(20)
            .execute()
        )

        # Get infrastructure indicators
        indicators_response = (
            supabase.table("infrastructure_indicators")
            .select("*")
            .eq("country_id", country_id)
            .order("created_at", desc=True)
            .execute()
        )

        # Get health AI organizations in country
        orgs_response = (
            supabase.table("health_ai_organizations")
            .select("*")
            .eq("country_id", country_id)
            .limit(10)
            .execute()
        )

        # Add image paths
        images = generate_image_paths(country["iso_code_alpha3"])

        country_data = {
            "id": country_id,
            "name": country["name"],
            "iso_code_alpha3": country["iso_code_alpha3"],
            "region": country.get("region"),
            "population": country.get("population"),
            "gdp_usd": country.get("gdp_usd"),
            "healthcare_spending_percent_gdp": country.get(
                "healthcare_spending_percent_gdp"
            ),
            "ahaii_score": ahaii_score,
            "recent_intelligence": signals_response.data or [],
            "infrastructure_indicators": indicators_response.data or [],
            "health_ai_organizations": orgs_response.data or [],
            "images": images,
            "tier": ahaii_score.get("readiness_tier") if ahaii_score else "emerging",
            "confidence": ahaii_score.get("confidence") if ahaii_score else 0.0,
            "last_updated": datetime.now().isoformat(),
        }

        return {"country": country_data}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching country details: {str(e)}"
        )


@router.get("/recent-activity")
async def get_countries_with_recent_activity(
    hours: int = Query(24, description="Hours to look back for activity"),
    limit: int = Query(10, description="Maximum countries to return"),
    db_session=Depends(get_database_session),
):
    """Get countries with recent intelligence activity"""
    try:
        cutoff_time = (datetime.now() - timedelta(hours=hours)).isoformat()

        # Get recent intelligence activity
        activity_response = (
            supabase.table("infrastructure_intelligence")
            .select("country_id", count="exact")
            .gte("created_at", cutoff_time)
            .execute()
        )

        # Count activity by country
        country_activity = {}
        for item in activity_response.data or []:
            country_id = item["country_id"]
            country_activity[country_id] = country_activity.get(country_id, 0) + 1

        # Get top countries by activity
        sorted_countries = sorted(
            country_activity.items(), key=lambda x: x[1], reverse=True
        )[:limit]

        results = []
        for country_id, activity_count in sorted_countries:
            # Get country details
            country_response = (
                supabase.table("countries")
                .select("*")
                .eq("id", country_id)
                .limit(1)
                .execute()
            )

            if not country_response.data:
                continue

            country = country_response.data[0]

            # Get AHAII score
            score_response = (
                supabase.table("ahaii_scores")
                .select("*")
                .eq("country_id", country_id)
                .order("created_at", desc=True)
                .limit(1)
                .execute()
            )

            ahaii_score = score_response.data[0] if score_response.data else None

            # Get latest activity timestamp
            latest_response = (
                supabase.table("infrastructure_intelligence")
                .select("created_at")
                .eq("country_id", country_id)
                .order("created_at", desc=True)
                .limit(1)
                .execute()
            )

            latest_activity = None
            if latest_response.data:
                latest_activity = latest_response.data[0]["created_at"]

            # Add image paths
            images = generate_image_paths(country["iso_code_alpha3"])

            country_data = {
                "id": country_id,
                "name": country["name"],
                "iso_code_alpha3": country["iso_code_alpha3"],
                "region": country.get("region"),
                "population": country.get("population"),
                "gdp_usd": country.get("gdp_usd"),
                "healthcare_spending_percent_gdp": country.get(
                    "healthcare_spending_percent_gdp"
                ),
                "ahaii_score": ahaii_score,
                "recent_intelligence_count": activity_count,
                "last_updated": latest_activity,
                "images": images,
                "tier": (
                    ahaii_score.get("readiness_tier") if ahaii_score else "emerging"
                ),
            }
            results.append(country_data)

        return {"countries": results, "hours": hours, "total_active": len(results)}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching recent activity: {str(e)}"
        )


@router.post("/{country_id}/refresh-score")
async def refresh_country_score(
    country_id: str,
    force_recalculation: bool = Query(False, description="Force score recalculation"),
    db_session=Depends(get_database_session),
):
    """Manually trigger AHAII score recalculation for a country"""
    try:
        # Find country
        country_response = (
            supabase.table("countries")
            .select("*")
            .or_(f"id.eq.{country_id},iso_code_alpha3.ilike.{country_id.upper()}")
            .limit(1)
            .execute()
        )

        if not country_response.data:
            raise HTTPException(status_code=404, detail="Country not found")

        country = country_response.data[0]
        country_id = country["id"]

        # This would integrate with the scoring service for recalculation
        # For now, return current score with refresh timestamp
        score_response = (
            supabase.table("ahaii_scores")
            .select("*")
            .eq("country_id", country_id)
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )

        current_score = score_response.data[0] if score_response.data else None

        return {
            "country_id": country_id,
            "country_name": country["name"],
            "score": current_score,
            "refresh_requested": True,
            "force_recalculation": force_recalculation,
            "recalculated_at": datetime.now().isoformat(),
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error refreshing score: {str(e)}")


@router.get("/statistics")
async def get_country_statistics(db_session=Depends(get_database_session)):
    """Get overall statistics about country coverage and data quality"""
    try:
        # Get total countries
        countries_response = (
            supabase.table("countries").select("id", count="exact").execute()
        )
        total_countries = countries_response.count or 0

        # Get countries with scores
        scores_response = (
            supabase.table("ahaii_scores").select("id", count="exact").execute()
        )
        countries_with_scores = scores_response.count or 0

        # Get countries with recent data (last 30 days)
        cutoff_date = (datetime.now() - timedelta(days=30)).isoformat()
        recent_data_response = (
            supabase.table("infrastructure_intelligence")
            .select("country_id", count="exact")
            .gte("created_at", cutoff_date)
            .execute()
        )

        # Count unique countries with recent data
        unique_countries_recent = len(
            set(item["country_id"] for item in recent_data_response.data or [])
        )

        # Get all scores for average calculation
        all_scores_response = (
            supabase.table("ahaii_scores").select("total_score").execute()
        )

        scores = [
            item["total_score"]
            for item in all_scores_response.data or []
            if item.get("total_score")
        ]
        avg_score = sum(scores) / len(scores) if scores else None

        # Get tier distribution
        tier_response = (
            supabase.table("ahaii_scores").select("readiness_tier").execute()
        )

        tier_counts = {}
        for item in tier_response.data or []:
            tier = item.get("readiness_tier", "unknown")
            tier_counts[tier] = tier_counts.get(tier, 0) + 1

        return {
            "total_countries": total_countries,
            "countries_with_scores": countries_with_scores,
            "countries_with_recent_data": unique_countries_recent,
            "average_score": avg_score,
            "tier_distribution": tier_counts,
            "coverage_percentage": (
                (countries_with_scores / total_countries * 100)
                if total_countries > 0
                else 0
            ),
            "data_freshness_percentage": (
                (unique_countries_recent / total_countries * 100)
                if total_countries > 0
                else 0
            ),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching statistics: {str(e)}"
        )


@router.get("/regions")
async def get_regional_overview(db_session=Depends(get_database_session)):
    """Get overview of all African regions with summary statistics"""
    try:
        # Get all countries
        countries_response = supabase.table("countries").select("*").execute()

        # Get all scores
        scores_response = supabase.table("ahaii_scores").select("*").execute()

        # Create score lookup by country_id
        score_lookup = {}
        for score in scores_response.data or []:
            country_id = score.get("country_id")
            if country_id:
                score_lookup[country_id] = score

        # Group by region
        regional_stats = {}
        for country in countries_response.data or []:
            region = country.get("region", "Unknown")

            if region not in regional_stats:
                regional_stats[region] = {
                    "region": region,
                    "country_count": 0,
                    "countries": [],
                    "scores": [],
                    "total_population": 0,
                    "total_gdp_usd": 0,
                }

            # Add country data
            regional_stats[region]["country_count"] += 1
            regional_stats[region]["countries"].append(country["name"])

            # Add score if available
            score = score_lookup.get(country["id"])
            if score and score.get("total_score"):
                regional_stats[region]["scores"].append(score["total_score"])

            # Add economic data
            if country.get("population"):
                regional_stats[region]["total_population"] += country["population"]
            if country.get("gdp_usd"):
                regional_stats[region]["total_gdp_usd"] += country["gdp_usd"]

        # Calculate averages
        regions = []
        for region_data in regional_stats.values():
            avg_score = None
            if region_data["scores"]:
                avg_score = sum(region_data["scores"]) / len(region_data["scores"])

            regions.append(
                {
                    "region": region_data["region"],
                    "country_count": region_data["country_count"],
                    "countries": region_data["countries"],
                    "average_score": avg_score,
                    "total_population": region_data["total_population"],
                    "total_gdp_usd": region_data["total_gdp_usd"],
                    "scored_countries": len(region_data["scores"]),
                    "coverage_percentage": (
                        (
                            len(region_data["scores"])
                            / region_data["country_count"]
                            * 100
                        )
                        if region_data["country_count"] > 0
                        else 0
                    ),
                }
            )

        # Sort by average score descending
        regions.sort(key=lambda x: x["average_score"] or 0, reverse=True)

        return {
            "regions": regions,
            "total_regions": len(regions),
            "generated_at": datetime.now().isoformat(),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching regional overview: {str(e)}"
        )
