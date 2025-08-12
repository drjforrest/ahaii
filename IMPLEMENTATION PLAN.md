# ETL Migration Execution Plan
*Step-by-step migration from TAIFA-FIALA to AHAII health AI infrastructure intelligence*

## Current Status Assessment
✅ Database schema deployed (11 functional tables)  
✅ Basic ETL directory structure exists  
🔄 **NEXT**: Copy and adapt core ETL components  

## Phase 1: Core Services Migration (Day 1-2)

### Step 1.1: Copy Essential Services
```bash
# Navigate to AHAII backend
cd /Users/drjforrest/dev/devprojects/AHAII/backend

# Copy core services from TAIFA-FIALA
cp ../TAIFA-FIALA/backend/services/database_service.py services/
cp ../TAIFA-FIALA/backend/services/vector_service.py services/
cp ../TAIFA-FIALA/backend/services/deduplication_service.py services/
cp ../TAIFA-FIALA/backend/services/serpapi_service.py services/
cp ../TAIFA-FIALA/backend/services/serper_service.py services/
cp ../TAIFA-FIALA/backend/config/settings.py config/
```

### Step 1.2: Update Database Service for AHAII Schema
**File**: `services/database_service.py`

**Key Changes Needed**:
1. Update table references for AHAII schema
2. Add AHAII-specific insert/update methods
3. Update connection string for Supabase

**Critical Methods to Add**:
```python
async def insert_infrastructure_indicator(self, indicator_data: Dict):
    """Insert infrastructure indicator into AHAII schema"""
    
async def update_ahaii_scores(self, country_id: str, scores: Dict):
    """Update AHAII scores for a country"""
    
async def insert_health_ai_organization(self, org_data: Dict):
    """Insert health AI organization"""
```

### Step 1.3: Update Vector Service for Health AI Context
**File**: `services/vector_service.py`

**Key Changes**:
```python
# Update embedding namespaces for health AI infrastructure
EMBEDDING_NAMESPACES = {
    'human_capital': 'health-ai-human-capital',
    'physical_infrastructure': 'health-ai-physical-infra', 
    'regulatory': 'health-ai-regulatory',
    'economic': 'health-ai-economic',
    'integrated': 'health-ai-integrated'
}
```

## Phase 2: Academic Processor Adaptation (Day 2-3)

### Step 2.1: Copy and Adapt Academic ETL
```bash
# Copy academic processing components
cp -r ../TAIFA-FIALA/backend/etl/academic/* etl/academic/
```

### Step 2.2: Update Academic Keywords
**File**: `etl/academic/unified_academic_processor.py`

**Replace Keywords Section**:
```python
# Health AI Infrastructure specific keywords
HEALTH_AI_INFRASTRUCTURE_KEYWORDS = {
    'human_capital': [
        'medical informatics education', 'clinical AI training', 
        'biomedical informatics curriculum', 'health data science programs',
        'clinical decision support training', 'medical AI workforce',
        'health informatics capacity', 'clinical AI literacy'
    ],
    'physical_infrastructure': [
        'hospital EMR implementation', 'medical imaging systems',
        'healthcare data centers', 'clinical data networks',
        'telemedicine infrastructure', 'PACS deployment',
        'health information systems', 'clinical decision support systems'
    ],
    'regulatory': [
        'medical AI regulation', 'health AI governance',
        'clinical AI validation', 'medical device AI approval',
        'health data privacy frameworks', 'clinical trial AI regulation',
        'medical AI safety standards', 'health AI ethics'
    ],
    'economic': [
        'health AI market analysis', 'medical AI investment',
        'healthcare digital transformation funding',
        'clinical AI adoption costs', 'health AI reimbursement',
        'digital health funding', 'medical AI venture capital'
    ]
}
```

