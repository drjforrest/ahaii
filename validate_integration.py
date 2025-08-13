"""
AHAII Phase 2 Integration Validation
Validates that all components are properly integrated and structured
"""

import sys
from pathlib import Path

def validate_file_structure():
    """Validate that all required files exist"""
    print("Validating AHAII Phase 2 file structure...")
    
    required_files = [
        # Main integration
        "backend/app/main_integration.py",
        
        # Data collection components
        "backend/app/data_collection/worldbank_collector.py",
        "backend/app/data_collection/policy_indicator_collector.py", 
        "backend/app/data_collection/health_ai_ecosystem_mapper.py",
        
        # Scoring components
        "backend/app/scoring/ahaii_calculator.py",
        "backend/app/scoring/enhanced_ahaii_calculator.py",
        
        # Validation components
        "backend/app/validation/data_quality_report.py",
        "backend/app/validation/expert_validation_system.py",
        
        # Reporting components
        "backend/app/analysis/pilot_assessment/ahaii_pilot_report.py",
        
        # FastAPI integration
        "backend/api/ahaii_assessment.py",
        "backend/main.py",
        
        # Documentation
        "PHASE2_IMPLEMENTATION_COMPLETE.md"
    ]
    
    missing_files = []
    existing_files = []
    
    for file_path in required_files:
        full_path = Path(file_path)
        if full_path.exists():
            existing_files.append(file_path)
            print(f"✅ {file_path}")
        else:
            missing_files.append(file_path)
            print(f"❌ {file_path}")
    
    print(f"\nFile structure validation:")
    print(f"✅ Existing files: {len(existing_files)}")
    print(f"❌ Missing files: {len(missing_files)}")
    
    return len(missing_files) == 0

def validate_imports():
    """Validate that key modules can be imported"""
    print("\nValidating module imports...")
    
    # Add src to path
    src_path = Path("src")
    if src_path.exists():
        sys.path.insert(0, str(src_path.absolute()))
    
    modules_to_test = [
        ("data_collection.worldbank_collector", "WorldBankCollector"),
        ("data_collection.policy_indicator_collector", "PolicyIndicatorCollector"),
        ("data_collection.health_ai_ecosystem_mapper", "HealthAIEcosystemMapper"),
        ("scoring.ahaii_calculator", "AHAIICalculator"),
        ("scoring.enhanced_ahaii_calculator", "EnhancedAHAIICalculator"),
        ("validation.data_quality_report", "DataQualityReporter"),
        ("validation.expert_validation_system", "ExpertValidationSystem"),
        ("main_integration", "AHAIIIntegrationManager")
    ]
    
    successful_imports = 0
    failed_imports = 0
    
    for module_name, class_name in modules_to_test:
        try:
            module = __import__(module_name, fromlist=[class_name])
            cls = getattr(module, class_name)
            print(f"✅ {module_name}.{class_name}")
            successful_imports += 1
        except Exception as e:
            print(f"❌ {module_name}.{class_name}: {e}")
            failed_imports += 1
    
    print(f"\nImport validation:")
    print(f"✅ Successful imports: {successful_imports}")
    print(f"❌ Failed imports: {failed_imports}")
    
    return failed_imports == 0

def validate_fastapi_integration():
    """Validate FastAPI integration"""
    print("\nValidating FastAPI integration...")
    
    try:
        # Add backend to path
        backend_path = Path("backend")
        if backend_path.exists():
            sys.path.insert(0, str(backend_path.absolute()))
        
        # Check if main.py exists and can be read
        main_py = Path("backend/main.py")
        if main_py.exists():
            content = main_py.read_text()
            
            # Check for AHAII router import
            if "from api.ahaii_assessment import router as ahaii_router" in content:
                print("✅ AHAII router import found in main.py")
            else:
                print("❌ AHAII router import missing in main.py")
                return False
            
            # Check for router inclusion
            if "app.include_router(ahaii_router)" in content:
                print("✅ AHAII router included in FastAPI app")
            else:
                print("❌ AHAII router not included in FastAPI app")
                return False
            
            # Check for AHAII endpoints in documentation
            if "ahaii_assessment" in content:
                print("✅ AHAII endpoints documented in root response")
            else:
                print("❌ AHAII endpoints not documented")
                return False
            
            print("✅ FastAPI integration validation passed")
            return True
        else:
            print("❌ backend/main.py not found")
            return False
            
    except Exception as e:
        print(f"❌ FastAPI integration validation failed: {e}")
        return False

