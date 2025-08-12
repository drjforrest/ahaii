import { Country, AHAIIScore, CountryWithScore } from '@/types/country';

// Sample AHAII Scores - these would normally come from the database
const sampleScores: Record<string, AHAIIScore> = {
  'rwa': {
    id: '1',
    country_id: 'rwa',
    assessment_year: 2024,
    total_score: 78.5,
    global_ranking: 23,
    regional_ranking: 1,
    human_capital_score: 82.3,
    physical_infrastructure_score: 71.2,
    regulatory_infrastructure_score: 79.8,
    economic_market_score: 68.9,
    readiness_tier: 1,
    development_trajectory: 'improving',
    key_strengths: [
      'Strong digital health strategy',
      'Government commitment to AI',
      'Established EMR systems',
      'Medical training partnerships'
    ],
    priority_improvement_areas: [
      'Increase healthcare funding',
      'Expand rural connectivity',
      'Develop local AI talent'
    ],
    peer_review_status: 'peer_reviewed',
    created_at: '2024-01-01',
    updated_at: '2024-01-01'
  },
  'zaf': {
    id: '2',
    country_id: 'zaf',
    assessment_year: 2024,
    total_score: 85.2,
    global_ranking: 18,
    regional_ranking: 2,
    human_capital_score: 88.1,
    physical_infrastructure_score: 79.5,
    regulatory_infrastructure_score: 84.7,
    economic_market_score: 72.3,
    readiness_tier: 1,
    development_trajectory: 'stable',
    key_strengths: [
      'Advanced healthcare infrastructure',
      'Strong research institutions',
      'Established medical AI companies',
      'Robust regulatory framework'
    ],
    priority_improvement_areas: [
      'Address healthcare inequality',
      'Improve rural access',
      'Strengthen data governance'
    ],
    peer_review_status: 'peer_reviewed',
    created_at: '2024-01-01',
    updated_at: '2024-01-01'
  },
  'mus': {
    id: '3',
    country_id: 'mus',
    assessment_year: 2024,
    total_score: 72.8,
    global_ranking: 28,
    regional_ranking: 3,
    human_capital_score: 69.4,
    physical_infrastructure_score: 75.8,
    regulatory_infrastructure_score: 71.2,
    economic_market_score: 74.9,
    readiness_tier: 1,
    development_trajectory: 'improving',
    key_strengths: [
      'High digital connectivity',
      'Government digitization focus',
      'Strong economic indicators',
      'Healthcare investment'
    ],
    priority_improvement_areas: [
      'Develop AI expertise',
      'Establish clinical validation',
      'Expand telemedicine'
    ],
    peer_review_status: 'expert_validated',
    created_at: '2024-01-01',
    updated_at: '2024-01-01'
  },
  'ken': {
    id: '4',
    country_id: 'ken',
    assessment_year: 2024,
    total_score: 65.7,
    global_ranking: 42,
    regional_ranking: 4,
    human_capital_score: 71.2,
    physical_infrastructure_score: 58.9,
    regulatory_infrastructure_score: 67.3,
    economic_market_score: 65.4,
    readiness_tier: 2,
    development_trajectory: 'improving',
    key_strengths: [
      'Innovation ecosystem',
      'Health tech startups',
      'Mobile health adoption',
      'University partnerships'
    ],
    priority_improvement_areas: [
      'Improve rural infrastructure',
      'Strengthen regulatory capacity',
      'Increase healthcare investment'
    ],
    peer_review_status: 'pending',
    created_at: '2024-01-01',
    updated_at: '2024-01-01'
  },
  'nga': {
    id: '5',
    country_id: 'nga',
    assessment_year: 2024,
    total_score: 58.3,
    global_ranking: 58,
    regional_ranking: 8,
    human_capital_score: 62.7,
    physical_infrastructure_score: 52.1,
    regulatory_infrastructure_score: 59.8,
    economic_market_score: 58.6,
    readiness_tier: 2,
    development_trajectory: 'improving',
    key_strengths: [
      'Large market potential',
      'Growing tech sector',
      'Medical schools capacity',
      'Diaspora expertise'
    ],
    priority_improvement_areas: [
      'Strengthen healthcare infrastructure',
      'Improve regulatory framework',
      'Address funding gaps'
    ],
    peer_review_status: 'pending',
    created_at: '2024-01-01',
    updated_at: '2024-01-01'
  }
};

