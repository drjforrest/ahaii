/**
 * AHAII Service - Frontend service for AHAII assessment API integration
 * Connects to the AHAII backend assessment pipeline
 */

export interface AHAIIAssessmentRequest {
  countries: string[];
  include_policy_indicators: boolean;
  include_ecosystem_mapping: boolean;
  include_expert_validation: boolean;
  generate_report: boolean;
  methodology_version?: string;
}

export interface AHAIICountryScore {
  country_code: string;
  country_name: string;
  total_score: number;
  tier: number;
  regional_rank?: number;
  pillar_scores: {
    human_capital: number;
    physical_infrastructure: number;
    regulatory_framework: number;
    economic_market: number;
  };
  confidence_score: number;
  confidence_interval?: [number, number];
  data_quality_grade?: string;
}

export interface AHAIIAssessmentResponse {
  assessment_id: string;
  assessment_date: string;
  methodology_version: string;
  countries_assessed: string[];
  total_countries: number;
  regional_average_score?: number;
  data_quality_grade?: string;
  country_scores: AHAIICountryScore[];
}

export interface AHAIIAssessmentStatus {
  status: 'pending' | 'in_progress' | 'completed' | 'failed';
  phases_completed: string[];
  current_phase: string;
  overall_progress: number;
  summary: any;
}

export interface AHAIIHealthStatus {
  status: 'healthy' | 'degraded' | 'unhealthy';
  timestamp: string;
  connectivity: {
    world_bank_api: boolean;
    local_databases: boolean;
    file_system_access: boolean;
    dependencies: boolean;
  };
  all_systems_operational: boolean;
}

export interface AHAIIMethodologyInfo {
  framework: {
    name: string;
    version: string;
    pillars: {
      [key: string]: {
        weight: number;
        description: string;
      };
    };
  };
  data_sources: {
    [key: string]: string;
  };
  scoring_methodology: {
    normalization: string;
    aggregation: string;
    confidence_adjustment: string;
    tier_classification: string;
  };
}

class AHAIIService {
  private baseUrl: string;
  
  constructor() {
    // Check if we're running in the browser and get the current host
    if (typeof window !== 'undefined') {
      const protocol = window.location.protocol;
      const hostname = window.location.hostname;
      
      // Use environment variable if available, otherwise construct from current location
      this.baseUrl = process.env.NEXT_PUBLIC_AHAII_API_URL || 
        `${protocol}//${hostname}:8000`;
    } else {
      // Server-side fallback
      this.baseUrl = process.env.NEXT_PUBLIC_AHAII_API_URL || 
        'http://localhost:8000';
    }
    
    console.log('AHAII Service initialized with base URL:', this.baseUrl);
  }

  /**
   * Check AHAII system health
   */
  async checkHealth(): Promise<AHAIIHealthStatus> {
    try {
      console.log('🔍 Checking AHAII system health...');
      const response = await fetch(`${this.baseUrl}/api/ahaii/health`);
      if (!response.ok) {
        throw new Error(`Health check failed: ${response.status}`);
      }
      const data = await response.json();
      console.log('✅ AHAII health check successful:', data);
      return data;
    } catch (error) {
      console.error('❌ AHAII health check failed:', error);
      throw error;
    }
  }

  /**
   * Get AHAII methodology information
   */
  async getMethodology(): Promise<AHAIIMethodologyInfo> {
    try {
      console.log('📖 Fetching AHAII methodology...');
      const response = await fetch(`${this.baseUrl}/api/ahaii/methodology`);
      if (!response.ok) {
        throw new Error(`Failed to fetch methodology: ${response.status}`);
      }
      const data = await response.json();
      console.log('✅ AHAII methodology fetched successfully');
      return data;
    } catch (error) {
      console.error('❌ Failed to fetch AHAII methodology:', error);
      throw error;
    }
  }

  /**
   * Start a complete AHAII assessment
   */
  async startAssessment(request: AHAIIAssessmentRequest): Promise<{ 
    message: string; 
    status: string; 
    countries: string[];
    estimated_completion: string;
  }> {
    try {
      console.log('🚀 Starting AHAII assessment for countries:', request.countries);
      const response = await fetch(`${this.baseUrl}/api/ahaii/run-complete-assessment`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        throw new Error(`Assessment start failed: ${response.status}`);
      }

      const data = await response.json();
      console.log('✅ AHAII assessment started successfully:', data);
      return data;
    } catch (error) {
      console.error('❌ Failed to start AHAII assessment:', error);
      throw error;
    }
  }

  /**
   * Get current assessment status
   */
  async getAssessmentStatus(): Promise<AHAIIAssessmentStatus> {
    try {
      console.log('📊 Checking AHAII assessment status...');
      const response = await fetch(`${this.baseUrl}/api/ahaii/status`);
      if (!response.ok) {
        throw new Error(`Status check failed: ${response.status}`);
      }
      const data = await response.json();
      console.log('📈 AHAII assessment status:', data);
      return data;
    } catch (error) {
      console.error('❌ Failed to get assessment status:', error);
      throw error;
    }
  }

  /**
   * Get AHAII scores for countries
   */
  async getScores(format: 'summary' | 'detailed' = 'summary'): Promise<AHAIIAssessmentResponse> {
    try {
      console.log(`📊 Fetching AHAII scores (${format} format)...`);
      const response = await fetch(`${this.baseUrl}/api/ahaii/scores?format=${format}`);
      if (!response.ok) {
        throw new Error(`Failed to fetch scores: ${response.status}`);
      }
      const data = await response.json();
      console.log('✅ AHAII scores fetched successfully');
      return data;
    } catch (error) {
      console.error('❌ Failed to fetch AHAII scores:', error);
      throw error;
    }
  }

