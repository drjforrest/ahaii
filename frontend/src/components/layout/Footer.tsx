"use client";

import Link from "next/link";

export default function Footer() {
  const handleMouseEnter = (e: React.MouseEvent<HTMLAnchorElement>) => {
    (e.target as HTMLElement).style.opacity = "0.8";
  };

  const handleMouseLeave = (e: React.MouseEvent<HTMLAnchorElement>) => {
    (e.target as HTMLElement).style.opacity = "1";
  };

  const linkStyle = {
    color: "var(--color-foreground)",
    textDecoration: "none",
    transition: "opacity 0.2s ease"
  };

  return (
    <footer
      className="border-t border-border py-12"
      style={{ backgroundColor: "var(--color-background-section-1)" }}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid md:grid-cols-4 gap-8">
          <div>
            <h4
              className="font-semibold mb-4"
              style={{ color: "var(--color-cyan-400)" }}
            >
              Assessment
            </h4>
            <ul className="space-y-2">
              <li>
                <Link 
                  href="/dashboard" 
                  style={linkStyle}
                  onMouseEnter={handleMouseEnter}
                  onMouseLeave={handleMouseLeave}
                >
                  Country Rankings
                </Link>
              </li>
              <li>
                <Link 
                  href="/methodology" 
                  style={linkStyle}
                  onMouseEnter={handleMouseEnter}
                  onMouseLeave={handleMouseLeave}
                >
                  Scoring Framework
                </Link>
              </li>
              <li>
                <Link 
                  href="/reports" 
                  style={linkStyle}
                  onMouseEnter={handleMouseEnter}
                  onMouseLeave={handleMouseLeave}
                >
                  Analysis Reports
                </Link>
              </li>
            </ul>
          </div>
          <div>
            <h4
              className="font-semibold mb-4"
              style={{ color: "var(--color-cyan-300)" }}
            >
              Country Data
            </h4>
            <ul className="space-y-2">
              <li>
                <Link 
                  href="/countries" 
                  style={linkStyle}
                  onMouseEnter={handleMouseEnter}
                  onMouseLeave={handleMouseLeave}
                >
                  Country Profiles
                </Link>
              </li>
              <li>
                <Link 
                  href="/pillars" 
                  style={linkStyle}
                  onMouseEnter={handleMouseEnter}
                  onMouseLeave={handleMouseLeave}
                >
                  Pillar Analysis
                </Link>
              </li>
              <li>
                <Link 
                  href="/tiers" 
                  style={linkStyle}
                  onMouseEnter={handleMouseEnter}
                  onMouseLeave={handleMouseLeave}
                >
                  Tier Classification
                </Link>
              </li>
            </ul>
          </div>
          <div>
            <h4
              className="font-semibold mb-4"
              style={{ color: "var(--color-green-400)" }}
            >
              Resources
            </h4>
            <ul className="space-y-2">
              <li>
                <Link 
                  href="/publications" 
                  style={linkStyle}
                  onMouseEnter={handleMouseEnter}
                  onMouseLeave={handleMouseLeave}
                >
                  Research Publications
                </Link>
              </li>
              <li>
                <Link 
                  href="/case-studies" 
                  style={linkStyle}
                  onMouseEnter={handleMouseEnter}
                  onMouseLeave={handleMouseLeave}
                >
                  Implementation Case Studies
                </Link>
              </li>
              <li>
                <Link 
                  href="/network" 
                  style={linkStyle}
                  onMouseEnter={handleMouseEnter}
                  onMouseLeave={handleMouseLeave}
                >
                  Expert Network
                </Link>
              </li>
            </ul>
          </div>
          <div>
            <h4
              className="font-semibold mb-4"
              style={{ color: "var(--color-gray-300)" }}
            >
              About
            </h4>
            <ul className="space-y-2">
              <li>
                <Link 
                  href="/about" 
                  style={linkStyle}
                  onMouseEnter={handleMouseEnter}
                  onMouseLeave={handleMouseLeave}
                >
                  Mission
                </Link>
              </li>
              <li>
                <Link 
                  href="/team" 
                  style={linkStyle}
                  onMouseEnter={handleMouseEnter}
                  onMouseLeave={handleMouseLeave}
                >
                  Research Team
                </Link>
              </li>
              <li>
                <Link 
                  href="/contact" 
                  style={linkStyle}
                  onMouseEnter={handleMouseEnter}
                  onMouseLeave={handleMouseLeave}
                >
                  Contact
                </Link>
              </li>
            </ul>
          </div>
        </div>
        <div className="border-t border-border mt-8 pt-8 text-center">
          <p style={{ color: "var(--color-foreground)" }}>
            &copy; 2025 AHAII. Assessing health AI readiness across Africa.
          </p>
          <p className="text-sm mt-2" style={{ color: "var(--color-foreground)" }}>
            Four-pillar framework • Evaluating 54 African countries • Supporting evidence-based health AI investment
          </p>
        </div>
      </div>
    </footer>
  );
}