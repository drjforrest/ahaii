// Using standard HTML elements instead of missing components
import {
  Award,
  Calendar,
  Globe,
  Heart,
  Lightbulb,
  Mail,
  MapPin,
  Shield,
  Target,
  Users,
} from "lucide-react";
import { Metadata } from "next";

export const metadata: Metadata = {
  title: "About AHAII | Leadership & Mission",
  description:
    "Learn about AHAII's mission to assess health AI infrastructure readiness across Africa. Meet our leadership team and discover our vision for evidence-based health AI development.",
  keywords: [
    "AHAII",
    "African Health AI",
    "infrastructure assessment",
    "health AI readiness",
    "leadership team",
    "AI development Africa",
    "healthcare AI",
  ],
};

export default function AboutPage() {
  return (
    <div
      className="min-h-screen"
      style={{ backgroundColor: "var(--color-background)" }}
    >
      {/* Section 1: Hero Section - Darkest Background */}
      <section
        className="py-16 relative"
        style={{ backgroundColor: "var(--color-background-section-1)" }}
      >
        {/* Background Africa Outline */}
        <div className="absolute inset-0 flex justify-center items-center z-0 opacity-10">
          <img
            src="/africa-outline-grey.png"
            alt="Africa outline"
            width={800}
            height={800}
            className="object-contain"
          />
        </div>

        <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <div
              className="inline-flex items-center px-4 py-2 rounded-full text-sm font-medium mb-6"
              style={{
                backgroundColor: "var(--color-primary)",
                color: "var(--color-primary-foreground)",
              }}
            >
              <Heart className="h-4 w-4 mr-2" />
              Our Story & Mission
            </div>

            <h1 className="text-4xl md:text-6xl font-bold mb-12 leading-tight text-white">
              About AHAII
            </h1>

            {/* Mission Statement */}
            <div className="card max-w-5xl mx-auto mb-12 p-8">
              <div className="flex items-center justify-center mb-6">
                <Target
                  className="h-6 w-6 mr-3"
                  style={{ color: "var(--color-primary)" }}
                />
                <h2 className="text-xl font-bold text-card-foreground">
                  Our Mission
                </h2>
              </div>
              <p className="text-lg leading-relaxed text-card-content">
                To systematically assess each African country's readiness to implement, scale, and regulate artificial intelligence solutions in healthcare by evaluating four critical infrastructure pillars: medical-grade infrastructure, clinical AI literacy, regulatory frameworks, and economic sustainability.
              </p>
            </div>

            {/* Core Values */}
            <div className="flex flex-wrap justify-center gap-6 md:gap-8">
              <div className="text-center">
                <div
                  className="w-12 h-12 rounded-4xl flex items-center justify-center mx-auto mb-3"
                  style={{
                    backgroundColor: "var(--color-accent)",
                    color: "var(--color-accent-foreground)",
                  }}
                >
                  <Lightbulb className="h-6 w-6" />
                </div>
                <div className="text-sm font-semibold text-white">
                  Evidence-Based
                </div>
              </div>
              <div className="text-center">
                <div
                  className="w-12 h-12 rounded-4xl flex items-center justify-center mx-auto mb-3"
                  style={{
                    backgroundColor: "var(--color-info)",
                    color: "var(--color-info-foreground)",
                  }}
                >
                  <Users className="h-6 w-6" />
                </div>
                <div className="text-sm font-semibold text-white">
                  Health-Focused
                </div>
              </div>
              <div className="text-center">
                <div
                  className="w-12 h-12 rounded-4xl flex items-center justify-center mx-auto mb-3"
                  style={{
                    backgroundColor: "var(--color-primary)",
                    color: "var(--color-primary-foreground)",
                  }}
                >
                  <Award className="h-6 w-6" />
                </div>
                <div className="text-sm font-semibold text-white">
                  Systematic
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Section 2: Leadership Team */}
      <section
        className="py-16"
        style={{ backgroundColor: "var(--color-background-section-2)" }}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-8">
            <div
              className="inline-flex items-center px-4 py-2 rounded-full text-sm font-medium mb-3"
              style={{
                backgroundColor: "var(--color-info)",
                color: "var(--color-info-foreground)",
              }}
            >
              <Users className="h-4 w-4 mr-2" />
              Meet Our Team
            </div>
            <h2 className="text-4xl font-bold mb-6 text-white">
              Leadership Team
            </h2>
            <p className="text-lg max-w-3xl mx-auto text-white opacity-90">
              Combining expertise in health AI infrastructure assessment and a passion for evidence-based development that serves African healthcare needs.
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8 max-w-6xl mx-auto mt-12">
            {/* Executive Director */}
            <div className="card hover:shadow-lg transition-all duration-300 p-6 md:p-8 text-center">
              <div
                className="w-24 h-24 rounded-full mx-auto mb-6 mt-4 flex items-center justify-center"
                style={{
                  backgroundColor: "var(--color-primary)",
                  color: "var(--color-primary-foreground)",
                }}
              >
                <Users className="h-12 w-12" />
              </div>

              <h3 className="text-2xl font-bold mb-2 text-card-foreground">
                Hinda Ruton
              </h3>
              <div
                className="inline-block font-semibold px-4 py-2 rounded-full text-sm mb-6"
                style={{
                  backgroundColor: "var(--color-primary)",
                  color: "var(--color-primary-foreground)",
                }}
              >
                Executive Director
              </div>

              <p className="leading-relaxed mb-6 text-left text-card-content">
                Hinda Ruton is the CEO and Founder of Africa Quantitative Sciences, Rwanda's premier data analytics firm. He and his team at AQS bring deep expertise in health data analytics to generate actionable insights for health AI infrastructure assessment. With a focus on public health outcome analytics and global health security, he has pioneered innovative data-driven solutions that enhance disease monitoring, support vaccine programs, and strengthen health systems. His vision bridges health AI technologies with the operational realities of African healthcare institutions and the lived needs of local communities.
              </p>

              <div className="flex justify-center items-center text-sm px-4 py-2 rounded-full bg-gray-200 text-gray-600">
                <MapPin className="h-4 w-4 mr-2" />
                <span className="font-medium">Kigali, Rwanda</span>
              </div>
            </div>

            {/* Scientific Director */}
            <div className="card hover:shadow-lg transition-all duration-300 p-6 md:p-8 text-center">
              <div
                className="w-24 h-24 rounded-full mx-auto mb-6 mt-4 flex items-center justify-center"
                style={{
                  backgroundColor: "var(--color-accent)",
                  color: "var(--color-accent-foreground)",
                }}
              >
                <Users className="h-12 w-12" />
              </div>

              <h3 className="text-2xl font-bold mb-2 text-card-foreground">
                Dr. Jamie Forrest
              </h3>
              <div
                className="inline-block font-semibold px-4 py-2 rounded-full text-sm mb-6"
                style={{
                  backgroundColor: "var(--color-accent)",
                  color: "var(--color-accent-foreground)",
                }}
              >
                Scientific Director
              </div>

              <p className="leading-relaxed mb-6 text-left text-card-content">
                Dr. Jamie Forrest holds a PhD in Population and Public Health from the University of British Columbia in Vancouver, Canada, and has dedicated his career to addressing health and development challenges in African countries. With years of experience living and working in Rwanda, and earlier roles in South Africa, he brings a grounded understanding of African healthcare contexts. His expertise spans digital health, clinical research methods, and implementation science—with a focus on equity-driven innovations like those powering AHAII's commitment to making health AI infrastructure assessment more accountable to African healthcare realities.
              </p>

              <div className="flex justify-center items-center text-sm px-4 py-2 rounded-full bg-gray-200 text-gray-600">
                <MapPin className="h-4 w-4 mr-2" />
                <span className="font-medium">Canada / Rwanda</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Section 3: Coming Soon - Advisory Board */}
      <section
        className="py-16"
        style={{ backgroundColor: "var(--color-background-section-3)" }}
      >
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="card mt-12 p-16 text-center">
            <div
              className="w-24 h-24 rounded-full flex items-center justify-center mx-auto mb-6"
              style={{
                backgroundColor: "var(--color-accent)",
                color: "var(--color-accent-foreground)",
              }}
            >
              <Calendar className="h-12 w-12" />
            </div>
            <div
              className="inline-block font-semibold px-4 py-2 rounded-full text-sm mb-4"
              style={{
                backgroundColor: "var(--color-accent)",
                color: "var(--color-accent-foreground)",
              }}
            >
              Coming Soon
            </div>
            <h2 className="text-3xl font-bold mb-4 text-white">
              Advisory Board
            </h2>
            <p className="text-lg max-w-3xl mx-auto leading-relaxed mb-6 text-white opacity-90">
              We are assembling a distinguished advisory board of African health AI
              researchers, healthcare policy makers, and health system practitioners to
              guide AHAII's strategic direction and ensure our infrastructure assessments
              serve the broader African health AI ecosystem.
            </p>
            <div className="inline-flex items-center px-6 py-3 rounded-full bg-gray-200 text-gray-600">
              <Globe className="h-4 w-4 mr-2" />
              <span className="font-medium">Announcements forthcoming</span>
            </div>
          </div>
        </div>
      </section>

      {/* Contact & Collaboration Section */}
      <section
        id="contact"
        className="py-16"
        style={{ backgroundColor: "var(--color-background-section-4)" }}
      >
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <div
              className="inline-flex items-center px-4 py-2 rounded-full text-sm font-medium mb-6"
              style={{
                backgroundColor: "var(--color-primary)",
                color: "var(--color-primary-foreground)",
              }}
            >
              <Mail className="h-4 w-4 mr-2" />
              Get In Touch
            </div>
            <h2 className="text-4xl font-bold mb-6 text-white">
              Contact & Collaboration
            </h2>
            <p className="text-xl max-w-3xl mx-auto mb-8 text-white opacity-90">
              Partner with us in building evidence-based health AI infrastructure 
              assessment across Africa
            </p>

            {/* Funding Statement */}
            <div
              className="card max-w-4xl mx-auto mb-12 p-8 transition-all duration-300 hover:shadow-lg"
              style={{
                borderColor: "var(--color-primary)",
                borderWidth: "2px",
              }}
            >
              <div className="flex items-center justify-center mb-6">
                <div 
                  className="w-12 h-12 rounded-full flex items-center justify-center mr-4"
                  style={{
                    backgroundColor: "var(--color-primary)",
                    color: "var(--color-primary-foreground)",
                  }}
                >
                  <Heart className="h-6 w-6" />
                </div>
                <span className="text-xl font-bold text-card-foreground">
                  Self-Supporting Initiative
                </span>
              </div>
              <div 
                className="w-full h-1 rounded-full mb-6"
                style={{ backgroundColor: "var(--color-primary-background)" }}
              >
                <div 
                  className="h-full w-1/3 rounded-full"
                  style={{ backgroundColor: "var(--color-primary)" }}
                ></div>
              </div>
              <p className="leading-relaxed text-lg text-center text-card-content">
                <strong className="block text-xl mb-3 text-card-foreground">
                  AHAII is currently self-supporting.
                </strong>
                If you are interested in helping us grow our reach and expand
                our health AI infrastructure assessment to serve more African healthcare systems, please get in
                touch with us below.
              </p>
            </div>
          </div>

          {/* Contact Form Placeholder */}
          <div className="mb-16 text-center">
            <div className="card max-w-2xl mx-auto p-8">
              <h3 className="text-xl font-bold mb-4 text-card-foreground">Get In Touch</h3>
              <p className="text-card-content mb-6">
                Contact us to learn more about AHAII's health AI infrastructure assessment work.
              </p>
              <a 
                href="mailto:info@ahaii.org" 
                className="inline-flex items-center px-6 py-3 rounded-full text-white font-semibold transition-colors"
                style={{ backgroundColor: "var(--color-primary)" }}
              >
                <Mail className="h-4 w-4 mr-2" />
                Contact Us
              </a>
            </div>
          </div>

          <div className="text-center">
            <div
              className="card max-w-4xl mx-auto p-8 transition-all duration-300 hover:shadow-lg"
              style={{
                borderColor: "var(--color-accent)",
                borderWidth: "2px",
              }}
            >
              <div className="flex items-center justify-center mb-6">
                <div 
                  className="w-12 h-12 rounded-full flex items-center justify-center mr-4"
                  style={{
                    backgroundColor: "var(--color-accent)",
                    color: "var(--color-accent-foreground)",
                  }}
                >
                  <Shield className="h-6 w-6" />
                </div>
                <span className="text-xl font-bold text-card-foreground">
                  Transparency Note
                </span>
              </div>
              <div 
                className="w-full h-1 rounded-full mb-6"
                style={{ backgroundColor: "var(--color-accent-background)" }}
              >
                <div 
                  className="h-full w-full rounded-full"
                  style={{ backgroundColor: "var(--color-accent)" }}
                ></div>
              </div>
              <p className="leading-relaxed mb-4 text-center text-card-content">
                <strong className="block text-lg mb-3 text-card-foreground">
                  AHAII operates as an independent initiative.
                </strong>
              </p>
              <p className="leading-relaxed text-center text-card-content">
                Our funding sources and methodology are fully documented to
                ensure accountability in our mission to provide transparent
                health AI infrastructure assessment across Africa.
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}