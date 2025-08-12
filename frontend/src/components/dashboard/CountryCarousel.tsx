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
      // Default navigation to country detail page
      window.location.href = `/country?id=${countryId}`;
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
        className="relative h-[85vh] overflow-hidden"
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
                  flex-shrink-0 w-96 h-full relative cursor-pointer
                  ${isActive ? 'z-20' : isAdjacent ? 'z-10' : 'z-0'}
                `}
                animate={{
                  scale: isActive ? 1 : isAdjacent ? 0.85 : 0.7,
                  opacity: distance > 2 ? 0.3 : distance > 1 ? 0.6 : 1,
                  rotateY: isActive ? 0 : (index < currentIndex ? 15 : -15),
                }}
                transition={{
                  type: "spring",
                  stiffness: 300,
                  damping: 20
                }}
                onClick={() => handleCountryClick(country.id)}
                whileHover={isActive ? { scale: 1.02 } : {}}
              >
                <div className="card h-full bg-gradient-to-br from-section-1 to-section-2 border-2 border-section-3 overflow-hidden">
                  
                  {/* Country Header */}
                  <div className="relative p-6 pb-4">
                    <div className="flex items-center justify-between mb-4">
                      <div className="flex items-center gap-4">
                        <Image
                          src={country.flag_image}
                          alt={`${country.name} flag`}
                          width={48}
                          height={32}
                          className="rounded shadow-md"
                        />
                        <div>
                          <h3 className="text-2xl font-bold text-foreground">
                            {country.name}
                          </h3>
                          <p className="text-sm text-paragraph-section-1">
                            {country.region}
                          </p>
                        </div>
                      </div>
                      
                      {/* AHAII Score Badge */}
                      {country.ahaii_score && (
                        <div className={`domain-badge ${getTierBadgeColor(country.ahaii_score.readiness_tier)} text-center`}>
                          <div className={`text-2xl font-bold ${getScoreColor(country.ahaii_score.total_score)}`}>
                            {country.ahaii_score.total_score.toFixed(1)}
                          </div>
                          <div className="text-xs opacity-75">
                            Tier {country.ahaii_score.readiness_tier}
                          </div>
                        </div>
                      )}
                    </div>

                    {/* Rankings */}
                    {country.ahaii_score && (
                      <div className="flex gap-4 text-sm">
                        <div>
                          <span className="text-paragraph-section-1">Global:</span>
                          <span className="font-semibold ml-1">
                            #{country.ahaii_score.global_ranking}
                          </span>
                        </div>
                        <div>
                          <span className="text-paragraph-section-1">Regional:</span>
                          <span className="font-semibold ml-1">
                            #{country.ahaii_score.regional_ranking}
                          </span>
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Country Outline Visual */}
                  <div className="relative h-48 bg-section-3 bg-opacity-20 flex items-center justify-center">
                    <Image
                      src={country.country_outline_image}
                      alt={`${country.name} outline`}
                      width={200}
                      height={150}
                      className="opacity-80 filter drop-shadow-lg"
                    />
                    
                    {/* Trend Indicator */}
                    {country.ahaii_score && (
                      <div className="absolute top-4 right-4">
                        <motion.div
                          className={`flex items-center gap-2 px-3 py-1 rounded-full text-xs font-medium ${
                            country.ahaii_score.development_trajectory === 'improving' 
                              ? 'bg-green-100 text-green-800' 
                              : country.ahaii_score.development_trajectory === 'declining'
                              ? 'bg-red-100 text-red-800'
                              : 'bg-gray-100 text-gray-800'
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
                    <div className="p-6">
                      <div className="grid grid-cols-2 gap-4 mb-6">
                        <div className="text-center">
                          <div className={`text-lg font-bold domain-human-capital`}>
                            {country.ahaii_score.human_capital_score.toFixed(1)}
                          </div>
                          <div className="text-xs text-paragraph-section-1">Human Capital</div>
                        </div>
                        <div className="text-center">
                          <div className={`text-lg font-bold domain-physical`}>
                            {country.ahaii_score.physical_infrastructure_score.toFixed(1)}
                          </div>
                          <div className="text-xs text-paragraph-section-1">Physical Infra</div>
                        </div>
                        <div className="text-center">
                          <div className={`text-lg font-bold domain-regulatory`}>
                            {country.ahaii_score.regulatory_infrastructure_score.toFixed(1)}
                          </div>
                          <div className="text-xs text-paragraph-section-1">Regulatory</div>
                        </div>
                        <div className="text-center">
                          <div className={`text-lg font-bold domain-economic`}>
                            {country.ahaii_score.economic_market_score.toFixed(1)}
                          </div>
                          <div className="text-xs text-paragraph-section-1">Economic</div>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Country Stats */}
                  <div className="px-6 pb-6">
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <span className="text-paragraph-section-1">Population:</span>
                        <div className="font-semibold">{formatPopulation(country.population)}</div>
                      </div>
                      <div>
                        <span className="text-paragraph-section-1">GDP:</span>
                        <div className="font-semibold">{formatGDP(country.gdp_usd)}</div>
                      </div>
                    </div>
                    
                    <div className="mt-4 text-sm">
                      <span className="text-paragraph-section-1">Healthcare Spending:</span>
                      <span className="font-semibold ml-1">
                        {country.healthcare_spending_percent_gdp}% of GDP
                      </span>
                    </div>

                    {/* Intelligence Activity */}
                    {country.recent_intelligence_count && (
                      <div className="mt-4 text-sm">
                        <div className="flex items-center gap-2">
                          <Image
                            src="/images/svg-icons/other-icons/ai-software-icon-light.svg"
                            alt="Intelligence"
                            width={16}
                            height={16}
                          />
                          <span className="text-paragraph-section-1">Recent Activity:</span>
                          <span className="font-semibold text-primary">
                            {country.recent_intelligence_count} signals
                          </span>
                        </div>
                        {country.last_updated && (
                          <div className="text-xs text-paragraph-section-1 opacity-75 mt-1">
                            Last updated: {country.last_updated}
                          </div>
                        )}
                      </div>
                    )}
                  </div>

                  {/* Call to Action */}
                  <div className="absolute bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-section-1 to-transparent">
                    <motion.button
                      className="w-full btn btn-primary btn-sm"
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