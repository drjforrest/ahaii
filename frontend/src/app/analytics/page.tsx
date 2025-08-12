"use client";

import React, { useState, useEffect } from "react";
import {
  Database,
  Globe,
  TrendingUp,
  Shield,
  CheckCircle,
  Activity,
  FileText,
  Users,
  Server,
  Clock,
  Target,
  Zap,
  BarChart3,
  PieChart,
  LineChart,
  Calendar,
} from "lucide-react";
// Removed adaptive-text components, using standard HTML elements
import Image from "next/image";

interface AnalyticsData {
  headline_stats: {
    total_records: number;
    countries_covered: number;
    days_operational: number;
    records_last_24h: number;
  };
  data_sources: {
    academic_papers: number;
    government_docs: number;
    news_articles: number;
    total_sources: number;
  };
  quality_metrics: {
    verified_records: number;
    high_confidence: number;
    peer_reviewed: number;
    avg_african_relevance: number;
    avg_ai_relevance: number;
  };
  system_health: {
    uptime_days: number;
    successful_runs: number;
    last_update: string;
    avg_daily_collection: number;
  };
  top_domains: Record<string, number>;
  top_countries: Record<string, number>;
}

interface ActivityData {
  records_last_24h: number;
  records_last_7d: number;
  records_last_30d: number;
  avg_records_per_day: number;
  days_operational: number;
  total_records: number;
  uptime_days: number;
  successful_pipeline_runs: number;
  failed_pipeline_runs: number;
  success_rate: number;
}

