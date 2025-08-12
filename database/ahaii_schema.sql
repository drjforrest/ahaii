-- AHAII Database Schema
-- African Health AI Infrastructure Index
-- Complete schema for health AI infrastructure assessment

-- =============================================================================
-- CORE COUNTRY AND INFRASTRUCTURE TABLES
-- =============================================================================

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
  african_percentile DECIMAL(3,1), -- Where this country ranks within Africa (0-100)
  regional_percentile DECIMAL(3,1), -- Where this country ranks within sub-region (0-100)
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  
  UNIQUE(country_id, indicator_name, data_year, data_quarter)
);

-- =============================================================================
-- HEALTH AI ECOSYSTEM TABLES
-- =============================================================================

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

-- =============================================================================
-- REGULATORY AND POLICY FRAMEWORK TABLES
-- =============================================================================

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

-- =============================================================================
-- CLINICAL VALIDATION AND OUTCOMES TABLES
-- =============================================================================

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

-- =============================================================================
-- DEVELOPMENT PARTNERSHIPS AND INTELLIGENCE TABLES
-- =============================================================================

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

-- Infrastructure Intelligence (ETL Pipeline Output)
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

-- =============================================================================
-- INDEXES FOR PERFORMANCE
-- =============================================================================

-- Country and scoring indexes
CREATE INDEX idx_countries_region ON countries(region);
CREATE INDEX idx_countries_iso_code ON countries(iso_code_alpha3);

-- AHAII scores indexes
CREATE INDEX idx_ahaii_scores_country_year ON ahaii_scores(country_id, assessment_year);
CREATE INDEX idx_ahaii_scores_total_score ON ahaii_scores(total_score DESC);
CREATE INDEX idx_ahaii_scores_tier ON ahaii_scores(readiness_tier);

-- Infrastructure indicators indexes
CREATE INDEX idx_infrastructure_indicators_country_pillar ON infrastructure_indicators(country_id, pillar);
CREATE INDEX idx_infrastructure_indicators_indicator_name ON infrastructure_indicators(indicator_name);
CREATE INDEX idx_infrastructure_indicators_year ON infrastructure_indicators(data_year);

-- Organization indexes
CREATE INDEX idx_health_ai_organizations_country ON health_ai_organizations(country_id);
CREATE INDEX idx_health_ai_organizations_type ON health_ai_organizations(organization_type);

-- Intelligence indexes
CREATE INDEX idx_infrastructure_intelligence_country ON infrastructure_intelligence(country_id);
CREATE INDEX idx_infrastructure_intelligence_report_type ON infrastructure_intelligence(report_type);
CREATE INDEX idx_infrastructure_intelligence_date ON infrastructure_intelligence(publication_date);

-- =============================================================================
-- INITIAL DATA - AFRICAN COUNTRIES
-- =============================================================================

-- Insert African countries with basic information
INSERT INTO countries (name, iso_code_alpha3, region, population, gdp_usd, healthcare_spending_percent_gdp) VALUES
-- North Africa
('Algeria', 'DZA', 'North Africa', 44700000, 169988000000, 6.2),
('Egypt', 'EGY', 'North Africa', 104000000, 469440000000, 4.4),
('Libya', 'LBY', 'North Africa', 6958000, 25280000000, 2.9),
('Morocco', 'MAR', 'North Africa', 37400000, 132730000000, 5.3),
('Sudan', 'SDN', 'North Africa', 46750000, 30060000000, 2.5),
('Tunisia', 'TUN', 'North Africa', 11935000, 46940000000, 7.2),

-- West Africa
('Benin', 'BEN', 'West Africa', 12450000, 17400000000, 2.6),
('Burkina Faso', 'BFA', 'West Africa', 22100000, 18930000000, 2.4),
('Cape Verde', 'CPV', 'West Africa', 560000, 2130000000, 4.8),
('Cote d''Ivoire', 'CIV', 'West Africa', 27500000, 70990000000, 3.3),
('Gambia', 'GMB', 'West Africa', 2420000, 2040000000, 2.1),
('Ghana', 'GHA', 'West Africa', 32830000, 77590000000, 3.2),
('Guinea', 'GIN', 'West Africa', 13530000, 18990000000, 2.3),
('Guinea-Bissau', 'GNB', 'West Africa', 2010000, 1550000000, 2.9),
('Liberia', 'LBR', 'West Africa', 5180000, 3070000000, 6.7),
('Mali', 'MLI', 'West Africa', 21900000, 19330000000, 3.9),
('Mauritania', 'MRT', 'West Africa', 4780000, 9520000000, 3.4),
('Niger', 'NER', 'West Africa', 25250000, 15290000000, 2.9),
('Nigeria', 'NGA', 'West Africa', 218500000, 440780000000, 3.4),
('Senegal', 'SEN', 'West Africa', 17200000, 27680000000, 3.8),
('Sierra Leone', 'SLE', 'West Africa', 8140000, 3740000000, 6.6),
('Togo', 'TGO', 'West Africa', 8280000, 8130000000, 5.2),

