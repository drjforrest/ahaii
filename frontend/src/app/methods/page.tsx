"use client";

import {
  Globe,
  Search,
  Zap,
  CheckCircle,
  ArrowRight,
  Database,
  Code,
  Server,
  Monitor,
  Shield,
  Users,
  TrendingUp,
  Target,
} from "lucide-react";
import React from "react";
// Using standard HTML elements instead of missing adaptive-text components

export default function MethodologyPage() {
  const stages = [
    {
      number: "01",
      title: "Health AI Infrastructure Intelligence",
      subtitle: "Comprehensive",
      description:
        "Systematic collection of health AI infrastructure signals across four pillars: medical-grade infrastructure, clinical AI literacy, regulatory frameworks, and economic sustainability—from academic research, government policies, and health system reports.",
      metrics: [
        "85-90% coverage rate",
        "50+ health AI indicators",
        "Real-time monitoring",
      ],
      icon: <Globe />,
    },
    {
      number: "02",
      title: "Multi-Source Validation",
      subtitle: "Accuracy",
      description:
        "Cross-validation of infrastructure assessments through multiple sources—ensuring accuracy through expert review, institutional verification, and confidence scoring for health AI readiness metrics.",
      metrics: ["Multi-source validation", "Expert verification", "95% accuracy"],
      icon: <Search />,
    },
    {
      number: "03",
      title: "Infrastructure Scoring",
      subtitle: "Analysis",
      description:
        "Systematic scoring of health AI readiness across the four infrastructure pillars, with contextual analysis of healthcare systems, policy environments, and development priorities specific to each African country.",
      metrics: [
        "Four-pillar assessment",
        "90% indicator coverage",
        "Country-specific analysis",
      ],
      icon: <Zap />,
    },
  ];

  const techStack = [
    {
      category: "Backend",
      icon: <Server />,
      technologies: [
        "PostgreSQL with health data extensions",
        "FastAPI async health data processing",
        "Python health AI assessment pipeline",
        "Automated health infrastructure monitoring",
      ],
    },
    {
      category: "Frontend",
      icon: <Monitor />,
      technologies: [
        "Next.js 15 with TypeScript",
        "Recharts health infrastructure visualization",
        "AHAII Tailwind CSS design system",
        "React Server Components",
      ],
    },
    {
      category: "Infrastructure",
      icon: <Shield />,
      technologies: [
        "Docker containerization",
        "OAuth 2.0 health data security",
        "Real-time infrastructure monitoring",
        "Horizontal scaling for 54 countries",
      ],
    },
  ];

  const qualityMetrics = [
    {
      label: "Field Completion",
      target: "90%+",
      current: "87%",
    },
    {
      label: "Accuracy Rate",
      target: "95%+",
      current: "96%",
    },
    {
      label: "Max Latency",
      target: "24h",
      current: "18h",
    },
    {
      label: "Country Coverage",
      target: "54",
      current: "54",
    },
  ];

  return (
    <div
      className="min-h-screen"
      style={{ backgroundColor: "var(--color-background)" }}
    >
      {/* Hero Section */}
      <section
        className="py-16"
        style={{ backgroundColor: "var(--color-background-section-1)" }}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            {/* Technical Documentation Badge */}
            <div
              className="inline-flex items-center px-4 py-2 rounded-full text-sm font-medium mb-6"
              style={{
                backgroundColor: "var(--color-primary)",
                color: "var(--color-primary-foreground)",
              }}
            >
              <Code className="h-4 w-4 mr-2" />
              Technical Methodology
            </div>

            <h1 className="text-4xl md:text-6xl font-bold mb-6 text-white">
              Methodology
            </h1>

            <p className="text-xl max-w-4xl mx-auto leading-relaxed text-white opacity-90">
              A systematic framework for assessing health AI infrastructure readiness across Africa—combining 
              evidence collection, multi-source validation, and expert analysis to support informed, 
              evidence-based health AI development decisions.
            </p>
          </div>
        </div>
      </section>

      {/* Three-Stage Pipeline */}
      <section
        className="py-16"
        style={{ backgroundColor: "var(--color-background-section-2)" }}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4 text-white">
              Three-Stage Health AI Infrastructure Assessment
            </h2>
            <p className="text-lg text-white">Intelligence → Validation → Assessment</p>
          </div>

          <div className="grid md:grid-cols-3 gap-10 mb-16">
            {stages.map((stage, index) => (
              <div key={index} className="relative group">
                <div
                  className="p-8 rounded-xl shadow-lg hover:shadow-2xl hover:-translate-y-2 transition-all duration-300 border-l-4"
                  style={{
                    backgroundColor: "var(--color-card)",
                    borderLeftColor:
                      index === 0
                        ? "var(--color-primary)"
                        : index === 1
                          ? "var(--color-info)"
                          : "var(--color-accent)",
                  }}
                >
                  <div className="flex items-center mb-6">
                    <div
                      className="w-16 h-16 rounded-full flex items-center justify-center mr-5 border-2 flex-shrink-0"
                      style={{
                        backgroundColor:
                          index === 0
                            ? "var(--color-primary)"
                            : index === 1
                              ? "var(--color-info)"
                              : "var(--color-accent)",
                        borderColor:
                          index === 0
                            ? "var(--color-primary)"
                            : index === 1
                              ? "var(--color-info)"
                              : "var(--color-accent)",
                        color: "white",
                      }}
                    >
                      {React.cloneElement(stage.icon, { 
                        className: "h-8 w-8",
                        style: { minWidth: '2rem', minHeight: '2rem' }
                      })}
                    </div>
                    <div>
                      <div
                        className="text-sm font-bold"
                        style={{
                          color:
                            index === 0
                              ? "var(--color-primary)"
                              : index === 1
                                ? "var(--color-info)"
                                : "var(--color-accent)",
                        }}
                      >
                        STAGE {stage.number}
                      </div>
                      <div className="text-xl font-semibold text-gray-800">
                        {stage.title}
                      </div>
                      <div
                        className="text-md font-medium"
                        style={{
                          color:
                            index === 0
                              ? "var(--color-primary)"
                              : index === 1
                                ? "var(--color-info)"
                                : "var(--color-accent)",
                        }}
                      >
                        {stage.subtitle}
                      </div>
                    </div>
                  </div>

                  <p className="mb-8 min-h-32 text-gray-600 leading-relaxed">{stage.description}</p>

                  <div className="space-y-4">
                    {stage.metrics.map((metric, idx) => (
                      <div key={idx} className="flex items-center text-sm">
                        <CheckCircle
                          className="h-5 w-5 mr-3"
                          style={{
                            color:
                              index === 0
                                ? "var(--color-primary)"
                                : index === 1
                                  ? "var(--color-info)"
                                  : "var(--color-accent)",
                          }}
                        />
                        <span className="text-gray-600">{metric}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {index < stages.length - 1 && (
                  <div className="hidden md:block absolute top-1/2 -right-5 transform -translate-y-1/2 group-hover:scale-110 transition-transform z-10">
                    <div 
                      className="w-12 h-12 rounded-full flex items-center justify-center shadow-lg"
                      style={{
                        backgroundColor: "var(--color-gray-700)",
                        color: "white",
                      }}
                    >
                      <ArrowRight className="h-6 w-6" />
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>

          {/* Pipeline Flow Diagram */}
          <div
            className="p-8 rounded-2xl shadow-xl border"
            style={{
              backgroundColor: "var(--color-card)",
              borderColor: "var(--color-border)",
            }}
          >
            <h3 className="text-2xl font-semibold mb-12 text-center text-gray-800">
              Complete Pipeline Flow
            </h3>
            <div className="flex flex-col md:flex-row items-center justify-between space-y-6 md:space-y-0 md:space-x-6">
              {[
                {
                  icon: <Database className="h-8 w-8" />,
                  title: "Health Infrastructure Data Aggregation",
                  subtitle: "Health system reports, medical journals, and policy documents",
                  color: "var(--color-primary)", // Input
                },
                {
                  icon: <Code className="h-8 w-8" />,
                  title: "Health AI Infrastructure Search",
                  subtitle: "Gap-filling with health system-specific queries and filters",
                  color: "var(--color-info)", // Processing
                },
                {
                  icon: <Search className="h-8 w-8" />,
                  title: "Intelligent Health Data Collection",
                  subtitle: "Automated health infrastructure monitoring and assessment",
                  color: "var(--color-accent)", // Validation
                },
                {
                  icon: <CheckCircle className="h-8 w-8" />,
                  title: "Health AI Readiness Profile Generation",
                  subtitle: "Validated, contextualized health infrastructure assessments",
                  color: "var(--color-success)", // Output
                },
              ].map((item, index, arr) => (
                <React.Fragment key={index}>
                  <div className="text-center group cursor-pointer">
                    <div
                      className="w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-3 border-2 group-hover:scale-110 transition-transform flex-shrink-0"
                      style={{
                        backgroundColor: item.color,
                        borderColor: item.color,
                        color: "white",
                      }}
                    >
                      {React.cloneElement(item.icon, { 
                        className: "h-8 w-8",
                        style: { minWidth: '2rem', minHeight: '2rem' }
                      })}
                    </div>
                    <div className="text-md font-medium text-gray-800">
                      {item.title}
                    </div>
                    <div className="text-sm text-gray-600">{item.subtitle}</div>
                  </div>
                  {index < arr.length - 1 && (
                    <div className="hidden md:flex items-center justify-center">
                      <div 
                        className="w-12 h-12 rounded-full flex items-center justify-center shadow-lg"
                        style={{
                          backgroundColor: "var(--color-gray-700)",
                          color: "white",
                        }}
                      >
                        <ArrowRight className="h-6 w-6" />
                      </div>
                    </div>
                  )}
                </React.Fragment>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Technology Stack */}
      <section
        className="py-16"
        style={{ backgroundColor: "var(--color-background-section-3)" }}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4 text-white">
              Technology Stack
            </h2>
            <p className="text-lg text-white">
              Modern, scalable architecture built for African health AI infrastructure assessment
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-10">
            {techStack.map((stack, index) => (
              <div
                key={index}
                className="p-8 rounded-2xl border-2 hover:shadow-xl transition-all duration-300 hover:-translate-y-1"
                style={{
                  backgroundColor: "var(--color-card)",
                  borderColor:
                    index === 0
                      ? "var(--color-primary)"
                      : index === 1
                        ? "var(--color-info)"
                        : "var(--color-accent)",
                }}
              >
                <div className="flex items-center mb-5">
                  <div
                    className="flex-shrink-0"
                    style={{
                      color:
                        index === 0
                          ? "var(--color-primary)"
                          : index === 1
                            ? "var(--color-info)"
                            : "var(--color-accent)",
                    }}
                  >
                    {React.cloneElement(stack.icon, { 
                      className: "h-8 w-8",
                      style: { minWidth: '2rem', minHeight: '2rem' }
                    })}
                  </div>
                  <h3
                    className="text-2xl font-semibold ml-4"
                    style={{
                      color:
                        index === 0
                          ? "var(--color-primary)"
                          : index === 1
                            ? "var(--color-info)"
                            : "var(--color-accent)",
                    }}
                  >
                    {stack.category}
                  </h3>
                </div>
                <ul className="space-y-3">
                  {stack.technologies.map((tech, idx) => (
                    <li
                      key={idx}
                      className="text-md flex items-center"
                      style={{ color: "var(--color-muted-foreground)" }}
                    >
                      <div
                        className="w-2.5 h-2.5 rounded-full mr-3 border"
                        style={{
                          backgroundColor: "var(--color-card)",
                          borderColor:
                            index === 0
                              ? "var(--color-primary)"
                              : index === 1
                                ? "var(--color-info)"
                                : "var(--color-accent)",
                        }}
                      ></div>
                      {tech}
                    </li>
                  ))}
                </ul>
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
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4 text-white">
              Data Quality & Performance
            </h2>
            <p className="text-lg text-white">
              Rigorous validation ensuring reliable intelligence
            </p>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {qualityMetrics.map((metric, index) => (
              <div
                key={index}
                className="p-6 rounded-2xl shadow-lg text-center hover:scale-105 transition-transform duration-300 border"
                style={{
                  backgroundColor: "var(--color-card)",
                  borderColor: "var(--color-border)",
                }}
              >
                <div
                  className="text-5xl font-bold mb-2"
                  style={{
                    color:
                      index === 0
                        ? "var(--color-primary)"
                        : index === 1
                          ? "var(--color-info)"
                          : index === 2
                            ? "var(--color-accent)"
                            : "#22c55e",
                  }}
                >
                  {metric.current}
                </div>
                <div className="text-md font-medium mb-1 text-gray-800">
                  {metric.label}
                </div>
                <div className="text-sm text-gray-600">
                  Target: {metric.target}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Roadmap Section */}
      <section
        className="py-16"
        style={{ backgroundColor: "var(--color-background-section-4)" }}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <div
              className="inline-flex items-center px-4 py-2 rounded-full text-sm font-medium mb-6"
              style={{
                backgroundColor: "var(--color-primary)",
                color: "var(--color-primary-foreground)",
              }}
            >
              <Target className="h-4 w-4 mr-2" />
              Strategic Evolution
            </div>
            <h2 className="text-4xl md:text-5xl font-bold mb-6 text-white">
              From Assessment to Action: AHAII Development Phases
            </h2>
            <p className="text-lg max-w-4xl mx-auto leading-relaxed text-white opacity-90">
              Having established our health AI infrastructure assessment framework, AHAII is now in the critical data collection phase—combining 
              systematic infrastructure monitoring with expert validation to build comprehensive health AI readiness profiles for each African country.
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-12 mb-16">
            {/* Phase 1 */}
            <div
              className="p-8 rounded-2xl border"
              style={{
                backgroundColor: "var(--color-card)",
                borderColor: "var(--color-border)",
              }}
            >
              <div className="flex items-center mb-6">
                <div
                  className="w-12 h-12 rounded-full flex items-center justify-center mr-4"
                  style={{
                    backgroundColor: "var(--color-primary)",
                    color: "var(--color-primary-foreground)",
                  }}
                >
                  <span className="text-lg font-bold">1</span>
                </div>
                <div>
                  <h3
                    className="text-xl font-semibold"
                    style={{ color: "var(--color-card-foreground)" }}
                  >
                    Infrastructure Data Collection & Validation
                  </h3>
                  <p
                    className="text-sm"
                    style={{ color: "var(--color-muted-foreground)" }}
                  >
                    Current Phase (Q3-Q4 2025)
                  </p>
                </div>
              </div>
              <ul
                className="space-y-3 text-sm"
                style={{ color: "var(--color-muted-foreground)" }}
              >
                <li className="flex items-start">
                  <CheckCircle className="h-4 w-4 mr-2 mt-0.5 text-green-500 flex-shrink-0" />
                  Health AI infrastructure monitoring and assessment database architecture
                </li>
                <li className="flex items-start">
                  <CheckCircle className="h-4 w-4 mr-2 mt-0.5 text-green-500 flex-shrink-0" />
                  Integration of African health system and medical technology datasets
                </li>
                <li className="flex items-start">
                  <ArrowRight className="h-4 w-4 mr-2 mt-0.5 text-blue-500 flex-shrink-0" />
                  Direct health ministry and medical institution data collaboration systems
                </li>
                <li className="flex items-start">
                  <ArrowRight className="h-4 w-4 mr-2 mt-0.5 text-blue-500 flex-shrink-0" />
                  Building trust relationships with African health AI researchers and policymakers
                </li>
              </ul>
            </div>

            {/* Phase 2 */}
            <div
              className="p-8 rounded-2xl border"
              style={{
                backgroundColor: "var(--color-card)",
                borderColor: "var(--color-border)",
              }}
            >
              <div className="flex items-center mb-6">
                <div
                  className="w-12 h-12 rounded-full flex items-center justify-center mr-4"
                  style={{
                    backgroundColor: "var(--color-accent)",
                    color: "var(--color-accent-foreground)",
                  }}
                >
                  <span className="text-lg font-bold">2</span>
                </div>
                <div>
                  <h3
                    className="text-xl font-semibold"
                    style={{ color: "var(--color-card-foreground)" }}
                  >
                    Health AI Infrastructure Intelligence Platform
                  </h3>
                  <p
                    className="text-sm"
                    style={{ color: "var(--color-muted-foreground)" }}
                  >
                    Target: January 2026
                  </p>
                </div>
              </div>
              <ul
                className="space-y-3 text-sm"
                style={{ color: "var(--color-muted-foreground)" }}
              >
                <li className="flex items-start">
                  <ArrowRight className="h-4 w-4 mr-2 mt-0.5 text-blue-500 flex-shrink-0" />
                  Health institutions trust AHAII to directly share infrastructure assessment data
                </li>
                <li className="flex items-start">
                  <ArrowRight className="h-4 w-4 mr-2 mt-0.5 text-blue-500 flex-shrink-0" />
                  Active showcasing of verified African health AI readiness improvements
                </li>
                <li className="flex items-start">
                  <ArrowRight className="h-4 w-4 mr-2 mt-0.5 text-blue-500 flex-shrink-0" />
                  Health system-driven infrastructure progress documentation
                </li>
                <li className="flex items-start">
                  <ArrowRight className="h-4 w-4 mr-2 mt-0.5 text-blue-500 flex-shrink-0" />
                  Established reputation as credible research infrastructure for African health AI
                </li>
              </ul>
            </div>
          </div>

          {/* Success Metrics */}
          <div
            className="p-8 rounded-2xl border"
            style={{
              backgroundColor: "var(--color-card)",
              borderColor: "var(--color-border)",
            }}
          >
            <h3
              className="text-2xl font-semibold mb-6 text-center"
              style={{ color: "var(--color-card-foreground)" }}
            >
              Success Metrics: Assessment Accuracy & Health AI Infrastructure Intelligence
            </h3>
            <div className="grid md:grid-cols-2 gap-8">
              <div>
                <h4
                  className="text-lg font-semibold mb-4"
                  style={{ color: "var(--color-primary)" }}
                >
                  Health AI Assessment Integrity Indicators
                </h4>
                <ul
                  className="space-y-2 text-sm"
                  style={{ color: "var(--color-muted-foreground)" }}
                >
                  <li>• Interactive infrastructure scorecards that accurately reflect country readiness levels</li>
                  <li>• Every health AI readiness claim backed by verifiable health system documentation</li>
                  <li>• User confidence metrics showing trust in platform assessment accuracy</li>
                  <li>• Academic citations referencing AHAII's health AI infrastructure methodology</li>
                </ul>
              </div>
              <div>
                <h4
                  className="text-lg font-semibold mb-4"
                  style={{ color: "var(--color-accent)" }}
                >
                  Verified Health AI Infrastructure Success
                </h4>
                <ul
                  className="space-y-2 text-sm"
                  style={{ color: "var(--color-muted-foreground)" }}
                >
                  <li>• Connection rate between infrastructure assessments and verified health system capabilities (target: &gt;80%)</li>
                  <li>• Recognition gained by health systems through verified infrastructure improvement documentation</li>
                  <li>• Replication of successful health AI infrastructure development approaches across African countries</li>
                  <li>• Adoption of assessment methodology by other health AI research institutions globally</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Vision Statement */}
      <section
        className="py-20"
        style={{ backgroundColor: "var(--color-background-section-1)" }}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <div
              className="inline-flex items-center px-4 py-2 rounded-full text-sm font-medium mb-6"
              style={{
                backgroundColor: "var(--color-primary)",
                color: "var(--color-primary-foreground)",
              }}
            >
              <Target className="h-4 w-4 mr-2" />
              Our Vision
            </div>
            <h2 className="text-4xl md:text-6xl font-bold mb-6 text-white">
              Trusted Intelligence Hub for African Health AI Infrastructure
            </h2>
            <p className="text-xl max-w-4xl mx-auto leading-relaxed text-white opacity-90">
              Our vision is to become Africa's most trusted research infrastructure 
              for health AI readiness intelligence—a humble yet rigorous scientific network 
              that transforms how we understand and support health AI infrastructure development 
              across the continent.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8 mb-16">
            {[
              {
                icon: <Users />,
                title: "For Health AI Researchers & Innovators",
                description: "Evidence platform and network connections for health AI infrastructure development",
                color: "var(--color-primary)",
                bgColor: "var(--color-primary-background)",
              },
              {
                icon: <TrendingUp />,
                title: "For Health System Funders & Investors", 
                description: "Infrastructure readiness showcase and credible third-party validation of health AI potential",
                color: "var(--color-info)",
                bgColor: "var(--color-info-background)",
              },
              {
                icon: <Shield />,
                title: "For Health Policymakers & Governments",
                description: "Evidence-based health AI infrastructure insights and data-driven strategic recommendations",
                color: "var(--color-accent)",
                bgColor: "var(--color-accent-background)",
              },
            ].map((item, index) => (
              <div
                key={index}
                className="p-8 rounded-2xl border transition-all duration-300 ease-in-out hover:shadow-lg hover:scale-105 hover:-translate-y-1"
                style={{
                  backgroundColor: "var(--color-card)",
                  borderColor: "var(--color-border)",
                }}
              >
                <div
                  className="p-3 rounded-lg mb-6 inline-block flex-shrink-0"
                  style={{
                    backgroundColor: item.bgColor,
                  }}
                >
                  {React.cloneElement(item.icon, { 
                    className: "h-6 w-6",
                    style: { 
                      color: item.color,
                      minWidth: '1.5rem',
                      minHeight: '1.5rem'
                    }
                  })}
                </div>
                <h3
                  className="text-xl font-bold mb-4"
                  style={{ color: "var(--color-card-foreground)" }}
                >
                  {item.title}
                </h3>
                <p
                  className="text-base"
                  style={{ color: "var(--color-muted-foreground)" }}
                >
                  {item.description}
                </p>
              </div>
            ))}
          </div>

          {/* Vision Details */}
          <div
            className="p-8 rounded-2xl border"
            style={{
              backgroundColor: "var(--color-card)",
              borderColor: "var(--color-border)",
            }}
          >
            <p className="text-lg leading-relaxed text-center text-gray-300">
              A future in which every African country's health AI infrastructure readiness is visible, valued, and strategically developed to serve human wellbeing.
              By making patterns of health system capabilities, AI readiness gaps, and infrastructure investment needs transparent, we seek to inform decisions that move beyond hype—toward 
              equitable progress in healthcare delivery, clinical outcomes, and health system resilience.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}