export default function AnalyticsPage() {
  const [analyticsData, setAnalyticsData] = useState<AnalyticsData | null>(null);
  const [activityData, setActivityData] = useState<ActivityData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastRefresh, setLastRefresh] = useState<Date>(new Date());

  const fetchAnalytics = async () => {
    try {
      setLoading(true);
      const [dashboardResponse, activityResponse] = await Promise.all([
        fetch('/api/analytics/dashboard'),
        fetch('/api/analytics/activity'),
      ]);
      
      if (!dashboardResponse.ok || !activityResponse.ok) {
        throw new Error('Failed to fetch analytics data');
      }
      
      const [dashboardData, activityData] = await Promise.all([
        dashboardResponse.json(),
        activityResponse.json(),
      ]);
      
      setAnalyticsData(dashboardData);
      setActivityData(activityData);
      setLastRefresh(new Date());
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
      console.error('Analytics fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAnalytics();
    
    // Auto-refresh every 5 minutes
    const interval = setInterval(fetchAnalytics, 5 * 60 * 1000);
    return () => clearInterval(interval);
  }, []);

  const handleRefresh = async () => {
    // Trigger backend cache refresh
    try {
      await fetch('/api/analytics/refresh', { method: 'POST' });
      await fetchAnalytics();
    } catch (err) {
      console.error('Refresh error:', err);
      await fetchAnalytics(); // Try to fetch anyway
    }
  };

  if (loading && !analyticsData) {
    return (
      <div className="min-h-screen" style={{ backgroundColor: "var(--color-background)" }}>
        <div className="flex items-center justify-center min-h-screen">
          <div className="text-center">
            <Activity className="h-12 w-12 animate-pulse mx-auto mb-4" style={{ color: "var(--color-primary)" }} />
            <p className="text-lg" style={{ color: "var(--color-foreground)" }}>
              Loading analytics data...
            </p>
          </div>
        </div>
      </div>
    );
  }

  if (error && !analyticsData) {
    return (
      <div className="min-h-screen" style={{ backgroundColor: "var(--color-background)" }}>
        <div className="flex items-center justify-center min-h-screen">
          <div className="text-center">
            <Shield className="h-12 w-12 mx-auto mb-4" style={{ color: "var(--color-destructive)" }} />
            <p className="text-lg mb-4" style={{ color: "var(--color-foreground)" }}>
              Error loading analytics: {error}
            </p>
            <button
              onClick={fetchAnalytics}
              className="btn btn-primary"
            >
              Retry
            </button>
          </div>
        </div>
      </div>
    );
  }

  const formatNumber = (num: number) => {
    if (num >= 1000000) {
      return (num / 1000000).toFixed(1) + 'M';
    }
    if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'K';
    }
    return num.toLocaleString();
  };

  const formatDate = (dateString: string) => {
    try {
      return new Date(dateString).toLocaleString();
    } catch {
      return dateString;
    }
  };

  return (
    <div className="min-h-screen" style={{ backgroundColor: "var(--color-background)" }}>
      {/* Hero Section */}
      <section
        className="py-16"
        style={{ backgroundColor: "var(--color-background-section-1)" }}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            {/* Analytics Badge */}
            <div
              className="inline-flex items-center px-4 py-2 rounded-full text-sm font-medium mb-6"
              style={{
                backgroundColor: "var(--color-primary)",
                color: "var(--color-primary-foreground)",
              }}
            >
              <BarChart3 className="h-4 w-4 mr-2" />
              Live Analytics Dashboard
            </div>

            <h1 className="text-4xl md:text-6xl font-bold mb-6 text-white">
              Data Collection
              <span className="text-gradient gradient-human-capital block">
                Intelligence Center
              </span>
            </h1>

            <p className="text-xl max-w-4xl mx-auto leading-relaxed mb-8 text-white opacity-90">
              Real-time analytics showcasing our comprehensive health AI infrastructure
              data collection across the African continent. Every metric reflects our
              commitment to evidence-based intelligence.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <button
                onClick={handleRefresh}
                disabled={loading}
                className="btn btn-primary btn-lg inline-flex items-center gap-3"
              >
                <Activity className={`h-5 w-5 ${loading ? 'animate-spin' : ''}`} />
                {loading ? 'Refreshing...' : 'Refresh Data'}
              </button>
              
              <div className="flex items-center gap-2 text-sm" style={{ color: "var(--color-muted-foreground)" }}>
                <Clock className="h-4 w-4" />
                Last updated: {lastRefresh.toLocaleTimeString()}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Headline Stats */}
      <section
        className="py-16"
        style={{ backgroundColor: "var(--color-background-section-2)" }}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold mb-4" style={{ color: "var(--color-foreground)" }}>
              🎉 Look How Hard We're Working! 🎉
            </h2>
            <p className="text-lg" style={{ color: "var(--color-muted-foreground)" }}>
              Comprehensive health AI infrastructure intelligence across Africa
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {analyticsData && [
              {
                icon: <Database className="h-8 w-8" />,
                title: "Total Records",
                value: formatNumber(analyticsData.headline_stats.total_records),
                subtitle: "Infrastructure intelligence records collected",
                color: "var(--color-primary)",
                bgColor: "var(--color-primary-background)",
              },
              {
                icon: <Globe className="h-8 w-8" />,
                title: "Countries Covered",
                value: analyticsData.headline_stats.countries_covered.toString(),
                subtitle: "African countries analyzed",
                color: "var(--color-info)",
                bgColor: "var(--color-info-background)",
              },
              {
                icon: <Calendar className="h-8 w-8" />,
                title: "Days Operational",
                value: analyticsData.headline_stats.days_operational.toString(),
                subtitle: "Days of continuous data collection",
                color: "var(--color-accent)",
                bgColor: "var(--color-accent-background)",
              },
              {
                icon: <TrendingUp className="h-8 w-8" />,
                title: "Last 24 Hours",
                value: formatNumber(analyticsData.headline_stats.records_last_24h),
                subtitle: "New records collected today",
                color: "var(--color-success)",
                bgColor: "var(--color-success-background)",
              },
            ].map((stat, index) => (
              <div
                key={index}
                className="p-8 rounded-2xl border transition-all duration-300 hover:shadow-xl hover:scale-105"
                style={{
                  backgroundColor: "var(--color-card)",
                  borderColor: "var(--color-border)",
                }}
              >
                <div
                  className="p-3 rounded-lg mb-4 inline-block"
                  style={{ backgroundColor: stat.bgColor }}
                >
                  {React.cloneElement(stat.icon, { 
                    style: { color: stat.color }
                  })}
                </div>
                <div
                  className="text-3xl font-bold mb-2"
                  style={{ color: stat.color }}
                >
                  {stat.value}
                </div>
                <div className="text-lg font-semibold mb-1" style={{ color: "var(--color-card-foreground)" }}>
                  {stat.title}
                </div>
                <div className="text-sm" style={{ color: "var(--color-muted-foreground)" }}>
                  {stat.subtitle}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Data Sources Breakdown */}
      <section
        className="py-16"
        style={{ backgroundColor: "var(--color-background-section-3)" }}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold mb-4" style={{ color: "var(--color-foreground)" }}>
              Data Sources Conquered
            </h2>
            <p className="text-lg" style={{ color: "var(--color-muted-foreground)" }}>
              Comprehensive multi-source intelligence gathering
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {analyticsData && [
              {
                icon: <FileText className="h-6 w-6" />,
                title: "Academic Papers",
                value: formatNumber(analyticsData.data_sources.academic_papers),
                description: "Peer-reviewed research processed",
                color: "var(--color-primary)",
              },
              {
                icon: <Shield className="h-6 w-6" />,
                title: "Government Docs",
                value: formatNumber(analyticsData.data_sources.government_docs),
                description: "Official documents analyzed",
                color: "var(--color-info)",
              },
              {
                icon: <Activity className="h-6 w-6" />,
                title: "News Articles",
                value: formatNumber(analyticsData.data_sources.news_articles),
                description: "Health AI news monitored",
                color: "var(--color-accent)",
              },
              {
                icon: <Target className="h-6 w-6" />,
                title: "Source Types",
                value: analyticsData.data_sources.total_sources.toString(),
                description: "Different data source categories",
                color: "var(--color-success)",
              },
            ].map((source, index) => (
              <div
                key={index}
                className="card p-6 text-center transition-all duration-300 hover:shadow-lg hover:-translate-y-1"
              >
                <div
                  className="w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-4"
                  style={{ backgroundColor: source.color, color: "white" }}
                >
                  {source.icon}
                </div>
                <div
                  className="text-2xl font-bold mb-2"
                  style={{ color: source.color }}
                >
                  {source.value}
                </div>
                <div className="text-lg font-semibold mb-2 text-card-foreground">
                  {source.title}
                </div>
                <div className="text-sm text-card-content">
                  {source.description}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Quality Metrics */}
      <section
        className="py-16"
        style={{ backgroundColor: "var(--color-background-section-4)" }}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold mb-4 text-white">
              Quality Excellence Report
            </h2>
            <p className="text-lg text-white opacity-90">
              Rigorous validation ensuring reliable intelligence
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-5 gap-6">
            {analyticsData && [
              {
                title: "Verified Records",
                value: formatNumber(analyticsData.quality_metrics.verified_records),
                subtitle: "Quality controlled",
                color: "var(--color-primary)",
              },
              {
                title: "High Confidence",
                value: formatNumber(analyticsData.quality_metrics.high_confidence),
                subtitle: "Reliable data points",
                color: "var(--color-info)",
              },
              {
                title: "Peer Reviewed",
                value: formatNumber(analyticsData.quality_metrics.peer_reviewed),
                subtitle: "Academic standards",
                color: "var(--color-accent)",
              },
              {
                title: "African Relevance",
                value: `${analyticsData.quality_metrics.avg_african_relevance}%`,
                subtitle: "Continental focus",
                color: "var(--color-success)",
              },
              {
                title: "AI Relevance",
                value: `${analyticsData.quality_metrics.avg_ai_relevance}%`,
                subtitle: "Health AI targeted",
                color: "var(--color-warning)",
              },
            ].map((metric, index) => (
              <div
                key={index}
                className="card p-6 text-center transition-all duration-300 hover:shadow-lg hover:scale-105"
              >
                <div
                  className="text-3xl font-bold mb-2"
                  style={{ color: metric.color }}
                >
                  {metric.value}
                </div>
                <div className="text-sm font-semibold mb-1 text-card-foreground">
                  {metric.title}
                </div>
                <div className="text-xs text-card-content">
                  {metric.subtitle}
                </div>
              </div>
            ))}
          </div>

          {/* System Performance */}
          <div className="mt-12">
            <div className="card p-8">
              <h3 className="text-2xl font-semibold mb-8 text-center text-card-foreground">
                System Performance & Reliability
              </h3>
              
              <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                {analyticsData && activityData && [
                  {
                    icon: <Clock className="h-6 w-6" />,
                    title: "System Uptime",
                    value: `${analyticsData.system_health.uptime_days} days`,
                    color: "var(--color-primary)",
                  },
                  {
                    icon: <CheckCircle className="h-6 w-6" />,
                    title: "Success Rate",
                    value: `${activityData.success_rate}%`,
                    color: "var(--color-success)",
                  },
                  {
                    icon: <TrendingUp className="h-6 w-6" />,
                    title: "Daily Collection",
                    value: `${analyticsData.system_health.avg_daily_collection} records`,
                    color: "var(--color-info)",
                  },
                  {
                    icon: <Zap className="h-6 w-6" />,
                    title: "Pipeline Runs",
                    value: formatNumber(analyticsData.system_health.successful_runs),
                    color: "var(--color-accent)",
                  },
                ].map((stat, index) => (
                  <div key={index} className="text-center">
                    <div
                      className="w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-3"
                      style={{ backgroundColor: stat.color, color: "white" }}
                    >
                      {stat.icon}
                    </div>
                    <div
                      className="text-xl font-bold mb-1"
                      style={{ color: stat.color }}
                    >
                      {stat.value}
                    </div>
                    <div className="text-sm text-card-content">
                      {stat.title}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Top Domains and Countries */}
      <section
        className="py-16"
        style={{ backgroundColor: "var(--color-background-section-2)" }}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold mb-4" style={{ color: "var(--color-foreground)" }}>
              Geographic & Domain Coverage
            </h2>
            <p className="text-lg" style={{ color: "var(--color-muted-foreground)" }}>
              Our comprehensive reach across domains and countries
            </p>
          </div>

          <div className="grid lg:grid-cols-2 gap-12">
            {/* Top Countries */}
            <div className="card p-8">
              <div className="flex items-center gap-3 mb-6">
                <Globe className="h-6 w-6" style={{ color: "var(--color-primary)" }} />
                <h3 className="text-xl font-semibold text-card-foreground">
                  Top Countries by Data Volume
                </h3>
              </div>
              
              <div className="space-y-4">
                {analyticsData && Object.entries(analyticsData.top_countries)
                  .slice(0, 8)
                  .map(([country, count], index) => (
                    <div key={country} className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <div
                          className="w-8 h-8 rounded flex items-center justify-center text-sm font-bold"
                          style={{
                            backgroundColor: index < 3 ? "var(--color-primary)" : "var(--color-muted)",
                            color: index < 3 ? "white" : "var(--color-muted-foreground)",
                          }}
                        >
                          {index + 1}
                        </div>
                        <span className="text-card-foreground font-medium">{country}</span>
                      </div>
                      <span className="text-card-content font-semibold">
                        {formatNumber(count)} records
                      </span>
                    </div>
                  ))}
              </div>
            </div>

            {/* Top Domains */}
            <div className="card p-8">
              <div className="flex items-center gap-3 mb-6">
                <Server className="h-6 w-6" style={{ color: "var(--color-accent)" }} />
                <h3 className="text-xl font-semibold text-card-foreground">
                  Top Data Source Domains
                </h3>
              </div>
              
              <div className="space-y-4">
                {analyticsData && Object.entries(analyticsData.top_domains)
                  .slice(0, 8)
                  .map(([domain, count], index) => (
                    <div key={domain} className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <div
                          className="w-8 h-8 rounded flex items-center justify-center text-sm font-bold"
                          style={{
                            backgroundColor: index < 3 ? "var(--color-accent)" : "var(--color-muted)",
                            color: index < 3 ? "white" : "var(--color-muted-foreground)",
                          }}
                        >
                          {index + 1}
                        </div>
                        <span className="text-card-foreground font-medium text-sm">
                          {domain}
                        </span>
                      </div>
                      <span className="text-card-content font-semibold">
                        {formatNumber(count)}
                      </span>
                    </div>
                  ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Recent Activity Summary */}
      <section
        className="py-16"
        style={{ backgroundColor: "var(--color-background-section-1)" }}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold mb-4 text-white">
              Recent Activity Highlights
            </h2>
            <p className="text-lg text-white opacity-90">
              Live intelligence collection across the continent
            </p>
          </div>

          {activityData && (
            <div className="grid md:grid-cols-3 gap-8">
              <div className="card p-8 text-center">
                <TrendingUp className="h-12 w-12 mx-auto mb-4" style={{ color: "var(--color-success)" }} />
                <div className="text-3xl font-bold mb-2" style={{ color: "var(--color-success)" }}>
                  {formatNumber(activityData.records_last_7d)}
                </div>
                <div className="text-lg font-semibold mb-2 text-card-foreground">Last 7 Days</div>
                <div className="text-sm text-card-content">
                  New infrastructure intelligence
                </div>
              </div>

              <div className="card p-8 text-center">
                <Calendar className="h-12 w-12 mx-auto mb-4" style={{ color: "var(--color-info)" }} />
                <div className="text-3xl font-bold mb-2" style={{ color: "var(--color-info)" }}>
                  {formatNumber(activityData.records_last_30d)}
                </div>
                <div className="text-lg font-semibold mb-2 text-card-foreground">Last 30 Days</div>
                <div className="text-sm text-card-content">
                  Monthly collection volume
                </div>
              </div>

              <div className="card p-8 text-center">
                <Target className="h-12 w-12 mx-auto mb-4" style={{ color: "var(--color-primary)" }} />
                <div className="text-3xl font-bold mb-2" style={{ color: "var(--color-primary)" }}>
                  {activityData.avg_records_per_day.toFixed(1)}
                </div>
                <div className="text-lg font-semibold mb-2 text-card-foreground">Daily Average</div>
                <div className="text-sm text-card-content">
                  Records collected per day
                </div>
              </div>
            </div>
          )}
        </div>
      </section>

      {/* Call to Action */}
      <section
        className="py-16"
        style={{ backgroundColor: "var(--color-background-section-4)" }}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl font-bold mb-6 text-white">
            Evidence-Based
            <span className="text-gradient gradient-human-capital block">
              Health AI Intelligence
            </span>
          </h2>
          
          <p className="text-xl max-w-4xl mx-auto leading-relaxed mb-8 text-white opacity-90">
            This comprehensive data collection effort represents one of the most systematic 
            approaches to mapping health AI infrastructure capabilities across the African continent.
            Every metric demonstrates our commitment to evidence-based intelligence.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a href="/dashboard" className="btn btn-primary btn-lg inline-flex items-center gap-3">
              <Image
                src="/images/svg-icons/other-icons/dashboard-icon-light.svg"
                alt="Dashboard"
                width={20}
                height={20}
              />
              Explore Country Data
            </a>
            <a href="/methods" className="btn btn-secondary btn-lg inline-flex items-center gap-3">
              <Image
                src="/images/svg-icons/other-icons/methods-icon-light.svg"
                alt="Methods"
                width={20}
                height={20}
              />
              View Methodology
            </a>
          </div>
        </div>
      </section>
    </div>
  );
}
