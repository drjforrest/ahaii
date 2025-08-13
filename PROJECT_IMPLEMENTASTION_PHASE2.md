# LLM Instructions: AHAII Quantitative Pilot Implementation

## Project Context
Build the African Health AI Infrastructure Index (AHAII) quantitative assessment system using real-world data. Transform the conceptual four-pillar framework into a working intelligence platform that generates concrete readiness scores for African countries.

## Phase 1: World Bank API Integration (Week 1)

### Task 1.1: World Bank Data Collection Pipeline
**File**: `src/data_collection/worldbank_collector.py`

Create automated data collection system:
```python
# Requirements:
# - Collect 12 priority World Bank indicators for 5 pilot countries
# - Handle missing data gracefully with confidence scoring
# - Store in PostgreSQL with data quality metadata
# - Implement caching to avoid API rate limits

KEY_INDICATORS = {
    'EG.ELC.ACCS.ZS': 'electricity_access_pct',
    'IT.CEL.SETS.P2': 'mobile_subscriptions_per_100', 
    'IT.NET.USER.ZS': 'internet_users_pct',
    'GB.XPD.RSDV.GD.ZS': 'rd_expenditure_pct_gdp',
    'SH.MED.BEDS.ZS': 'hospital_beds_per_1000',
    # ... add all 12 indicators
}

PILOT_COUNTRIES = ['ZAF', 'KEN', 'NGA', 'GHA', 'EGY']
```

**Success Criteria**: 
- Collect data for 12 indicators across 5 countries (2020-2023)
- Generate data completeness report showing % coverage per country
- Populate `infrastructure_indicators` table with confidence scores

### Task 1.2: AHAII Scoring Algorithm  
**File**: `src/scoring/ahaii_calculator.py`

Implement transparent scoring methodology:
```python
# Requirements:
# - Min-max normalization (0-100 scale) for each indicator
# - Weighted aggregation by pillar (Human Capital 30%, Physical 30%, Regulatory 25%, Economic 15%)
# - Confidence-weighted scoring (lower scores for missing/uncertain data)
# - Generate tier classifications (1=Implementation Ready, 2=Foundation Building, 3=Development)

class AHAIICalculator:
    def calculate_pillar_scores(self, country_data):
        # Implement pillar scoring with sub-component breakdown
        
    def generate_tier_classification(self, total_score, confidence):
        # Implement tier assignment with confidence thresholds
```

**Success Criteria**:
- Generate complete AHAII scores for all 5 pilot countries
- Produce ranking comparison with justification for positions
- Export results to dashboard-ready JSON format

### Task 1.3: Data Quality Dashboard
**File**: `src/validation/data_quality_report.py`

Build data quality assessment and reporting:
```python
# Requirements: 
# - Generate data completeness matrix (countries × indicators)
# - Identify proxy indicators for missing data
# - Calculate confidence intervals for each country's score
# - Produce validation report comparing to existing AI readiness indices
```

**Success Criteria**:
- Interactive data quality heatmap showing coverage gaps
- Confidence interval visualization for country scores  
- Comparison table with Oxford Insights GARI scores where available

## Phase 2: Supplementary Data Integration (Week 2)

### Task 2.1: Policy Indicator Collection
**File**: `src/data_collection/policy_indicator_collector.py`

Collect binary policy indicators through web scraping and expert validation:
```python
# Requirements:
# - Scrape Oxford Insights GARI data for regulatory scores
# - Build policy document detection for AI strategies/ethics guidelines
# - Implement expert validation workflow for uncertain indicators
# - Cross-reference with AU AI Strategy country assessments

POLICY_INDICATORS = {
    'national_ai_strategy': 'Binary indicator for AI strategy existence',
    'data_protection_regulation': 'Binary indicator for data governance',
    'ai_ethics_guidelines': 'Binary indicator for ethics framework'
}
```

**Success Criteria**:
- Complete policy indicator matrix for all 5 pilot countries
- Expert validation confidence scores for uncertain indicators
- Documentation of evidence sources for each binary determination

### Task 2.2: Enhanced Scoring Integration
**File**: `src/scoring/enhanced_ahaii_calculator.py`

Integrate supplementary data into scoring algorithm:
```python
# Requirements:
# - Add policy indicators to regulatory infrastructure pillar
# - Implement proxy indicator logic for missing health system data
# - Add regional benchmarking context (Sub-Saharan Africa averages)
# - Generate detailed score explanations and improvement recommendations
```

