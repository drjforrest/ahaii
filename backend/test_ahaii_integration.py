"""
FastAPI Integration Test for AHAII Phase 2
Tests the FastAPI endpoints for AHAII assessment components
"""

import asyncio
import json
import sys
from pathlib import Path

try:
    from fastapi.testclient import TestClient
except ImportError:
    print("FastAPI not available - running basic validation only")
    TestClient = None

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from backend.main import app
    # Create test client
    if TestClient:
        client = TestClient(app)
    else:
        client = None
except ImportError as e:
    print(f"Could not import backend.main: {e}")
    app = None
    client = None

def test_root_endpoint():
    """Test the root endpoint includes AHAII information"""
    response = client.get("/")
    assert response.status_code == 200
    
    data = response.json()
    assert "ahaii_components" in data
    assert "ahaii_assessment" in data["endpoints"]
    
    # Check AHAII components are present
    ahaii_components = data["ahaii_components"]
    expected_components = [
        "world_bank_collector",
        "policy_indicator_collector", 
        "ecosystem_mapper",
        "scoring_calculator",
        "expert_validation",
        "report_generator"
    ]
    
    for component in expected_components:
        assert component in ahaii_components
        assert ahaii_components[component] == "active"

def test_health_check():
    """Test the main health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert "ahaii_components" in data or "services" in data

def test_ahaii_health_check():
    """Test AHAII-specific health check"""
    response = client.get("/api/ahaii/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert "connectivity" in data
    assert "all_systems_operational" in data
    
    # Check connectivity results
    connectivity = data["connectivity"]
    expected_checks = [
        "world_bank_api",
        "local_databases", 
        "file_system_access",
        "dependencies"
    ]
    
    for check in expected_checks:
        assert check in connectivity

def test_supported_countries():
    """Test getting supported countries"""
    response = client.get("/api/ahaii/countries")
    assert response.status_code == 200
    
    data = response.json()
    assert "pilot_countries" in data
    assert "total_pilot_countries" in data
    assert data["total_pilot_countries"] == 5
    
    # Check pilot countries structure
    pilot_countries = data["pilot_countries"]
    assert len(pilot_countries) == 5
    
    expected_countries = ["ZAF", "KEN", "NGA", "GHA", "EGY"]
    country_codes = [country["code"] for country in pilot_countries]
    
    for code in expected_countries:
        assert code in country_codes

def test_methodology_endpoint():
    """Test methodology documentation endpoint"""
    response = client.get("/api/ahaii/methodology")
    assert response.status_code == 200
    
    data = response.json()
    assert "framework" in data
    assert "data_sources" in data
    assert "scoring_methodology" in data
    
    # Check framework structure
    framework = data["framework"]
    assert framework["name"] == "African Health AI Infrastructure Index (AHAII)"
    assert "pillars" in framework
    
    # Check all four pillars are present
    pillars = framework["pillars"]
    expected_pillars = [
        "human_capital",
        "physical_infrastructure", 
        "regulatory_framework",
        "economic_market"
    ]
    
    for pillar in expected_pillars:
        assert pillar in pillars
        assert "weight" in pillars[pillar]
        assert "description" in pillars[pillar]
    
    # Verify pillar weights sum to 1.0
    total_weight = sum(pillars[pillar]["weight"] for pillar in pillars)
    assert abs(total_weight - 1.0) < 0.01  # Allow for floating point precision

def test_data_collection_status_initial():
    """Test data collection status when no collection has started"""
    response = client.get("/api/ahaii/data-collection-status")
    assert response.status_code == 200
    
    data = response.json()
    assert "world_bank_status" in data
    assert "policy_indicators_status" in data
    assert "ecosystem_mapping_status" in data
    assert "total_data_points" in data
    assert "completeness_percentage" in data
    
    # Initially should be not_started
    assert data["world_bank_status"] == "not_started"
    assert data["policy_indicators_status"] == "not_started"
    assert data["ecosystem_mapping_status"] == "not_started"
    assert data["total_data_points"] == 0
    assert data["completeness_percentage"] == 0.0

def test_assessment_status_initial():
    """Test assessment status when no assessment has started"""
    response = client.get("/api/ahaii/status")
    assert response.status_code == 200
    
    data = response.json()
    assert "status" in data
    assert "phases_completed" in data
    assert "overall_progress" in data
    
    # Initially should be not_started
    assert data["status"] == "not_started"
    assert len(data["phases_completed"]) == 0
    assert data["overall_progress"] == 0

def test_start_data_collection():
    """Test starting data collection"""
    response = client.post("/api/ahaii/collect-data?countries=ZAF,KEN")
    assert response.status_code == 200
    
    data = response.json()
    assert data["message"] == "Data collection started"
    assert data["status"] == "running"
    assert "countries" in data
    assert "estimated_completion" in data

def test_start_complete_assessment():
    """Test starting complete assessment pipeline"""
    assessment_request = {
        "countries": ["ZAF", "KEN"],
        "include_policy_indicators": True,
        "include_ecosystem_mapping": True,
        "include_expert_validation": True,
        "generate_report": True
    }
    
    response = client.post("/api/ahaii/run-complete-assessment", json=assessment_request)
    assert response.status_code == 200
    
    data = response.json()
    assert data["message"] == "Complete AHAII assessment pipeline started"
    assert data["status"] == "running"
    assert "countries" in data
    assert "components" in data
    assert "estimated_completion" in data

def test_scores_not_available_initially():
    """Test that scores are not available before calculation"""
    response = client.get("/api/ahaii/scores")
    assert response.status_code == 404
    
    data = response.json()
    assert "AHAII scores not available" in data["detail"]

def test_scores_different_formats():
    """Test different score formats (when available)"""
    # These would work after running assessment, but will fail initially
    formats = ["summary", "detailed", "dashboard"]
    
    for format_type in formats:
        response = client.get(f"/api/ahaii/scores?format={format_type}")
        # Should fail initially since no scores are calculated
        assert response.status_code == 404

def test_config_info():
    """Test configuration info endpoint"""
    response = client.get("/config/info")
    assert response.status_code == 200
    
    data = response.json()
    assert "ahaii_pillars" in data
    assert len(data["ahaii_pillars"]) == 4
    assert "human_capital" in data["ahaii_pillars"]
    assert "physical_infrastructure" in data["ahaii_pillars"]
    assert "regulatory" in data["ahaii_pillars"]
    assert "economic" in data["ahaii_pillars"]

def test_invalid_score_format():
    """Test invalid score format parameter"""
    response = client.get("/api/ahaii/scores?format=invalid")
    assert response.status_code == 422  # Validation error

# Integration test for running a simplified assessment
def test_simplified_assessment_flow():
    """Test a simplified assessment flow (may take time)"""
    # Note: This is a more comprehensive test that would actually run components
    # In a production environment, you might want to skip this or run it separately
    
    # 1. Check health
    health_response = client.get("/api/ahaii/health")
    assert health_response.status_code == 200
    
    # 2. Check methodology
    method_response = client.get("/api/ahaii/methodology")
    assert method_response.status_code == 200
    
    # 3. Check supported countries
    countries_response = client.get("/api/ahaii/countries")
    assert countries_response.status_code == 200
    
    # 4. Check initial status
    status_response = client.get("/api/ahaii/status")
    assert status_response.status_code == 200
    assert status_response.json()["status"] == "not_started"
    
    print("✅ All AHAII FastAPI endpoints are properly configured and accessible")

if __name__ == "__main__":
    """Run tests directly"""
    print("Running AHAII FastAPI Integration Tests...")
    
    # Run basic endpoint tests
    try:
        test_root_endpoint()
        print("✅ Root endpoint test passed")
        
        test_health_check()
        print("✅ Health check test passed")
        
        test_ahaii_health_check()
        print("✅ AHAII health check test passed")
        
        test_supported_countries()
        print("✅ Supported countries test passed")
        
        test_methodology_endpoint()
        print("✅ Methodology endpoint test passed")
        
        test_data_collection_status_initial()
        print("✅ Data collection status test passed")
        
        test_assessment_status_initial()
        print("✅ Assessment status test passed")
        
        test_scores_not_available_initially()
        print("✅ Scores not available test passed")
        
        test_config_info()
        print("✅ Config info test passed")
        
        test_simplified_assessment_flow()
        print("✅ Simplified assessment flow test passed")
        
        print("\n🎉 All AHAII FastAPI integration tests passed!")
        print("The AHAII Phase 2 implementation is properly integrated with FastAPI")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise