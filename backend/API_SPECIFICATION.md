# AHAII Backend API Specification for Frontend Integration

**Target**: Power the Country Carousel & Dashboard with real-time ETL data  
**Principle**: "Accept data, make pretty graphs" - Zero manual curation  
**Goal**: Automated scoring from ETL pipeline → Beautiful carousel visualization

## 🎯 Frontend Requirements Satisfied

Based on the frontend architecture analysis:
- ✅ **CountryCarousel.tsx** - 3D carousel using country flags/images
- ✅ **countryDataService.ts** - Data transformation layer 
- ✅ **country.ts** - Complete TypeScript contracts
- ✅ **Automated image mapping** - ISO codes → PNG/SVG assets
- ✅ **Real-time updates** - Intelligence activity integration

## 📊 Core API Endpoints

### 1. Countries with AHAII Scores
**Endpoint**: `GET /api/countries/with-scores`
**Purpose**: Power main carousel display
**Frontend Usage**: `countryDataService.getAllCountriesWithScores()`

```json
{
  "countries": [
    {
      "id": "zaf",
      "name": "South Africa", 
      "iso_code_alpha3": "ZAF",
      "iso_code_alpha2": "za",
      "region": "Southern Africa",
      "population": 60418738,
      "gdp_usd": 419015082264,
      "healthcare_spending_percent_gdp": 8.1,
      
      "ahaii_score": {
        "id": "ahaii-zaf-2025-q3",
        "country_id": "zaf", 
        "assessment_year": 2025,
        "assessment_quarter": 3,
        "total_score": 74.2,
        "global_ranking": 1,
        "regional_ranking": 1,
        "sub_regional_ranking": 1,
        
        "human_capital_score": 78.5,
        "human_capital_clinical_literacy": 82.1,
        "human_capital_informatics_capacity": 76.8,
        "human_capital_workforce_pipeline": 73.2,
        
        "physical_infrastructure_score": 71.8,
        "physical_digitization_level": 75.4,
        "physical_computational_capacity": 68.9,
        "physical_connectivity_reliability": 71.1,
        
        "regulatory_infrastructure_score": 69.3,
        "regulatory_approval_pathways": 72.8,
        "regulatory_data_governance": 67.5,
        "regulatory_market_access": 67.6,
        
        "economic_market_score": 76.8,
        "economic_market_maturity": 79.2,
        "economic_financial_sustainability": 74.1,
        "economic_research_funding": 77.1,
        
        "readiness_tier": 1,
        "tier_justification": "Strong across all pillars with excellent human capital and economic foundations",
        
        "overall_confidence_score": 0.87,
        "data_completeness_percentage": 94.2,
        "peer_review_status": "expert_validated",
        
        "development_trajectory": "improving",
        "key_strengths": [
          "Advanced medical research universities",
          "Strong regulatory framework",
          "High healthcare spending",
          "Established digital health market"
        ],
        "priority_improvement_areas": [
          "Rural connectivity infrastructure",
          "Clinical AI training standardization"
        ],
        
        "created_at": "2025-08-11T22:15:00Z",
        "updated_at": "2025-08-11T23:45:00Z"
      },
      
      "recent_intelligence_count": 23,
      "last_updated": "2025-08-11T23:45:00Z"
    }
  ],
  "total_countries": 54,
  "last_etl_run": "2025-08-11T23:30:00Z",
  "data_freshness_hours": 0.25
}
```

### 2. Featured Countries for Carousel
**Endpoint**: `GET /api/countries/featured?limit=8`
**Purpose**: Smart selection for carousel rotation
**Frontend Usage**: `countryDataService.getFeaturedCountries(8)`

**Selection Algorithm (Automated)**:
- Tier 1 countries (highest AHAII scores)
- Countries with recent intelligence activity (last 48hrs)
- Regional representatives (ensure geographic diversity)
- Economic significance (GDP/population weight)

```json
{
  "countries": [
    // Same structure as above, but pre-selected featured countries
    // Returns 8 countries optimized for carousel display
  ],
  "selection_criteria": {
    "tier_1_countries": 3,
    "recent_activity_countries": 2, 
    "regional_diversity_countries": 2,
    "economic_significance_countries": 1
  },
  "auto_refresh_minutes": 15
}
```

### 3. Countries by Region
**Endpoint**: `GET /api/countries/by-region/{region}`
**Purpose**: Regional filtering for carousel
**Frontend Usage**: `countryDataService.getCountriesByRegion('Southern Africa')`

**Valid Regions**:
- "Northern Africa" 
- "Western Africa"
- "Eastern Africa"
- "Southern Africa"
- "Central Africa"

