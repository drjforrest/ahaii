'use client';

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import CountryCarousel from '@/components/dashboard/CountryCarousel';
import { countryDataService } from '@/services/countryDataService';
import { CountryWithScore } from '@/types/country';

export default function DashboardPage() {
  const [countries, setCountries] = useState<CountryWithScore[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Load real data from backend
    const loadData = async () => {
      try {
        setLoading(true);
        setError(null);
        console.log('🔄 Loading featured countries from backend...');
        const featuredCountries = await countryDataService.getFeaturedCountries(8);
        setCountries(featuredCountries);
        console.log('✅ Loaded', featuredCountries.length, 'featured countries');
      } catch (err) {
        console.error('❌ Failed to load countries:', err);
        setError('Failed to load country data. Please try again.');
        // Fallback to empty array instead of static data
        setCountries([]);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  const handleCountrySelect = (countryId: string) => {
    // Navigate to country profiles page
    window.location.href = `/country-profiles/${countryId}`;
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-section-1">
        <div className="text-center space-y-4">
          <motion.div
            className="w-16 h-16 border-4 border-blue-600 border-t-transparent rounded-full mx-auto"
            animate={{ rotate: 360 }}
            transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
          />
          <p className="text-lg text-gray-700">Loading real-time country intelligence...</p>
          <p className="text-sm text-gray-500">Fetching latest World Bank data...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-section-1">
        <div className="text-center space-y-4 max-w-md">
          <div className="text-red-500 text-6xl mb-4">⚠️</div>
          <h2 className="text-xl font-semibold text-gray-900">Unable to Load Data</h2>
          <p className="text-gray-600">{error}</p>
          <button 
            onClick={() => window.location.reload()}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  if (countries.length === 0) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-section-1">
        <div className="text-center space-y-4">
          <div className="text-gray-400 text-6xl mb-4">🌍</div>
          <h2 className="text-xl font-semibold text-gray-900">No Country Data Available</h2>
          <p className="text-gray-600">The backend data is still being processed. Please check back soon.</p>
        </div>
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-section-1">
      {/* Country Carousel with integrated header */}
      <section className="section bg-section-1 py-8">
        <CountryCarousel 
          countries={countries}
          onCountrySelect={handleCountrySelect}
          className="px-4"
        />
      </section>

      {/* Quick Stats */}
      <section className="section bg-section-3 py-16">
        <div className="container">
          <div className="grid md:grid-cols-4 gap-8 text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="space-y-3"
            >
              <div className="text-4xl font-bold text-gradient gradient-human-capital">54</div>
              <div className="text-sm text-paragraph-section-3">African Countries</div>
              <div className="text-xs text-paragraph-section-3 opacity-75">Continuous Assessment</div>
            </motion.div>
            
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.1 }}
              className="space-y-3"
            >
              <div className="text-4xl font-bold text-gradient gradient-physical">4</div>
              <div className="text-sm text-paragraph-section-3">Infrastructure Pillars</div>
              <div className="text-xs text-paragraph-section-3 opacity-75">Comprehensive Framework</div>
            </motion.div>
            
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="space-y-3"
            >
              <div className="text-4xl font-bold text-gradient gradient-regulatory">24/7</div>
              <div className="text-sm text-paragraph-section-3">Data Collection</div>
              <div className="text-xs text-paragraph-section-3 opacity-75">Real-Time Intelligence</div>
            </motion.div>
            
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.3 }}
              className="space-y-3"
            >
              <div className="text-4xl font-bold text-gradient gradient-economic">100%</div>
              <div className="text-sm text-paragraph-section-3">Evidence-Based</div>
              <div className="text-xs text-paragraph-section-3 opacity-75">No Guesswork</div>
            </motion.div>
          </div>
        </div>
      </section>
    </main>
  );
}