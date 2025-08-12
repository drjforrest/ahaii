# TAIFA-FIALA Technical Migration Plan
*From Funding Tracker to African Health AI Infrastructure Index*

## Migration Strategy Overview

### What We're Preserving (The Gold)
- **ETL Pipeline Architecture** - The automated academic scraping and news monitoring system
- **Interactive Dashboard Framework** - React components and visualization infrastructure  
- **Vector Search Capabilities** - Pinecone integration for semantic analysis
- **Database Infrastructure** - Supabase foundation with systematic data validation
- **FastAPI Backend** - Modular service architecture

### What We're Transforming
- **Data Schema** - From funding-centric to infrastructure-centric
- **ETL Focus** - From funding announcements to health AI infrastructure signals
- **Dashboard Metrics** - From financial tracking to readiness scoring
- **Search Indexing** - From innovation discovery to infrastructure intelligence

## New Database Schema Design

### Core Infrastructure Tables

```sql
-- Country Infrastructure Profiles
CREATE TABLE countries (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL UNIQUE,
  iso_code_alpha3 TEXT NOT NULL UNIQUE,
  region TEXT NOT NULL, -- 'North Africa', 'East Africa', etc.
  population BIGINT,
  gdp_usd BIGINT,
  healthcare_spending_percent_gdp DECIMAL(4,2),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enhanced AHAII Scores with Validation Research Integration
CREATE TABLE ahaii_scores (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  country_id UUID REFERENCES countries(id),
  assessment_year INTEGER NOT NULL,
  assessment_quarter INTEGER, -- For quarterly updates
  
  -- Overall Score with Enhanced Validation
  total_score DECIMAL(5,2) NOT NULL, -- 0-100 scale
  global_ranking INTEGER,
  regional_ranking INTEGER,
  sub_regional_ranking INTEGER, -- East Africa, West Africa, etc.
  
  -- Pillar Scores with Sub-component Tracking
  human_capital_score DECIMAL(5,2) NOT NULL,
  human_capital_clinical_literacy DECIMAL(5,2),
  human_capital_informatics_capacity DECIMAL(5,2),
  human_capital_workforce_pipeline DECIMAL(5,2),
  
  physical_infrastructure_score DECIMAL(5,2) NOT NULL,
  physical_digitization_level DECIMAL(5,2),
  physical_computational_capacity DECIMAL(5,2),
  physical_connectivity_reliability DECIMAL(5,2),
  
  regulatory_infrastructure_score DECIMAL(5,2) NOT NULL,
  regulatory_approval_pathways DECIMAL(5,2),
  regulatory_data_governance DECIMAL(5,2),
  regulatory_market_access DECIMAL(5,2),
  
  economic_market_score DECIMAL(5,2) NOT NULL,
  economic_market_maturity DECIMAL(5,2),
  economic_financial_sustainability DECIMAL(5,2),
  economic_research_funding DECIMAL(5,2),
  
  -- Tier Classification with Validation Research Basis
  readiness_tier INTEGER NOT NULL CHECK (readiness_tier IN (1,2,3)),
  tier_justification TEXT, -- Specific reasoning for tier placement
  
  -- Data Quality and Validation (Enhanced based on research)
  overall_confidence_score DECIMAL(3,2), -- 0-1 scale for overall data quality
  data_completeness_percentage DECIMAL(5,2), -- % of required indicators with data
  expert_validation_score DECIMAL(3,2), -- Expert panel validation rating
  peer_review_status TEXT DEFAULT 'pending', -- 'peer_reviewed', 'expert_validated', 'pending', 'disputed'
  
  -- International Framework Alignment Impact
  who_alignment_bonus DECIMAL(3,2) DEFAULT 0, -- Bonus points for WHO framework alignment
  unesco_alignment_bonus DECIMAL(3,2) DEFAULT 0,
  au_strategy_alignment_bonus DECIMAL(3,2) DEFAULT 0,
  
  -- Benchmarking Context (from research showing need for comparative analysis)
  compared_to_similar_economies JSONB, -- Comparison with similar GDP/population countries
  development_trajectory TEXT, -- 'improving', 'stable', 'declining', 'rapid_growth'
  key_strengths TEXT[],
  priority_improvement_areas TEXT[],
  
  -- Assessment Methodology Metadata
  assessment_methodology_version TEXT DEFAULT '1.0',
  indicator_weights_used JSONB, -- Record of specific weights used
  methodology_adjustments TEXT, -- Any country-specific methodology adjustments
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(country_id, assessment_year, assessment_quarter)
);

-- Infrastructure Indicators (Raw data feeding into scores)
CREATE TABLE infrastructure_indicators (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  country_id UUID REFERENCES countries(id),
  pillar TEXT NOT NULL, -- 'human_capital', 'physical', 'regulatory', 'economic'
  indicator_name TEXT NOT NULL,
  indicator_value DECIMAL(10,4),
  indicator_unit TEXT, -- 'per_100k_population', 'percentage', 'count', etc.
  data_year INTEGER NOT NULL,
  data_quarter INTEGER,
  
  -- Enhanced Data Quality Metadata (based on validation research)
  data_source TEXT NOT NULL,
  data_source_type TEXT NOT NULL, -- 'who_official', 'government_ministry', 'academic_peer_reviewed', 'industry_report', 'ngo_survey'
  data_collection_method TEXT, -- 'national_survey', 'administrative_records', 'expert_assessment', 'facility_audit'
  sample_size INTEGER, -- For survey-based indicators
  geographic_coverage TEXT DEFAULT 'national', -- 'national', 'regional', 'urban_only', 'sample_areas'
  
  verification_status TEXT DEFAULT 'unverified', -- 'who_validated', 'peer_reviewed', 'government_verified', 'unverified', 'disputed'
  confidence_level TEXT DEFAULT 'medium', -- 'high', 'medium', 'low'
  confidence_score DECIMAL(3,2), -- 0-1 numerical confidence score
  validation_notes TEXT, -- Specific validation methodology or concerns
  last_verified_at TIMESTAMP WITH TIME ZONE,
  
  -- Benchmarking context (from research showing need for global comparison)
  global_benchmark_available BOOLEAN DEFAULT FALSE,
  global_percentile DECIMAL(3,1), -- Where this country ranks globally (0-100)
  african_percentile DECIMAL(3,1), -- Where this country ranks within Africa (0-1)
  regional_percentile DECIMAL(3,1), -- Where this country ranks within sub-region
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  
  UNIQUE(country_id, indicator_name, data_year, data_quarter)
);

-- Health AI Organizations (Companies, Universities, Hospitals)
CREATE TABLE health_ai_organizations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  organization_type TEXT NOT NULL, -- 'startup', 'university', 'hospital', 'research_center', 'government', 'ngo', 'development_partner'
  country_id UUID REFERENCES countries(id),
  city TEXT,
  founding_year INTEGER,
  employee_count INTEGER,
  website TEXT,
  description TEXT,
  
  -- Health AI Specific Fields
  primary_health_ai_focus TEXT[], -- Array: 'medical_imaging', 'clinical_decision_support', 'drug_discovery', 'epidemiology', 'telemedicine'
  clinical_partnerships TEXT[],
  regulatory_approvals TEXT[], -- FDA, CE mark, local approvals
  
  -- Funding and Investment (from research showing $50.1M market growth)
  total_funding_usd DECIMAL(12,2),
  latest_funding_round_usd DECIMAL(12,2),
  latest_funding_date DATE,
  funding_sources TEXT[], -- 'gates_foundation', 'venture_capital', 'government_grant', 'development_aid'
  
  -- Clinical Implementation (from research on deployment challenges)
  active_clinical_deployments INTEGER DEFAULT 0,
  countries_with_deployments TEXT[],
  validated_clinical_outcomes BOOLEAN DEFAULT FALSE,
  peer_reviewed_publications INTEGER DEFAULT 0,
  
  -- WHO/International Recognition (from research on validation needs)
  who_collaboration BOOLEAN DEFAULT FALSE,
  international_partnerships TEXT[],
  global_health_initiatives TEXT[],
  
  -- Infrastructure Contributions
  contributes_to_human_capital BOOLEAN DEFAULT FALSE,
  contributes_to_physical_infra BOOLEAN DEFAULT FALSE,
  contributes_to_regulatory_framework BOOLEAN DEFAULT FALSE,
  contributes_to_market_development BOOLEAN DEFAULT FALSE,
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Academic Programs (Biomedical Informatics, Clinical AI, etc.)
CREATE TABLE academic_programs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  university_name TEXT NOT NULL,
  program_name TEXT NOT NULL,
  degree_level TEXT NOT NULL, -- 'bachelor', 'master', 'phd', 'certificate'
  country_id UUID REFERENCES countries(id),
  program_type TEXT NOT NULL, -- 'medical_informatics', 'health_data_science', 'clinical_ai', 'biomedical_engineering'
  
  annual_graduates_estimated INTEGER,
  curriculum_includes_ai BOOLEAN DEFAULT FALSE,
  clinical_partnerships BOOLEAN DEFAULT FALSE,
  research_output_annual INTEGER, -- Estimated papers per year
  
  program_url TEXT,
  accreditation_status TEXT,
  establishment_year INTEGER,
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Healthcare Facilities (Infrastructure tracking)
CREATE TABLE healthcare_facilities (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  facility_name TEXT NOT NULL,
  facility_type TEXT NOT NULL, -- 'hospital', 'clinic', 'research_center'
  country_id UUID REFERENCES countries(id),
  region_state TEXT,
  city TEXT,
  
  -- Digital Infrastructure
  emr_system TEXT, -- Name of EMR system in use
  emr_implementation_year INTEGER,
  pacs_system BOOLEAN DEFAULT FALSE, -- Picture Archiving System
  digital_imaging_capability BOOLEAN DEFAULT FALSE,
  telemedicine_capability BOOLEAN DEFAULT FALSE,
  
  -- AI Readiness
  ai_tools_in_use TEXT[], -- Array of AI tools currently deployed
  ai_pilot_programs TEXT[],
  clinical_decision_support BOOLEAN DEFAULT FALSE,
  
  -- Capacity Metrics
  bed_count INTEGER,
  annual_patients INTEGER,
  staff_physicians INTEGER,
  staff_nurses INTEGER,
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Regulatory Framework Tracking
CREATE TABLE regulatory_frameworks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  country_id UUID REFERENCES countries(id),
  framework_type TEXT NOT NULL, -- 'medical_device_ai', 'health_data_privacy', 'telemedicine', 'clinical_trials'
  framework_name TEXT NOT NULL,
  
  status TEXT NOT NULL, -- 'proposed', 'draft', 'enacted', 'implemented'
  introduction_date DATE,
  implementation_date DATE,
  last_updated DATE,
  
  framework_details JSONB, -- Structured details about the framework
  international_alignment TEXT[], -- ['FDA_compliant', 'CE_mark_recognized', etc.]
  
  effectiveness_score DECIMAL(3,2), -- 0-5 scale based on implementation success
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- WHO/International Framework Alignment Tracking
CREATE TABLE international_framework_alignment (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  country_id UUID REFERENCES countries(id),
  framework_name TEXT NOT NULL, -- 'WHO_AI_Ethics', 'UNESCO_RAM', 'WHO_PAHO_Toolkit', 'AU_AI_Strategy'
  framework_category TEXT NOT NULL, -- 'ethics', 'readiness_assessment', 'regulatory', 'development_strategy'
  
  alignment_status TEXT NOT NULL, -- 'fully_aligned', 'partially_aligned', 'planning_alignment', 'not_aligned'
  alignment_score DECIMAL(3,2), -- 0-1 score for degree of alignment
  
  specific_requirements_met TEXT[], -- Array of specific framework requirements met
  requirements_in_progress TEXT[], -- Requirements being worked on
  requirements_gaps TEXT[], -- Missing requirements
  
  assessment_date DATE NOT NULL,
  assessment_source TEXT, -- Who conducted the assessment
  next_review_date DATE,
  
  -- Impact on AHAII scoring
  affects_regulatory_score BOOLEAN DEFAULT FALSE,
  affects_human_capital_score BOOLEAN DEFAULT FALSE,
  regulatory_weight_adjustment DECIMAL(3,2) DEFAULT 0, -- Adjustment to regulatory pillar score
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  
  UNIQUE(country_id, framework_name, assessment_date)
);

-- Clinical Validation and Outcomes Tracking
CREATE TABLE clinical_validation_studies (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  study_title TEXT NOT NULL,
  organization_id UUID REFERENCES health_ai_organizations(id),
  country_id UUID REFERENCES countries(id),
  
  -- Study Details
  study_type TEXT NOT NULL, -- 'rct', 'observational', 'pilot', 'retrospective', 'prospective'
  patient_population TEXT,
  sample_size INTEGER,
  study_duration_months INTEGER,
  
  -- AI Technology Details
  ai_technology_type TEXT NOT NULL, -- 'medical_imaging', 'clinical_decision_support', 'predictive_analytics', 'nlp'
  deployment_setting TEXT, -- 'tertiary_hospital', 'primary_care', 'community_health', 'telemedicine'
  
  -- Outcomes (from research on clinical validation needs)
  primary_outcome_met BOOLEAN,
  clinical_effectiveness_demonstrated BOOLEAN DEFAULT FALSE,
  cost_effectiveness_demonstrated BOOLEAN DEFAULT FALSE,
  safety_profile_acceptable BOOLEAN DEFAULT FALSE,
  
  -- Publication and Validation Status
  peer_reviewed_publication TEXT, -- DOI or citation
  publication_date DATE,
  regulatory_submission BOOLEAN DEFAULT FALSE,
  regulatory_approval_received BOOLEAN DEFAULT FALSE,
  
  -- Impact on Infrastructure Scoring
  validates_local_infrastructure BOOLEAN DEFAULT FALSE,
  infrastructure_lessons_learned TEXT,
  scalability_assessment TEXT,
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Development Partner and International Aid Tracking
CREATE TABLE development_partnerships (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  country_id UUID REFERENCES countries(id),
  partner_organization TEXT NOT NULL, -- 'Gates Foundation', 'WHO', 'World Bank', 'USAID', etc.
  partner_type TEXT NOT NULL, -- 'multilateral', 'bilateral', 'foundation', 'ngo'
  
  -- Partnership Details
  partnership_name TEXT NOT NULL,
  partnership_focus TEXT NOT NULL, -- 'capacity_building', 'infrastructure_development', 'research_support', 'policy_development'
  start_date DATE,
  end_date DATE,
  total_commitment_usd DECIMAL(12,2),
  disbursed_amount_usd DECIMAL(12,2),
  
  -- Health AI Specific Components
  ai_component_percentage DECIMAL(5,2), -- What % of partnership is AI-focused
  target_health_areas TEXT[], -- 'maternal_health', 'infectious_disease', 'ncd', 'mental_health'
  capacity_building_focus TEXT[], -- 'clinical_training', 'research_capacity', 'regulatory_capacity', 'infrastructure'
  
  -- Infrastructure Impact Assessment
  expected_infrastructure_impact TEXT[], -- Which pillars this partnership targets
  measured_outcomes TEXT[],
  success_metrics JSONB,
  
  -- Partnership Status and Performance
  partnership_status TEXT DEFAULT 'active', -- 'active', 'completed', 'suspended', 'cancelled'
  performance_rating TEXT, -- 'excellent', 'satisfactory', 'needs_improvement', 'unsatisfactory'
  lessons_learned TEXT,
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE TABLE infrastructure_intelligence (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  report_type TEXT NOT NULL, -- 'academic_scan', 'news_monitoring', 'policy_tracking', 'market_analysis'
  country_id UUID REFERENCES countries(id),
  
  report_title TEXT NOT NULL,
  report_summary TEXT,
  key_findings JSONB,
  
  -- Source Information
  source_type TEXT NOT NULL, -- 'academic_paper', 'news_article', 'government_report', 'company_announcement'
  source_url TEXT,
  source_publication TEXT,
  publication_date DATE,
  
  -- Infrastructure Impact Assessment
  affects_human_capital BOOLEAN DEFAULT FALSE,
  affects_physical_infrastructure BOOLEAN DEFAULT FALSE,
  affects_regulatory_framework BOOLEAN DEFAULT FALSE,
  affects_economic_market BOOLEAN DEFAULT FALSE,
  
  impact_significance TEXT DEFAULT 'low', -- 'high', 'medium', 'low'
  
  -- Processing Metadata
  processed_by_ai BOOLEAN DEFAULT TRUE,
  confidence_score DECIMAL(3,2), -- 0-1 scale
  verification_status TEXT DEFAULT 'pending', -- 'verified', 'pending', 'disputed'
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Legacy Data Migration Tables

```sql
-- Archive original funding data
CREATE TABLE legacy_funding_data (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  original_table TEXT NOT NULL,
  original_record_id TEXT,
  archived_data JSONB NOT NULL,
  archived_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  migration_notes TEXT
);