**Success Criteria**:
- Updated AHAII scores incorporating all available data
- Country-specific improvement recommendations by pillar
- Regional ranking context for each country

## Phase 3: Expert Validation & Primary Research (Week 3)

### Task 3.1: Health AI Ecosystem Mapping
**File**: `src/data_collection/health_ai_ecosystem_mapper.py`

Map health AI organizations and initiatives:
```python
# Requirements:
# - Scrape university websites for health AI/biomedical informatics programs
# - Collect health AI startup data from Crunchbase, AfricArena, local sources
# - Identify healthcare AI pilot programs through news analysis
# - Build confidence scoring for ecosystem maturity indicators
```

**Success Criteria**:
- Health AI organization database for all 5 pilot countries
- Quantified ecosystem maturity scores feeding into Economic pillar
- Evidence documentation for all identified organizations/programs

### Task 3.2: Expert Validation Framework
**File**: `src/validation/expert_validation_system.py`

Build expert validation and consensus system:
```python
# Requirements:
# - Create expert survey system for validating uncertain indicators  
# - Implement consensus scoring for policy indicators
# - Cross-validate AHAII scores against expert country knowledge
# - Generate validation confidence scores and uncertainty bounds
```

**Success Criteria**:
- Expert consensus scores for all binary policy indicators
- Validation report comparing AHAII results to expert expectations
- Refined scoring methodology based on expert feedback

### Task 3.3: Final AHAII Assessment Report
**File**: `analysis/pilot_assessment/ahaii_pilot_report.py`

Generate comprehensive pilot assessment:
```python
# Requirements:
# - Complete AHAII scores with confidence intervals for all 5 countries
# - Ranking justification and comparative analysis
# - Methodology transparency documentation
# - Identification of data gaps requiring ongoing monitoring
```

**Success Criteria**:
- Publication-ready AHAII pilot assessment report
- Interactive dashboard showing country scores and drill-down capability
- Research methodology documentation for academic validation

## Technical Requirements

### Database Schema
Use existing AHAII PostgreSQL schema (`ahaii_schema.sql`) with emphasis on:
- `infrastructure_indicators` table for all quantitative data
- `ahaii_scores` table for calculated results  
- `international_framework_alignment` for policy indicators

### API Integrations  
- World Bank API (primary data source)
- Oxford Insights GARI (where available)
- WHO eHealth survey data
- ITU Digital Skills Insights

### Output Formats
- PostgreSQL database updates
- JSON exports for dashboard integration
- CSV exports for analysis and validation
- Interactive HTML reports for stakeholder review

## Success Metrics

### Week 1 Targets
- 80%+ data coverage for World Bank indicators across pilot countries
- Complete AHAII score calculation pipeline
- Initial country rankings with confidence scores

### Week 2 Targets  
- Policy indicator collection for regulatory infrastructure pillar
- Enhanced scoring incorporating all available quantitative data
- Regional benchmarking context

### Week 3 Targets
- Expert-validated assessment for all uncertain indicators
- Complete AHAII assessment report ready for academic review
- Methodology documentation enabling replication

## Error Handling & Data Quality

### Missing Data Strategy
1. Use most recent available data (within 5-year window)
2. Apply regional averages for structural indicators
3. Expert estimation for policy indicators
4. Adjust confidence scores based on data quality

### Validation Checkpoints
- Cross-reference all World Bank data with original sources
- Validate policy indicators through multiple evidence sources
- Expert review for country scores that deviate significantly from expectations
- Academic review of methodology and results

## File Organization
```
AHAII/
├── src/
│   ├── data_collection/
│   │   ├── worldbank_collector.py
│   │   ├── policy_indicator_collector.py  
│   │   └── health_ai_ecosystem_mapper.py
│   ├── scoring/
│   │   ├── ahaii_calculator.py
│   │   └── enhanced_ahaii_calculator.py
│   └── validation/
│       ├── data_quality_report.py
│       └── expert_validation_system.py
├── analysis/
│   └── pilot_assessment/
│       └── ahaii_pilot_report.py
└── data/
    ├── raw/              # World Bank downloads
    ├── processed/        # Cleaned datasets  
    └── indicators/       # AHAII calculations
```

This implementation will transform AHAII from concept to working intelligence platform, providing the first quantitative health AI infrastructure assessment for Africa.