# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AHAII (African Health AI Infrastructure Index) is a research intelligence platform that systematically assesses each African country's readiness to implement, scale, and regulate artificial intelligence solutions in healthcare. The project consists of:

- **Backend**: FastAPI-based ETL pipeline and API server
- **Frontend**: Next.js dashboard and visualization platform  
- **Database**: PostgreSQL/Supabase with health AI infrastructure schema
- **Architecture**: Evolved from TAIFA-FIALA (African AI innovation tracker)

## Key Development Commands

### Backend Development
```bash
# Navigate to backend directory
cd backend

# Start development server (requires .env file)
python3 run.py

# Or use the comprehensive startup script from TAIFA-FIALA
../TAIFA-FIALA/start_backend_dev.sh

# Install dependencies
pip install -r requirements.txt

# Run specific ETL components
python -m etl.academic.unified_academic_processor --test
python -m etl.news.rss_monitor --test
python -m services.database_service --test
```

### Frontend Development
```bash
# Navigate to frontend directory
cd frontend

# Development with Turbopack (recommended)
npm run dev

# Development with Webpack
npm run dev:webpack

# Build for production
npm run build

# Start production server
npm start

# Lint code
npm run lint

# Install dependencies
npm install
```

### Database Operations
```bash
# Apply AHAII schema
psql -f database/ahaii_schema.sql

# Apply TAIFA-FIALA migration (if needed)
psql -f TAIFA-FIALA/migration_fix_dashboard.sql
```

## Architecture Overview

### Backend Architecture (FastAPI)
```
backend/
├── main.py              # FastAPI app entry point
├── api/                 # API route modules
├── config/              # Settings and database config
├── etl/                 # Data collection pipeline
│   ├── academic/        # Academic paper scraping
│   ├── news/           # News monitoring
│   └── government/     # Policy/regulatory tracking
├── models/             # Database models and schemas
├── services/           # Core business logic services
└── utils/              # Utility functions
```

**Key Services:**
- `database_service.py`: Supabase/PostgreSQL operations
- `vector_service.py`: Pinecone integration for semantic search
- `ahaii_scoring_service.py`: Infrastructure scoring algorithms
- `deduplication_service.py`: Data quality and duplicate detection

### Frontend Architecture (Next.js)
```
frontend/src/
├── app/                # Next.js 15 App Router
│   ├── layout.tsx      # Root layout with navigation
│   ├── page.tsx        # Homepage
│   ├── dashboard/      # Main analytics dashboard
│   ├── about/          # About page
│   └── methods/        # Methodology page
├── components/         # Reusable React components
│   ├── layout/         # Navigation, Footer
│   ├── dashboard/      # Dashboard-specific components
│   └── ui/             # Base UI components
├── lib/                # API clients and utilities
└── types/              # TypeScript type definitions
```

**Key Technologies:**
- Next.js 15 with App Router
- Tailwind CSS v4 with custom design system
- Chart.js/Recharts for data visualization
- Supabase client for real-time data
- Framer Motion for animations

### Database Schema (Health AI Focus)
The database is designed around four infrastructure pillars:

1. **Human Capital**: Clinical AI literacy, medical informatics capacity
2. **Physical Infrastructure**: EMR adoption, computational capacity, connectivity
3. **Regulatory**: Medical AI approval pathways, data governance
4. **Economic/Market**: Health AI ecosystem, funding, sustainability

**Core Tables:**
- `countries`: African country profiles
- `ahaii_scores`: Infrastructure readiness scores by country/year
- `infrastructure_indicators`: Raw metrics feeding into scores
- `health_ai_organizations`: Companies, universities, hospitals
- `infrastructure_intelligence`: ETL pipeline outputs

## ETL Pipeline Architecture

The ETL system continuously collects and processes health AI infrastructure signals:

### Academic Intelligence (`etl/academic/`)
- Scrapes arXiv, PubMed for health AI infrastructure papers
- Extracts quantitative infrastructure metrics from research
- Focuses on: EMR implementation rates, clinical AI training programs, regulatory frameworks

### News Monitoring (`etl/news/`)
- Monitors health tech RSS feeds
- Classifies articles by infrastructure pillar impact
- Tracks policy announcements, funding, technology deployments

