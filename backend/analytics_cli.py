#!/usr/bin/env python3
"""
AHAII Analytics CLI
Command-line tool for testing and compiling analytics metrics
Perfect for seeing how impressive your data collection is!
"""

import asyncio
import click
import json
from datetime import datetime
from tabulate import tabulate

from services.analytics_service import AHAIIAnalyticsService


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """🏥 AHAII Analytics CLI
    
    Generate impressive metrics and analytics for your health AI infrastructure data collection!
    """
    pass


@cli.command()
@click.option('--format', '-f', type=click.Choice(['table', 'json', 'summary']), default='summary', 
              help='Output format')
@click.option('--save', '-s', help='Save results to file')
def dashboard(format, save):
    """Get dashboard analytics - the impressive headline numbers! 📊"""
    
    click.echo("🔍 Compiling your impressive dashboard metrics...")
    
    async def _get_dashboard():
        service = AHAIIAnalyticsService()
        summary = await service.get_dashboard_summary()
        
        if format == 'json':
            output = json.dumps(summary, indent=2, default=str)
        elif format == 'table':
            # Convert to table format
            headline_data = [
                ["Total Records", summary["headline_stats"]["total_records"]],
                ["Countries Covered", summary["headline_stats"]["countries_covered"]],
                ["Days Operational", summary["headline_stats"]["days_operational"]],
                ["Records Last 24h", summary["headline_stats"]["records_last_24h"]]
            ]
            
            sources_data = [
                ["Academic Papers", summary["data_sources"]["academic_papers"]],
                ["Government Docs", summary["data_sources"]["government_docs"]],
                ["News Articles", summary["data_sources"]["news_articles"]],
                ["Total Source Types", summary["data_sources"]["total_sources"]]
            ]
            
            output = "📈 HEADLINE STATS\n" + "=" * 50 + "\n"
            output += tabulate(headline_data, headers=['Metric', 'Value'], tablefmt='grid')
            output += "\n\n📊 DATA SOURCES\n" + "=" * 50 + "\n"
            output += tabulate(sources_data, headers=['Source', 'Count'], tablefmt='grid')
            
        else:  # summary format
            stats = summary["headline_stats"]
            sources = summary["data_sources"]
            quality = summary["quality_metrics"]
            
            output = f"""
🎉 AHAII Data Collection Success Story! 🎉
{'='*50}

📊 HEADLINE ACHIEVEMENTS:
• {stats['total_records']:,} total infrastructure records collected
• {stats['countries_covered']} African countries analyzed  
• {stats['days_operational']} days of continuous operation
• {stats['records_last_24h']} new records in last 24 hours

📚 DATA SOURCES CONQUERED:
• {sources['academic_papers']:,} academic papers processed
• {sources['government_docs']:,} government documents analyzed  
• {sources['news_articles']:,} news articles monitored
• {sources['total_sources']} different source types

🏆 QUALITY ACHIEVEMENTS:
• {quality['verified_records']:,} verified records
• {quality['high_confidence']:,} high-confidence records
• {quality['peer_reviewed']:,} peer-reviewed sources
• {quality['avg_african_relevance']}% average African relevance
• {quality['avg_ai_relevance']}% average AI relevance

🚀 SYSTEM PERFORMANCE:
• {summary['system_health']['uptime_days']} days uptime
• {summary['system_health']['successful_runs']} successful pipeline runs
• {summary['system_health']['avg_daily_collection']} records collected per day

💪 We're working HARD for African Health AI! 💪
"""
        
        if save:
            with open(save, 'w') as f:
                f.write(output)
            click.echo(f"📄 Results saved to {save}")
        
        return output
    
    result = asyncio.run(_get_dashboard())
    click.echo(result)