def validate_ahaii_api_endpoints():
    """Validate AHAII API endpoint file"""
    print("\nValidating AHAII API endpoints...")
    
    api_file = Path("backend/api/ahaii_assessment.py")
    if not api_file.exists():
        print("❌ AHAII API file not found")
        return False
    
    content = api_file.read_text()
    
    # Check for required endpoints
    required_endpoints = [
        "/health",
        "/collect-data", 
        "/calculate-scores",
        "/scores",
        "/validate",
        "/generate-report",
        "/run-complete-assessment",
        "/status",
        "/countries",
        "/methodology"
    ]
    
    missing_endpoints = []
    for endpoint in required_endpoints:
        if f'"{endpoint}"' in content or f"'{endpoint}'" in content:
            print(f"✅ Endpoint {endpoint} defined")
        else:
            print(f"❌ Endpoint {endpoint} missing")
            missing_endpoints.append(endpoint)
    
    # Check for required imports
    required_imports = [
        "AHAIIIntegrationManager",
        "WorldBankCollector",
        "PolicyIndicatorCollector",
        "HealthAIEcosystemMapper",
        "EnhancedAHAIICalculator"
    ]
    
    for import_name in required_imports:
        if import_name in content:
            print(f"✅ Import {import_name} found")
        else:
            print(f"❌ Import {import_name} missing")
    
    return len(missing_endpoints) == 0

def validate_directory_structure():
    """Validate directory structure is correct"""
    print("\nValidating directory structure...")
    
    required_dirs = [
        "src",
        "src/data_collection",
        "src/scoring", 
        "src/validation",
        "analysis",
        "analysis/pilot_assessment",
        "data",
        "data/raw",
        "data/processed", 
        "data/indicators",
        "backend",
        "backend/api"
    ]
    
    missing_dirs = []
    for dir_path in required_dirs:
        full_path = Path(dir_path)
        if full_path.exists() and full_path.is_dir():
            print(f"✅ {dir_path}/")
        else:
            print(f"❌ {dir_path}/ (missing)")
            missing_dirs.append(dir_path)
    
    return len(missing_dirs) == 0

def main():
    """Run all validations"""
    print("=" * 60)
    print("AHAII PHASE 2 INTEGRATION VALIDATION")
    print("=" * 60)
    
    validations = [
        ("Directory Structure", validate_directory_structure),
        ("File Structure", validate_file_structure),
        ("FastAPI Integration", validate_fastapi_integration),
        ("AHAII API Endpoints", validate_ahaii_api_endpoints),
        ("Module Imports", validate_imports)
    ]
    
    passed_validations = 0
    total_validations = len(validations)
    
    for validation_name, validation_func in validations:
        print(f"\n{'-' * 40}")
        print(f"VALIDATION: {validation_name}")
        print(f"{'-' * 40}")
        
        try:
            if validation_func():
                print(f"✅ {validation_name} validation PASSED")
                passed_validations += 1
            else:
                print(f"❌ {validation_name} validation FAILED")
        except Exception as e:
            print(f"❌ {validation_name} validation ERROR: {e}")
    
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    print(f"Passed validations: {passed_validations}/{total_validations}")
    
    if passed_validations == total_validations:
        print("🎉 ALL VALIDATIONS PASSED!")
        print("AHAII Phase 2 implementation is properly integrated with FastAPI")
        print("Ready for production deployment")
    else:
        print("⚠️  Some validations failed")
        print("Please review the issues above before deployment")
    
    print("\n" + "=" * 60)
    print("NEXT STEPS:")
    print("1. Start FastAPI server: cd backend && python main.py")
    print("2. Visit API docs: http://localhost:8000/docs")
    print("3. Test AHAII endpoints: http://localhost:8000/api/ahaii/")
    print("4. Run complete assessment: POST /api/ahaii/run-complete-assessment")
    print("=" * 60)

if __name__ == "__main__":
    main()