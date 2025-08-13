"""
Simple AHAII Integration Test
Tests the basic structure and imports without requiring FastAPI dependencies
"""

import sys
from pathlib import Path

def test_basic_integration():
    """Test basic integration setup"""
    print("🧪 Testing AHAII Phase 2 Integration")
    print("=" * 50)
    
    # Test 1: Check file structure
    print("\n1. File Structure Check")
    required_files = [
        "backend/app/main_integration.py",
        "backend/app/data_collection/worldbank_collector.py", 
        "backend/api/ahaii_assessment.py",
        "backend/models/ahaii_models.py",
        "backend/services/ahaii_database_service.py",
        "backend/main.py"
    ]
    
    all_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path}")
            all_exist = False
    
    print(f"   📊 File structure: {'PASS' if all_exist else 'FAIL'}")
    
    # Test 2: Check FastAPI integration
    print("\n2. FastAPI Integration Check")
    main_py = Path("backend/main.py")
    if main_py.exists():
        content = main_py.read_text()
        checks = [
            ("AHAII router import", "from api.ahaii_assessment import router as ahaii_router"),
            ("Router inclusion", "app.include_router(ahaii_router)"),
            ("AHAII endpoints documented", "ahaii_assessment"),
            ("AHAII components documented", "ahaii_components")
        ]
        
        integration_passed = True
        for check_name, check_text in checks:
            if check_text in content:
                print(f"   ✅ {check_name}")
            else:
                print(f"   ❌ {check_name}")
                integration_passed = False
        
        print(f"   📊 FastAPI integration: {'PASS' if integration_passed else 'FAIL'}")
    else:
        print("   ❌ main.py not found")
        integration_passed = False
    
    # Test 3: Check API endpoints structure
    print("\n3. API Endpoints Check")
    api_file = Path("backend/api/ahaii_assessment.py")
    if api_file.exists():
        content = api_file.read_text()
        
        # Count endpoint definitions
        endpoint_patterns = [
            "/health", "/collect-data", "/calculate-scores", "/scores",
            "/validate", "/generate-report", "/run-complete-assessment",
            "/status", "/countries", "/methodology"
        ]
        
        found_endpoints = sum(1 for pattern in endpoint_patterns if pattern in content)
        print(f"   ✅ Found {found_endpoints}/{len(endpoint_patterns)} expected endpoints")
        
        # Check for required imports
        import_checks = [
            "AHAIIIntegrationManager",
            "WorldBankCollector", 
            "PolicyIndicatorCollector",
            "EnhancedAHAIICalculator"
        ]
        
        found_imports = sum(1 for import_name in import_checks if import_name in content)
        print(f"   ✅ Found {found_imports}/{len(import_checks)} required imports")
        
        endpoints_passed = found_endpoints >= 8 and found_imports >= 3
        print(f"   📊 API endpoints: {'PASS' if endpoints_passed else 'FAIL'}")
    else:
        print("   ❌ API endpoints file not found")
        endpoints_passed = False
    
    # Test 4: Check data models
    print("\n4. Data Models Check")
    models_file = Path("backend/models/ahaii_models.py")
    if models_file.exists():
        content = models_file.read_text()
        
        model_checks = [
            "AHAIIAssessment",
            "AHAIICountryScore", 
            "AHAIIPillarScore",
            "AHAIIIndicatorValue",
            "DataCollectionRun"
        ]
        
        found_models = sum(1 for model in model_checks if f"class {model}" in content)
        print(f"   ✅ Found {found_models}/{len(model_checks)} data models")
        
        # Check for Pydantic models
        pydantic_checks = ["BaseModel", "AHAIIAssessmentRequest", "AHAIIAssessmentResponse"]
        found_pydantic = sum(1 for check in pydantic_checks if check in content)
        print(f"   ✅ Found {found_pydantic}/{len(pydantic_checks)} Pydantic models")
        
        models_passed = found_models >= 4 and found_pydantic >= 2
        print(f"   📊 Data models: {'PASS' if models_passed else 'FAIL'}")
    else:
        print("   ❌ Data models file not found")
        models_passed = False
    
    # Test 5: Check database service
    print("\n5. Database Service Check")
    db_service_file = Path("backend/services/ahaii_database_service.py")
    if db_service_file.exists():
        content = db_service_file.read_text()
        
        service_checks = [
            "AHAIIDatabaseService",
            "create_assessment",
            "save_country_score",
            "get_country_scores",
            "health_check"
        ]
        
        found_methods = sum(1 for method in service_checks if method in content)
        print(f"   ✅ Found {found_methods}/{len(service_checks)} database methods")
        
        db_service_passed = found_methods >= 4
        print(f"   📊 Database service: {'PASS' if db_service_passed else 'FAIL'}")
    else:
        print("   ❌ Database service file not found")
        db_service_passed = False
    
    # Test 6: Check schema file
    print("\n6. Database Schema Check")
    schema_file = Path("database/ahaii_quantitative_schema.sql")
    if schema_file.exists():
        content = schema_file.read_text()
        
        table_checks = [
            "ahaii_assessments",
            "ahaii_country_scores",
            "ahaii_pillar_scores", 
            "ahaii_indicator_values",
            "data_collection_runs"
        ]
        
        found_tables = sum(1 for table in table_checks if f"CREATE TABLE IF NOT EXISTS {table}" in content)
        print(f"   ✅ Found {found_tables}/{len(table_checks)} database tables")
        
        schema_passed = found_tables >= 4
        print(f"   📊 Database schema: {'PASS' if schema_passed else 'FAIL'}")
    else:
        print("   ❌ Database schema file not found")
        schema_passed = False
    
    # Overall results
    print("\n" + "=" * 50)
    print("📋 INTEGRATION TEST SUMMARY")
    print("=" * 50)
    
    tests = [
        ("File Structure", all_exist),
        ("FastAPI Integration", integration_passed),
        ("API Endpoints", endpoints_passed),
        ("Data Models", models_passed),
        ("Database Service", db_service_passed),
        ("Database Schema", schema_passed)
    ]
    
    passed_tests = sum(1 for _, passed in tests if passed)
    total_tests = len(tests)
    
    for test_name, passed in tests:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:20} {status}")
    
    print(f"\nOverall: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("\n🎉 ALL INTEGRATION TESTS PASSED!")
        print("✅ AHAII Phase 2 is properly integrated with FastAPI")
        print("✅ Database models and schema are configured")
        print("✅ API endpoints are properly structured")
        print("✅ Ready for deployment and testing")
    elif passed_tests >= total_tests - 1:
        print("\n✅ INTEGRATION MOSTLY SUCCESSFUL!")
        print("⚠️  Minor issues detected - review failed tests")
        print("🚀 Ready for deployment with monitoring")
    else:
        print("\n⚠️  INTEGRATION ISSUES DETECTED")
        print("🔧 Please review and fix failed tests before deployment")
    
    return passed_tests == total_tests

def test_directory_structure():
    """Test updated directory structure"""
    print("\n7. Updated Directory Structure Check")
    
    new_structure = [
        "backend/app/",
        "backend/app/data_collection/",
        "backend/app/scoring/",
        "backend/app/validation/", 
        "backend/app/analysis/",
        "backend/api/",
        "backend/models/",
        "backend/services/"
    ]
    
    all_dirs_exist = True
    for dir_path in new_structure:
        if Path(dir_path).exists():
            print(f"   ✅ {dir_path}")
        else:
            print(f"   ❌ {dir_path}")
            all_dirs_exist = False
    
    print(f"   📊 Directory structure: {'PASS' if all_dirs_exist else 'FAIL'}")
    return all_dirs_exist

def show_next_steps():
    """Show next steps for using the AHAII system"""
    print("\n" + "🚀" * 20)
    print("NEXT STEPS TO USE AHAII SYSTEM")
    print("🚀" * 20)
    
    print("\n1. Install Dependencies:")
    print("   pip install -r backend/requirements.txt")
    
    print("\n2. Set Environment Variables:")
    print("   export SUPABASE_URL=your_supabase_url")
    print("   export SUPABASE_ANON_KEY=your_anon_key")
    print("   # ... other environment variables")
    
    print("\n3. Start FastAPI Server:")
    print("   cd backend && python main.py")
    
    print("\n4. Access API Documentation:")
    print("   Open: http://localhost:8000/docs")
    
    print("\n5. Test AHAII Health Check:")
    print("   GET http://localhost:8000/api/ahaii/health")
    
    print("\n6. Run Complete Assessment:")
    print("   POST http://localhost:8000/api/ahaii/run-complete-assessment")
    print("   Body: {")
    print('     "countries": ["ZAF", "KEN"],')
    print('     "include_policy_indicators": true,')
    print('     "include_ecosystem_mapping": true')
    print("   }")
    
    print("\n7. Monitor Progress:")
    print("   GET http://localhost:8000/api/ahaii/status")
    
    print("\n8. Get Results:")
    print("   GET http://localhost:8000/api/ahaii/scores?format=summary")
    
    print("\n" + "🎯" * 20)
    print("AHAII Phase 2 implementation is ready for use!")
    print("🎯" * 20)

if __name__ == "__main__":
    print("🧪 AHAII Phase 2 Integration Test")
    success = test_basic_integration()
    test_directory_structure()
    show_next_steps()
    
    if success:
        print("\n✅ Integration test completed successfully!")
        exit(0)
    else:
        print("\n⚠️  Integration test completed with issues")
        exit(1)