// Country and AHAII Score Type Definitions
export interface Country {
  id: string;
  name: string;
  iso_code_alpha3: string;
  iso_code_alpha2: string; // For image file naming
  region: string;
  population: number;
  gdp_usd: number;
  healthcare_spending_percent_gdp: number;
  flag_image: string;
  country_outline_image: string;
  country_icon_light: string;
  country_icon_dark: string;
}

export interface AHAIIScore {
  id: string;
  country_id: string;
  assessment_year: number;
  assessment_quarter?: number;
  
  // Overall Score
  total_score: number; // 0-100 scale
  global_ranking?: number;
  regional_ranking?: number;
  sub_regional_ranking?: number;
  
  // Pillar Scores
  human_capital_score: number;
  human_capital_clinical_literacy?: number;
  human_capital_informatics_capacity?: number;
  human_capital_workforce_pipeline?: number;
  
  physical_infrastructure_score: number;
  physical_digitization_level?: number;
  physical_computational_capacity?: number;
  physical_connectivity_reliability?: number;
  
  regulatory_infrastructure_score: number;
  regulatory_approval_pathways?: number;
  regulatory_data_governance?: number;
  regulatory_market_access?: number;
  
  economic_market_score: number;
  economic_market_maturity?: number;
  economic_financial_sustainability?: number;
  economic_research_funding?: number;
  
  // Tier Classification
  readiness_tier: 1 | 2 | 3;
  tier_justification?: string;
  
  // Data Quality
  overall_confidence_score?: number; // 0-1 scale
  data_completeness_percentage?: number;
  peer_review_status: 'peer_reviewed' | 'expert_validated' | 'pending' | 'disputed';
  
  // Benchmarking Context
  development_trajectory: 'improving' | 'stable' | 'declining' | 'rapid_growth';
  key_strengths: string[];
  priority_improvement_areas: string[];
  
  created_at: string;
  updated_at: string;
}

export interface CountryWithScore extends Country {
  ahaii_score?: AHAIIScore;
  recent_intelligence_count?: number;
  last_updated?: string;
}

export interface IntelligenceSignal {
  id: string;
  country_id: string;
  report_type: 'academic_scan' | 'news_monitoring' | 'policy_tracking' | 'market_analysis';
  report_title: string;
  report_summary: string;
  
  // Infrastructure Impact
  affects_human_capital: boolean;
  affects_physical_infrastructure: boolean;
  affects_regulatory_framework: boolean;
  affects_economic_market: boolean;
  
  impact_significance: 'high' | 'medium' | 'low';
  confidence_score: number; // 0-1 scale
  
  source_url?: string;
  publication_date: string;
  created_at: string;
}

export interface CountryCarouselData extends CountryWithScore {
  featured_intelligence?: IntelligenceSignal[];
  regional_rank_display?: string;
  score_trend?: {
    direction: 'up' | 'down' | 'stable';
    magnitude: 'significant' | 'moderate' | 'slight';
  };
}

// Utility type for the carousel component
export interface CarouselCountry {
  country: Country;
  score?: AHAIIScore;
  intelligence_preview?: {
    count: number;
    latest_update: string;
    key_development?: string;
  };
}