# AHAII Analytics System 📊

A comprehensive analytics and metrics system to showcase your impressive data collection efforts!

## 🎯 What This Does

The AHAII Analytics System compiles all your hard work into impressive, dashboard-ready metrics that show:

- **How much data** you've collected (total records, papers, docs)
- **How long** you've been working (days operational, uptime)
- **Which domains** you've conquered (academic, government, news)
- **How good** your data quality is (verification rates, confidence scores)
- **Geographic coverage** across African countries
- **System performance** (pipeline success rates, collection trends)

Perfect for showing stakeholders: **"Look how hard we're working!"** 💪

## 🚀 Quick Start

### 1. Test the System

```bash
# Test analytics connectivity
python analytics_cli.py test

# Get impressive dashboard summary
python analytics_cli.py dashboard

# See domain breakdown (shows your data sources)
python analytics_cli.py domains
```

### 2. Generate Reports

```bash
# Comprehensive report
python analytics_cli.py report --save ahaii_analytics_report.md

# Quality metrics (show data excellence)
python analytics_cli.py quality

# Geographic coverage
python analytics_cli.py countries

# Collection trends
python analytics_cli.py trends --days 30
```

### 3. API Endpoints (for Frontend)

The system provides REST API endpoints for your frontend dashboard:

```
GET /api/analytics/dashboard       # Quick dashboard summary
GET /api/analytics/full           # Comprehensive metrics
GET /api/analytics/domains        # Data source breakdown
GET /api/analytics/quality        # Quality metrics
GET /api/analytics/activity       # Collection activity
GET /api/analytics/countries      # Country coverage
GET /api/analytics/time-series    # Trend data for charts
POST /api/analytics/refresh       # Force cache refresh
```

## 📈 What Metrics You Get

### Headline Stats
- **Total records collected** (infrastructure intelligence)
- **Countries covered** (geographic reach)
- **Days operational** (how long you've been working)
- **Recent activity** (last 24h, 7d, 30d collection)

### Data Sources ("Look How Hard We Work!")
- **Academic papers processed** (shows scholarly rigor)
- **Government documents analyzed** (shows official sourcing)
- **News articles monitored** (shows current awareness)
- **Domain diversity** (shows comprehensive coverage)
- **Snowball discoveries** (shows advanced techniques)

### Quality Metrics (Data Excellence)
- **Verification rates** (shows quality control)
- **High-confidence records** (shows reliability)
- **Peer-reviewed sources** (shows academic standards)
- **Relevance scores** (shows targeted collection)

### System Performance
- **Pipeline success rates** (shows reliable operation)
- **Uptime tracking** (shows system stability)
- **Collection velocity** (shows productivity)
- **Error rates** (shows system health)

### Geographic Analysis
- **Country coverage rates** (shows continental scope)
- **Data distribution** (shows balanced collection)
- **Regional focus** (shows African emphasis)

## 🔧 Technical Details

### Caching
- Analytics are cached for 15 minutes to avoid expensive re-computation
- Use `force_refresh=true` parameter to get fresh data
- Cache auto-refreshes in background when expired

### Performance
- Uses parallel queries for efficiency
- Graceful degradation - partial results if some queries fail
- Optimized for dashboard loading speed

### Data Sources
The analytics pull from these database tables:
- `infrastructure_intelligence` (main data store)
- `countries` (geographic coverage)
- `infrastructure_indicators` (indicator data)
- `health_ai_organizations` (organization data)
- `ahaii_scores` (assessment data)

## 📊 Sample Output

```bash
$ python analytics_cli.py dashboard

🎉 AHAII Data Collection Success Story! 🎉
==================================================

📊 HEADLINE ACHIEVEMENTS:
• 15,423 total infrastructure records collected
• 54 African countries analyzed  
• 127 days of continuous operation
• 89 new records in last 24 hours

📚 DATA SOURCES CONQUERED:
• 3,456 academic papers processed
• 1,234 government documents analyzed  
• 8,901 news articles monitored
• 12 different source types

🏆 QUALITY ACHIEVEMENTS:
• 12,456 verified records
• 9,876 high-confidence records
• 2,345 peer-reviewed sources
• 87.5% average African relevance
• 92.1% average AI relevance

🚀 SYSTEM PERFORMANCE:
• 127 days uptime
• 245 successful pipeline runs
• 121.4 records collected per day

💪 We're working HARD for African Health AI! 💪
```

## 🎨 Frontend Integration

### React Example
```typescript
// Fetch dashboard metrics
const response = await fetch('/api/analytics/dashboard');
const metrics = await response.json();

// Display headline stats
<div className="stats-grid">
  <StatCard 
    title="Total Records" 
    value={metrics.headline_stats.total_records.toLocaleString()} 
    icon="📊"
  />
  <StatCard 
    title="Countries Covered" 
    value={metrics.headline_stats.countries_covered} 
    icon="🌍"
  />
  <StatCard 
    title="Days Operational" 
    value={metrics.headline_stats.days_operational} 
    icon="⏰"
  />
</div>
```

### Chart Data
```typescript
// Get time series for charts
const timeSeriesResponse = await fetch('/api/analytics/time-series?days=30');
const chartData = await timeSeriesResponse.json();

// Use daily_collection for line charts
<LineChart data={chartData.daily_collection} />
```

## 🔄 Automation

### Auto-Refresh After ETL Runs
Add this to your ETL orchestrator:

```python
# After successful pipeline run
import requests
requests.post("http://localhost:8000/api/analytics/refresh")
```

### Scheduled Reports
```bash
# Add to cron for daily reports
0 9 * * * cd /path/to/ahaii && python analytics_cli.py report --save daily_report.md
```

## 🎯 Pro Tips

1. **Show Growth**: Use time-series data to show increasing collection over time
2. **Highlight Quality**: Emphasize verification rates and confidence scores
3. **Geographic Reach**: Show country coverage maps
4. **Source Diversity**: Highlight the variety of data sources
5. **System Reliability**: Show uptime and success rates

## 🚨 Troubleshooting

### No Data Showing
```bash
# Check database connection
python analytics_cli.py test

# Check if you have any infrastructure_intelligence records
python -c "from config.database import supabase; print(supabase.table('infrastructure_intelligence').select('id').execute())"
```

### Slow Performance
- Analytics are cached for 15 minutes
- First load after cache expiry will be slower
- Use background refresh to pre-populate cache

### API Errors
- Check FastAPI server is running
- Verify analytics routes are included: `setup_analytics_routes(app)`
- Check database credentials

## 📧 Need Help?

The analytics system is designed to be **bulletproof** and **impressive**. If you have issues:

1. Run `python analytics_cli.py test` for diagnostics
2. Check the logs for specific error messages  
3. Verify your database has data in `infrastructure_intelligence` table
4. Try the CLI tools first before API endpoints

---

**Remember**: This system is built to make your data collection look AMAZING! 🌟

Use it to show stakeholders, funders, and collaborators exactly how much valuable work you're doing for African Health AI infrastructure. 💪🏥🌍