-- East Africa
('Burundi', 'BDI', 'East Africa', 12550000, 2780000000, 6.2),
('Comoros', 'COM', 'East Africa', 890000, 1330000000, 3.9),
('Djibouti', 'DJI', 'East Africa', 990000, 3780000000, 2.3),
('Eritrea', 'ERI', 'East Africa', 3600000, 2610000000, 3.8),
('Ethiopia', 'ETH', 'East Africa', 120300000, 111270000000, 3.5),
('Kenya', 'KEN', 'East Africa', 54000000, 115700000000, 4.3),
('Madagascar', 'MDG', 'East Africa', 28430000, 15790000000, 3.0),
('Malawi', 'MWI', 'East Africa', 19650000, 12630000000, 5.3),
('Mauritius', 'MUS', 'East Africa', 1270000, 14780000000, 6.0),
('Mozambique', 'MOZ', 'East Africa', 32160000, 16750000000, 4.9),
('Rwanda', 'RWA', 'East Africa', 13460000, 11070000000, 7.5),
('Seychelles', 'SYC', 'East Africa', 99000, 1730000000, 4.2),
('Somalia', 'SOM', 'East Africa', 17070000, 7370000000, 2.9),
('South Sudan', 'SSD', 'East Africa', 11620000, 3090000000, 2.7),
('Tanzania', 'TZA', 'East Africa', 61500000, 71000000000, 3.6),
('Uganda', 'UGA', 'East Africa', 47100000, 47730000000, 4.1),

-- Central Africa
('Angola', 'AGO', 'Central Africa', 33930000, 106930000000, 2.9),
('Cameroon', 'CMR', 'Central Africa', 27910000, 45180000000, 3.5),
('Central African Republic', 'CAF', 'Central Africa', 4920000, 2380000000, 4.2),
('Chad', 'TCD', 'Central Africa', 17180000, 11310000000, 3.2),
('Democratic Republic of Congo', 'COD', 'Central Africa', 95890000, 58070000000, 3.3),
('Equatorial Guinea', 'GNQ', 'Central Africa', 1450000, 10020000000, 2.5),
('Gabon', 'GAB', 'Central Africa', 2280000, 18580000000, 2.7),
('Republic of Congo', 'COG', 'Central Africa', 5660000, 12270000000, 2.2),
('São Tomé and Príncipe', 'STP', 'Central Africa', 220000, 470000000, 5.1),

-- Southern Africa
('Botswana', 'BWA', 'Southern Africa', 2400000, 18340000000, 5.4),
('Eswatini', 'SWZ', 'Southern Africa', 1160000, 4400000000, 6.5),
('Lesotho', 'LSO', 'Southern Africa', 2160000, 2460000000, 10.6),
('Namibia', 'NAM', 'Southern Africa', 2540000, 12370000000, 8.9),
('South Africa', 'ZAF', 'Southern Africa', 59890000, 419010000000, 8.1),
('Zambia', 'ZMB', 'Southern Africa', 19470000, 22150000000, 4.9),
('Zimbabwe', 'ZWE', 'Southern Africa', 15990000, 21440000000, 4.7);

COMMENT ON TABLE countries IS 'African countries with basic demographic and economic indicators';
COMMENT ON TABLE ahaii_scores IS 'AHAII infrastructure readiness scores and assessments by country and time period';
COMMENT ON TABLE infrastructure_indicators IS 'Raw infrastructure indicators feeding into AHAII scoring methodology';
COMMENT ON TABLE health_ai_organizations IS 'Health AI organizations, companies, universities, and institutions across Africa';
COMMENT ON TABLE infrastructure_intelligence IS 'Intelligence reports from ETL pipeline monitoring health AI infrastructure developments';
