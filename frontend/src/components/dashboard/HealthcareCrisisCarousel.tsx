'use client';

import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, ResponsiveContainer, Cell, LineChart, Line, CartesianGrid, Tooltip } from 'recharts';

// Crisis data based on your research
const spendingData = [
  { country: 'United States', amount: 14561, color: '#4a9b8e' },
  { country: 'OECD Average', amount: 7456, color: '#f4a460' },
  { country: 'European Average', amount: 5982, color: '#f4a460' },
  { country: 'Sub-Saharan Africa Avg', amount: 89, color: '#b91c1c' },
  { country: 'Madagascar', amount: 18, color: '#991b1b' },
  { country: 'Chad', amount: 36, color: '#991b1b' },
  { country: 'Niger', amount: 41, color: '#991b1b' },
  { country: 'Ethiopia', amount: 45, color: '#b91c1c' }
];

const healthcareWorkersData = [
  { region: 'Americas', workers: 24.8, color: '#b91c1c' },
  { region: 'Europe Average', workers: 18.2, color: '#f4a460' },
  { region: 'WHO Threshold', workers: 4.45, color: '#4a9b8e' },
  { region: 'Global Average', workers: 9.3, color: '#6b7280' },
  { region: 'Africa', workers: 2.3, color: '#b91c1c' },
  { region: 'Niger (Lowest)', workers: 0.4, color: '#991b1b' }
];

const hospitalBedsData = [
  { country: 'Japan', beds: 12.8, color: '#f4a460' },
  { country: 'South Korea', beds: 12.4, color: '#f4a460' },
  { country: 'Germany', beds: 7.9, color: '#f4a460' },
  { country: 'OECD Average', beds: 4.4, color: '#6b7280' },
  { country: 'Global Average', beds: 2.7, color: '#4a9b8e' },
  { country: 'Africa Average', beds: 0.9, color: '#b91c1c' },
  { country: 'Mali (Lowest)', beds: 0.1, color: '#991b1b' }
];

const africaVariationsData = [
  { country: 'Seychelles', amount: 718, color: '#4a9b8e' },
  { country: 'South Africa', amount: 573, color: '#4a9b8e' },
  { country: 'Mauritius', amount: 561, color: '#4a9b8e' },
  { country: 'Botswana', amount: 456, color: '#f4a460' },
  { country: 'Ghana', amount: 89, color: '#fbbf24' },
  { country: 'Kenya', amount: 88, color: '#fbbf24' },
  { country: 'Nigeria', amount: 78, color: '#fbbf24' },
  { country: 'Uganda', amount: 41, color: '#dc2626' },
  { country: 'Ethiopia', amount: 25, color: '#dc2626' },
  { country: 'Madagascar', amount: 18, color: '#dc2626' }
];

const crisisProjectionData = [
  { year: 2022, shortage: 5.6 },
  { year: 2030, shortage: 6.4 }
];

const disparityData = [
  { category: 'Disease Burden', percentage: 25, color: '#dc2626' },
  { category: 'Healthcare Workers', percentage: 3, color: '#dc2626' }
];

// Enhanced data for new storytelling approach
const digitalInfrastructureData = [
  { metric: 'Internet Penetration', africa: 38, global: 68, developed: 85 },
  { metric: 'Reliable Electricity', africa: 43, global: 78, developed: 95 },
  { metric: 'Data Centers (MW/M)', africa: 0.8, americas: 88.5, europe: 73.9 },
  { metric: '5G Coverage', africa: 11, global: 35, developed: 70 }
];

const skillsGapData = [
  { metric: 'Digital Skills Index', africa: 3.4, global: 6.0, developed: 8.2 },
  { metric: 'Children w/ Digital Skills', africa: 10, global: 60, developed: 85 },
  { metric: 'AI/ML Programs', africa: 62, global: 2400, note: '62 concentrated in 3 countries only' }
];

const opportunityGapData = [
  { application: 'Remote Diagnostics', potential: 85, readiness: 25, gap: 60 },
  { application: 'Telemedicine', potential: 90, readiness: 35, gap: 55 },
  { application: 'Drug Discovery', potential: 75, readiness: 15, gap: 60 },
  { application: 'Predictive Analytics', potential: 80, readiness: 30, gap: 50 },
  { application: 'Health Records', potential: 70, readiness: 40, gap: 30 }
];

