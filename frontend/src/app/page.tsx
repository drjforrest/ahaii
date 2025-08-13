"use client";

import HealthcareCrisisCarousel from "@/components/dashboard/HealthcareCrisisCarousel";
import Image from "next/image";
import Link from "next/link";

const pillars = [
  {
    id: "physical",
    title: "Strategic Physical Infrastructure",
    weight: "30%",
    description:
      "Medical-grade data centres, EMR systems, telemedicine networks, and computational capacity for clinical AI deployment.",
    icon: "/images/svg-icons/other-icons/server-icon-dark.svg",
    secondaryIcon: "/images/svg-icons/other-icons/hospital-icon-light.svg",
    color: "domain-physical",
    examples: [
      "EMR adoption rates",
      "GPU clusters for medical imaging",
      "Telemedicine platform coverage",
    ],
  },
  {
    id: "human-capital",
    title: "Investment in Human Capital",
    weight: "30%",
    description:
      "AI-trained clinicians, biomedical informatics programs, and technical workforce pipelines for health AI implementation.",
    icon: "/images/svg-icons/other-icons/users-icon-dark.svg",
    secondaryIcon: "/images/svg-icons/other-icons/doctors-icon-light.svg",
    color: "domain-human-capital",
    examples: [
      "Clinical AI training programs",
      "Medical informatics degrees",
      "AI-literate healthcare workforce",
    ],
  },
  {
    id: "regulatory",
    title: "Resilient Regulatory & Legal Infrastructure",
    weight: "25%",
    description:
      "Medical AI approval pathways, health data governance frameworks, and clinical validation standards.",
    icon: "/images/svg-icons/other-icons/regulatory-icon-dark.svg",
    secondaryIcon: "/images/svg-icons/other-icons/certificate-icon-light.svg",
    color: "domain-regulatory",
    examples: [
      "Medical AI approval processes",
      "Health data privacy laws",
      "Clinical validation requirements",
    ],
  },
  {
    id: "economic",
    title: "Economic & Market Opportunity",
    weight: "15%",
    description:
      "Investment capacity, market maturity, and financial sustainability for health AI ecosystem development.",
    icon: "/images/svg-icons/other-icons/economic-icon-dark.svg",
    secondaryIcon: "/images/svg-icons/other-icons/medical-chart-icon-light.svg",
    color: "domain-economic",
    examples: [
      "Health AI investment flows",
      "Market demand indicators",
      "Research funding capacity",
    ],
  },
];

