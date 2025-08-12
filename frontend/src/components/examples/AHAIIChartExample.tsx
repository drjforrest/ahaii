"use client";

import { motion } from 'framer-motion';
import { TrendingUp, TrendingDown, Activity, BarChart3 } from 'lucide-react';

// Example chart data for African countries
const sampleData = [
  {
    country: "South Africa",
    overall: 78,
    physical: 82,
    humanCapital: 75,
    regulatory: 80,
    economic: 76,
    tier: "Tier 1",
    trend: "up",
    change: 5.2
  },
  {
    country: "Kenya",
    overall: 65,
    physical: 70,
    humanCapital: 68,
    regulatory: 60,
    economic: 62,
    tier: "Tier 2", 
    trend: "up",
    change: 3.1
  },
  {
    country: "Ghana",
    overall: 58,
    physical: 55,
    humanCapital: 64,
    regulatory: 52,
    economic: 60,
    tier: "Tier 2",
    trend: "down",
    change: -1.5
  },
  {
    country: "Rwanda",
    overall: 62,
    physical: 58,
    humanCapital: 70,
    regulatory: 65,
    economic: 55,
    tier: "Tier 2",
    trend: "up", 
    change: 4.8
  }
];

// Animation variants
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1
    }
  }
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 }
};

export default function AHAIIChartExample() {
  return (
    <div className="section bg-section-2">
      <div className="container">
        <motion.div
          className="text-center mb-12"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          <h2 className="text-3xl font-bold mb-4 text-foreground">
            Health AI Readiness Dashboard
          </h2>
          <p className="text-lg max-w-2xl mx-auto text-paragraph-section-2">
            Interactive visualization of the four-pillar assessment framework
          </p>
        </motion.div>

        {/* Overall Summary Cards */}
        <motion.div
          className="grid md:grid-cols-4 gap-6 mb-12"
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
        >
          {/* Total Countries Card */}
          <motion.div variants={itemVariants} className="data-card">
            <div className="data-card-title">Total Countries</div>
            <div className="data-card-value text-primary">54</div>
            <div className="data-card-trend kpi-good">
              <Activity className="w-3 h-3 mr-1" />
              Active assessments
            </div>
          </motion.div>

          {/* Average Score Card */}
          <motion.div variants={itemVariants} className="data-card">
            <div className="data-card-title">Average Readiness</div>
            <div className="data-card-value text-human-capital">65.8</div>
            <div className="data-card-trend data-card-trend-up">
              <TrendingUp className="w-3 h-3 mr-1" />
              +2.4% from last quarter
            </div>
          </motion.div>

          {/* Tier 1 Countries Card */}
          <motion.div variants={itemVariants} className="data-card">
            <div className="data-card-title">Tier 1 Countries</div>
            <div className="data-card-value text-physical">8</div>
            <div className="data-card-trend kpi-excellent">
              <BarChart3 className="w-3 h-3 mr-1" />
              Implementation ready
            </div>
          </motion.div>

          {/* Improvement Rate Card */}
          <motion.div variants={itemVariants} className="data-card">
            <div className="data-card-title">Improvement Rate</div>
            <div className="data-card-value text-economic">87%</div>
            <div className="data-card-trend data-card-trend-up">
              <TrendingUp className="w-3 h-3 mr-1" />
              Countries showing growth
            </div>
          </motion.div>
        </motion.div>

        {/* Country Comparison Chart */}
        <motion.div
          className="chart-container mb-12"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
        >
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-xl font-semibold text-card-foreground">
              Country Readiness Comparison
            </h3>
            <div className="flex gap-2">
              <div className="kpi-badge kpi-badge-excellent">Tier 1</div>
              <div className="kpi-badge kpi-badge-good">Tier 2</div>
              <div className="kpi-badge kpi-badge-fair">Tier 3</div>
            </div>
          </div>

          {/* Legend */}
          <div className="flex flex-wrap gap-4 mb-6 text-sm">
            <div className="flex items-center">
              <div className="w-3 h-3 rounded mr-2 bg-physical"></div>
              <span>Physical Infrastructure</span>
            </div>
            <div className="flex items-center">
              <div className="w-3 h-3 rounded mr-2 bg-human-capital"></div>
              <span>Human Capital</span>
            </div>
            <div className="flex items-center">
              <div className="w-3 h-3 rounded mr-2 bg-regulatory"></div>
              <span>Regulatory Framework</span>
            </div>
            <div className="flex items-center">
              <div className="w-3 h-3 rounded mr-2 bg-economic"></div>
              <span>Economic Potential</span>
            </div>
          </div>

          {/* Chart Data */}
          <div className="space-y-6">
            {sampleData.map((country, index) => (
              <motion.div
                key={country.country}
                className="p-4 rounded-lg border border-border"
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
              >
                {/* Country Header */}
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center">
                    <img
                      src={`/images/svg-icons/country-icons/${country.country.toLowerCase().replace(' ', '-')}-icon-light.svg`}
                      alt={country.country}
                      className="w-8 h-8 mr-3 rounded"
                    />
                    <div>
                      <h4 className="font-semibold text-card-foreground">
                        {country.country}
                      </h4>
                      <div className="flex items-center text-sm">
                        <span className={`kpi-badge kpi-badge-${
                          country.overall >= 70 ? 'excellent' :
                          country.overall >= 60 ? 'good' :
                          country.overall >= 50 ? 'fair' : 'poor'
                        } mr-2`}>
                          {country.tier}
                        </span>
                        <span className={`flex items-center ${
                          country.trend === 'up' ? 'data-card-trend-up' : 'data-card-trend-down'
                        }`}>
                          {country.trend === 'up' ? (
                            <TrendingUp className="w-3 h-3 mr-1" />
                          ) : (
                            <TrendingDown className="w-3 h-3 mr-1" />
                          )}
                          {country.change > 0 ? '+' : ''}{country.change}%
                        </span>
                      </div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-2xl font-bold text-card-foreground">
                      {country.overall}
                    </div>
                    <div className="text-sm text-muted-foreground">
                      Overall Score
                    </div>
                  </div>
                </div>

                {/* Progress Bars */}
                <div className="space-y-3">
                  {/* Physical Infrastructure */}
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-muted-foreground">Physical Infrastructure</span>
                      <span className="font-medium">{country.physical}/100</span>
                    </div>
                    <div className="w-full bg-secondary-200 rounded-full h-2">
                      <motion.div
                        className="h-2 rounded-full bg-physical"
                        initial={{ width: 0 }}
                        whileInView={{ width: `${country.physical}%` }}
                        viewport={{ once: true }}
                        transition={{ duration: 1, delay: index * 0.1 }}
                      />
                    </div>
                  </div>

                  {/* Human Capital */}
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-muted-foreground">Human Capital</span>
                      <span className="font-medium">{country.humanCapital}/100</span>
                    </div>
                    <div className="w-full bg-secondary-200 rounded-full h-2">
                      <motion.div
                        className="h-2 rounded-full bg-human-capital"
                        initial={{ width: 0 }}
                        whileInView={{ width: `${country.humanCapital}%` }}
                        viewport={{ once: true }}
                        transition={{ duration: 1, delay: index * 0.1 + 0.1 }}
                      />
                    </div>
                  </div>

                  {/* Regulatory Framework */}
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-muted-foreground">Regulatory Framework</span>
                      <span className="font-medium">{country.regulatory}/100</span>
                    </div>
                    <div className="w-full bg-secondary-200 rounded-full h-2">
                      <motion.div
                        className="h-2 rounded-full bg-regulatory"
                        initial={{ width: 0 }}
                        whileInView={{ width: `${country.regulatory}%` }}
                        viewport={{ once: true }}
                        transition={{ duration: 1, delay: index * 0.1 + 0.2 }}
                      />
                    </div>
                  </div>

                  {/* Economic Potential */}
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-muted-foreground">Economic Potential</span>
                      <span className="font-medium">{country.economic}/100</span>
                    </div>
                    <div className="w-full bg-secondary-200 rounded-full h-2">
                      <motion.div
                        className="h-2 rounded-full bg-economic"
                        initial={{ width: 0 }}
                        whileInView={{ width: `${country.economic}%` }}
                        viewport={{ once: true }}
                        transition={{ duration: 1, delay: index * 0.1 + 0.3 }}
                      />
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Chart Color Palette Demo */}
        <motion.div
          className="chart-container"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          <h3 className="text-xl font-semibold text-card-foreground mb-6">
            Chart Color Palette
          </h3>
          <div className="grid grid-cols-4 md:grid-cols-8 gap-4">
            {Array.from({ length: 8 }, (_, i) => (
              <motion.div
                key={i}
                className="text-center"
                whileHover={{ scale: 1.05 }}
                transition={{ duration: 0.2 }}
              >
                <div 
                  className={`w-full h-16 rounded-lg mb-2 shadow-sm`}
                  style={{ backgroundColor: `var(--color-chart-${i + 1})` }}
                />
                <div className="text-xs text-muted-foreground">
                  Chart {i + 1}
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  );
}