  /**
   * Get list of supported countries
   */
  async getSupportedCountries(): Promise<{ countries: string[]; total_countries: number }> {
    try {
      console.log('🌍 Fetching supported countries...');
      const response = await fetch(`${this.baseUrl}/api/ahaii/countries`);
      if (!response.ok) {
        throw new Error(`Failed to fetch countries: ${response.status}`);
      }
      const data = await response.json();
      console.log('✅ Supported countries fetched successfully:', data);
      return data;
    } catch (error) {
      console.error('❌ Failed to fetch supported countries:', error);
      throw error;
    }
  }

  /**
   * Trigger data collection for specific countries
   */
  async collectData(countries?: string[]): Promise<{ message: string; run_id: string; status: string }> {
    try {
      console.log('🔄 Starting AHAII data collection...');
      const url = new URL(`${this.baseUrl}/api/ahaii/collect-data`);
      if (countries && countries.length > 0) {
        url.searchParams.append('countries', countries.join(','));
      }

      const response = await fetch(url.toString(), {
        method: 'POST',
      });

      if (!response.ok) {
        throw new Error(`Data collection failed: ${response.status}`);
      }

      const data = await response.json();
      console.log('✅ AHAII data collection started:', data);
      return data;
    } catch (error) {
      console.error('❌ Failed to start data collection:', error);
      throw error;
    }
  }

  /**
   * Calculate AHAII scores
   */
  async calculateScores(): Promise<{ message: string; assessment_id: string; status: string }> {
    try {
      console.log('🧮 Starting AHAII score calculation...');
      const response = await fetch(`${this.baseUrl}/api/ahaii/calculate-scores`, {
        method: 'POST',
      });

      if (!response.ok) {
        throw new Error(`Score calculation failed: ${response.status}`);
      }

      const data = await response.json();
      console.log('✅ AHAII score calculation started:', data);
      return data;
    } catch (error) {
      console.error('❌ Failed to start score calculation:', error);
      throw error;
    }
  }

  /**
   * Generate AHAII assessment report
   */
  async generateReport(): Promise<{ message: string; report_id: string; status: string }> {
    try {
      console.log('📄 Generating AHAII assessment report...');
      const response = await fetch(`${this.baseUrl}/api/ahaii/generate-report`, {
        method: 'POST',
      });

      if (!response.ok) {
        throw new Error(`Report generation failed: ${response.status}`);
      }

      const data = await response.json();
      console.log('✅ AHAII report generation started:', data);
      return data;
    } catch (error) {
      console.error('❌ Failed to generate report:', error);
      throw error;
    }
  }

  /**
   * Poll assessment status until completion
   */
  async pollAssessmentStatus(
    onProgress?: (status: AHAIIAssessmentStatus) => void,
    maxAttempts: number = 120,
    interval: number = 5000
  ): Promise<AHAIIAssessmentStatus> {
    let attempts = 0;
    
    while (attempts < maxAttempts) {
      try {
        const status = await this.getAssessmentStatus();
        
        if (onProgress) {
          onProgress(status);
        }
        
        if (status.status === 'completed' || status.status === 'failed') {
          return status;
        }
        
        await new Promise(resolve => setTimeout(resolve, interval));
        attempts++;
      } catch (error) {
        console.warn(`Status check attempt ${attempts + 1} failed:`, error);
        attempts++;
        await new Promise(resolve => setTimeout(resolve, interval));
      }
    }
    
    throw new Error('Assessment polling timed out');
  }
}

// Singleton instance
export const ahaiiService = new AHAIIService();

// React Hook for AHAII assessment management
import { useState, useCallback, useEffect } from 'react';

export interface UseAHAIIAssessmentResult {
  isRunning: boolean;
  currentStatus: AHAIIAssessmentStatus | null;
  scores: AHAIIAssessmentResponse | null;
  error: string | null;
  startAssessment: (request: AHAIIAssessmentRequest) => Promise<void>;
  refreshStatus: () => Promise<void>;
  refreshScores: () => Promise<void>;
}

export const useAHAIIAssessment = (): UseAHAIIAssessmentResult => {
  const [isRunning, setIsRunning] = useState(false);
  const [currentStatus, setCurrentStatus] = useState<AHAIIAssessmentStatus | null>(null);
  const [scores, setScores] = useState<AHAIIAssessmentResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const refreshStatus = useCallback(async () => {
    try {
      const status = await ahaiiService.getAssessmentStatus();
      setCurrentStatus(status);
      setIsRunning(status.status === 'in_progress');
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to get status');
    }
  }, []);

  const refreshScores = useCallback(async () => {
    try {
      const scoresData = await ahaiiService.getScores('detailed');
      setScores(scoresData);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to get scores');
    }
  }, []);

  const startAssessment = useCallback(async (request: AHAIIAssessmentRequest) => {
    try {
      setError(null);
      setIsRunning(true);
      
      await ahaiiService.startAssessment(request);
      
      // Poll for completion
      await ahaiiService.pollAssessmentStatus(
        (status) => setCurrentStatus(status),
        120, // 10 minutes max
        5000 // Check every 5 seconds
      );
      
      // Refresh scores when complete
      await refreshScores();
      setIsRunning(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Assessment failed');
      setIsRunning(false);
    }
  }, [refreshScores]);

  // Auto-refresh status every 10 seconds when running
  useEffect(() => {
    if (!isRunning) return;

    const interval = setInterval(refreshStatus, 10000);
    return () => clearInterval(interval);
  }, [isRunning, refreshStatus]);

  return {
    isRunning,
    currentStatus,
    scores,
    error,
    startAssessment,
    refreshStatus,
    refreshScores,
  };
};

export default ahaiiService;