### 4. Country Details
**Endpoint**: `GET /api/countries/{country_id}/details`
**Purpose**: Full country profile for detail pages
**Frontend Usage**: `countryDataService.getCountryDetails('zaf')`

```json
{
  "country": {
    // Same structure as countries endpoint
    // Plus additional detailed fields:
    
    "intelligence_signals": [
      {
        "id": "sig-zaf-001",
        "country_id": "zaf",
        "report_type": "academic_scan",
        "report_title": "AI-Enhanced Clinical Decision Support System Deployed at Groote Schuur Hospital",
        "report_summary": "Major teaching hospital implements $2.5M AI system for clinical decision support, training 500+ medical staff",
        
        "affects_human_capital": true,
        "affects_physical_infrastructure": true, 
        "affects_regulatory_framework": false,
        "affects_economic_market": true,
        
        "impact_significance": "high",
        "confidence_score": 0.89,
        
        "source_url": "https://example.com/article",
        "publication_date": "2025-08-10T14:30:00Z",
        "created_at": "2025-08-11T08:15:00Z"
      }
    ],
    
    "pillar_breakdown": {
      "human_capital": {
        "score": 78.5,
        "indicators": [
          {
            "name": "Medical AI Training Programs", 
            "value": 12,
            "change_from_last_quarter": "+3",
            "data_source": "academic_scan"
          }
        ]
      }
      // ... other pillars
    }
  }
}
```

### 5. Countries with Recent Activity
**Endpoint**: `GET /api/countries/recent-activity?hours=24`
**Purpose**: Dynamic carousel updates based on intelligence
**Frontend Usage**: `countryDataService.getCountriesWithRecentActivity(24)`

```json
{
  "countries": [
    // Countries with intelligence signals in last N hours
  ],
  "activity_summary": {
    "academic_papers": 15,
    "news_articles": 8, 
    "policy_announcements": 3,
    "funding_announcements": 2
  },
  "last_activity_timestamp": "2025-08-11T23:45:00Z"
}
```

## 🔄 Real-Time Integration Points

### ETL Pipeline → API Integration
The backend services automatically:

1. **Academic Processor** → Updates country scores when new papers found
2. **News Monitor** → Triggers country intelligence_count updates  
3. **AHAII Scoring Service** → Recalculates scores every 4 hours
4. **Vector Service** → Powers similarity-based recommendations

### Database Tables Used
- `countries` → Basic country information
- `ahaii_scores` → Current scores and rankings
- `infrastructure_indicators` → Detailed metrics per pillar
- `infrastructure_intelligence` → News and academic signals
- `health_ai_organizations` → Referenced in country profiles

## 🎨 Image Asset Integration

The API provides image paths that map to your PNG/SVG assets:

```json
{
  "flag_image": "/images/countries/south-africa-flag.png",
  "country_outline_image": "/images/countries/south-africa-country.png", 
  "country_icon_light": "/images/svg-icons/country-icons/south-africa-icon-light.svg",
  "country_icon_dark": "/images/svg-icons/country-icons/south-africa-icon-dark.svg"
}
```

**Automated Mapping**: `iso3ToImageName()` function converts database ISO codes to your file naming convention.

## 🚀 Implementation Phases

### Phase 1: Core Carousel API (Immediate)
- [ ] Countries with scores endpoint
- [ ] Featured countries selection algorithm
- [ ] Basic country details
- [ ] Image path automation

### Phase 2: Real-Time Intelligence (Next)
- [ ] Recent activity endpoint  
- [ ] Intelligence signals integration
- [ ] Score update triggers
- [ ] Activity-based carousel refresh

### Phase 3: Advanced Analytics (Future)
- [ ] Trend analysis endpoints
- [ ] Comparative analysis
- [ ] Prediction models
- [ ] Advanced filtering

### Phase 4: Performance Optimization (Future)
- [ ] Response caching
- [ ] CDN integration for images
- [ ] Database query optimization
- [ ] Real-time WebSocket updates

## 🎯 Success Metrics

**Frontend Integration Success**:
- ✅ Carousel loads 8 featured countries automatically
- ✅ AHAII scores display with proper tier colors
- ✅ Country images load from automated paths
- ✅ Intelligence activity counts update in real-time
- ✅ Regional filtering works seamlessly
- ✅ Country detail navigation functions
- ✅ Zero manual country curation required

**Backend Performance Targets**:
- Countries endpoint: < 200ms response time
- Featured selection: < 500ms processing time  
- Real-time updates: < 5 minute data freshness
- Image assets: 100% automated path generation
- ETL integration: Scores update within 15 minutes of new data

This specification ensures perfect alignment between your ETL pipeline intelligence generation and the beautiful carousel visualization, maintaining the "accept data, make pretty graphs" principle while providing rich, automated insights for all 54 African countries.
