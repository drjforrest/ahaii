'use client';

import Link from 'next/link';
import CountryCard from '@/components/dashboard/CountryCard';
import { CountryData } from '@/types/ahaii';

// Sample country data - will connect to backend later
const countryData: CountryData[] = [
  {
    id: 'south-africa',
    name: 'South Africa',
    code: 'ZA',
    flag: 'https://lh3.googleusercontent.com/aida-public/AB6AXuAWUQcjP-wpTMwj-Jr3fAVQvam3lOxCFhj72IL08Af0otn5WvPAHVrlUgt0h2uDJEA_9N0qi8EZwvUTnF0o2Cd__q42ZjmdoepX5rkH6gRkoeA8t5kwRh-E73fvR0i74hjy4Z48sK2BGkJuhCB3iqa3VyqUTttuevSQBjtL8Pn7MHaa9eDU0VVx1esfrp9NINtRG-IiInYhlBMOzEIk4SO_8k5cbux6lNj0whIRoHdgsHs26Kxoc6G5INLueMpPPtfAjdlVbpSp-34P',
    region: 'Southern Africa',
    overallScore: 78.5,
    description: 'South Africa shows strong readiness with robust infrastructure and evolving legal frameworks. Investment in digital literacy programs is boosting its human capital.',
    pillars: {
      physical: { score: 85, description: 'High mobile broadband penetration and significant investments in data centers.' },
      humanCapital: { score: 75, description: 'Growing pool of tech talent, but disparities in access to quality education remain.' },
      regulatory: { score: 80, description: 'Comprehensive data protection laws are in place, with ongoing AI policy development.' },
      economic: { score: 72, description: 'A vibrant startup scene supported by increasing venture capital funding.' }
    },
    lastAssessment: '2024-01-15',
    dataQuality: {
      overallConfidence: 0.85,
      primarySources: 12,
      expertValidation: true,
      lastVerification: '2024-01-15'
    }
  },
  {
    id: 'nigeria',
    name: 'Nigeria',
    code: 'NG',
    flag: 'https://lh3.googleusercontent.com/aida-public/AB6AXuDXzq86rVIGy5ugQok0xytOLDLvDCVpZikliAy3SIchEuAezley7XPtqDHcBaBLPi3oE4ULNZ31PuA7P9R8p3726tCnecd4TiSQcfUjLoVD6lfPQAQnmECvSYgVJ087TnLzrgQvZQkwPlx2Wjun9RDiVRzSgZUn5clH43641NjWubdaLBNVAAjOSzYPoScZB2CwJWwvpz4PIeWzCiAfLjo0BvHYSnwFv2TefaL5J1QGHScphRaKVhb8w1KzLGjeEZCej2azGC8kGvS1',
    region: 'Western Africa',
    overallScore: 65.2,
    description: 'Nigeria is rapidly growing its tech scene, driving a dynamic economic ecosystem. Focus is needed on infrastructure development to match its human capital potential.',
    pillars: {
      physical: { score: 60, description: 'Challenges with reliable power supply and internet connectivity persist in some areas.' },
      humanCapital: { score: 70, description: 'A large, youthful population fuels a dynamic and entrepreneurial workforce.' },
      regulatory: { score: 55, description: 'National AI strategy is in development, but implementation is in early stages.' },
      economic: { score: 68, description: 'Africa\'s largest tech hub, with strong growth in fintech and e-commerce.' }
    },
    lastAssessment: '2024-01-10',
    dataQuality: {
      overallConfidence: 0.78,
      primarySources: 8,
      expertValidation: true,
      lastVerification: '2024-01-10'
    }
  },
  {
    id: 'kenya',
    name: 'Kenya',
    code: 'KE',
    flag: 'https://lh3.googleusercontent.com/aida-public/AB6AXuB8q0GxtD5exT60dVOQFj6GrM3nuoKog-Yokbl9xtp8Xgr6l9BkNWob1XuY5WNGnVvAoM12lyr9KgU2FRhq9VUpWS24-n8lDzf38bpu1rOnUTbqdj5knROiA9K4aoF828iPa02AY7ciKgTZ5JB8uEIyyw3Dmm_9ssyavXTGguFwB9EVLegfmHy3b4Nfvls1b0FqcOrCcDsJQXBM0U18n44mPUsGL1WODsCHyuwJLxZUDW9-1besv8NWzS3ss-csyIsnuef9YAnIgZFZ',
    region: 'Eastern Africa',
    overallScore: 71.8,
    description: 'Kenya\'s "Silicon Savannah" fosters a vibrant economic ecosystem and innovation. Continued progress in legal frameworks will be key to unlocking its full AI potential.',
    pillars: {
      physical: { score: 75, description: 'Widespread mobile money adoption provides a unique platform for digital services.' },
      humanCapital: { score: 68, description: 'Strong emphasis on STEM education and a growing number of innovation hubs.' },
      regulatory: { score: 72, description: 'Data protection act is in place, but specific AI governance is still emerging.' },
      economic: { score: 70, description: 'A leader in mobile tech innovation, attracting significant international investment.' }
    },
    lastAssessment: '2024-01-12',
    dataQuality: {
      overallConfidence: 0.82,
      primarySources: 10,
      expertValidation: true,
      lastVerification: '2024-01-12'
    }
  },
  {
    id: 'egypt',
    name: 'Egypt',
    code: 'EG',
    flag: 'https://lh3.googleusercontent.com/aida-public/AB6AXuD21pSbvpChTV2QXAw4UQwkCawKsfKa2RF55WXd_qDbXEILg926h4uo16FaNGUIKvIF2XI3o9oFk0R6N7_nOcQsbcwxCmj0dFbdyyHT6dfeottyCllBj0Eow8B8MvHopilmcjjTZhEz27Z-gc3G7g7v8Pux3xmwn-79WZ8KvUbyLcWl5xAO_l0oBzmOArgcoHj68T6ojCMeT7zqgA45p7hnBUDqh8aC_UyVXo5VbXgEDzGJzU94mwNXS56GoOstzn1R_-Qbt_0tE_Th',
    region: 'Northern Africa',
    overallScore: 74.3,
    description: 'Egypt benefits from strong government support for tech infrastructure. The country is making strides in developing a skilled workforce for the AI era.',
    pillars: {
      physical: { score: 80, description: 'Government-led initiatives are rapidly expanding national fiber-optic networks.' },
      humanCapital: { score: 70, description: 'Efforts to build AI skills are underway through universities and public programs.' },
      regulatory: { score: 75, description: 'A national AI council has been established to guide strategy and regulation.' },
      economic: { score: 71, description: 'Growing outsourcing and shared services industry is driving tech adoption.' }
    },
    lastAssessment: '2024-01-08',
    dataQuality: {
      overallConfidence: 0.88,
      primarySources: 14,
      expertValidation: true,
      lastVerification: '2024-01-08'
    }
  },
  {
    id: 'ghana',
    name: 'Ghana',
    code: 'GH',
    flag: 'https://lh3.googleusercontent.com/aida-public/AB6AXuCtWAhV6KNux4tIuFgn3Vun8hLj5NTofXon92wx3m6j0sNdGrc-PrUMghblzgR68ot4aRSC7xUcTrAFVw2i_YxMIBWWxgEoRF10oF7wLC4PdYu4owm00ScJdXkRbeMYlx3xkr3sPT3UiUMV_WNGTBv-q0MDMxi04qiIDfXshVE53X1FZIoza-37MWFaqzlBCQ-jB7eo4pQDd9nf9ARRlPjVwRwn4NM_3biBv-OLwE5oARJw-s2-HssTp_5fkMzMZSpDiwF6GhywWo7u',
    region: 'Western Africa',
    overallScore: 62.1,
    description: 'Ghana shows promise with a stable political environment fostering a reliable legal framework. Targeted investments in infrastructure are crucial for future growth.',
    pillars: {
      physical: { score: 58, description: 'Internet access is improving, but more investment is needed in rural connectivity.' },
      humanCapital: { score: 65, description: 'A growing focus on digital skills in education is building a future-ready workforce.' },
      regulatory: { score: 60, description: 'Strong data protection laws provide a solid foundation for digital trust.' },
      economic: { score: 64, description: 'Mobile money is a key driver of digital transformation and financial inclusion.' }
    },
    lastAssessment: '2024-01-05',
    dataQuality: {
      overallConfidence: 0.75,
      primarySources: 9,
      expertValidation: true,
      lastVerification: '2024-01-05'
    }
  }
];

