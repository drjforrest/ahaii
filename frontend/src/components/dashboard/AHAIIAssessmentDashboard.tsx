'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { useAHAIIAssessment, ahaiiService, AHAIIAssessmentRequest } from '@/services/ahaiiService';

interface AHAIIAssessmentDashboardProps {
  className?: string;
}

const PILOT_COUNTRIES = ['ZAF', 'KEN', 'NGA', 'GHA', 'EGY'];

const tierLabels = {
  1: { label: 'Implementation Ready', color: 'bg-green-500' },
  2: { label: 'Foundation Building', color: 'bg-yellow-500' },
  3: { label: 'Development', color: 'bg-red-500' }
};

const pillarNames = {
  human_capital: 'Human Capital',
  physical_infrastructure: 'Physical Infrastructure', 
  regulatory_framework: 'Regulatory Framework',
  economic_market: 'Economic Market'
};

export const AHAIIAssessmentDashboard: React.FC<AHAIIAssessmentDashboardProps> = ({ 
  className = '' 
}) => {
  const {
    isRunning,
    currentStatus,
    scores,
    error,
    startAssessment,
    refreshStatus,
    refreshScores
  } = useAHAIIAssessment();

  const [systemHealth, setSystemHealth] = useState<any>(null);
  const [methodology, setMethodology] = useState<any>(null);
  const [selectedCountries, setSelectedCountries] = useState<string[]>(PILOT_COUNTRIES);

  // Load initial data
  useEffect(() => {
    const loadInitialData = async () => {
      try {
        const [healthData, methodologyData] = await Promise.all([
          ahaiiService.checkHealth(),
          ahaiiService.getMethodology()
        ]);
        setSystemHealth(healthData);
        setMethodology(methodologyData);
        
        // Also try to get existing scores
        try {
          await refreshScores();
        } catch (e) {
          // It's ok if there are no existing scores
        }
      } catch (error) {
        console.error('Failed to load initial data:', error);
      }
    };

    loadInitialData();
  }, [refreshScores]);

  const handleStartAssessment = async () => {
    const request: AHAIIAssessmentRequest = {
      countries: selectedCountries,
      include_policy_indicators: true,
      include_ecosystem_mapping: true,
      include_expert_validation: false, // Disabled for demo
      generate_report: true,
      methodology_version: '1.0'
    };

    await startAssessment(request);
  };

  const formatProgress = (progress: number) => {
    return `${Math.round(progress * 100)}%`;
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'text-green-600';
      case 'in_progress': return 'text-blue-600';
      case 'failed': return 'text-red-600';
      default: return 'text-gray-600';
    }
  };

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">AHAII Assessment Dashboard</h2>
          <p className="text-gray-600">African Health AI Infrastructure Index - Live Assessment</p>
        </div>
        <div className="flex gap-3">
          <Button 
            onClick={refreshStatus} 
            variant="outline"
            disabled={isRunning}
          >
            Refresh Status
          </Button>
          <Button 
            onClick={handleStartAssessment}
            disabled={isRunning || !systemHealth?.all_systems_operational}
          >
            {isRunning ? 'Assessment Running...' : 'Start Assessment'}
          </Button>
        </div>
      </div>

      {/* System Health */}
      {systemHealth && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              System Health
              <Badge variant={systemHealth.all_systems_operational ? 'default' : 'destructive'}>
                {systemHealth.status}
              </Badge>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {Object.entries(systemHealth.connectivity).map(([system, status]) => (
                <div key={system} className="flex items-center gap-2">
                  <div className={`w-3 h-3 rounded-full ${status ? 'bg-green-500' : 'bg-red-500'}`} />
                  <span className="text-sm">{system.replace(/_/g, ' ')}</span>
                </div>
              ))}
            </div>
            <p className="text-xs text-gray-500 mt-2">
              Last checked: {new Date(systemHealth.timestamp).toLocaleString()}
            </p>
          </CardContent>
        </Card>
      )}

      {/* Current Assessment Status */}
      {currentStatus && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              Assessment Status
              <Badge variant={currentStatus.status === 'completed' ? 'default' : 'secondary'}>
                {currentStatus.status}
              </Badge>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div>
                <div className="flex justify-between text-sm">
                  <span>Overall Progress</span>
                  <span>{formatProgress(currentStatus.overall_progress)}</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2 mt-1">
                  <div 
                    className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: formatProgress(currentStatus.overall_progress) }}
                  />
                </div>
              </div>
              
              {currentStatus.current_phase && (
                <div>
                  <span className="text-sm font-medium">Current Phase: </span>
                  <span className="text-sm">{currentStatus.current_phase.replace(/_/g, ' ')}</span>
                </div>
              )}

              {currentStatus.phases_completed.length > 0 && (
                <div>
                  <span className="text-sm font-medium">Completed Phases: </span>
                  <div className="flex flex-wrap gap-1 mt-1">
                    {currentStatus.phases_completed.map((phase, index) => (
                      <Badge key={index} variant="outline" className="text-xs">
                        {phase.replace(/_/g, ' ')}
                      </Badge>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Error Display */}
      {error && (
        <Card className="border-red-200">
          <CardHeader>
            <CardTitle className="text-red-600">Error</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-red-600">{error}</p>
          </CardContent>
        </Card>
      )}

      {/* Assessment Results */}
      {scores && (
        <Card>
          <CardHeader>
            <CardTitle>Assessment Results</CardTitle>
            <p className="text-sm text-gray-600">
              Assessment: {scores.assessment_id} | Date: {new Date(scores.assessment_date).toLocaleDateString()}
            </p>
          </CardHeader>
          <CardContent>
            <div className="space-y-6">
              {/* Overall Summary */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">{scores.total_countries}</div>
                  <div className="text-sm text-gray-600">Countries Assessed</div>
                </div>
                {scores.regional_average_score && (
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-600">
                      {scores.regional_average_score.toFixed(1)}
                    </div>
                    <div className="text-sm text-gray-600">Regional Average</div>
                  </div>
                )}
                {scores.data_quality_grade && (
                  <div className="text-center">
                    <div className="text-2xl font-bold text-purple-600">{scores.data_quality_grade}</div>
                    <div className="text-sm text-gray-600">Data Quality Grade</div>
                  </div>
                )}
              </div>

              {/* Country Results */}
              <div>
                <h4 className="font-semibold mb-3">Country Scores</h4>
                <div className="space-y-3">
                  {scores.country_scores
                    .sort((a, b) => b.total_score - a.total_score)
                    .map((country) => (
                    <div key={country.country_code} className="border rounded-lg p-4">
                      <div className="flex justify-between items-start mb-3">
                        <div>
                          <h5 className="font-semibold">{country.country_name}</h5>
                          <div className="flex items-center gap-2 mt-1">
                            <Badge 
                              className={`${tierLabels[country.tier as keyof typeof tierLabels]?.color} text-white`}
                            >
                              {tierLabels[country.tier as keyof typeof tierLabels]?.label}
                            </Badge>
                            {country.regional_rank && (
                              <span className="text-sm text-gray-600">
                                Rank #{country.regional_rank}
                              </span>
                            )}
                          </div>
                        </div>
                        <div className="text-right">
                          <div className="text-2xl font-bold">{country.total_score.toFixed(1)}</div>
                          <div className="text-sm text-gray-600">Total Score</div>
                          {country.confidence_score && (
                            <div className="text-xs text-gray-500">
                              Confidence: {(country.confidence_score * 100).toFixed(0)}%
                            </div>
                          )}
                        </div>
                      </div>

                      {/* Pillar Scores */}
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                        {Object.entries(country.pillar_scores).map(([pillar, score]) => (
                          <div key={pillar} className="text-center">
                            <div className="text-lg font-semibold">{score.toFixed(1)}</div>
                            <div className="text-xs text-gray-600">
                              {pillarNames[pillar as keyof typeof pillarNames]}
                            </div>
                          </div>
                        ))}
                      </div>

                      {country.data_quality_grade && (
                        <div className="mt-2 text-sm text-gray-600">
                          Data Quality: <span className="font-medium">{country.data_quality_grade}</span>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Methodology Info */}
      {methodology && (
        <Card>
          <CardHeader>
            <CardTitle>Assessment Methodology</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div>
                <h4 className="font-semibold">{methodology.framework.name}</h4>
                <p className="text-sm text-gray-600">Version {methodology.framework.version}</p>
              </div>
              
              <div>
                <h5 className="font-medium">Infrastructure Pillars</h5>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mt-2">
                  {Object.entries(methodology.framework.pillars).map(([pillar, info]: [string, any]) => (
                    <div key={pillar} className="border rounded p-3">
                      <div className="flex justify-between items-center">
                        <span className="font-medium">{pillarNames[pillar as keyof typeof pillarNames]}</span>
                        <Badge variant="outline">{(info.weight * 100).toFixed(0)}%</Badge>
                      </div>
                      <p className="text-sm text-gray-600 mt-1">{info.description}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default AHAIIAssessmentDashboard;