-- Funding to Infrastructure Linkage (where applicable)
CREATE TABLE funding_infrastructure_links (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  legacy_funding_record UUID,
  linked_organization_id UUID REFERENCES health_ai_organizations(id),
  linked_facility_id UUID REFERENCES healthcare_facilities(id),
  linked_program_id UUID REFERENCES academic_programs(id),
  link_type TEXT NOT NULL, -- 'direct_funding', 'infrastructure_development', 'capacity_building'
  link_confidence DECIMAL(3,2), -- 0-1 scale
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## ETL Pipeline Transformation

### Current Pipeline Adaptations

#### 1. Academic Scraper Conversion (`etl/academic/`)

**From:** Generic AI paper collection
**To:** Health AI infrastructure signal detection

```python
# New target keywords for academic scraping
HEALTH_AI_INFRASTRUCTURE_KEYWORDS = {
    'human_capital': [
        'medical informatics education', 'clinical AI training', 
        'biomedical informatics curriculum', 'health data science programs',
        'clinical decision support training', 'medical AI workforce'
    ],
    'physical_infrastructure': [
        'hospital EMR implementation', 'medical imaging systems',
        'healthcare data centers', 'clinical data networks',
        'telemedicine infrastructure', 'PACS deployment'
    ],
    'regulatory': [
        'medical AI regulation', 'health AI governance',
        'clinical AI validation', 'medical device AI approval',
        'health data privacy frameworks'
    ],
    'economic': [
        'health AI market analysis', 'medical AI investment',
        'healthcare digital transformation funding',
        'clinical AI adoption costs', 'health AI reimbursement'
    ]
}

# Enhanced extraction for infrastructure indicators
class HealthAIInfrastructureExtractor:
    def extract_infrastructure_indicators(self, paper: Dict) -> List[Dict]:
        """Extract specific infrastructure metrics from papers"""
        indicators = []
        
        # Look for quantitative metrics
        patterns = {
            'emr_adoption': r'(\d+)% of hospitals.*EMR',
            'ai_training_programs': r'(\d+).*medical.*AI.*program',
            'clinical_ai_implementations': r'(\d+).*clinical.*AI.*deployment'
        }
        
        for indicator_type, pattern in patterns.items():
            matches = re.findall(pattern, paper['content'], re.IGNORECASE)
            if matches:
                indicators.append({
                    'indicator_name': indicator_type,
                    'indicator_value': float(matches[0]),
                    'data_source': paper['journal'],
                    'confidence_level': 'medium'
                })
        
        return indicators
```

#### 2. News Monitoring Enhancement (`etl/news/`)

**From:** Funding announcement tracking
**To:** Infrastructure development monitoring

```python
# New RSS feeds focused on health AI infrastructure
HEALTH_AI_INFRASTRUCTURE_FEEDS = [
    'https://healthcareitnews.com/rss.xml',
    'https://www.mobihealthnews.com/rss.xml',
    'https://africanews.com/health/rss.xml',
    'https://www.who.int/rss-feeds/news-english.xml'
]

# Enhanced signal detection
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
        
        # Human capital signals
        if any(keyword in article['content'].lower() for keyword in 
               ['medical training', 'clinical education', 'health informatics', 'ai curriculum']):
            classification['human_capital'] = True
        
        # Physical infrastructure signals
        if any(keyword in article['content'].lower() for keyword in 
               ['hospital system', 'emr implementation', 'data center', 'telemedicine platform']):
            classification['physical_infrastructure'] = True
        
        # Regulatory signals
        if any(keyword in article['content'].lower() for keyword in 
               ['medical device approval', 'health regulation', 'ai governance', 'clinical validation']):
            classification['regulatory'] = True
        
        # Economic signals
        if any(keyword in article['content'].lower() for keyword in 
               ['health ai funding', 'medical ai investment', 'digital health budget']):
            classification['economic'] = True
        
        # Assess significance based on multiple factors
        if sum(classification[k] for k in ['human_capital', 'physical_infrastructure', 'regulatory', 'economic']) > 2:
            classification['significance'] = 'high'
        elif sum(classification[k] for k in ['human_capital', 'physical_infrastructure', 'regulatory', 'economic']) > 1:
            classification['significance'] = 'medium'
        
        return classification
```

#### 3. New Specialized Scrapers

```python
# Government Health Ministry AI Strategy Scraper
class HealthMinistryAIStrategyScaper:
    def scrape_african_health_ministry_ai_strategies(self):
        """Scrape official health ministry AI strategies and policies"""
        
        ministry_urls = {
            'south_africa': 'https://www.health.gov.za',
            'kenya': 'https://www.health.go.ke',
            'nigeria': 'https://www.health.gov.ng',
            'ghana': 'https://www.moh.gov.gh',
            'egypt': 'https://www.mohp.gov.eg'
        }
        
        for country, base_url in ministry_urls.items():
            # Implementation specific to each ministry's document structure
            pass

# Medical Regulatory Authority Tracker
class MedicalAIRegulationTracker:
    def track_medical_ai_approvals(self):
        """Track medical AI device approvals across African regulatory bodies"""
        
        regulatory_bodies = {
            'south_africa': 'https://www.sahpra.org.za',
            'kenya': 'https://ppp.health.go.ke',
            'nigeria': 'https://www.nafdac.gov.ng',
            'ghana': 'https://fdaghana.gov.gh',
            'egypt': 'https://www.eda.mohp.gov.eg'
        }
        
        # Track approvals, guidelines, and regulatory updates
        pass

# Hospital System Digital Infrastructure Scanner
class HospitalInfrastructureScanner:
    def scan_hospital_digital_infrastructure(self):
        """Scan major hospital systems for digital infrastructure implementation"""
        
        # Target major hospital groups across Africa
        hospital_systems = [
            'netcare.co.za',  # South Africa
            'aku.edu',        # Aga Khan (Kenya, Tanzania, Uganda)
            'lagosuniversityteachinghospital.org.ng',  # Nigeria
            'kath.gov.gh'     # Ghana
        ]
        
        # Look for EMR implementations, AI tool deployments, digital transformation announcements
        pass
```

### New Vector Embeddings Strategy

```python
# Health AI Infrastructure specific embeddings
class HealthAIInfrastructureEmbeddings:
    def __init__(self):
        self.embedding_namespaces = {
            'human_capital': 'health-ai-human-capital',
            'physical_infrastructure': 'health-ai-physical-infra',
            'regulatory': 'health-ai-regulatory',
            'economic': 'health-ai-economic',
            'integrated': 'health-ai-integrated'
        }
    
    def create_infrastructure_embeddings(self, content: str, pillar: str, country: str):
        """Create specialized embeddings for infrastructure content"""
        
        # Add context prefixes for better semantic clustering
        context_prefix = f"African health AI {pillar} infrastructure in {country}: "
        enhanced_content = context_prefix + content
        
        # Generate embeddings with pillar-specific namespace
        embedding = self.generate_embedding(enhanced_content)
        
        return {
            'embedding': embedding,
            'namespace': self.embedding_namespaces[pillar],
            'metadata': {
                'pillar': pillar,
                'country': country,
                'content_type': 'infrastructure_intelligence'
            }
        }
```

## Dashboard Component Transformation

### New React Components

```typescript
// Replace funding tracker components with infrastructure readiness components

// 1. AHAII Score Dashboard
interface AHAIIScoreProps {
  country: Country;
  scores: AHAIIScores;
  historicalData: AHAIIScores[];
}

const AHAIIScoreDashboard: React.FC<AHAIIScoreProps> = ({country, scores, historicalData}) => {
  return (
    <div className="ahaii-dashboard">
      <CountryOverviewCard country={country} overallScore={scores.total_score} />
      <PillarBreakdownChart scores={scores} />
      <TierClassificationBadge tier={scores.readiness_tier} />
      <HistoricalTrendChart data={historicalData} />
      <RegionalComparisonChart country={country} />
    </div>
  );
};

// 2. Infrastructure Signal Intelligence Feed
const InfrastructureIntelligenceFeed: React.FC = () => {
  const [signals, setSignals] = useState<InfrastructureSignal[]>([]);
  
  useEffect(() => {
    // Real-time infrastructure signal updates
    const eventSource = new EventSource('/api/infrastructure-signals/stream');
    eventSource.onmessage = (event) => {
      const newSignal = JSON.parse(event.data);
      setSignals(prev => [newSignal, ...prev.slice(0, 49)]); // Keep latest 50
    };
  }, []);
  
  return (
    <div className="infrastructure-intelligence-feed">
      {signals.map(signal => (
        <InfrastructureSignalCard key={signal.id} signal={signal} />
      ))}
    </div>
  );
};

// 3. Country Infrastructure Heatmap
const CountryInfrastructureHeatmap: React.FC = () => {
  return (
    <div className="infrastructure-heatmap">
      <AfricaMapVisualization 
        data={countryScores}
        metric="total_score"
        colorScheme="readiness"
      />
      <PillarFilterControls />
      <MetricSelector />
    </div>
  );
};
```

### API Endpoint Transformation

```python
# New FastAPI endpoints for health AI infrastructure

@app.get("/api/countries/{country_id}/ahaii-score")
async def get_country_ahaii_score(country_id: str, year: int = None):
    """Get AHAII score for a specific country"""
    pass

@app.get("/api/infrastructure-indicators")
async def get_infrastructure_indicators(
    country_id: str = None, 
    pillar: str = None,
    indicator_name: str = None
):
    """Get specific infrastructure indicators"""
    pass

@app.get("/api/infrastructure-signals/stream")
async def stream_infrastructure_signals():
    """Server-sent events for real-time infrastructure intelligence"""
    pass

@app.post("/api/infrastructure-assessment")
async def trigger_infrastructure_assessment(country_ids: List[str]):
    """Trigger manual infrastructure assessment for specific countries"""
    pass

@app.get("/api/regional-rankings")
async def get_regional_rankings(region: str = None):
    """Get AHAII rankings by region"""
    pass
```

## Migration Execution Plan

### Phase 1: Schema Migration (Week 1)
1. **Database Backup**: Full backup of existing funding tracker data
2. **Legacy Data Archive**: Migrate all funding data to `legacy_funding_data` table
3. **New Schema Deployment**: Create all new health AI infrastructure tables
4. **Data Migration Scripts**: Convert relevant funding data to organization records

### Phase 2: ETL Pipeline Conversion (Week 2-3)  
1. **Academic Scraper Update**: Retrain on health AI infrastructure keywords
2. **News Monitor Enhancement**: Add health AI infrastructure RSS feeds
3. **New Scrapers Deployment**: Government, regulatory, hospital system scrapers
4. **Vector Database Migration**: Re-embed all content with infrastructure focus

### Phase 3: Dashboard Transformation (Week 4)
1. **Component Replacement**: Replace funding components with infrastructure components
2. **API Endpoint Updates**: Implement all new infrastructure-focused endpoints
3. **Real-time Features**: Add infrastructure signal streaming
4. **User Experience Testing**: Ensure smooth transition for existing users

### Phase 4: Pilot Assessment (Week 5-6)
1. **Baseline Data Collection**: Gather infrastructure data for 5 pilot countries
2. **Scoring Algorithm Implementation**: Calculate initial AHAII scores
3. **Validation Process**: Verify scores against expert knowledge
4. **Methodology Refinement**: Adjust weighting and indicators based on pilot results

## Technical Risk Mitigation

### Data Quality Assurance
- **Multi-source Verification**: Cross-reference infrastructure indicators from multiple sources
- **Confidence Scoring**: Every data point includes confidence level and verification status
- **Expert Validation**: Partner with health informatics experts for spot-checking

### System Reliability
- **Gradual Migration**: Maintain parallel systems during transition period
- **Rollback Capability**: Ability to restore funding tracker if critical issues arise
- **Monitoring and Alerting**: Comprehensive monitoring of all new ETL processes

### Performance Optimization
- **Database Indexing**: Proper indexes on all query-heavy tables
- **Caching Strategy**: Redis caching for frequently accessed infrastructure scores
- **Load Testing**: Ensure dashboard performance under expected user load

This technical plan preserves all your architectural innovations while completely pivoting the focus to health AI infrastructure intelligence. The migration can be executed systematically over 6 weeks while maintaining system availability.