### Government/Regulatory Tracking (`etl/government/`)
- Monitors health ministry AI strategies
- Tracks medical device regulatory approvals
- Scans hospital system digital transformation announcements

### Data Quality Pipeline
- Multi-source verification and confidence scoring
- Deduplication across all data sources
- Expert validation workflows
- International framework alignment tracking

## Key Configuration Files

### Environment Variables Required
```bash
# Database
SUPABASE_URL=
SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=

# AI Services
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
PERPLEXITY_API_KEY=

# Vector Database
PINECONE_API_KEY=
PINECONE_HOST=

# Search APIs
SERPER_API_KEY=
SERPAPI_KEY=

# Development
ENVIRONMENT=development  # or production
DEBUG=true
```

### Health AI Keywords Focus
The system uses specialized keyword sets for health AI infrastructure:
- **Human Capital**: "medical informatics education", "clinical AI training", "biomedical informatics curriculum"
- **Physical**: "hospital EMR implementation", "telemedicine infrastructure", "healthcare data centers"
- **Regulatory**: "medical AI regulation", "clinical AI validation", "health data privacy frameworks"
- **Economic**: "health AI market analysis", "medical AI investment", "clinical AI adoption costs"

## Migration from TAIFA-FIALA

This project evolved from TAIFA-FIALA (African AI innovation tracker). Key transformations:

- **Data Focus**: From funding tracking → infrastructure readiness assessment
- **ETL Target**: From innovation discovery → health AI infrastructure signals  
- **Scoring**: From funding aggregation → multi-pillar infrastructure scoring
- **Dashboard**: From financial metrics → readiness analytics

Legacy TAIFA-FIALA components in the repository serve as reference architecture and can be adapted for health AI infrastructure use cases.

## Development Workflow

### Adding New Infrastructure Indicators
1. Update `database/ahaii_schema.sql` with new indicator definitions
2. Add extraction logic to relevant ETL processors (`etl/academic/`, `etl/news/`)
3. Update scoring algorithms in `services/ahaii_scoring_service.py`
4. Add frontend visualization in dashboard components

### Testing ETL Components
```bash
# Test with limited data
python -m etl.academic.unified_academic_processor --test --max-results=10
python -m etl.news.rss_monitor --test --hours-back=6

# Validate database integration
python -m services.database_service --test
```

### Deployment
Uses the TAIFA-FIALA deployment script with production environment:
```bash
# Deploy to production server
./TAIFA-FIALA/deploy.sh

# Manual backend start (port 8030)
cd backend && python -m uvicorn main:app --host 0.0.0.0 --port 8030

# Manual frontend start (port 3030)
cd frontend && npm start -- -p 3030
```

## Common Tasks

### Run Full ETL Pipeline
```bash
# Academic papers (health AI infrastructure focus)
curl -X POST "http://localhost:8030/api/etl/academic?days_back=7&max_results=50"

# News monitoring
curl -X POST "http://localhost:8030/api/etl/news?hours_back=24" 

# Innovation search (health AI specific)
curl -X POST "http://localhost:8030/api/etl/serper-search?num_results=25"
```

### Check System Health
```bash
# API health
curl http://localhost:8030/health

# ETL status
curl http://localhost:8030/api/etl/status

# Database connection
curl http://localhost:8030/test-db
```

### Build and Lint
```bash
# Backend linting (if black is installed)
cd backend && black .

# Frontend linting and building
cd frontend && npm run lint && npm run build
```

## Architecture Principles

1. **Health-Focused**: All data collection targets health AI infrastructure specifically
2. **Multi-Source Validation**: Cross-reference infrastructure metrics from multiple sources
3. **Real-Time Intelligence**: Continuous monitoring of health AI infrastructure developments
4. **Academic Rigor**: Methodology based on established AI readiness frameworks (IMF AIPI, Oxford, UNESCO)
5. **African Context**: Tailored for African health systems and development priorities
6. **Scalable Pipeline**: Modular ETL architecture supporting 54 African countries

The system provides evidence-based intelligence for health AI infrastructure investment and policy decisions across Africa.