// Base country data using your image assets
export const countries: Country[] = [
  {
    id: 'ago',
    name: 'Angola',
    iso_code_alpha3: 'AGO',
    iso_code_alpha2: 'ao',
    region: 'Central Africa',
    population: 33930000,
    gdp_usd: 106930000000,
    healthcare_spending_percent_gdp: 2.9,
    flag_image: '/images/countries/angola-flag.png',
    country_outline_image: '/images/countries/angola-country.png',
    country_icon_light: '/images/svg-icons/country-icons/angola-icon-light.svg',
    country_icon_dark: '/images/svg-icons/country-icons/angola-icon-dark.svg',
  },
  {
    id: 'ben',
    name: 'Benin',
    iso_code_alpha3: 'BEN',
    iso_code_alpha2: 'bj',
    region: 'West Africa',
    population: 12450000,
    gdp_usd: 17400000000,
    healthcare_spending_percent_gdp: 2.6,
    flag_image: '/images/countries/benin-flag.png',
    country_outline_image: '/images/countries/benin-country.png',
    country_icon_light: '/images/svg-icons/country-icons/benin-icon-light.svg',
    country_icon_dark: '/images/svg-icons/country-icons/benin-icon-dark.svg',
  },
  {
    id: 'bwa',
    name: 'Botswana',
    iso_code_alpha3: 'BWA',
    iso_code_alpha2: 'bw',
    region: 'Southern Africa',
    population: 2400000,
    gdp_usd: 18340000000,
    healthcare_spending_percent_gdp: 5.4,
    flag_image: '/images/countries/botwana-flag.png', // Note: keeping your filename spelling
    country_outline_image: '/images/countries/botswana-country.png',
    country_icon_light: '/images/svg-icons/country-icons/botswana-icon-light.svg',
    country_icon_dark: '/images/svg-icons/country-icons/botwana-icon-dark.svg', // Note: keeping your filename spelling
  },
  {
    id: 'civ',
    name: "Côte d'Ivoire",
    iso_code_alpha3: 'CIV',
    iso_code_alpha2: 'ci',
    region: 'West Africa',
    population: 27500000,
    gdp_usd: 70990000000,
    healthcare_spending_percent_gdp: 3.3,
    flag_image: '/images/countries/cote-divoire-flag.png',
    country_outline_image: '/images/countries/cote-divoire-country.png',
    country_icon_light: '/images/svg-icons/country-icons/cote-divoire-icon-light.svg',
    country_icon_dark: '/images/svg-icons/country-icons/cote-divoire-icon-dark.svg',
  },
  {
    id: 'egy',
    name: 'Egypt',
    iso_code_alpha3: 'EGY',
    iso_code_alpha2: 'eg',
    region: 'North Africa',
    population: 104000000,
    gdp_usd: 469440000000,
    healthcare_spending_percent_gdp: 4.4,
    flag_image: '/images/countries/egypt-flag.png',
    country_outline_image: '/images/countries/egypt-country.png',
    country_icon_light: '/images/svg-icons/country-icons/egypt-icon-light.svg',
    country_icon_dark: '/images/svg-icons/country-icons/egypt-icon-dark.svg',
  },
  {
    id: 'eth',
    name: 'Ethiopia',
    iso_code_alpha3: 'ETH',
    iso_code_alpha2: 'et',
    region: 'East Africa',
    population: 120300000,
    gdp_usd: 111270000000,
    healthcare_spending_percent_gdp: 3.5,
    flag_image: '/images/countries/ethiopia-flag.png',
    country_outline_image: '/images/countries/ethiopia-country.png',
    country_icon_light: '/images/svg-icons/country-icons/ethiopia-icon-light.svg',
    country_icon_dark: '/images/svg-icons/country-icons/ethiopia-icon-dark.svg',
  },
  {
    id: 'gha',
    name: 'Ghana',
    iso_code_alpha3: 'GHA',
    iso_code_alpha2: 'gh',
    region: 'West Africa',
    population: 32830000,
    gdp_usd: 77590000000,
    healthcare_spending_percent_gdp: 3.2,
    flag_image: '/images/countries/ghana-flag.png',
    country_outline_image: '/images/countries/ghana-coun try.png', // Note: keeping your filename with space
    country_icon_light: '/images/svg-icons/country-icons/ghana-icon-light.svg',
    country_icon_dark: '/images/svg-icons/country-icons/ghana-icon-dark.svg',
  },
  {
    id: 'ken',
    name: 'Kenya',
    iso_code_alpha3: 'KEN',
    iso_code_alpha2: 'ke',
    region: 'East Africa',
    population: 54000000,
    gdp_usd: 115700000000,
    healthcare_spending_percent_gdp: 4.3,
    flag_image: '/images/countries/kenya-flag.png',
    country_outline_image: '/images/countries/kenya-country.png',
    country_icon_light: '/images/svg-icons/country-icons/kenya-icon-light.svg',
    country_icon_dark: '/images/svg-icons/country-icons/kenya-icon-dark.svg',
  },
  {
    id: 'mus',
    name: 'Mauritius',
    iso_code_alpha3: 'MUS',
    iso_code_alpha2: 'mu',
    region: 'East Africa',
    population: 1270000,
    gdp_usd: 14780000000,
    healthcare_spending_percent_gdp: 6.0,
    flag_image: '/images/countries/mauritius-flag.png',
    country_outline_image: '/images/countries/mauritius-country.png',
    country_icon_light: '/images/svg-icons/country-icons/mauritius-icon-light.svg',
    country_icon_dark: '/images/svg-icons/country-icons/mauritius-icon-dark.svg',
  },
  {
    id: 'nga',
    name: 'Nigeria',
    iso_code_alpha3: 'NGA',
    iso_code_alpha2: 'ng',
    region: 'West Africa',
    population: 218500000,
    gdp_usd: 440780000000,
    healthcare_spending_percent_gdp: 3.4,
    flag_image: '/images/countries/nigeria-flag.png',
    country_outline_image: '/images/countries/nigeria-country.png',
    country_icon_light: '/images/svg-icons/country-icons/nigeria-icon-light.svg',
    country_icon_dark: '/images/svg-icons/country-icons/nigeria-icon-dark.svg',
  },
  {
    id: 'rwa',
    name: 'Rwanda',
    iso_code_alpha3: 'RWA',
    iso_code_alpha2: 'rw',
    region: 'East Africa',
    population: 13460000,
    gdp_usd: 11070000000,
    healthcare_spending_percent_gdp: 7.5,
    flag_image: '/images/countries/rwanda-flag.png',
    country_outline_image: '/images/countries/rwanda-country.png',
    country_icon_light: '/images/svg-icons/country-icons/rwanda-icon-light.svg',
    country_icon_dark: '/images/svg-icons/country-icons/rwanda-icon-dark.svg',
  },
  {
    id: 'sen',
    name: 'Senegal',
    iso_code_alpha3: 'SEN',
    iso_code_alpha2: 'sn',
    region: 'West Africa',
    population: 17200000,
    gdp_usd: 27680000000,
    healthcare_spending_percent_gdp: 3.8,
    flag_image: '/images/countries/senegal-flag.png',
    country_outline_image: '/images/countries/senegal-country.png',
    country_icon_light: '/images/svg-icons/country-icons/senegal-icon-light.svg',
    country_icon_dark: '/images/svg-icons/country-icons/senegal-icon-dark.svg',
  },
  {
    id: 'syc',
    name: 'Seychelles',
    iso_code_alpha3: 'SYC',
    iso_code_alpha2: 'sc',
    region: 'East Africa',
    population: 99000,
    gdp_usd: 1730000000,
    healthcare_spending_percent_gdp: 4.2,
    flag_image: '/images/countries/seychelles-flag.png',
    country_outline_image: '/images/countries/seychelles-country.png',
    country_icon_light: '/images/svg-icons/country-icons/seychelles-icon-light.svg',
    country_icon_dark: '/images/svg-icons/country-icons/seychelles-icon-dark.svg',
  },
  {
    id: 'zaf',
    name: 'South Africa',
    iso_code_alpha3: 'ZAF',
    iso_code_alpha2: 'za',
    region: 'Southern Africa',
    population: 59890000,
    gdp_usd: 419010000000,
    healthcare_spending_percent_gdp: 8.1,
    flag_image: '/images/countries/south-africa-flag.png',
    country_outline_image: '/images/countries/south-africa-country.png',
    country_icon_light: '/images/svg-icons/country-icons/south-africa-icon-light.svg',
    country_icon_dark: '/images/svg-icons/country-icons/south-africa-icon-dark.svg',
  },
  {
    id: 'tun',
    name: 'Tunisia',
    iso_code_alpha3: 'TUN',
    iso_code_alpha2: 'tn',
    region: 'North Africa',
    population: 11935000,
    gdp_usd: 46940000000,
    healthcare_spending_percent_gdp: 7.2,
    flag_image: '/images/countries/tunisia-flag.png',
    country_outline_image: '/images/countries/tunisia-country.png',
    country_icon_light: '/images/svg-icons/country-icons/tunisia-icon-light.svg',
    country_icon_dark: '/images/svg-icons/country-icons/tunisia-icon-dark.svg',
  },
  {
    id: 'zmb',
    name: 'Zambia',
    iso_code_alpha3: 'ZMB',
    iso_code_alpha2: 'zm',
    region: 'Southern Africa',
    population: 19470000,
    gdp_usd: 22150000000,
    healthcare_spending_percent_gdp: 4.9,
    flag_image: '/images/countries/zambia-flag.png',
    country_outline_image: '/images/countries/zambia-country.png',
    country_icon_light: '/images/svg-icons/country-icons/zambia-icon-light.svg',
    country_icon_dark: '/images/svg-icons/country-icons/zambia-icon-dark.svg',
  },
];