const shockingStats = [
  { number: '171.4x', label: 'Less Healthcare Spending', detail: 'US spends $14,570 vs Africa average $85 per capita' },
  { number: '16x', label: 'Fewer Healthcare Workers', detail: 'Africa has only 1.55 per 1,000 vs 24.8 in Americas' },
  { number: '111x', label: 'Fewer Data Centers', detail: 'Africa has 0.8MW vs 88.5MW per million people in Americas' }
];

const HealthcareCrisisCarousel: React.FC = () => {
  const [currentSlide, setCurrentSlide] = useState(0);
  const [isVisible, setIsVisible] = useState(false);

  const slides = [
    {
      title: 'African Healthcare & AI Infrastructure Crisis',
      subtitle: 'Africa bears 25% of the world\'s disease burden but has only 3% of global healthcare workers and faces massive AI infrastructure gaps',
      chart: 'hero',
      color: 'crisis',
      type: 'hero'
    },
    {
      title: 'The Spending Catastrophe',
      subtitle: 'US spends 171.4x more per capita than African countries',
      chart: 'spending',
      color: 'crisis',
      stat: '171.4x',
      statLabel: 'Less Healthcare Spending'
    },
    {
      title: 'Healthcare Worker Desert',
      subtitle: 'Africa has 16x fewer healthcare workers per capita',
      chart: 'workers',
      color: 'crisis',
      stat: '16x',
      statLabel: 'Fewer Healthcare Workers'
    },
    {
      title: 'The Most Shocking Disparity',
      subtitle: '25% disease burden, only 3% healthcare workers',
      chart: 'disparity',
      color: 'crisis',
      stat: '25% vs 3%',
      statLabel: 'Disease Burden vs Workers'
    },
    {
      title: 'Digital Infrastructure Desert',
      subtitle: 'Africa has 111x fewer data centers, critical for AI deployment',
      chart: 'digital',
      color: 'crisis',
      stat: '111x',
      statLabel: 'Fewer Data Centers'
    },
    {
      title: 'Skills & Human Capital Crisis',
      subtitle: '90% of African children leave school without digital skills',
      chart: 'skills',
      color: 'crisis',
      stat: '90%',
      statLabel: 'No Digital Skills'
    },
    {
      title: 'Healthcare AI Opportunity Gap',
      subtitle: 'High potential impact, catastrophically low infrastructure readiness',
      chart: 'opportunity',
      color: 'critical',
      type: 'opportunity'
    },
    {
      title: 'The AHAII Solution',
      subtitle: 'Evidence-based intelligence for health AI infrastructure development',
      chart: 'solution',
      color: 'solution',
      type: 'solution'
    }
  ];

  useEffect(() => {
    setIsVisible(true);
    
    // Auto-cycle through slides
    const interval = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % slides.length);
    }, 4000);

    return () => clearInterval(interval);
  }, [slides.length]);

  const renderChart = (chartType: string) => {
    switch (chartType) {
      case 'hero':
        return (
          <div className="flex items-center justify-center h-60">
            <div className="grid grid-cols-3 gap-8 w-full max-w-5xl">
              {shockingStats.map((stat, index) => (
                <div key={index} className="text-center">
                  <div className="text-5xl font-bold text-kpi-critical mb-3 animate-pulse">
                    {stat.number}
                  </div>
                  <div className="text-lg font-semibold text-foreground mb-2">
                    {stat.label}
                  </div>
                  <div className="text-sm text-muted-foreground opacity-90">
                    {stat.detail}
                  </div>
                </div>
              ))}
            </div>
          </div>
        );
      case 'spending':
        return (
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={spendingData.slice(0, 4)}>
              <XAxis 
                dataKey="country" 
                tick={{ fill: '#f8fafc', fontSize: 11 }}
                angle={-20}
                textAnchor="end"
                height={60}
              />
              <YAxis tick={{ fill: '#f8fafc', fontSize: 11 }} />
              <Bar dataKey="amount" radius={[4, 4, 0, 0]}>
                {spendingData.slice(0, 4).map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Bar>
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: 'rgba(0,0,0,0.8)', 
                  border: 'none', 
                  borderRadius: '8px',
                  color: '#fff' 
                }}
                formatter={(value) => [`$${value}`, 'Per capita spending']}
              />
            </BarChart>
          </ResponsiveContainer>
        );

      case 'workers':
        return (
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={healthcareWorkersData} layout="horizontal">
              <XAxis type="number" tick={{ fill: '#f8fafc', fontSize: 11 }} />
              <YAxis 
                type="category" 
                dataKey="region" 
                tick={{ fill: '#f8fafc', fontSize: 11 }}
                width={100}
              />
              <Bar dataKey="workers" radius={[0, 4, 4, 0]}>
                {healthcareWorkersData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Bar>
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: 'rgba(0,0,0,0.8)', 
                  border: 'none', 
                  borderRadius: '8px',
                  color: '#fff' 
                }}
                formatter={(value) => [`${value}`, 'Healthcare workers per 1,000 people']}
              />
            </BarChart>
          </ResponsiveContainer>
        );

      case 'disparity':
        return (
          <div className="flex items-center justify-center h-60">
            <div className="grid grid-cols-2 gap-8 w-full max-w-md">
              <div className="text-center">
                <div className="text-6xl font-bold text-kpi-critical mb-2">25%</div>
                <div className="text-paragraph-section-1 text-sm">Disease Burden</div>
                <div className="w-full h-24 bg-kpi-critical rounded-lg mt-3 opacity-80"></div>
              </div>
              <div className="text-center">
                <div className="text-6xl font-bold text-kpi-critical mb-2">3%</div>
                <div className="text-paragraph-section-1 text-sm">Healthcare Workers</div>
                <div className="w-full h-6 bg-kpi-critical rounded-lg mt-3 opacity-80"></div>
              </div>
            </div>
          </div>
        );

      case 'beds':
        return (
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={hospitalBedsData}>
              <XAxis 
                dataKey="country" 
                tick={{ fill: '#f8fafc', fontSize: 11 }}
                angle={-20}
                textAnchor="end"
                height={60}
              />
              <YAxis tick={{ fill: '#f8fafc', fontSize: 11 }} />
              <Bar dataKey="beds" radius={[4, 4, 0, 0]}>
                {hospitalBedsData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Bar>
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: 'rgba(0,0,0,0.8)', 
                  border: 'none', 
                  borderRadius: '8px',
                  color: '#fff' 
                }}
                formatter={(value) => [`${value}`, 'Hospital beds per 1,000 people']}
              />
            </BarChart>
          </ResponsiveContainer>
        );

      case 'variations':
        return (
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={africaVariationsData}>
              <XAxis 
                dataKey="country" 
                tick={{ fill: '#f8fafc', fontSize: 11 }}
                angle={-45}
                textAnchor="end"
                height={80}
              />
              <YAxis tick={{ fill: '#f8fafc', fontSize: 11 }} />
              <Bar dataKey="amount" radius={[4, 4, 0, 0]}>
                {africaVariationsData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Bar>
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: 'rgba(0,0,0,0.8)', 
                  border: 'none', 
                  borderRadius: '8px',
                  color: '#fff' 
                }}
                formatter={(value) => [`$${value}`, 'Per capita spending']}
              />
            </BarChart>
          </ResponsiveContainer>
        );

      case 'projection':
        return (
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={crisisProjectionData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
              <XAxis 
                dataKey="year" 
                tick={{ fill: '#f8fafc', fontSize: 12 }}
                domain={['dataMin', 'dataMax']}
              />
              <YAxis 
                tick={{ fill: '#f8fafc', fontSize: 12 }}
                label={{ value: 'Million Workers', angle: -90, position: 'insideLeft', style: { textAnchor: 'middle', fill: '#f8fafc' } }}
              />
              <Line 
                type="monotone" 
                dataKey="shortage" 
                stroke="#dc2626" 
                strokeWidth={4}
                dot={{ fill: '#dc2626', strokeWidth: 2, r: 8 }}
              />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: 'rgba(0,0,0,0.8)', 
                  border: 'none', 
                  borderRadius: '8px',
                  color: '#fff' 
                }}
                formatter={(value) => [`${value}M`, 'Healthcare worker shortage']}
              />
            </LineChart>
          </ResponsiveContainer>
        );

      case 'digital':
        return (
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={digitalInfrastructureData}>
              <XAxis 
                dataKey="metric" 
                tick={{ fill: '#f8fafc', fontSize: 10 }}
                angle={-20}
                textAnchor="end"
                height={60}
              />
              <YAxis tick={{ fill: '#f8fafc', fontSize: 11 }} />
              <Bar dataKey="africa" fill="#dc2626" name="Africa" />
              <Bar dataKey="global" fill="#6b7280" name="Global" />
              <Bar dataKey="developed" fill="#4a9b8e" name="Developed" />
              <Bar dataKey="americas" fill="#4a9b8e" name="Americas" />
              <Bar dataKey="europe" fill="#4a9b8e" name="Europe" />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: 'rgba(0,0,0,0.8)', 
                  border: 'none', 
                  borderRadius: '8px',
                  color: '#fff' 
                }}
              />
            </BarChart>
          </ResponsiveContainer>
        );

      case 'skills':
        return (
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={skillsGapData}>
              <XAxis 
                dataKey="metric" 
                tick={{ fill: '#f8fafc', fontSize: 10 }}
                angle={-20}
                textAnchor="end"
                height={60}
              />
              <YAxis tick={{ fill: '#f8fafc', fontSize: 11 }} />
              <Bar dataKey="africa" fill="#dc2626" name="Africa" />
              <Bar dataKey="global" fill="#6b7280" name="Global" />
              <Bar dataKey="developed" fill="#4a9b8e" name="Developed" />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: 'rgba(0,0,0,0.8)', 
                  border: 'none', 
                  borderRadius: '8px',
                  color: '#fff' 
                }}
              />
            </BarChart>
          </ResponsiveContainer>
        );

      case 'opportunity':
        return (
          <div className="space-y-4">
            {opportunityGapData.map((item, index) => (
              <div key={index} className="flex items-center justify-between bg-white/5 rounded-lg p-4">
                <div className="flex-1">
                  <div className="font-semibold text-foreground mb-2">{item.application}</div>
                  <div className="flex items-center space-x-4">
                    <div className="flex items-center space-x-2">
                      <span className="text-sm text-muted-foreground">Potential:</span>
                      <div className="w-20 bg-white/20 rounded-full h-2">
                        <div 
                          className="bg-kpi-excellent h-2 rounded-full" 
                          style={{ width: `${item.potential}%` }}
                        />
                      </div>
                      <span className="text-sm text-foreground">{item.potential}%</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <span className="text-sm text-muted-foreground">Readiness:</span>
                      <div className="w-20 bg-white/20 rounded-full h-2">
                        <div 
                          className="bg-kpi-critical h-2 rounded-full" 
                          style={{ width: `${item.readiness}%` }}
                        />
                      </div>
                      <span className="text-sm text-foreground">{item.readiness}%</span>
                    </div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-bold text-kpi-critical">{item.gap}pt</div>
                  <div className="text-sm text-muted-foreground">Gap</div>
                </div>
              </div>
            ))}
          </div>
        );

      case 'solution':
        return (
          <div className="text-center space-y-6">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-physical/20 border border-physical/40 rounded-lg p-4">
                <div className="text-2xl mb-2">🏥</div>
                <div className="text-sm font-semibold text-foreground">Physical Infrastructure</div>
                <div className="text-xs text-muted-foreground mt-1">Medical-grade systems</div>
              </div>
              <div className="bg-human-capital/20 border border-human-capital/40 rounded-lg p-4">
                <div className="text-2xl mb-2">👩‍⚕️</div>
                <div className="text-sm font-semibold text-foreground">Human Capital</div>
                <div className="text-xs text-muted-foreground mt-1">Clinical AI literacy</div>
              </div>
              <div className="bg-regulatory/20 border border-regulatory/40 rounded-lg p-4">
                <div className="text-2xl mb-2">📋</div>
                <div className="text-sm font-semibold text-foreground">Regulatory Frameworks</div>
                <div className="text-xs text-muted-foreground mt-1">Health data governance</div>
              </div>
              <div className="bg-economic/20 border border-economic/40 rounded-lg p-4">
                <div className="text-2xl mb-2">💰</div>
                <div className="text-sm font-semibold text-foreground">Economic Sustainability</div>
                <div className="text-xs text-muted-foreground mt-1">Investment pathways</div>
              </div>
            </div>
            <div className="text-lg font-semibold text-primary">
              Transform crisis into opportunity with evidence-based health AI infrastructure development
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className={`space-y-6 transition-all duration-1000 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}>
      {/* Crisis Narrative Carousel */}
      <div className={`bg-white/5 backdrop-blur-sm rounded-lg p-6 border border-white/10 ${slides[currentSlide].type === 'hero' ? 'bg-gradient-to-r from-kpi-critical/10 to-kpi-warning/10' : ''}`}>
        <div className="text-center space-y-4 mb-6">
          {slides[currentSlide].stat && (
            <div className="text-6xl font-bold text-kpi-critical mb-4 animate-pulse">
              {slides[currentSlide].stat}
            </div>
          )}
          <h2 className={`font-bold text-foreground ${slides[currentSlide].type === 'hero' ? 'text-3xl lg:text-4xl' : 'text-2xl'}`}>
            {slides[currentSlide].title}
          </h2>
          <p className={`text-paragraph-section-1 ${slides[currentSlide].type === 'hero' ? 'text-lg max-w-4xl mx-auto' : ''}`}>
            {slides[currentSlide].subtitle}
          </p>
        </div>

        {/* Chart Container */}
        <div className="bg-white/10 rounded-lg p-4">
          {renderChart(slides[currentSlide].chart)}
        </div>

        {/* Slide Indicators */}
        <div className="flex justify-center mt-6 space-x-2">
          {slides.map((_, index) => (
            <button
              key={index}
              onClick={() => setCurrentSlide(index)}
              className={`w-3 h-3 rounded-full transition-all duration-300 ${
                index === currentSlide 
                  ? 'bg-primary scale-125' 
                  : 'bg-white/30 hover:bg-white/50'
              }`}
            />
          ))}
        </div>

        {/* Progress Indicator */}
        <div className="mt-4">
          <div className="w-full bg-white/20 rounded-full h-1">
            <div 
              className="bg-primary h-1 rounded-full transition-all duration-4000 ease-linear"
              style={{ 
                width: `${((currentSlide + 1) / slides.length) * 100}%`,
                animation: 'slideProgress 4s linear infinite'
              }}
            />
          </div>
        </div>
      </div>

      {/* Call to Action */}
      <div className="text-center">
        <div className="text-foreground font-semibold mb-2">
          The Dual Crisis: Healthcare & AI Infrastructure
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4 max-w-4xl mx-auto">
          <div className="bg-kpi-critical/10 border border-kpi-critical/20 rounded-lg p-4">
            <div className="font-semibold text-kpi-critical mb-2">Healthcare Crisis</div>
            <div className="text-sm text-muted-foreground">
              US spends $14,570 per capita while African countries average $85, with 6.1M healthcare worker shortage
            </div>
          </div>
          <div className="bg-primary/10 border border-primary/20 rounded-lg p-4">
            <div className="font-semibold text-primary mb-2">AI Infrastructure Gap</div>
            <div className="text-sm text-muted-foreground">
              111x fewer data centers, 90% lack digital skills, creating barriers to AI-driven healthcare solutions
            </div>
          </div>
        </div>
        <div className="text-paragraph-section-1 text-sm mt-4">
          <span className="text-gradient gradient-primary font-semibold">AHAII</span> provides systematic intelligence to transform this crisis into opportunity through evidence-based health AI infrastructure development.
        </div>
      </div>

      <style jsx>{`
        @keyframes slideProgress {
          0% { width: 0%; }
          100% { width: ${100 / slides.length}%; }
        }
      `}</style>
    </div>
  );
};

export default HealthcareCrisisCarousel;