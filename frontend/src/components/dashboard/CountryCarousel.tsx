'use client';

import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence, PanInfo } from 'framer-motion';
import Image from 'next/image';
import Link from 'next/link';
import { CountryWithScore } from '@/types/country';
import { getTierColor, getTierBadgeColor } from '@/data/countries';

interface CountryCarouselProps {
  countries: CountryWithScore[];
  onCountrySelect?: (countryId: string) => void;
  className?: string;
}

const CountryCarousel: React.FC<CountryCarouselProps> = ({
  countries,
  onCountrySelect,
  className = ''
}) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [dragConstraints, setDragConstraints] = useState({ left: 0, right: 0 });
  const carouselRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const updateConstraints = () => {
      if (carouselRef.current) {
        const containerWidth = carouselRef.current.offsetWidth;
        const cardWidth = 400; // Card width + gap
        const totalWidth = countries.length * cardWidth;
        const maxDrag = Math.max(0, totalWidth - containerWidth);
        
        setDragConstraints({
          left: -maxDrag,
          right: 0
        });
      }
    };

    updateConstraints();
    window.addEventListener('resize', updateConstraints);
    return () => window.removeEventListener('resize', updateConstraints);
  }, [countries.length]);

  const handleDrag = (event: any, info: PanInfo) => {
    const cardWidth = 400;
    const threshold = 100;
    
    if (Math.abs(info.offset.x) > threshold) {
      if (info.offset.x > 0 && currentIndex > 0) {
        setCurrentIndex(currentIndex - 1);
      } else if (info.offset.x < 0 && currentIndex < countries.length - 1) {
        setCurrentIndex(currentIndex + 1);
      }
    }
  };

  const navigateToCountry = (index: number) => {
    setCurrentIndex(index);
  };

  const handleCountryClick = (countryId: string) => {
    if (onCountrySelect) {
      onCountrySelect(countryId);
    } else {
      // Default navigation to country profiles page
      window.location.href = `/country-profiles/${countryId}`;
    }
  };

  const getScoreColor = (score?: number): string => {
    if (!score) return 'text-muted-foreground';
    if (score >= 75) return 'text-kpi-excellent';
    if (score >= 60) return 'text-kpi-good';
    if (score >= 45) return 'text-kpi-warning';
    return 'text-kpi-poor';
  };

  const formatPopulation = (pop: number): string => {
    if (pop >= 1000000) return `${(pop / 1000000).toFixed(1)}M`;
    if (pop >= 1000) return `${(pop / 1000).toFixed(0)}K`;
    return pop.toString();
  };

  const formatGDP = (gdp: number): string => {
    if (gdp >= 1000000000) return `$${(gdp / 1000000000).toFixed(1)}B`;
    if (gdp >= 1000000) return `$${(gdp / 1000000).toFixed(0)}M`;
    return `$${gdp}`;
  };

  return (
    <div className={`relative w-full ${className}`}>
      {/* Carousel Header */}
      <div className="text-center mb-12">
        <h2 className="text-4xl font-bold text-foreground mb-4">
          African Health AI
          <span className="text-gradient gradient-primary block">
            Readiness Assessment
          </span>
        </h2>
        <p className="text-xl text-paragraph-section-1 max-w-3xl mx-auto">
          Explore real-time intelligence on health AI infrastructure across Africa. 
          Click any country to dive deep into their readiness profile.
        </p>
      </div>

      {/* Main Carousel Container */}
      <div 
        ref={carouselRef}
        className="relative h-[600px] overflow-hidden"
      >
        <motion.div
          className="flex gap-8 h-full"
          animate={{
            x: -currentIndex * 400
          }}
          transition={{
            type: "spring",
            stiffness: 300,
            damping: 30
          }}
          drag="x"
          dragConstraints={dragConstraints}
          onDragEnd={handleDrag}
          style={{ cursor: 'grab' }}
          whileDrag={{ cursor: 'grabbing' }}
        >
          {countries.map((country, index) => {
            const isActive = index === currentIndex;
            const isAdjacent = Math.abs(index - currentIndex) === 1;
            const distance = Math.abs(index - currentIndex);

            return (
              <motion.div
                key={country.id}
                className={`
                  flex-shrink-0 w-80 h-full relative cursor-pointer
                  ${isActive ? 'z-20' : isAdjacent ? 'z-10' : 'z-0'}
                `}
                animate={{
                  scale: isActive ? 1 : isAdjacent ? 0.9 : 0.8,
                  opacity: distance > 2 ? 0.3 : distance > 1 ? 0.7 : 1,
                  rotateY: isActive ? 0 : (index < currentIndex ? 10 : -10),
                }}
                transition={{
                  type: "spring",
                  stiffness: 300,
                  damping: 25
                }}
                onClick={() => handleCountryClick(country.id)}
                whileHover={isActive ? { scale: 1.02 } : {}}
              >
                <div className="card h-full bg-white/95 backdrop-blur-sm border border-gray-200 shadow-xl overflow-hidden">
                  
                  {/* Country Header */}
                  <div className="relative p-6 text-center">
                    {/* Country Name at Top */}
                    <h3 className="text-2xl font-bold text-gray-900 mb-4">
                      {country.name}
                    </h3>
                    
                    {/* Prominent Flag */}
                    <div className="flex justify-center mb-4">
                      <Image
                        src={country.flag_image}
                        alt={`${country.name} flag`}
                        width={80}
                        height={60}
                        className="rounded-lg shadow-lg border-2 border-gray-100"
                      />
                    </div>
                    
                    <p className="text-sm text-gray-600 mb-4">
                      {country.region}
                    </p>
                    
                    {/* AHAII Score Badge */}
                    {country.ahaii_score && (
                      <div className="inline-flex items-center gap-3 bg-gray-50 rounded-lg px-4 py-2 mb-4">
                        <div className="text-center">
                          <div className={`text-xl font-bold ${getScoreColor(country.ahaii_score.total_score)}`}>
                            {country.ahaii_score.total_score.toFixed(1)}
                          </div>
                          <div className="text-xs text-gray-500">
                            Overall Score
                          </div>
                        </div>
                        <div className="text-center">
                          <div className="text-lg font-semibold text-blue-600">
                            {country.ahaii_score.readiness_tier}
                          </div>
                          <div className="text-xs text-gray-500">
                            Tier
                          </div>
                        </div>
                      </div>
                    )}

                    {/* Rankings */}
                    {country.ahaii_score && (
                      <div className="flex justify-center gap-6 text-sm mb-4">
                        <div className="text-center">
                          <div className="font-semibold text-gray-900">#{country.ahaii_score.global_ranking}</div>
                          <div className="text-xs text-gray-500">Global</div>
                        </div>
                        <div className="text-center">
                          <div className="font-semibold text-gray-900">#{country.ahaii_score.regional_ranking}</div>
                          <div className="text-xs text-gray-500">Regional</div>
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Country Outline Visual */}
                  <div className="relative h-40 bg-gray-50 flex items-center justify-center">
                    <Image
                      src={country.country_outline_image}
                      alt={`${country.name} outline`}
                      width={160}
                      height={120}
                      className="opacity-60 filter grayscale"
                    />
                    
                    {/* Trend Indicator */}
                    {country.ahaii_score && (
                      <div className="absolute top-3 right-3">
                        <motion.div
                          className={`flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium ${
                            country.ahaii_score.development_trajectory === 'improving' 
                              ? 'bg-green-100 text-green-700' 
                              : country.ahaii_score.development_trajectory === 'declining'
                              ? 'bg-red-100 text-red-700'
                              : 'bg-gray-100 text-gray-700'
                          }`}
                          initial={{ opacity: 0, scale: 0 }}
                          animate={{ opacity: 1, scale: 1 }}
                          transition={{ delay: 0.3 }}
                        >
                          {country.ahaii_score.development_trajectory === 'improving' ? '↗' : 
                           country.ahaii_score.development_trajectory === 'declining' ? '↘' : '→'}
                          {country.ahaii_score.development_trajectory}
                        </motion.div>
                      </div>
                    )}
                  </div>

                  {/* Four Pillars Quick View */}
                  {country.ahaii_score && (
                    <div className="p-4">
                      <div className="grid grid-cols-2 gap-3">
                        <div className="text-center p-2 bg-blue-50 rounded">
                          <div className="text-lg font-bold text-blue-600">
                            {country.ahaii_score.human_capital_score.toFixed(1)}
                          </div>
                          <div className="text-xs text-gray-600">Human Capital</div>
                        </div>
                        <div className="text-center p-2 bg-green-50 rounded">
                          <div className="text-lg font-bold text-green-600">
                            {country.ahaii_score.physical_infrastructure_score.toFixed(1)}
                          </div>
                          <div className="text-xs text-gray-600">Physical Infra</div>
                        </div>
                        <div className="text-center p-2 bg-purple-50 rounded">
                          <div className="text-lg font-bold text-purple-600">
                            {country.ahaii_score.regulatory_infrastructure_score.toFixed(1)}
                          </div>
                          <div className="text-xs text-gray-600">Regulatory</div>
                        </div>
                        <div className="text-center p-2 bg-orange-50 rounded">
                          <div className="text-lg font-bold text-orange-600">
                            {country.ahaii_score.economic_market_score.toFixed(1)}
                          </div>
                          <div className="text-xs text-gray-600">Economic</div>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Country Stats */}
                  <div className="px-4 pb-4">
                    <div className="grid grid-cols-2 gap-4 text-sm mb-3">
                      <div className="text-center">
                        <div className="font-semibold text-gray-900">{formatPopulation(country.population)}</div>
                        <div className="text-xs text-gray-500">Population</div>
                      </div>
                      <div className="text-center">
                        <div className="font-semibold text-gray-900">{formatGDP(country.gdp_usd)}</div>
                        <div className="text-xs text-gray-500">GDP</div>
                      </div>
                    </div>
                    
                    <div className="text-center text-sm mb-3">
                      <div className="font-semibold text-gray-900">
                        {country.healthcare_spending_percent_gdp}% of GDP
                      </div>
                      <div className="text-xs text-gray-500">Healthcare Spending</div>
                    </div>

                    {/* Intelligence Activity */}
                    {country.recent_intelligence_count && (
                      <div className="text-center text-sm">
                        <div className="font-semibold text-blue-600">
                          {country.recent_intelligence_count} signals
                        </div>
                        <div className="text-xs text-gray-500">Recent Activity</div>
                        {country.last_updated && (
                          <div className="text-xs text-gray-400 mt-1">
                            Updated: {country.last_updated}
                          </div>
                        )}
                      </div>
                    )}
                  </div>

                  {/* Call to Action */}
                  <div className="p-4 mt-auto">
                    <motion.button
                      className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors"
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                    >
                      Explore {country.name} →
                    </motion.button>
                  </div>
                </div>
              </motion.div>
            );
          })}
        </motion.div>
      </div>

      {/* Navigation Dots */}
      <div className="flex justify-center gap-2 mt-8">
        {countries.map((_, index) => (
          <button
            key={index}
            onClick={() => navigateToCountry(index)}
            className={`w-3 h-3 rounded-full transition-all duration-300 ${
              index === currentIndex
                ? 'bg-primary scale-125'
                : 'bg-section-3 hover:bg-primary-light'
            }`}
          />
        ))}
      </div>

      {/* Navigation Arrows */}
      <div className="absolute top-1/2 -translate-y-1/2 left-4">
        <button
          onClick={() => navigateToCountry(Math.max(0, currentIndex - 1))}
          disabled={currentIndex === 0}
          className="btn btn-secondary btn-icon-lg opacity-75 hover:opacity-100 disabled:opacity-25"
        >
          ←
        </button>
      </div>
      <div className="absolute top-1/2 -translate-y-1/2 right-4">
        <button
          onClick={() => navigateToCountry(Math.min(countries.length - 1, currentIndex + 1))}
          disabled={currentIndex === countries.length - 1}
          className="btn btn-secondary btn-icon-lg opacity-75 hover:opacity-100 disabled:opacity-25"
        >
          →
        </button>
      </div>
    </div>
  );
};

export default CountryCarousel;