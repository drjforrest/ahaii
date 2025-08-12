#!/usr/bin/env python3
"""
Simple test of AHAII Intelligence Processing
Tests the core signal extraction without database dependencies
"""

import re
import json
from datetime import datetime
from typing import Dict, List, Optional


class SimpleCountryMatcher:
    """Simplified country detection for testing"""
    
    def __init__(self):
        self.patterns = {
            'ZAF': ['south africa', 'south african', 'johannesburg', 'cape town', 'university of cape town', 'witwatersrand'],
            'KEN': ['kenya', 'kenyan', 'nairobi', 'kenyatta', 'university of nairobi'],
            'NGA': ['nigeria', 'nigerian', 'lagos', 'abuja'],
            'EGY': ['egypt', 'egyptian', 'cairo'],
            'GHA': ['ghana', 'ghanaian', 'accra']
        }
    
    def detect_country(self, text: str) -> Optional[str]:
        text_lower = text.lower()
        
        country_scores = {}
        for iso_code, patterns in self.patterns.items():
            score = 0
            for pattern in patterns:
                if pattern in text_lower:
                    score += 10 if len(pattern.split()) == 2 else 5
            
            if score > 0:
                country_scores[iso_code] = score
        
        if country_scores:
            best_country = max(country_scores.keys(), key=lambda k: country_scores[k])
            return best_country if country_scores[best_country] >= 5 else None
        
        return None


class SimpleIndicatorExtractor:
    """Simplified indicator extraction for testing"""
    
    def __init__(self):
        self.patterns = {
            'emr_adoption_rate': [
                r'(\d+(?:\.\d+)?)\s*(?:percent|%)\s*(?:of\s+)?(?:hospitals|facilities|clinics)\s*(?:have|use|implemented|adopted)\s*(?:EMR|electronic medical record|electronic health record)',
                r'EMR\s*(?:adoption|implementation)\s*(?:rate|level)\s*(?:of|at)\s*(\d+(?:\.\d+)?)\s*(?:percent|%)',
                r'(\d+(?:\.\d+)?)\s*(?:percent|%).*?(?:hospitals|facilities).*?(?:implemented|adopted).*?(?:EMR|electronic medical record)'
            ],
            'clinical_ai_certification_programs': [
                r'(\d+)\s*(?:new\s+)?(?:AI|artificial intelligence)\s*(?:training|certification|education)\s*programs?',
                r'(?:includes|established)\s*(\d+)\s*(?:new\s+)?(?:AI|artificial intelligence).*?programs'
            ],
            'telemedicine_capability': [
                r'(\d+(?:\.\d+)?)\s*(?:percent|%)\s*(?:of\s+)?(?:hospitals|facilities).*?(?:offer|provide)\s*(?:telemedicine|telehealth|remote consultation)'
            ]
        }
    
    def extract_indicators(self, text: str, country_iso: str) -> List[Dict]:
        signals = []
        
        # Clean text for better matching
        text = ' '.join(text.split())  # Normalize whitespace
        
        for indicator_name, pattern_list in self.patterns.items():
            for pattern in pattern_list:
                matches = re.finditer(pattern, text, re.IGNORECASE | re.DOTALL)
                
                for match in matches:
                    try:
                        value = float(match.group(1))
                        
                        # Determine pillar
                        if 'emr' in indicator_name or 'telemedicine' in indicator_name:
                            pillar = 'physical_infrastructure'
                        elif 'certification' in indicator_name or 'training' in indicator_name:
                            pillar = 'human_capital'
                        else:
                            pillar = 'regulatory_infrastructure'
                        
                        signals.append({
                            'indicator_name': indicator_name,
                            'indicator_value': value,
                            'pillar': pillar,
                            'confidence_score': 0.8,
                            'extracted_text': match.group(0),
                            'country_iso': country_iso
                        })
                        
                    except (ValueError, IndexError):
                        continue
        
        return signals


def test_intelligence_processing():
    """Test intelligence processing with sample reports"""
    
    # Test reports
    test_reports = [
        {
            'title': 'South Africa Launches National Health AI Initiative', 
            'content': '''
            South Africa's Department of Health announces that 78% of public hospitals 
            now have electronic medical record systems operational. The program includes 
            25 new artificial intelligence certification programs for healthcare workers 
            across major medical schools including University of Cape Town and 
            Witwatersrand Medical School.
            ''',
            'expected_country': 'ZAF'
        },
        {
            'title': 'Kenya Ministry of Health Digital Health Update',
            'content': '''
            Kenya's health ministry reported that 85% of public hospitals have 
            successfully implemented EMR systems. Additionally, 12 new AI training 
            programs for clinical staff have been established in partnership with 
            University of Nairobi Medical School.
            ''',
            'expected_country': 'KEN'
        },
        {
            'title': 'Ghana Health Service Telemedicine Expansion',
            'content': '''
            Ghana Health Service announces that 45% of hospitals now offer 
            telemedicine services. The expansion includes 8 new AI certification 
            programs for healthcare professionals in Accra and Kumasi.
            ''',
            'expected_country': 'GHA'
        }
    ]
    
    # Initialize processors
    country_matcher = SimpleCountryMatcher()
    indicator_extractor = SimpleIndicatorExtractor()
    
    print("AHAII Intelligence Processing Test Results")
    print("=" * 60)
    
    for i, report in enumerate(test_reports, 1):
        print(f"\n📰 TEST REPORT {i}: {report['title']}")
        
        # Detect country
        detected_country = country_matcher.detect_country(
            report['title'] + ' ' + report['content']
        )
        
        country_correct = "✅" if detected_country == report['expected_country'] else "❌"
        print(f"🌍 Country Detection: {detected_country} {country_correct}")
        
        if detected_country:
            # Extract indicators
            signals = indicator_extractor.extract_indicators(
                report['title'] + ' ' + report['content'],
                detected_country
            )
            
            print(f"📊 Infrastructure Signals Extracted: {len(signals)}")
            
            for signal in signals:
                print(f"   • {signal['indicator_name']}: {signal['indicator_value']}")
                print(f"     Pillar: {signal['pillar']} | Confidence: {signal['confidence_score']}")
                print(f"     Text: \"{signal['extracted_text'][:80]}...\"")
                print()
        
        print("-" * 50)
    
    print("\n🎯 Summary:")
    print("This demonstrates how AHAII automatically:")
    print("1. Detects African countries from intelligence sources")
    print("2. Extracts quantitative infrastructure indicators") 
    print("3. Maps indicators to AHAII pillars")
    print("4. Provides confidence scores for data quality")
    print("\nIn the full system, these signals would:")
    print("→ Update the infrastructure_indicators database table")
    print("→ Trigger automatic AHAII score recalculation")
    print("→ Update country rankings in real-time")
    print("→ Refresh dashboard visualizations")


if __name__ == "__main__":
    test_intelligence_processing()