### Step 2.3: Update Extraction Logic
**Add Infrastructure Signal Detection**:
```python
class HealthAIInfrastructureExtractor:
    def extract_infrastructure_indicators(self, paper: Dict) -> List[Dict]:
        """Extract specific infrastructure metrics from papers"""
        indicators = []
        
        # Look for quantitative metrics
        patterns = {
            'emr_adoption_rate': r'(\d+(?:\.\d+)?)\s*(?:percent|%)\s*(?:of\s+)?(?:hospitals|facilities|clinics)\s*(?:have|use|implemented|adopted)\s*(?:EMR|electronic medical record)',
            'ai_training_programs': r'(\d+)\s*(?:new\s+)?(?:AI|artificial intelligence)\s*(?:training|certification|education)\s*programs?',
            'telemedicine_capability': r'(\d+(?:\.\d+)?)\s*(?:percent|%)\s*(?:of\s+)?(?:hospitals|facilities).*?(?:offer|provide)\s*(?:telemedicine|telehealth)'
        }
        
        for indicator_type, pattern in patterns.items():
            matches = re.findall(pattern, paper['content'], re.IGNORECASE)
            if matches:
                # Map to AHAII pillar
                pillar = self.determine_pillar(indicator_type)
                indicators.append({
                    'indicator_name': indicator_type,
                    'indicator_value': float(matches[0]),
                    'pillar': pillar,
                    'confidence_score': 0.8,
                    'data_source': paper['journal']
                })
        
        return indicators
```

## Phase 3: News Monitor Enhancement (Day 3-4)

### Step 3.1: Copy News Monitor
```bash
cp -r ../TAIFA-FIALA/backend/etl/news/* etl/news/
```

### Step 3.2: Update RSS Feeds
**File**: `etl/news/rss_monitor.py`

**Add Health AI Infrastructure Feeds**:
```python
HEALTH_AI_INFRASTRUCTURE_FEEDS = [
    'https://healthcareitnews.com/rss.xml',
    'https://www.mobihealthnews.com/rss.xml',
    'https://africanews.com/health/rss.xml',
    'https://www.who.int/rss-feeds/news-english.xml',
    'https://www.himss.org/rss.xml',
    'https://medcitynews.com/feed/',
    'https://www.healthdatamanagement.com/rss.xml'
]
```

### Step 3.3: Add Infrastructure Signal Classification
```python
class HealthAIInfrastructureSignalProcessor:
    def classify_infrastructure_signal(self, article: Dict) -> Dict:
        """Classify news articles by infrastructure pillar impact"""
        classification = {
            'human_capital': False,
            'physical_infrastructure': False,
            'regulatory': False,
            'economic': False,
            'significance': 'low'
        }
        
        content_lower = article['content'].lower()
        
        # Human capital signals
        if any(keyword in content_lower for keyword in 
               ['medical training', 'clinical education', 'health informatics', 'ai curriculum']):
            classification['human_capital'] = True
        
        # Physical infrastructure signals  
        if any(keyword in content_lower for keyword in
               ['hospital system', 'emr implementation', 'data center', 'telemedicine platform']):
            classification['physical_infrastructure'] = True
        
        # Regulatory signals
        if any(keyword in content_lower for keyword in
               ['medical device approval', 'health regulation', 'ai governance', 'clinical validation']):
            classification['regulatory'] = True
        
        # Economic signals
        if any(keyword in content_lower for keyword in
               ['health ai funding', 'medical ai investment', 'digital health budget']):
            classification['economic'] = True
        
        # Assess significance
        signal_count = sum(classification[k] for k in ['human_capital', 'physical_infrastructure', 'regulatory', 'economic'])
        if signal_count > 2:
            classification['significance'] = 'high'
        elif signal_count > 1:
            classification['significance'] = 'medium'
        
        return classification
```

## Phase 4: New Health-Specific Scrapers (Day 4-5)

### Step 4.1: Create Health Ministry Scraper
**File**: `etl/government/health_ministry_scraper.py`

```python
class HealthMinistryAIStrategyScaper:
    """Scrape official health ministry AI strategies and policies"""
    
    def __init__(self):
        self.ministry_urls = {
            'south_africa': 'https://www.health.gov.za',
            'kenya': 'https://www.health.go.ke',
            'nigeria': 'https://www.health.gov.ng',
            'ghana': 'https://www.moh.gov.gh',
            'egypt': 'https://www.mohp.gov.eg',
            'rwanda': 'https://www.moh.gov.rw'
        }
    
    async def scrape_ministry_strategies(self):
        """Scrape AI strategies and digital health policies"""
        # Implementation follows existing scraper patterns from TAIFA-FIALA
        pass
```

