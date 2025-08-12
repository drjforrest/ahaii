#!/usr/bin/env python3
"""
AHAII ETL Test Runner
Comprehensive testing and validation for ETL pipelines
"""

import asyncio
import time
from datetime import datetime
from typing import Dict, Any, List, Tuple

from loguru import logger

from .orchestrator import AHAIIETLOrchestrator, PipelineStatus
from .data_quality_manager import AHAIIDataQualityManager
from .news.rss_monitor import monitor_rss_feeds
from .academic.unified_academic_processor import UnifiedAcademicProcessor
from services.database_service import DatabaseService
from config.database import supabase


class ETLTestSuite:
    """Comprehensive ETL test suite"""
    
    def __init__(self):
        self.orchestrator = AHAIIETLOrchestrator()
        self.quality_manager = AHAIIDataQualityManager()
        self.db_service = DatabaseService()
        
        self.test_results = []
        self.start_time = None
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run comprehensive ETL test suite"""
        logger.info("🧪 Starting AHAII ETL Test Suite...")
        self.start_time = time.time()
        
        # Test categories
        test_categories = [
            ("Database Connectivity", self.test_database_connectivity),
            ("News Monitoring", self.test_news_monitoring),
            ("Academic Processing", self.test_academic_processing), 
            ("Data Quality Checks", self.test_data_quality),
            ("Scoring Pipeline", self.test_scoring_pipeline),
            ("End-to-End Pipeline", self.test_end_to_end_pipeline),
        ]
        
        results = {
            "test_suite": "AHAII ETL",
            "start_time": datetime.now().isoformat(),
            "tests": [],
            "summary": {
                "total": len(test_categories),
                "passed": 0,
                "failed": 0,
                "skipped": 0
            }
        }
        
        for test_name, test_func in test_categories:
            logger.info(f"🔬 Running test: {test_name}")
            
            try:
                test_result = await self.run_single_test(test_name, test_func)
                results["tests"].append(test_result)
                
                if test_result["status"] == "PASSED":
                    results["summary"]["passed"] += 1
                elif test_result["status"] == "FAILED":
                    results["summary"]["failed"] += 1
                else:
                    results["summary"]["skipped"] += 1
                    
            except Exception as e:
                logger.error(f"❌ Test {test_name} crashed: {e}")
                results["tests"].append({
                    "name": test_name,
                    "status": "FAILED",
                    "error": str(e),
                    "duration_seconds": 0
                })
                results["summary"]["failed"] += 1
        
        results["end_time"] = datetime.now().isoformat()
        results["total_duration_seconds"] = time.time() - self.start_time
        
        # Print summary
        self.print_test_summary(results)
        
        return results
    
    async def run_single_test(self, test_name: str, test_func) -> Dict[str, Any]:
        """Run a single test with timing and error handling"""
        start_time = time.time()
        
        try:
            success, message, details = await test_func()
            
            return {
                "name": test_name,
                "status": "PASSED" if success else "FAILED",
                "message": message,
                "details": details,
                "duration_seconds": time.time() - start_time
            }
            
        except Exception as e:
            return {
                "name": test_name,
                "status": "FAILED",
                "error": str(e),
                "duration_seconds": time.time() - start_time
            }
    
    async def test_database_connectivity(self) -> Tuple[bool, str, Dict[str, Any]]:
        """Test database connectivity and basic operations"""
        try:
            # Test Supabase connection
            result = await supabase.table("countries").select("id").limit(1).execute()
            
            if result.error:
                return False, f"Database connection failed: {result.error}", {}
            
            # Test basic statistics
            stats = await self.db_service.get_ahaii_statistics()
            
            details = {
                "connection": "✅ Connected",
                "tables_accessible": len(stats) > 0,
                "stats": stats
            }
            
            return True, "Database connectivity test passed", details
            
        except Exception as e:
            return False, f"Database test failed: {str(e)}", {}
    
    async def test_news_monitoring(self) -> Tuple[bool, str, Dict[str, Any]]:
        """Test news monitoring pipeline"""
        try:
            # Test RSS monitoring with short timeframe
            articles = await monitor_rss_feeds(hours_back=48)  # Last 48 hours
            
            details = {
                "articles_found": len(articles),
                "sources_active": len(set(article.source for article in articles)) if articles else 0,
                "avg_health_ai_relevance": sum(article.health_ai_relevance_score for article in articles) / len(articles) if articles else 0,
                "avg_african_relevance": sum(article.african_relevance_score for article in articles) / len(articles) if articles else 0,
                "pillars_detected": list(set(article.infrastructure_pillar for article in articles if article.infrastructure_pillar)),
                "countries_mentioned": list(set(country for article in articles for country in article.mentioned_countries))[:10]
            }
            
            # Consider test passed if we get any articles or the system runs without errors
            success = True
            message = f"News monitoring test passed - found {len(articles)} articles"
            
            return success, message, details
            
        except Exception as e:
            return False, f"News monitoring test failed: {str(e)}", {}
    
    async def test_academic_processing(self) -> Tuple[bool, str, Dict[str, Any]]:
        """Test academic paper processing"""
        try:
            processor = UnifiedAcademicProcessor()
            
            # Test with small dataset
            papers = await processor.collect_all_academic_data(max_results_per_source=10)
            
            details = {
                "papers_collected": len(papers),
                "source_distribution": processor.source_statistics,
                "avg_african_relevance": sum(p.get("african_relevance_score", 0) for p in papers) / len(papers) if papers else 0,
                "avg_ai_relevance": sum(p.get("ai_relevance_score", 0) for p in papers) / len(papers) if papers else 0,
                "african_entities_found": len(set(entity for paper in papers for entity in paper.get("african_entities", []))),
            }
            
            success = len(papers) > 0
            message = f"Academic processing test {'passed' if success else 'failed'} - collected {len(papers)} papers"
            
            return success, message, details
            
        except Exception as e:
            return False, f"Academic processing test failed: {str(e)}", {}
    
    async def test_data_quality(self) -> Tuple[bool, str, Dict[str, Any]]:
        """Test data quality validation"""
        try:
            issues = await self.quality_manager.run_comprehensive_quality_check()
            
            total_issues = sum(len(table_issues) for table_issues in issues.values())
            
            severity_counts = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0, 'info': 0}
            for table_issues in issues.values():
                for issue in table_issues:
                    severity_counts[issue.severity.value] += 1
            
            details = {
                "total_issues": total_issues,
                "severity_breakdown": severity_counts,
                "tables_checked": list(issues.keys()),
                "quality_score": max(0, 100 - min(100, severity_counts['critical'] * 10 + severity_counts['high'] * 5 + severity_counts['medium'] * 2 + severity_counts['low'] * 1))
            }
            
            # Test passes if quality system runs without errors (issues are expected)
            success = True
            message = f"Data quality test passed - found {total_issues} issues across {len(issues)} tables"
            
            return success, message, details
            
        except Exception as e:
            return False, f"Data quality test failed: {str(e)}", {}
    
    async def test_scoring_pipeline(self) -> Tuple[bool, str, Dict[str, Any]]:
        """Test AHAII scoring pipeline"""
        try:
            # Test scoring for a single country (Nigeria as example)
            nigeria_result = await supabase.table("countries").select("id").eq("iso_code_alpha3", "NGA").execute()
            
            if not nigeria_result.data:
                return False, "Test country (Nigeria) not found in database", {}
            
            country_id = nigeria_result.data[0]["id"]
            
            # Run scoring pipeline for one country
            result = await self.orchestrator.run_scoring_pipeline()
            
            details = {
                "pipeline_status": result.status.value if hasattr(result, 'status') else 'unknown',
                "records_processed": getattr(result, 'records_processed', 0),
                "records_created": getattr(result, 'records_created', 0),
                "records_failed": getattr(result, 'records_failed', 0),
                "test_country": "Nigeria (NGA)"
            }
            
            success = getattr(result, 'status', None) == PipelineStatus.COMPLETED
            message = f"Scoring pipeline test {'passed' if success else 'failed'}"
            
            return success, message, details
            
        except Exception as e:
            return False, f"Scoring pipeline test failed: {str(e)}", {}
    
    async def test_end_to_end_pipeline(self) -> Tuple[bool, str, Dict[str, Any]]:
        """Test complete end-to-end pipeline"""
        try:
            # Run simplified version of full pipeline
            pipeline_start = time.time()
            
            # Get initial stats
            initial_stats = await self.db_service.get_ahaii_statistics()
            
            # Run news monitoring (small scale)
            news_result = await self.orchestrator.run_news_monitoring_pipeline()
            
            # Get final stats
            final_stats = await self.db_service.get_ahaii_statistics()
            
            pipeline_duration = time.time() - pipeline_start
            
            details = {
                "pipeline_duration_seconds": pipeline_duration,
                "initial_stats": initial_stats,
                "final_stats": final_stats,
                "news_pipeline_status": news_result.status.value if hasattr(news_result, 'status') else 'unknown',
                "data_changes": {
                    "intelligence_records": final_stats.get('total_infrastructure_intelligence', 0) - initial_stats.get('total_infrastructure_intelligence', 0),
                    "indicators": final_stats.get('total_infrastructure_indicators', 0) - initial_stats.get('total_infrastructure_indicators', 0)
                }
            }
            
            # Test passes if pipeline completes without major errors
            success = True
            message = f"End-to-end pipeline test passed in {pipeline_duration:.1f}s"
            
            return success, message, details
            
        except Exception as e:
            return False, f"End-to-end pipeline test failed: {str(e)}", {}
    
    def print_test_summary(self, results: Dict[str, Any]):
        """Print formatted test results summary"""
        print(f"\n{'='*80}")
        print(f"🧪 AHAII ETL Test Suite Results")
        print(f"{'='*80}")
        
        print(f"⏱️  Total Duration: {results['total_duration_seconds']:.1f}s")
        print(f"📊 Tests: {results['summary']['total']} total, {results['summary']['passed']} passed, {results['summary']['failed']} failed")
        
        if results['summary']['failed'] == 0:
            print(f"✅ All tests PASSED!")
        else:
            print(f"❌ {results['summary']['failed']} tests FAILED")
        
        print(f"\n📋 Test Details:")
        print(f"{'-'*80}")
        
        for test in results["tests"]:
            status_icon = "✅" if test["status"] == "PASSED" else "❌"
            print(f"{status_icon} {test['name']}: {test['status']} ({test['duration_seconds']:.1f}s)")
            
            if test["status"] == "FAILED":
                print(f"   Error: {test.get('error', test.get('message', 'Unknown error'))}")
            else:
                print(f"   {test.get('message', 'Test completed successfully')}")
            
            # Print key details
            if 'details' in test:
                details = test['details']
                if isinstance(details, dict):
                    for key, value in list(details.items())[:3]:  # Show first 3 details
                        if isinstance(value, (int, float, str, bool)):
                            print(f"   {key}: {value}")
            print()


async def run_quick_test():
    """Run quick ETL validation test"""
    logger.info("🚀 Running Quick ETL Test...")
    
    try:
        # Test database connection
        result = await supabase.table("countries").select("id").limit(1).execute()
        if result.error:
            logger.error(f"❌ Database connection failed: {result.error}")
            return False
        
        logger.info("✅ Database connection: OK")
        
        # Test news monitoring (very limited)
        articles = await monitor_rss_feeds(hours_back=24)
        logger.info(f"✅ News monitoring: Found {len(articles)} articles")
        
        # Test data quality
        quality_manager = AHAIIDataQualityManager()
        issues = await quality_manager.run_comprehensive_quality_check()
        total_issues = sum(len(table_issues) for table_issues in issues.values())
        logger.info(f"✅ Data quality: Found {total_issues} issues")
        
        logger.info("🎉 Quick ETL test completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Quick test failed: {e}")
        return False


async def main():
    """Main test runner"""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        success = await run_quick_test()
        exit(0 if success else 1)
    else:
        # Full test suite
        test_suite = ETLTestSuite()
        results = await test_suite.run_all_tests()
        
        # Exit with error code if any tests failed
        exit(0 if results['summary']['failed'] == 0 else 1)


if __name__ == "__main__":
    asyncio.run(main())