export default function AHAIILandingPage() {
  return (
    <main className="page-main">
      {/* Hero Section */}
      <section className="section bg-section-1 hero-section">
        <div className="container">
          <div className="hero-grid">
            {/* Left Column: Hero Title and Text Content */}
            <div className="flex flex-col h-full pt-8 lg:pt-12">
              <div className="flex-1 space-y-6">
                <h1 className="text-4xl lg:text-5xl font-bold text-foreground leading-tight">
                  Health is Unique.
                  <span className="text-3xl block" style={{ color: '#4A9B8E' }}>
                    AI Solutions Must Be Too.
                  </span>
                </h1>
                <p className="text-xl text-paragraph-section-1 leading-relaxed">
                  Broad AI readiness frameworks miss the nuances of Africa's unique health challenges.
                </p>
                
                {/* Crisis boxes moved from carousel */}
                <div className="grid grid-cols-1 gap-4 mt-6">
                  <div className="bg-kpi-critical/10 border border-kpi-critical/20 rounded-lg p-4">
                    <div className="font-semibold text-kpi-critical mb-2">Healthcare Crisis</div>
                    <div className="text-sm text-paragraph-section-1">
                      US spends $14,570 per capita while African countries average $85, with 6.1M healthcare worker shortage
                    </div>
                  </div>
                  <div className="bg-primary/10 border border-primary/20 rounded-lg p-4">
                    <div className="font-semibold text-primary mb-2">AI Infrastructure Gap</div>
                    <div className="text-sm text-paragraph-section-1">
                      111x fewer data centers, 90% lack digital skills, creating barriers to AI-driven healthcare solutions
                    </div>
                  </div>
                </div>
              </div>
                            {/* CTA button moved to bottom */}
              <div className="mt-2">
                <Link
                  href="#solution"
                  className="btn btn-primary btn-lg inline-flex items-center gap-3 mb-4"
                >
                  <Image
                    src="/images/svg-icons/other-icons/compass-icon-dark.svg"
                    alt="Navigation"
                    width={20}
                    height={20}
                  />
                  Discover the Solution
                </Link>
              </div>
            </div>
              
            {/* Right Column: Healthcare Crisis Carousel */}
            <div>
              <HealthcareCrisisCarousel />
            </div>
          </div>
        </div>
      </section>

      {/* Problem Section */}
      <section className="section bg-section-2">
        <div className="container">
          <div className="text-center space-y-8">
            <h2 className="text-3xl font-bold text-foreground">
              Health AI is Promising but has Fundamentally Different Challenges
            </h2>

            <div className="grid md:grid-cols-3 gap-8">
              <div className="card space-y-4">
                <div className="w-12 h-12 mx-auto bg-primary/40 rounded-lg flex items-center justify-center">
                  <Image
                    src="/images/svg-icons/other-icons/globe-icon-dark.svg"
                    alt="Global development"
                    width={36}
                    height={36}
                  />
                </div>
                <h3 className="text-lg font-semibold text-card-foreground">
                  Developed Elsewhere
                </h3>
                <p className="text-card-content">
                  Most health AI solutions are developed in high-resource
                  settings, and not tailored to African patient population
                  contexts.
                </p>
              </div>

              <div className="card space-y-4">
                <div className="w-12 h-12 mx-auto bg-primary/40 rounded-lg flex items-center justify-center">
                  <Image
                    src="/images/svg-icons/other-icons/ai-software-icon-dark.svg"
                    alt="AI training"
                    width={36}
                    height={36}
                  />
                </div>
                <h3 className="text-lg font-semibold text-card-foreground">
                  Trained on Others' Data
                </h3>
                <p className="text-card-content">
                  AI models learn from Western datasets, creating algorithms
                  that fail to recognize local demographics and disease
                  presentations.
                </p>
              </div>

              <div className="card space-y-4">
                <div className="w-12 h-12 mx-auto bg-primary/40 rounded-lg flex items-center justify-center">
                  <Image
                    src="/images/svg-icons/other-icons/medical-chart-icon-dark.svg"
                    alt="Deployment challenges"
                    width={36}
                    height={36}
                  />
                </div>
                <h3 className="text-lg font-semibold text-card-foreground">
                  Deployed Blindly
                </h3>
                <p className="text-card-content">
                  Without infrastructure assessment, AI deployments fail,
                  wasting resources and missing opportunities to save lives.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Academic Foundation */}
      <section className="section bg-section-3">
        <div className="container">
          <div className="space-y-12">
            <div className="text-center space-y-6">
              <h2 className="text-3xl font-bold text-foreground">
                Building on Established
                <span className="text-gradient gradient-human-capital block">
                  AI Readiness Science
                </span>
              </h2>
              <p className="text-lg text-paragraph-section-3 max-w-4xl mx-auto leading-relaxed">
                AI readiness assessment isn't new. The IMF, Oxford, and Gates
                Foundation have mapped digital infrastructure across all African
                countries. But health AI has unique requirements that even
                comprehensive frameworks can miss.
              </p>
            </div>

            <div className="bg-section-2 rounded-lg p-8 text-center">
              <h3 className="text-xl font-semibold text-foreground mb-4">
                The Unique Domains that
              </h3>
              <p className="text-paragraph-section-2 max-w-3xl mx-auto leading-relaxed">
                Healthcare AI requires{" "}
                <strong className="text-foreground">
                  Highly technical and specialized equipment
                </strong>
                ,
                <strong className="text-foreground">
                  Clinical and public health certified personnel
                </strong>
                ,
                <strong className="text-foreground">
                  Specialized regulatory pathways
                </strong>
                , and
                <strong className="text-foreground">
                  validation standards
                </strong>{" "}
                that protect patient safety.
                <br />
                <br />
                <strong className="text-foreground">
                  That's where AHAII comes in.
                </strong>{" "}
                Health is unique. Our assessment framework should be too.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Four Domains Framework */}
      <section id="solution" className="section bg-section-4">
        <div className="container">
          <div className="space-y-8">
            {/* Framework Introduction Card */}
            <div className="card text-center space-y-6 p-8">
              <div className="w-16 h-16 mx-auto bg-primary/30 rounded-full flex items-center justify-center">
                <Image
                  src="/images/svg-icons/other-icons/compass-icon-dark.svg"
                  alt="AHAII Direction"
                  width={32}
                  height={32}
                />
              </div>
              <h2 className="text-3xl font-bold text-card-foreground">
                Four Domains.
                <span className="text-gradient gradient-physical block">
                  One Framework.
                </span>
              </h2>
              <p className="text-lg text-card-content max-w-4xl mx-auto leading-relaxed">
                The African Health AI Infrastructure Index (AHAII) adapts proven
                readiness methodology to health AI deployment. It provides
                stakeholders with data-driven intelligence to measure readiness
                and chart strategic paths forward.
              </p>

              <div className="grid md:grid-cols-2 gap-6 max-w-4xl mx-auto">
                <div className="bg-section-4/50 p-4 rounded-lg space-y-2">
                  <h3 className="text-lg font-semibold text-card-foreground">
                    Health-Specific Assessment
                  </h3>
                  <p className="text-card-content text-sm">
                    We continuously monitor data sources in academia, media, and
                    government to provide a comprehensive view of health AI
                    challenges and successes.
                  </p>
                </div>
                <div className="bg-section-4/50 p-4 rounded-lg space-y-2">
                  <h3 className="text-lg font-semibold text-card-foreground">
                    Africa-Focused Intelligence
                  </h3>
                  <p className="text-card-content text-sm">
                    Continental coverage with deep understanding of African
                    health systems, disease burdens, and development partnership
                    landscape.
                  </p>
                </div>
              </div>
            </div>

            {/* Four Pillars Grid */}
            <div className="grid lg:grid-cols-2 gap-6">
              {pillars.map((pillar) => (
                <div key={pillar.id} className="card space-y-4">
                  <div className="flex items-start gap-4">
                    <div
                      className={`w-12 h-12 ${pillar.color} rounded-lg flex items-center justify-center flex-shrink-0`}
                    >
                      <Image
                        src={pillar.icon}
                        alt={pillar.title}
                        width={24}
                        height={24}
                      />
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        <h3 className="text-xl font-semibold text-card-foreground">
                          {pillar.title}
                        </h3>
                        <span className="text-xs px-2 py-1 bg-section-3 rounded text-card-foreground">
                          {pillar.weight}
                        </span>
                      </div>
                      <p className="text-card-content text-sm leading-relaxed">
                        {pillar.description}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Real-Time Intelligence Section */}
      <section className="section bg-section-2">
        <div className="container">
          <div className="space-y-8">
            <div className="text-center space-y-4">
              <h2 className="text-3xl font-bold text-foreground">
                Automated by
                <span className="text-gradient gradient-physical block">
                  Real-Time Intelligence
                </span>
              </h2>
              <p className="text-lg text-paragraph-section-2 max-w-3xl mx-auto leading-relaxed">
                AHAII continuously monitors health AI developments across
                Africa, providing current intelligence to guide infrastructure
                decisions.
              </p>
            </div>

            <div className="grid md:grid-cols-3 gap-6">
              <div className="card space-y-3">
                <div className="w-12 h-12 mx-auto bg-primary/40 rounded-lg flex items-center justify-center">
                  <Image
                    src="/images/svg-icons/other-icons/search-icon-1-light.svg"
                    alt="Academic monitoring"
                    width={28}
                    height={28}
                  />
                </div>
                <h3 className="text-lg font-semibold text-card-foreground">
                  Academic Intelligence
                </h3>
                <p className="text-card-content text-sm">
                  Scans global scientific research for health AI infrastructure
                  developments and implementation outcomes, extracting relevant
                  insights.
                </p>
              </div>

              <div className="card space-y-3">
                <div className="w-12 h-12 mx-auto bg-primary/40 rounded-lg flex items-center justify-center">
                  <Image
                    src="/images/svg-icons/other-icons/dashboard-icon-dark.svg"
                    alt="Policy tracking"
                    width={28}
                    height={28}
                  />
                </div>
                <h3 className="text-lg font-semibold text-card-foreground">
                  Policy Monitoring
                </h3>
                <p className="text-card-content text-sm">
                  Tracks regulatory changes and infrastructure deployments
                  across African health ministries, multilateral agencies, and
                  biotech industries.
                </p>
              </div>

              <div className="card space-y-3">
                <div className="w-12 h-12 mx-auto bg-primary/40 rounded-lg flex items-center justify-center">
                  <Image
                    src="/images/svg-icons/other-icons/ai-software-icon-dark.svg"
                    alt="Real-time analysis"
                    width={36}
                    height={36}
                  />
                </div>
                <h3 className="text-lg font-semibold text-card-foreground">
                  AI-Powered Analysis
                </h3>
                <p className="text-card-content text-sm">
                  Uses semantic parsing and extraction and machine learning to
                  classify infrastructure signals and identify emerging trends.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="section bg-section-4">
        <div className="container">
          <div className="text-center space-y-8">
            <div className="space-y-4">
              <h2 className="text-3xl font-bold text-foreground leading-tight">
                Health AI is Revolutionary.
                <span className="text-gradient gradient-human-capital block">
                  Transformative power.
                </span>
                Solutions tailored to Africa's unique challenges.
              </h2>
              <p className="text-lg text-paragraph-section-4 max-w-3xl mx-auto leading-relaxed">
                Readiness efforts for this transformative change must also be
                tailored to the specific challenges faced by African countries
                and driven by local data to inform the path forward for each
                country's unique context.
              </p>
            </div>

            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <Link
                href="/dashboard"
                className="btn btn-primary btn-lg inline-flex items-center gap-3"
              >
                <Image
                  src="/images/svg-icons/other-icons/dashboard-icon-dark.svg"
                  alt="Dashboard"
                  width={20}
                  height={20}
                />
                Explore Country Data
              </Link>

              <Link
                href="/methods"
                className="btn btn-secondary btn-lg inline-flex items-center gap-3"
              >
                <Image
                  src="/images/svg-icons/other-icons/methods-icon-dark.svg"
                  alt="Methodology"
                  width={20}
                  height={20}
                />
                View Methodology
              </Link>
            </div>

            <div className="pt-4">
              <p className="text-paragraph-section-4 max-w-2xl mx-auto text-sm">
                Join the movement toward local data-driven health AI
                infrastructure development.
                <Link
                  href="/about"
                  className="text-primary-light hover:text-primary underline ml-1"
                >
                  Learn more about our mission
                </Link>
                .
              </p>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
