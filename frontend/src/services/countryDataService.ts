// Service for automatically generating country carousel data from ETL pipeline
import React from 'react';
import { Country, AHAIIScore, CountryWithScore, IntelligenceSignal } from '@/types/country';

interface ETLCountryData {
  country_id: string;
  recent_signals: IntelligenceSignal[];
  indicator_counts: {
    human_capital: number;
    physical_infrastructure: number;
    regulatory: number;
    economic: number;
  };
  data_freshness_score: number; // 0-1 based on how recent the data is
}

class CountryDataService {
  private baseApiUrl = process.env.NEXT_PUBLIC_API_URL || 
    (process.env.NODE_ENV === 'production' ? 'https://api.taifa-fiala.net' : 'http://localhost:8030');

  /**
   * Fetch all African countries with their current AHAII scores
   * Automatically calculated from ETL data
   */
  async getAllCountriesWithScores(): Promise<CountryWithScore[]> {
    try {
      const response = await fetch(`${this.baseApiUrl}/api/countries/with-scores`);
      if (!response.ok) throw new Error('Failed to fetch countries');
      
      const data = await response.json();
      return data.countries.map((country: any) => this.transformCountryData(country));
    } catch (error) {
      console.error('Error fetching countries:', error);
      // Fallback to static data during development
      return this.generateFallbackCountries();
    }
  }

  /**
   * Get featured countries for carousel based on:
   * - Tier 1 countries (top performers)
   * - Countries with recent significant activity
   * - Regional representatives
   * - Large population/GDP significance
   */
  async getFeaturedCountries(limit: number = 8): Promise<CountryWithScore[]> {
    try {
      const response = await fetch(`${this.baseApiUrl}/api/countries/featured?limit=${limit}`);
      if (!response.ok) throw new Error('Failed to fetch featured countries');
      
      const data = await response.json();
      return data.countries.map((country: any) => this.transformCountryData(country));
    } catch (error) {
      console.error('Error fetching featured countries:', error);
      const allCountries = await this.getAllCountriesWithScores();
      return this.selectFeaturedCountries(allCountries, limit);
    }
  }

  /**
   * Get countries by region with automatic filtering
   */
  async getCountriesByRegion(region: string): Promise<CountryWithScore[]> {
    try {
      const response = await fetch(`${this.baseApiUrl}/api/countries/by-region/${encodeURIComponent(region)}`);
      if (!response.ok) throw new Error('Failed to fetch countries by region');
      
      const data = await response.json();
      return data.countries.map((country: any) => this.transformCountryData(country));
    } catch (error) {
      console.error('Error fetching countries by region:', error);
      return [];
    }
  }

  /**
   * Get single country with full detail for country page
   */
  async getCountryDetails(countryId: string): Promise<CountryWithScore | null> {
    try {
      const response = await fetch(`${this.baseApiUrl}/api/countries/${countryId}/details`);
      if (!response.ok) return null;
      
      const data = await response.json();
      return this.transformCountryData(data.country);
    } catch (error) {
      console.error('Error fetching country details:', error);
      return null;
    }
  }