@cli.command()
@click.option('--days', '-d', default=30, help='Number of days for time series')
def trends(days):
    """Show data collection trends over time 📈"""
    
    click.echo(f"📈 Getting {days} days of collection trends...")
    
    async def _get_trends():
        service = AHAIIAnalyticsService()
        time_series = await service.get_time_series_data(days)
        
        daily_data = time_series.get("daily_collection", [])
        if not daily_data:
            return "No time series data available"
        
        # Show recent days in table
        recent_days = daily_data[-7:]  # Last 7 days
        table_data = [[day["date"], day["records"]] for day in recent_days]
        
        total_recent = sum(day["records"] for day in recent_days)
        avg_daily = total_recent / len(recent_days) if recent_days else 0
        
        output = f"""
📈 DATA COLLECTION TRENDS ({days} days)
{'='*50}

Last 7 Days Activity:
{tabulate(table_data, headers=['Date', 'Records'], tablefmt='grid')}

📊 TREND SUMMARY:
• Total records last 7 days: {total_recent:,}
• Average per day: {avg_daily:.1f}
• Most productive day: {max(recent_days, key=lambda x: x['records'])['date']} ({max(day['records'] for day in recent_days)} records)
• Data points analyzed: {len(daily_data)}

🔥 Consistent data collection shows we're committed! 🔥
"""
        return output
    
    result = asyncio.run(_get_trends())
    click.echo(result)


@cli.command()
def domains():
    """Show breakdown of data sources by domain 🌐"""
    
    click.echo("🌐 Analyzing data source domains...")
    
    async def _get_domains():
        service = AHAIIAnalyticsService()
        metrics = await service.get_comprehensive_metrics()
        
        if not metrics.domain_distribution:
            return "No domain data available"
        
        # Top domains table
        sorted_domains = sorted(metrics.domain_distribution.items(), key=lambda x: x[1], reverse=True)[:15]
        table_data = [[domain, count] for domain, count in sorted_domains]
        
        # Source types
        source_data = list(metrics.source_distribution.items()) if metrics.source_distribution else []
        
        output = f"""
🌐 DATA SOURCE DOMAIN ANALYSIS
{'='*50}

Top 15 Domains by Records:
{tabulate(table_data, headers=['Domain', 'Records'], tablefmt='grid')}

📊 SOURCE TYPE BREAKDOWN:
"""
        
        for source_type, count in source_data:
            output += f"• {source_type.replace('_', ' ').title()}: {count:,} records\n"
        
        output += f"""

🎯 DOMAIN DIVERSITY STATS:
• Total unique domains: {len(metrics.domain_distribution)}
• Government docs processed: {metrics.government_docs_processed:,}
• Academic papers: {metrics.total_academic_papers:,}
• Snowball discoveries: {metrics.snowball_discoveries:,}

🏅 We cast a WIDE net for comprehensive data! 🏅
"""
        return output
    
    result = asyncio.run(_get_domains())
    click.echo(result)


@cli.command()
def quality():
    """Show data quality and verification metrics 🏆"""
    
    click.echo("🏆 Analyzing data quality achievements...")
    
    async def _get_quality():
        service = AHAIIAnalyticsService()
        metrics = await service.get_comprehensive_metrics()
        
        total = metrics.total_infrastructure_intelligence
        if total == 0:
            return "No data available for quality analysis"
        
        verification_rate = (metrics.verified_records / total) * 100
        confidence_rate = (metrics.high_confidence_records / total) * 100
        peer_review_rate = (metrics.peer_reviewed_sources / total) * 100
        
        quality_data = [
            ["Total Records", f"{total:,}"],
            ["Verified Records", f"{metrics.verified_records:,} ({verification_rate:.1f}%)"],
            ["High Confidence", f"{metrics.high_confidence_records:,} ({confidence_rate:.1f}%)"],
            ["Peer Reviewed", f"{metrics.peer_reviewed_sources:,} ({peer_review_rate:.1f}%)"],
            ["Avg African Relevance", f"{metrics.african_relevance_avg*100:.1f}%"],
            ["Avg AI Relevance", f"{metrics.ai_relevance_avg*100:.1f}%"]
        ]
        
        output = f"""
🏆 DATA QUALITY EXCELLENCE REPORT
{'='*50}

{tabulate(quality_data, headers=['Quality Metric', 'Achievement'], tablefmt='grid')}

🌟 QUALITY HIGHLIGHTS:
• Our verification rate of {verification_rate:.1f}% shows rigorous standards
• {confidence_rate:.1f}% high-confidence records demonstrate reliability
• {peer_review_rate:.1f}% peer-reviewed sources ensure academic rigor
• Average relevance scores show targeted, quality content

📊 QUALITY GRADES:
"""
        
        # Quality grading
        if verification_rate >= 80:
            output += "• Verification: A+ (Excellent) ⭐⭐⭐\n"
        elif verification_rate >= 60:
            output += "• Verification: B+ (Good) ⭐⭐\n"
        else:
            output += "• Verification: C+ (Improving) ⭐\n"
        
        if confidence_rate >= 70:
            output += "• Confidence: A+ (Excellent) ⭐⭐⭐\n"
        elif confidence_rate >= 50:
            output += "• Confidence: B+ (Good) ⭐⭐\n"
        else:
            output += "• Confidence: C+ (Building) ⭐\n"
        
        output += "\n🎯 Quality control is our TOP PRIORITY! 🎯\n"
        
        return output
    
    result = asyncio.run(_get_quality())
    click.echo(result)


