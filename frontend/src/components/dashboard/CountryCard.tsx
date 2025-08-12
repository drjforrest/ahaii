'use client';

import Image from 'next/image';
import Link from 'next/link';
import { CountryData, CountryCardProps, AHAIIPillarType } from '@/types/ahaii';

interface PillarProgressBarProps {
  label: string;
  score: number;
  description: string;
  colorClass: string;
}

function PillarProgressBar({ label, score, description, colorClass }: PillarProgressBarProps) {
  return (
    <div>
      <div className="flex justify-between items-center mb-1">
        <span className="text-card-foreground font-medium">{label}</span>
        <div className="w-2/5 bg-section-3 rounded-full h-2.5">
          <div 
            className={`${colorClass} h-2.5 rounded-full transition-all duration-500`}
            style={{ width: `${score}%` }}
          />
        </div>
      </div>
      <p className="text-muted-foreground text-xs">{description}</p>
    </div>
  );
}

export default function CountryCard({ 
  country, 
  className = "", 
  variant = 'default',
  showTrends = false,
  onSelect 
}: CountryCardProps) {
  return (
    <div className={`flex-shrink-0 w-96 carousel-card ${className}`}>
      <div className="card bg-opacity-95 backdrop-filter backdrop-blur-lg overflow-hidden h-full flex flex-col card-inner">
        <div className="p-6 flex-grow">
          <div className="flex items-center mb-4">
            <Image
              src={country.flag}
              alt={`Flag of ${country.name}`}
              width={40}
              height={40}
              className="rounded-full mr-4"
            />
            <div>
              <h3 className="text-xl font-bold text-card-foreground">{country.name}</h3>
              <p className="text-muted-foreground text-sm">Overall Score: {country.overallScore}</p>
            </div>
          </div>
          <p className="text-card-content text-sm mb-6">{country.description}</p>
          
          <div className="space-y-4 text-sm">
            <PillarProgressBar
              label="Physical Infrastructure"
              score={country.pillars.physical.score}
              description={country.pillars.physical.description}
              colorClass="bg-physical"
            />
            
            <PillarProgressBar
              label="Human Capital"
              score={country.pillars.humanCapital.score}
              description={country.pillars.humanCapital.description}
              colorClass="bg-human-capital"
            />
            
            <PillarProgressBar
              label="Regulatory Frameworks"
              score={country.pillars.regulatory.score}
              description={country.pillars.regulatory.description}
              colorClass="bg-regulatory"
            />
            
            <PillarProgressBar
              label="Economic Ecosystem"
              score={country.pillars.economic.score}
              description={country.pillars.economic.description}
              colorClass="bg-economic"
            />
          </div>
        </div>
        
        <div className="p-6 bg-section-3 bg-opacity-50 mt-auto">
          <Link 
            href={`/country-profiles/${country.id}`}
            className="btn btn-primary btn-lg w-full text-center"
          >
            View Full Report
          </Link>
        </div>
      </div>
    </div>
  );
}