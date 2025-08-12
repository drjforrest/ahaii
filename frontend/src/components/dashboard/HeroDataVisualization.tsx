'use client';

import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, ResponsiveContainer, Cell, PieChart, Pie, Legend } from 'recharts';

const africanHealthData = [
  { country: 'South Africa', score: 72, physical: 75, human: 68, regulatory: 70, economic: 75 },
  { country: 'Kenya', score: 58, physical: 60, human: 55, regulatory: 58, economic: 60 },
  { country: 'Nigeria', score: 54, physical: 50, human: 58, regulatory: 52, economic: 56 },
  { country: 'Ghana', score: 51, physical: 48, human: 54, regulatory: 50, economic: 52 },
  { country: 'Rwanda', score: 49, physical: 52, human: 46, regulatory: 48, economic: 50 },
  { country: 'Ethiopia', score: 35, physical: 32, human: 38, regulatory: 34, economic: 36 }
];

const pillarData = [
  { name: 'Physical', value: 30, color: '#4a9b8e' },
  { name: 'Human Capital', value: 30, color: '#1e3a8a' },
  { name: 'Regulatory', value: 25, color: '#6b7280' },
  { name: 'Economic', value: 15, color: '#92400e' }
];

const HeroDataVisualization: React.FC = () => {
  const [animatedData, setAnimatedData] = useState(africanHealthData.map(d => ({ ...d, score: 0 })));
  const [currentMetric, setCurrentMetric] = useState(0);
  const [isVisible, setIsVisible] = useState(false);

  const metrics = [
    { label: 'Countries Assessed', value: '54' },
    { label: 'Data Points Collected', value: '50K+' },
    { label: 'Real-time Updates', value: '24/7' },
    { label: 'Infrastructure Signals', value: '10K+' }
  ];

  useEffect(() => {
    setIsVisible(true);
    
    // Animate bars growing
    const animateScores = () => {
      africanHealthData.forEach((item, index) => {
        setTimeout(() => {
          setAnimatedData(prev => 
            prev.map((d, i) => 
              i === index ? { ...d, score: item.score } : d
            )
          );
        }, index * 200);
      });
    };

    // Rotate metrics
    const rotateMetrics = () => {
      setCurrentMetric(prev => (prev + 1) % metrics.length);
    };

    const animationTimeout = setTimeout(animateScores, 500);
    const metricInterval = setInterval(rotateMetrics, 2000);

    return () => {
      clearTimeout(animationTimeout);
      clearInterval(metricInterval);
    };
  }, []);

  const getBarColor = (score: number) => {
    if (score >= 65) return '#4a9b8e'; // Teal
    if (score >= 50) return '#1e3a8a'; // Navy
    if (score >= 35) return '#6b7280'; // Gray
    return '#92400e'; // Brown
  };

  return (
    <div className={`space-y-6 transition-all duration-1000 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}>
      {/* Dynamic Metrics Display */}
      <div className="text-center space-y-2">
        <div className="flex items-center gap-3 justify-center">
          <div className="w-3 h-3 bg-gradient-to-r from-physical to-human-capital rounded-full animate-pulse"></div>
          <span className="text-lg text-paragraph-section-1">Live Intelligence</span>
        </div>
        <div 
          key={currentMetric}
          className="transition-all duration-500 transform"
        >
          <div className="text-5xl font-bold text-gradient gradient-primary">
            {metrics[currentMetric].value}
          </div>
          <p className="text-paragraph-section-1">{metrics[currentMetric].label}</p>
        </div>
      </div>

      {/* Main Chart */}
      <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4">
        <h3 className="text-lg font-semibold text-foreground mb-4 text-center">
          AI Readiness Scores - Top African Countries
        </h3>
        <ResponsiveContainer width="100%" height={200}>
          <BarChart data={animatedData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
            <XAxis 
              dataKey="country" 
              tick={{ fill: '#f8fafc', fontSize: 12 }}
              angle={-45}
              textAnchor="end"
              height={70}
            />
            <YAxis 
              tick={{ fill: '#f8fafc', fontSize: 12 }}
              domain={[0, 100]}
            />
            <Bar dataKey="score" radius={[4, 4, 0, 0]}>
              {animatedData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={getBarColor(entry.score)} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Pillar Breakdown */}
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-white/10 backdrop-blur-sm rounded-lg p-3">
          <h4 className="text-sm font-semibold text-foreground mb-2">Assessment Framework</h4>
          <ResponsiveContainer width="100%" height={120}>
            <PieChart>
              <Pie
                data={pillarData}
                cx="50%"
                cy="50%"
                innerRadius={20}
                outerRadius={40}
                paddingAngle={2}
                dataKey="value"
              >
                {pillarData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white/10 backdrop-blur-sm rounded-lg p-3">
          <h4 className="text-sm font-semibold text-foreground mb-2">Coverage</h4>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-xs text-paragraph-section-1">Countries</span>
              <span className="text-sm font-semibold text-foreground">54/54</span>
            </div>
            <div className="flex justify-between">
              <span className="text-xs text-paragraph-section-1">Domains</span>
              <span className="text-sm font-semibold text-foreground">4/4</span>
            </div>
            <div className="flex justify-between">
              <span className="text-xs text-paragraph-section-1">Updates</span>
              <span className="text-sm font-semibold text-physical">Live</span>
            </div>
            <div className="w-full bg-white/20 rounded-full h-2">
              <div className="bg-gradient-to-r from-physical via-human-capital to-regulatory h-2 rounded-full animate-pulse" style={{width: '87%'}}></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HeroDataVisualization;