export default function CountryProfilesPage() {
  return (
    <main className="page-main">
      {/* Hero Section */}
      <section className="section bg-section-1 hero-section">
        <div className="container">
          <div className="text-center space-y-6">
            <h1 className="text-4xl lg:text-5xl font-bold text-foreground leading-tight">
              African Health AI
              <span className="text-gradient gradient-primary block">
                Infrastructure Index
              </span>
            </h1>
            <p className="text-xl text-paragraph-section-1 max-w-4xl mx-auto leading-relaxed">
              Evaluating national capacity to harness health AI across four critical domains: 
              medical-grade infrastructure, clinical AI literacy, regulatory frameworks, and economic sustainability.
            </p>
          </div>
        </div>
      </section>

      {/* Comparative Country View */}
      <section className="section bg-section-2">
        <div className="container">
          <h2 className="text-3xl font-bold text-center mb-12 text-foreground">
            Comparative 
            <span className="text-gradient gradient-physical block">
              Country Assessment
            </span>
          </h2>
          
          <div className="flex overflow-x-auto space-x-8 pb-8 scrollbar-hide">
            {countryData.map((country) => (
              <CountryCard key={country.id} country={country} />
            ))}
          </div>
          
          <div className="text-center mt-12">
            <Link 
              href="/dashboard"
              className="btn btn-primary btn-xl inline-flex items-center gap-3"
            >
              <span>Explore Full Dashboard</span>
              <svg 
                className="w-5 h-5" 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </Link>
          </div>
        </div>
      </section>
    </main>
  );
}