@cli.command()
def countries():
    """Show country coverage and geographic reach 🌍"""
    
    click.echo("🌍 Analyzing geographic coverage...")
    
    async def _get_countries():
        service = AHAIIAnalyticsService()
        metrics = await service.get_comprehensive_metrics()
        
        if not metrics.country_coverage:
            return "No country coverage data available"
        
        # Top countries by data
        sorted_countries = sorted(metrics.country_coverage.items(), key=lambda x: x[1], reverse=True)[:15]
        table_data = [[country, records] for country, records in sorted_countries]
        
        coverage_rate = (len(metrics.country_coverage) / metrics.total_countries) * 100 if metrics.total_countries > 0 else 0
        
        output = f"""
🌍 AFRICAN COUNTRY COVERAGE ANALYSIS
{'='*50}

Top 15 Countries by Data Records:
{tabulate(table_data, headers=['Country', 'Records'], tablefmt='grid')}

📊 GEOGRAPHIC REACH STATS:
• Total African countries in database: {metrics.total_countries}
• Countries with data collected: {len(metrics.country_coverage)}
• Coverage rate: {coverage_rate:.1f}%
• Most documented country: {sorted_countries[0][0]} ({sorted_countries[0][1]:,} records)

🎯 CONTINENTAL IMPACT:
"""
        
        # Categorize coverage
        high_coverage = [c for c, r in sorted_countries if r >= 100]
        medium_coverage = [c for c, r in sorted_countries if 20 <= r < 100]
        emerging_coverage = [c for c, r in sorted_countries if 1 <= r < 20]
        
        output += f"• High coverage countries (100+ records): {len(high_coverage)}\n"
        output += f"• Medium coverage countries (20-99 records): {len(medium_coverage)}\n"
        output += f"• Emerging coverage countries (1-19 records): {len(emerging_coverage)}\n"
        
        output += f"\n🌟 We're building a CONTINENTAL view of African health AI! 🌟\n"
        
        return output
    
    result = asyncio.run(_get_countries())
    click.echo(result)