  /**
   * Transform API country data to frontend format
   * Automatically maps database fields to component props
   */
  private transformCountryData(apiData: any): CountryWithScore {
    const country: Country = {
      id: apiData.iso_code_alpha3.toLowerCase(),
      name: apiData.name,
      iso_code_alpha3: apiData.iso_code_alpha3,
      iso_code_alpha2: this.getISO2Code(apiData.iso_code_alpha3),
      region: apiData.region,
      population: apiData.population || 0,
      gdp_usd: apiData.gdp_usd || 0,
      healthcare_spending_percent_gdp: apiData.healthcare_spending_percent_gdp || 0,
      flag_image: this.getFlagImagePath(apiData.iso_code_alpha3),
      country_outline_image: this.getCountryImagePath(apiData.iso_code_alpha3),
      country_icon_light: this.getCountryIconPath(apiData.iso_code_alpha3, 'light'),
      country_icon_dark: this.getCountryIconPath(apiData.iso_code_alpha3, 'dark'),
    };

    // Transform AHAII score if available
    const ahaiiScore: AHAIIScore | undefined = apiData.ahaii_score ? {
      id: apiData.ahaii_score.id,
      country_id: country.id,
      assessment_year: apiData.ahaii_score.assessment_year,
      assessment_quarter: apiData.ahaii_score.assessment_quarter,
      total_score: apiData.ahaii_score.total_score,
      global_ranking: apiData.ahaii_score.global_ranking,
      regional_ranking: apiData.ahaii_score.regional_ranking,
      sub_regional_ranking: apiData.ahaii_score.sub_regional_ranking,
      human_capital_score: apiData.ahaii_score.human_capital_score,
      human_capital_clinical_literacy: apiData.ahaii_score.human_capital_clinical_literacy,
      human_capital_informatics_capacity: apiData.ahaii_score.human_capital_informatics_capacity,
      human_capital_workforce_pipeline: apiData.ahaii_score.human_capital_workforce_pipeline,
      physical_infrastructure_score: apiData.ahaii_score.physical_infrastructure_score,
      physical_digitization_level: apiData.ahaii_score.physical_digitization_level,
      physical_computational_capacity: apiData.ahaii_score.physical_computational_capacity,
      physical_connectivity_reliability: apiData.ahaii_score.physical_connectivity_reliability,
      regulatory_infrastructure_score: apiData.ahaii_score.regulatory_infrastructure_score,
      regulatory_approval_pathways: apiData.ahaii_score.regulatory_approval_pathways,
      regulatory_data_governance: apiData.ahaii_score.regulatory_data_governance,
      regulatory_market_access: apiData.ahaii_score.regulatory_market_access,
      economic_market_score: apiData.ahaii_score.economic_market_score,
      economic_market_maturity: apiData.ahaii_score.economic_market_maturity,
      economic_financial_sustainability: apiData.ahaii_score.economic_financial_sustainability,
      economic_research_funding: apiData.ahaii_score.economic_research_funding,
      readiness_tier: apiData.ahaii_score.readiness_tier,
      tier_justification: apiData.ahaii_score.tier_justification,
      overall_confidence_score: apiData.ahaii_score.overall_confidence_score,
      data_completeness_percentage: apiData.ahaii_score.data_completeness_percentage,
      peer_review_status: apiData.ahaii_score.peer_review_status || 'pending',
      development_trajectory: apiData.ahaii_score.development_trajectory || 'stable',
      key_strengths: apiData.ahaii_score.key_strengths || [],
      priority_improvement_areas: apiData.ahaii_score.priority_improvement_areas || [],
      created_at: apiData.ahaii_score.created_at,
      updated_at: apiData.ahaii_score.updated_at
    } : undefined;

    return {
      ...country,
      ahaii_score: ahaiiScore,
      recent_intelligence_count: apiData.recent_intelligence_count || 0,
      last_updated: apiData.last_updated
    };
  }

  /**
   * Automatically select featured countries based on multiple criteria
   */
  private selectFeaturedCountries(countries: CountryWithScore[], limit: number): CountryWithScore[] {
    // Scoring algorithm for featured selection
    const scoredCountries = countries.map(country => {
      let featureScore = 0;
      
      // High AHAII score (40% weight)
      if (country.ahaii_score) {
        featureScore += (country.ahaii_score.total_score / 100) * 40;
      }
      
      // Recent activity (30% weight) 
      if (country.recent_intelligence_count) {
        featureScore += Math.min(country.recent_intelligence_count / 50, 1) * 30;
      }
      
      // Economic significance (20% weight)
      const maxGDP = Math.max(...countries.map(c => c.gdp_usd));
      featureScore += (country.gdp_usd / maxGDP) * 20;
      
      // Population significance (10% weight)
      const maxPop = Math.max(...countries.map(c => c.population));
      featureScore += (country.population / maxPop) * 10;
      
      return { country, featureScore };
    });

    // Sort by feature score and ensure regional diversity
    const sorted = scoredCountries.sort((a, b) => b.featureScore - a.featureScore);
    const featured: CountryWithScore[] = [];
    const regionsUsed = new Set<string>();
    
    // First pass: Top scorers ensuring regional diversity
    for (const { country } of sorted) {
      if (featured.length >= limit) break;
      
      if (!regionsUsed.has(country.region) || featured.length >= 5) {
        featured.push(country);
        regionsUsed.add(country.region);
      }
    }
    
    // Second pass: Fill remaining slots with highest scorers
    for (const { country } of sorted) {
      if (featured.length >= limit) break;
      if (!featured.find(c => c.id === country.id)) {
        featured.push(country);
      }
    }
    
    return featured.slice(0, limit);
  }

