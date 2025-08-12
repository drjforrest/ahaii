'use client';

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import CountryCarousel from '@/components/dashboard/CountryCarousel';
import { featuredCountries } from '@/data/countries';
import { CountryWithScore } from '@/types/country';

export default function DashboardPage() {
  const [countries, setCountries] = useState<CountryWithScore[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate loading data
    const loadData = async () => {
      setLoading(true);
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      setCountries(featuredCountries);
      setLoading(false);
    };

    loadData();
  }, []);

  const handleCountrySelect = (countryId: string) => {
    // Navigate to country detail page
    window.location.href = `/country?id=${countryId}`;
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-section-1">
        <div className="text-center space-y-4">
          <motion.div
            className="w-16 h-16 border-4 border-primary border-t-transparent rounded-full mx-auto"
            animate={{ rotate: 360 }}
            transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
          />
          <p className="text-lg text-paragraph-section-1">Loading country intelligence...</p>
        </div>
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-section-1">
      {/* Dashboard Header */}
      <section className="section bg-section-1 py-16">
        <div className="container text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h1 className="text-5xl font-bold text-foreground mb-6">
              Health AI Readiness
              <span className="text-gradient gradient-primary block">
                Intelligence Dashboard
              </span>
            </h1>
            <p className="text-xl text-paragraph-section-1 max-w-4xl mx-auto">
              Real-time assessment of health AI infrastructure readiness across Africa. 
              Powered by continuous intelligence collection and automated analysis.
            </p>
          </motion.div>
        </div>
      </section>

      {/* Country Carousel */}
      <section className="section bg-section-2 py-8">
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