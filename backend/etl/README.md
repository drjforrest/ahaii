# AHAII Enhanced ETL System 🏥

[![ETL Status](https://img.shields.io/badge/ETL-Production_Ready-brightgreen)](https://github.com/ahaii/etl)
[![Data Quality](https://img.shields.io/badge/Data_Quality-Monitored-blue)](https://github.com/ahaii/etl)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## Overview

The AHAII (African Health AI Infrastructure Index) Enhanced ETL System is a comprehensive data pipeline that monitors, processes, and analyzes health AI infrastructure data across African countries. This production-ready system includes automated scheduling, data quality management, and comprehensive monitoring.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Supabase account and database
- API keys for external services (SerpAPI, etc.)

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Install additional ETL dependencies
pip install click tabulate schedule fuzzywuzzy pycountry
```

### Basic Usage
```bash
# Run the ETL CLI
python -m etl.etl_cli --help

# Quick health check
python -m etl.etl_cli health

# Run a specific pipeline component
python -m etl.etl_cli pipeline run --component news

# Check data quality
python -m etl.etl_cli quality check

# Start the scheduler
python -m etl.etl_cli scheduler start
```

## 📊 System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Data Sources  │────│   ETL Pipeline   │────│   Database      │
├─────────────────┤    ├──────────────────┤    ├─────────────────┤
│ • RSS Feeds     │    │ • Orchestrator   │    │ • Countries     │
│ • Academic Papers│   │ • News Monitor   │    │ • Indicators    │
│ • Research DBs  │    │ • Quality Checks │    │ • Intelligence  │
│ • News Sources  │    │ • Scoring Engine │    │ • Organizations │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                       ┌──────────────────┐
                       │   Scheduler      │
                       │ • Automated Runs │
                       │ • Monitoring     │
                       │ • Alerting       │
                       └──────────────────┘
```

## 🔧 Components

### 1. ETL Orchestrator (`orchestrator.py`)
Central coordinator for all ETL pipelines with error handling and monitoring.

**Features:**
- Multi-pipeline orchestration
- Error handling and retry logic
- Performance monitoring
- Comprehensive reporting

**Usage:**
```python
from etl.orchestrator import AHAIIETLOrchestrator

orchestrator = AHAIIETLOrchestrator()
results = await orchestrator.run_full_pipeline()
```

### 2. News Monitoring (`news/rss_monitor.py`)
Real-time health AI infrastructure news monitoring from 13+ RSS sources.

**Features:**
- 13 curated health AI RSS feeds
- Health AI infrastructure signal processing
- Country detection and relevance scoring
- Automated content analysis

**Sources Monitored:**
- Healthcare IT News
- MobiHealthNews
- TechCabal Health
- WHO News
- HIMSS
- And 8 more...

### 3. Academic Processing (`academic/unified_academic_processor.py`)
Comprehensive academic paper processing from multiple sources.

**Features:**
- ArXiv, PubMed, Google Scholar integration
- Systematic review processing
- Infrastructure indicator extraction
- African relevance scoring

### 4. Data Quality Manager (`data_quality_manager.py`)
Advanced data validation and quality assurance.

**Features:**
- 5-tier severity validation
- Country name standardization
- URL validation
- Auto-fix capabilities
- Comprehensive reporting

**Quality Checks:**
- Missing required fields
- Invalid data ranges
- Country association validation
- URL format validation
- Data freshness monitoring

### 5. Snowball Sampler (`snowball_sampler.py`) 🆕
Intelligent reference discovery system for health AI infrastructure resources.

**Features:**
- **Health AI Focus**: Specialized patterns for health, AI, and infrastructure content
- **Multi-depth Sampling**: Iterative citation extraction with configurable depth limits
- **Government Document Safety**: Conservative handling with strict domain whitelisting
- **Quality Filtering**: Advanced relevance and confidence scoring
- **African Context**: Specialized filtering for African health systems and organizations

**Safety Features:**
- Government domain whitelisting (WHO, international organizations only)
- Triple safety checks on URLs, content, and access levels
- Respectful rate limiting and robots.txt compliance
- Academic researcher user-agent identification
- Detailed security documentation (see `GOVERNMENT_DOCS_STRATEGY.md`)

### 6. Scheduler (`scheduler.py`)
Production-ready task scheduler with monitoring and alerting.

**Default Schedule:**
- News Monitoring: Every 6 hours
- Academic Processing: Daily at 2 AM
- Snowball Sampling: Every 8 hours (conservative)
- AHAII Scoring: Twice daily (6 AM, 6 PM)
- Data Quality: Every 4 hours
- Full Pipeline: Weekly on Sunday

### 7. CLI Management (`etl_cli.py`)
Comprehensive command-line interface for ETL operations including snowball sampling.

## 📋 CLI Commands

### Pipeline Management
```bash
# Run specific components
python -m etl.etl_cli pipeline run --component news
python -m etl.etl_cli pipeline run --component academic
python -m etl.etl_cli pipeline run --component scoring
python -m etl.etl_cli pipeline run --component snowball
python -m etl.etl_cli pipeline run --component all

# Check pipeline status
python -m etl.etl_cli pipeline status

# Run snowball sampling with custom settings
python -m etl.etl_cli pipeline snowball --max-depth 2 --max-citations 15
# Enable government docs (use with extreme caution)
python -m etl.etl_cli pipeline snowball --government-docs --max-depth 1
```

### Scheduler Operations
```bash
# Start scheduler
python -m etl.etl_cli scheduler start [--daemon]

# Check scheduler status
python -m etl.etl_cli scheduler status

# Run specific task
python -m etl.etl_cli scheduler run-task news_monitoring_6h

# Enable/disable tasks
python -m etl.etl_cli scheduler enable news_monitoring_6h
python -m etl.etl_cli scheduler disable academic_processing_daily
```

### Data Quality Management
```bash
# Run quality checks
python -m etl.etl_cli quality check

# Check specific table
python -m etl.etl_cli quality check --table infrastructure_intelligence

# Filter by severity
python -m etl.etl_cli quality check --severity high

# Export issues to file
python -m etl.etl_cli quality check --export quality_issues.json

# Auto-fix issues (dry run first)
python -m etl.etl_cli quality fix --dry-run
python -m etl.etl_cli quality fix
```

### Monitoring
```bash
# Real-time dashboard
python -m etl.etl_cli monitor dashboard [--watch]

# Database statistics
python -m etl.etl_cli db stats

# System health check
python -m etl.etl_cli health

# Configuration info
python -m etl.etl_cli config
```

## 🧪 Testing

### Quick Test
```bash
python -m etl.test_etl quick
```

### Comprehensive Test Suite
```bash
python -m etl.test_etl
```

**Test Categories:**
- Database connectivity
- News monitoring
- Academic processing
- Data quality validation
- Scoring pipeline
- End-to-end pipeline

## 📊 Data Quality Metrics

The system maintains comprehensive data quality metrics:

- **Quality Score**: 0-100 composite score
- **Severity Levels**: Critical, High, Medium, Low, Info
- **Coverage**: All major database tables
- **Auto-Fix**: Automatic resolution of common issues

### Quality Thresholds
- **Critical Issues**: 🚨 Immediate attention required
- **High Issues**: 🔴 Fix within 24 hours
- **Medium Issues**: 🟡 Fix within 1 week
- **Low Issues**: 🟢 Fix when convenient

## 📈 Monitoring & Alerting

### Health Metrics
- Pipeline execution status
- Data freshness
- Error rates
- Quality scores
- System performance

### Notifications
- Email alerts for failures
- Success notifications for major runs
- Quality threshold violations
- System health warnings

## 🔄 Production Deployment

### Scheduler Setup
1. Start the scheduler as a daemon:
```bash
python -m etl.etl_cli scheduler start --daemon
```

2. Monitor with systemd/supervisor for production reliability

### Environment Variables
```bash
# Database
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# External APIs
SERPAPI_KEY=your_serpapi_key

# Notifications
NOTIFICATION_EMAILS=admin@ahaii.org
SLACK_WEBHOOK_URL=your_slack_webhook
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "-m", "etl.scheduler"]
```

## 📝 Configuration

### Pipeline Configuration
```python
pipeline_configs = {
    "news_monitoring": {
        "enabled": True,
        "frequency_hours": 6,
        "max_runtime_minutes": 30,
        "retry_attempts": 3
    },
    "academic_processing": {
        "enabled": True,
        "frequency_hours": 24,
        "max_runtime_minutes": 120,
        "retry_attempts": 2
    }
    # ... more configurations
}
```

### Quality Thresholds
```python
freshness_thresholds = {
    'infrastructure_intelligence': timedelta(days=90),
    'infrastructure_indicators': timedelta(days=365),
    'ahaii_scores': timedelta(days=90),
    'health_ai_organizations': timedelta(days=180)
}
```

## 🚨 Troubleshooting

### Common Issues

1. **Database Connection Errors**
   ```bash
   # Check connection
   python -m etl.etl_cli health
   
   # Verify credentials
   python -c "from config.database import supabase; print(supabase.table('countries').select('id').limit(1).execute())"
   ```

2. **RSS Feed Failures**
   ```bash
   # Test news monitoring
   python -c "import asyncio; from etl.news.rss_monitor import monitor_rss_feeds; asyncio.run(monitor_rss_feeds(hours_back=1))"
   ```

3. **Quality Issues**
   ```bash
   # Run quality check with details
   python -m etl.etl_cli quality check --severity critical --export issues.json
   ```

### Debug Mode
```bash
# Enable verbose logging
export LOGURU_LEVEL=DEBUG
python -m etl.etl_cli pipeline run --component news --verbose
```

## 📚 API Reference

### Core Classes

#### `AHAIIETLOrchestrator`
Main orchestration class for ETL pipelines.

```python
orchestrator = AHAIIETLOrchestrator()

# Run individual pipelines
await orchestrator.run_news_monitoring_pipeline()
await orchestrator.run_academic_processing_pipeline()
await orchestrator.run_scoring_pipeline()

# Run full pipeline
results = await orchestrator.run_full_pipeline()
```

#### `AHAIIDataQualityManager`
Data quality validation and management.

```python
quality_manager = AHAIIDataQualityManager()

# Run quality checks
issues = await quality_manager.run_comprehensive_quality_check()

# Auto-fix issues
fix_results = await quality_manager.auto_fix_issues(issues, dry_run=False)
```

#### `AHAIIETLScheduler`
Production scheduler for automated ETL runs.

```python
scheduler = AHAIIETLScheduler()

# Start scheduler
await scheduler.start_scheduler()

# Get status
status = scheduler.get_scheduler_status()

# Run task immediately
await scheduler.run_task_now('news_monitoring_6h')
```

## 🤝 Contributing

1. Follow existing code patterns
2. Add comprehensive tests
3. Update documentation
4. Ensure quality checks pass
5. Submit pull request

### Development Setup
```bash
# Clone repository
git clone https://github.com/ahaii/etl.git
cd etl

# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
python -m etl.test_etl

# Run quality checks
python -m etl.etl_cli quality check
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [ETL Wiki](https://github.com/ahaii/etl/wiki)
- **Issues**: [GitHub Issues](https://github.com/ahaii/etl/issues)
- **Email**: support@ahaii.org
- **Community**: [AHAII Discord](https://discord.gg/ahaii)

---

**AHAII ETL System** - Powering African Health AI Infrastructure Intelligence 🏥🌍
