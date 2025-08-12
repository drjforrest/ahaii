/**
 * AHAII (African Health AI Infrastructure Index) TypeScript Types
 * 
 * This file defines the comprehensive type system for the AHAII platform,
 * including country data, infrastructure scores, and health AI metrics.
 */

// ===============================================
// CORE PILLAR TYPES
// ===============================================

/**
 * The four pillars of health AI infrastructure assessment
 */
export type AHAIIPillarType = 'physical' | 'humanCapital' | 'regulatory' | 'economic';

/**
 * Individual pillar score and analysis
 */
export interface PillarScore {
  score: number; // 0-100 scale
  description: string;
  indicators?: HealthAIIndicator[];
  lastUpdated?: string;
  confidence?: number; // 0-1 scale indicating data quality
}

/**
 * Complete pillar assessment for a country
 */
export interface CountryPillars {
  physical: PillarScore;      // Medical-grade infrastructure, EMR systems, computational capacity
  humanCapital: PillarScore;  // Clinical AI literacy, biomedical informatics programs
  regulatory: PillarScore;    // Medical AI approval pathways, health data governance
  economic: PillarScore;      // Investment capacity, market maturity, sustainability
}

// ===============================================
// COUNTRY DATA STRUCTURES
// ===============================================

/**
 * Comprehensive country data for AHAII assessment
 */
export interface CountryData {
  // Basic identification
  id: string;
  name: string;
  code: string; // ISO country code (e.g., 'ZA', 'NG', 'KE')
  flag: string; // URL to flag image
  
  // Geographic and demographic context
  region: AfricanRegion;
  population?: number;
  gdpPerCapita?: number;
  healthExpenditurePerCapita?: number;
  
  // AHAII scores and assessment
  overallScore: number; // Weighted average of four pillars
  pillars: CountryPillars;
  
  // Descriptive analysis
  description: string;
  executiveSummary?: string;
  keyStrengths?: string[];
  keyWeaknesses?: string[];
  recommendations?: string[];
  
  // Metadata
  lastAssessment: string; // ISO date string
  dataQuality: DataQuality;
  sources?: DataSource[];
}

/**
 * African regional classifications for analysis
 */
export type AfricanRegion = 
  | 'Northern Africa'
  | 'Western Africa' 
  | 'Eastern Africa'
  | 'Central Africa'
  | 'Southern Africa';

/**
 * Data quality assessment for transparency
 */
export interface DataQuality {
  overallConfidence: number; // 0-1 scale
  primarySources: number; // Number of primary data sources
  expertValidation: boolean; // Whether expert review was conducted
  lastVerification: string; // ISO date string
}

/**
 * Data source attribution
 */
export interface DataSource {
  type: 'academic' | 'government' | 'industry' | 'international';
  name: string;
  url?: string;
  date: string;
  reliability: number; // 0-1 scale
}

// ===============================================
// HEALTH AI INDICATORS
// ===============================================

/**
 * Specific measurable indicators feeding into pillar scores
 */
export interface HealthAIIndicator {
  id: string;
  name: string;
  pillar: AHAIIPillarType;
  category: IndicatorCategory;
  value: number | string | boolean;
  unit?: string;
  trend?: TrendDirection;
  benchmark?: number; // International or regional benchmark
  source: string;
  date: string;
}

/**
 * Categories of health AI infrastructure indicators
 */
export type IndicatorCategory =
  // Physical Infrastructure
  | 'emr_adoption'
  | 'computational_capacity'
  | 'connectivity'
  | 'data_centers'
  | 'telemedicine_infrastructure'
  
  // Human Capital
  | 'clinical_ai_training'
  | 'biomedical_informatics'
  | 'healthcare_workforce'
  | 'research_capacity'
  | 'digital_literacy'
  
  // Regulatory
  | 'medical_ai_approval'
  | 'health_data_governance'
  | 'clinical_validation'
  | 'privacy_frameworks'
  | 'international_standards'
  
  // Economic
  | 'health_ai_investment'
  | 'market_maturity'
  | 'healthcare_financing'
  | 'innovation_ecosystem'
  | 'sustainability_metrics';

/**
 * Trend direction for indicators over time
 */
export type TrendDirection = 'improving' | 'stable' | 'declining' | 'unknown';

// ===============================================
// SCORING AND ANALYSIS
// ===============================================

/**
 * Historical scoring data for trend analysis
 */
export interface HistoricalScore {
  date: string;
  overallScore: number;
  pillars: {
    physical: number;
    humanCapital: number;
    regulatory: number;
    economic: number;
  };
}

/**
 * Country comparison data
 */
export interface CountryComparison {
  country: string;
  rank: number;
  score: number;
  change: number; // Year-over-year change
}

/**
 * Readiness classification levels
 */
export type ReadinessLevel = 
  | 'advanced'     // 80-100: Ready for comprehensive health AI deployment
  | 'developing'   // 60-79: Solid foundation, strategic gaps to address
  | 'emerging'     // 40-59: Basic capabilities, significant investment needed
  | 'nascent';     // 0-39: Early stage, fundamental infrastructure required

/**
 * Investment priority recommendations
 */
export interface InvestmentPriority {
  pillar: AHAIIPillarType;
  priority: 'critical' | 'high' | 'medium' | 'low';
  impact: number; // Expected impact on overall score (0-10)
  timeline: 'immediate' | 'short-term' | 'medium-term' | 'long-term';
  description: string;
  estimatedCost?: string;
}

// ===============================================
// API RESPONSE TYPES
// ===============================================

/**
 * Standard API response wrapper
 */
export interface APIResponse<T> {
  data: T;
  success: boolean;
  message?: string;
  timestamp: string;
}

/**
 * Country profiles API response
 */
export interface CountriesResponse {
  countries: CountryData[];
  totalCount: number;
  lastUpdated: string;
  methodology: string;
}

/**
 * Individual country detail response
 */
export interface CountryDetailResponse extends CountryData {
  historicalScores: HistoricalScore[];
  regionalComparison: CountryComparison[];
  investmentPriorities: InvestmentPriority[];
  detailedIndicators: HealthAIIndicator[];
}

// ===============================================
// FILTERING AND SEARCH
// ===============================================

/**
 * Search and filter parameters
 */
export interface CountryFilters {
  regions?: AfricanRegion[];
  scoreRange?: {
    min: number;
    max: number;
  };
  readinessLevels?: ReadinessLevel[];
  pillars?: {
    [key in AHAIIPillarType]?: {
      min: number;
      max: number;
    };
  };
  populationRange?: {
    min: number;
    max: number;
  };
  searchQuery?: string;
}

/**
 * Sorting options for country lists
 */
export interface SortOptions {
  field: 'name' | 'overallScore' | 'population' | AHAIIPillarType;
  direction: 'asc' | 'desc';
}

// ===============================================
// COMPONENT PROPS TYPES
// ===============================================

/**
 * Props for country card components
 */
export interface CountryCardProps {
  country: CountryData;
  variant?: 'default' | 'compact' | 'detailed';
  showTrends?: boolean;
  onSelect?: (country: CountryData) => void;
  className?: string;
}

/**
 * Props for pillar visualization components
 */
export interface PillarVisualizationProps {
  pillars: CountryPillars;
  variant?: 'bars' | 'radar' | 'cards';
  interactive?: boolean;
  showDescriptions?: boolean;
}

/**
 * Props for country comparison components
 */
export interface CountryComparisonProps {
  countries: CountryData[];
  focusPillar?: AHAIIPillarType;
  showHistorical?: boolean;
}