@cli.command()
@click.option('--save', '-s', help='Save comprehensive report to file')
def report(save):
    """Generate comprehensive analytics report 📑"""
    
    click.echo("📑 Generating comprehensive analytics report...")
    
    async def _generate_report():
        service = AHAIIAnalyticsService()
        metrics = await service.get_comprehensive_metrics()
        summary = await service.get_dashboard_summary()
        
        report_content = f"""
# AHAII Data Collection Analytics Report
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Executive Summary
The African Health AI Infrastructure Index (AHAII) has achieved remarkable data collection success:

- **{metrics.total_infrastructure_intelligence:,} total records** collected across the continent
- **{metrics.total_countries} African countries** covered in our analysis
- **{metrics.days_operational} days** of continuous operational excellence
- **{len(metrics.source_distribution)} different source types** systematically monitored

## Data Collection Achievements

### Volume Metrics
- Total Infrastructure Intelligence Records: {metrics.total_infrastructure_intelligence:,}
- Academic Papers Processed: {metrics.total_academic_papers:,}
- Government Documents Analyzed: {metrics.government_docs_processed:,}
- News Articles Monitored: {summary['data_sources']['news_articles']:,}
- Snowball Discoveries: {metrics.snowball_discoveries:,}

### Temporal Performance  
- Days Operational: {metrics.days_operational}
- Average Records/Day: {metrics.avg_records_per_day:.1f}
- Records Last 24h: {metrics.records_collected_last_24h:,}
- Records Last 7d: {metrics.records_collected_last_7d:,}
- Records Last 30d: {metrics.records_collected_last_30d:,}

### Geographic Coverage
- Countries with Data: {len(metrics.country_coverage)}/{metrics.total_countries} ({(len(metrics.country_coverage)/metrics.total_countries)*100:.1f}%)
- Top Country by Records: {max(metrics.country_coverage.items(), key=lambda x: x[1])[0] if metrics.country_coverage else 'N/A'}

### Data Quality Excellence
- Verified Records: {metrics.verified_records:,} ({(metrics.verified_records/metrics.total_infrastructure_intelligence)*100:.1f}%)
- High Confidence: {metrics.high_confidence_records:,} ({(metrics.high_confidence_records/metrics.total_infrastructure_intelligence)*100:.1f}%)
- Peer Reviewed: {metrics.peer_reviewed_sources:,} ({(metrics.peer_reviewed_sources/metrics.total_infrastructure_intelligence)*100:.1f}%)
- Avg African Relevance: {metrics.african_relevance_avg*100:.1f}%
- Avg AI Relevance: {metrics.ai_relevance_avg*100:.1f}%

### System Performance  
- System Uptime: {metrics.uptime_days} days
- Successful Pipeline Runs: {metrics.successful_pipeline_runs:,}
- Pipeline Success Rate: {(metrics.successful_pipeline_runs/(metrics.successful_pipeline_runs + metrics.failed_pipeline_runs))*100:.1f}%

### Source Diversity
"""
        
        # Add domain breakdown
        if metrics.domain_distribution:
            report_content += "\n#### Top Data Source Domains:\n"
            for domain, count in list(metrics.domain_distribution.items())[:10]:
                report_content += f"- {domain}: {count:,} records\n"
        
        # Add source type breakdown
        if metrics.source_distribution:
            report_content += "\n#### Source Type Distribution:\n"
            for source_type, count in metrics.source_distribution.items():
                report_content += f"- {source_type.replace('_', ' ').title()}: {count:,} records\n"
        
        report_content += f"""

## Conclusion

The AHAII project demonstrates exceptional commitment to comprehensive data collection across the African continent. With {metrics.total_infrastructure_intelligence:,} records collected over {metrics.days_operational} days, we've established a robust foundation for understanding health AI infrastructure across Africa.

Our multi-source approach, covering academic literature, government documentation, news monitoring, and citation network analysis, ensures comprehensive coverage. The {(metrics.high_confidence_records/metrics.total_infrastructure_intelligence)*100:.1f}% high-confidence record rate demonstrates our commitment to quality over quantity.

This data collection effort represents one of the most comprehensive attempts to map health AI infrastructure capabilities across the African continent.

---
Report generated by AHAII Analytics System
{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
        
        return report_content
    
    report_content = asyncio.run(_generate_report())
    
    if save:
        with open(save, 'w') as f:
            f.write(report_content)
        click.echo(f"📄 Comprehensive report saved to {save}")
    else:
        click.echo(report_content)


@cli.command()
def test():
    """Test analytics system connectivity 🔧"""
    
    click.echo("🔧 Testing analytics system...")
    
    async def _test_system():
        try:
            service = AHAIIAnalyticsService()
            
            # Test basic connectivity
            click.echo("  ✅ Analytics service initialized")
            
            # Test database queries
            metrics = await service.get_comprehensive_metrics()
            click.echo(f"  ✅ Database queries successful")
            click.echo(f"  📊 Found {metrics.total_infrastructure_intelligence:,} records")
            
            # Test dashboard summary
            summary = await service.get_dashboard_summary()
            click.echo(f"  ✅ Dashboard summary generated")
            
            # Test time series
            time_series = await service.get_time_series_data(7)
            click.echo(f"  ✅ Time series data retrieved ({len(time_series.get('daily_collection', []))} data points)")
            
            click.echo("\n🎉 Analytics system is working perfectly!")
            
        except Exception as e:
            click.echo(f"  ❌ Error: {e}")
            click.echo("\n💡 Check your database connection and try again")
    
    asyncio.run(_test_system())


if __name__ == "__main__":
    cli()