  /**
   * Generate image paths automatically based on country ISO codes
   */
  private getFlagImagePath(iso3: string): string {
    const countryName = this.iso3ToImageName(iso3);
    return `/images/countries/${countryName}-flag.png`;
  }

  private getCountryImagePath(iso3: string): string {
    const countryName = this.iso3ToImageName(iso3);
    return `/images/countries/${countryName}-country.png`;
  }

  private getCountryIconPath(iso3: string, variant: 'light' | 'dark'): string {
    const countryName = this.iso3ToImageName(iso3);
    return `/images/svg-icons/country-icons/${countryName}-icon-${variant}.svg`;
  }

  /**
   * Map ISO3 codes to your image file naming convention
   */
  private iso3ToImageName(iso3: string): string {
    const mapping: Record<string, string> = {
      'AGO': 'angola',
      'BEN': 'benin',
      'BWA': 'botswana', // Note: image is 'botwana-flag.png' but country is 'botswana-country.png'
      'CIV': 'cote-divoire',
      'EGY': 'egypt',
      'ETH': 'ethiopia',
      'GHA': 'ghana',
      'KEN': 'kenya',
      'MUS': 'mauritius',
      'NGA': 'nigeria',
      'RWA': 'rwanda',
      'SEN': 'senegal',
      'SYC': 'seychelles',
      'ZAF': 'south-africa',
      'TUN': 'tunisia',
      'ZMB': 'zambia',
      // Add more mappings as needed for all 54 African countries
    };
    
    return mapping[iso3] || iso3.toLowerCase();
  }

  /**
   * Convert ISO3 to ISO2 codes
   */
  private getISO2Code(iso3: string): string {
    const mapping: Record<string, string> = {
      'AGO': 'ao', 'BEN': 'bj', 'BWA': 'bw', 'CIV': 'ci', 'EGY': 'eg',
      'ETH': 'et', 'GHA': 'gh', 'KEN': 'ke', 'MUS': 'mu', 'NGA': 'ng',
      'RWA': 'rw', 'SEN': 'sn', 'SYC': 'sc', 'ZAF': 'za', 'TUN': 'tn',
      'ZMB': 'zm',
      // Add all 54 African countries as needed
    };
    
    return mapping[iso3] || iso3.toLowerCase().slice(0, 2);
  }

  /**
   * Fallback static data for development
   */
  private generateFallbackCountries(): CountryWithScore[] {
    // Return the static data from countries.ts as fallback
    // This will be replaced by actual ETL data in production
    return [];
  }

  /**
   * Get countries with recent activity (for dynamic carousel rotation)
   */
  async getCountriesWithRecentActivity(hours: number = 24): Promise<CountryWithScore[]> {
    try {
      const response = await fetch(`${this.baseApiUrl}/api/countries/recent-activity?hours=${hours}`);
      if (!response.ok) throw new Error('Failed to fetch recent activity');
      
      const data = await response.json();
      return data.countries.map((country: any) => this.transformCountryData(country));
    } catch (error) {
      console.error('Error fetching recent activity:', error);
      return [];
    }
  }

  /**
   * Refresh carousel data (called periodically to show new intelligence)
   */
  async refreshCarouselData(): Promise<{
    featured: CountryWithScore[];
    recentActivity: CountryWithScore[];
    lastUpdated: string;
  }> {
    const [featured, recentActivity] = await Promise.all([
      this.getFeaturedCountries(8),
      this.getCountriesWithRecentActivity(24)
    ]);

    return {
      featured,
      recentActivity,
      lastUpdated: new Date().toISOString()
    };
  }
}

// Singleton instance
export const countryDataService = new CountryDataService();

// React Hook for easy component integration
export const useCountries = () => {
  const [countries, setCountries] = React.useState<CountryWithScore[]>([]);
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState<string | null>(null);

  const fetchCountries = React.useCallback(async (featured: boolean = true) => {
    try {
      setLoading(true);
      const data = featured 
        ? await countryDataService.getFeaturedCountries()
        : await countryDataService.getAllCountriesWithScores();
      setCountries(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch countries');
    } finally {
      setLoading(false);
    }
  }, []);

  React.useEffect(() => {
    fetchCountries();
  }, [fetchCountries]);

  return { countries, loading, error, refetch: fetchCountries };
};

// Export service instance as default
export default countryDataService;