### Step 4.2: Create Medical Regulatory Tracker
**File**: `etl/regulatory/medical_ai_tracker.py`

```python
class MedicalAIRegulationTracker:
    """Track medical AI device approvals across African regulatory bodies"""
    
    def __init__(self):
        self.regulatory_bodies = {
            'south_africa': 'https://www.sahpra.org.za',
            'kenya': 'https://ppp.health.go.ke',  
            'nigeria': 'https://www.nafdac.gov.ng',
            'ghana': 'https://fdaghana.gov.gh',
            'egypt': 'https://www.eda.mohp.gov.eg'
        }
    
    async def track_medical_ai_approvals(self):
        """Track approvals, guidelines, and regulatory updates"""
        # Implementation follows RSS monitor pattern
        pass
```

## Phase 5: AHAII Scoring Service (Day 5-6)

### Step 5.1: Create AHAII Scoring Calculator
**File**: `services/ahaii_scoring_service.py`

```python
class AHAIIScoringService:
    """Calculate AHAII scores from infrastructure indicators"""
    
    def __init__(self):
        self.pillar_weights = {
            'human_capital': 0.35,  # Increased based on comparative analysis
            'physical_infrastructure': 0.25,  # Decreased
            'regulatory': 0.25,
            'economic': 0.15
        }
    
    async def calculate_country_score(self, country_id: str) -> Dict:
        """Calculate comprehensive AHAII score for a country"""
        # 1. Aggregate indicators by pillar
        # 2. Apply normalization and weighting
        # 3. Calculate sub-component scores
        # 4. Determine tier classification
        # 5. Generate confidence metrics
        pass
```

## Phase 6: Data Collection Orchestrator Update (Day 6-7)

### Step 6.1: Copy and Adapt Orchestrator
```bash
cp ../TAIFA-FIALA/backend/etl/intelligence/data_collection_orchestrator.py etl/
```

### Step 6.2: Update Collection Targets
**Modify collection missions for health AI infrastructure focus**:
- Academic: Health AI infrastructure research
- News: Health ministry announcements, medical AI approvals
- Government: Digital health strategies, AI policies
- Clinical: Hospital system implementations, validation studies

## Testing and Validation

### Step 7.1: Create Test Configuration
**File**: `config/test_settings.py`

```python
# Test with small dataset first
TEST_COUNTRIES = ['ZAF', 'KEN', 'RWA']  # South Africa, Kenya, Rwanda
MAX_RESULTS_PER_SOURCE = 10  # Limit for testing
```

### Step 7.2: Run Initial ETL Test
```bash
# Test academic processor
python -m etl.academic.unified_academic_processor --test

# Test news monitor  
python -m etl.news.rss_monitor --test

# Test database connectivity
python -m services.database_service --test
```

## Success Metrics

**Phase 1 Complete When**:
- [ ] All core services migrated and database connected
- [ ] Academic processor finds health AI infrastructure papers
- [ ] News monitor detects health AI infrastructure signals
- [ ] AHAII scoring service calculates pilot scores
- [ ] Test data populates all 11 tables successfully

**Ready for Phase 2**: Dashboard prototype and Rwanda partnership outreach

## Next Steps After ETL Migration

1. **Create Pilot Dataset**: Generate AHAII scores for Rwanda, Kenya, South Africa
2. **Build Dashboard Prototype**: Visualize comparative analysis results
3. **Initiate Rwanda Partnership**: Contact Health Intelligence Center
4. **Academic Validation**: Compare initial AHAII scores with IMF AIPI
5. **Stakeholder Outreach**: Begin Kenya and South Africa engagement

This systematic migration preserves your excellent ETL architecture while adapting it for health AI infrastructure intelligence. Each phase builds on the previous, ensuring stable progression toward a functional health AI infrastructure intelligence platform.