// Combine countries with their scores for the carousel
export const countriesWithScores: CountryWithScore[] = countries.map(country => ({
  ...country,
  ahaii_score: sampleScores[country.id],
  recent_intelligence_count: Math.floor(Math.random() * 25) + 5, // Sample data
  last_updated: '2024-01-15' // Sample data
}));

// Featured countries for the carousel (top performers + interesting cases)
export const featuredCountries = [
  'zaf', // South Africa - Top performer
  'rwa', // Rwanda - Rapid improvement
  'mus', // Mauritius - Island nation success
  'ken', // Kenya - Innovation hub
  'nga', // Nigeria - Largest market
  'egy', // Egypt - North Africa leader
  'eth', // Ethiopia - Emerging player
  'gha', // Ghana - West Africa potential
].map(id => countriesWithScores.find(c => c.id === id)).filter(Boolean) as CountryWithScore[];

// Helper functions
export const getCountryById = (id: string): CountryWithScore | undefined => 
  countriesWithScores.find(country => country.id === id);

export const getCountryByISO = (iso: string): CountryWithScore | undefined => 
  countriesWithScores.find(country => 
    country.iso_code_alpha3.toLowerCase() === iso.toLowerCase() ||
    country.iso_code_alpha2.toLowerCase() === iso.toLowerCase()
  );

export const getTierColor = (tier?: number): string => {
  switch (tier) {
    case 1: return 'text-gradient gradient-human-capital';
    case 2: return 'text-gradient gradient-physical';
    case 3: return 'text-gradient gradient-economic';
    default: return 'text-muted-foreground';
  }
};

export const getTierBadgeColor = (tier?: number): string => {
  switch (tier) {
    case 1: return 'domain-human-capital';
    case 2: return 'domain-physical'; 
    case 3: return 'domain-economic';
    default: return 'bg-section-3';
  }
};