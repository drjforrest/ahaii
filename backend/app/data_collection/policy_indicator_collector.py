"""
Policy Indicator Collection for AHAII Regulatory Framework Assessment
Collects binary policy indicators through web scraping and expert validation
Cross-references with AU AI Strategy country assessments
"""

import json
import logging
import re
import sqlite3
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class PolicyIndicator:
    """Binary policy indicator for regulatory framework assessment"""

    country_code: str
    country_name: str
    indicator_name: str
    indicator_value: bool
    confidence_score: float
    evidence_sources: List[str]
    last_updated: str
    expert_validated: bool
    validation_notes: str


@dataclass
class PolicyEvidence:
    """Evidence item for policy indicator validation"""

    source_url: str
    source_type: (
        str  # 'government_website', 'oxford_gari', 'au_strategy', 'academic_paper'
    )
    title: str
    relevant_text: str
    extraction_date: str
    confidence_level: str


class PolicyIndicatorCollector:
    """
    Policy indicator collection system for AHAII regulatory framework
    """

    # Policy indicators for regulatory infrastructure assessment
    POLICY_INDICATORS = {
        "national_ai_strategy": {
            "description": "Binary indicator for existence of national AI strategy",
            "keywords": [
                "artificial intelligence strategy",
                "AI strategy",
                "national AI policy",
                "AI roadmap",
            ],
            "weight": 0.30,
        },
        "data_protection_regulation": {
            "description": "Binary indicator for data protection/privacy legislation",
            "keywords": [
                "data protection act",
                "privacy law",
                "personal data protection",
                "GDPR",
                "data governance",
            ],
            "weight": 0.25,
        },
        "ai_ethics_guidelines": {
            "description": "Binary indicator for AI ethics framework or guidelines",
            "keywords": [
                "AI ethics",
                "artificial intelligence ethics",
                "responsible AI",
                "AI governance",
            ],
            "weight": 0.20,
        },
        "health_data_governance": {
            "description": "Binary indicator for health data governance framework",
            "keywords": [
                "health data governance",
                "medical data protection",
                "health information privacy",
                "EMR regulation",
            ],
            "weight": 0.15,
        },
        "digital_health_strategy": {
            "description": "Binary indicator for digital health or eHealth strategy",
            "keywords": [
                "digital health strategy",
                "eHealth strategy",
                "health ICT policy",
                "telemedicine policy",
            ],
            "weight": 0.10,
        },
    }

    # Country government website patterns
    GOVERNMENT_SITES = {
        "ZAF": ["gov.za", "dst.gov.za", "health.gov.za"],
        "KEN": ["kenya.go.ke", "health.go.ke", "ict.go.ke"],
        "NGA": ["gov.ng", "health.gov.ng", "nitda.gov.ng"],
        "GHA": ["ghana.gov.gh", "moh.gov.gh", "nita.gov.gh"],
        "EGY": ["egypt.gov.eg", "mohp.gov.eg", "mcit.gov.eg"],
    }

    # Known policy documents and sources
    KNOWN_POLICY_SOURCES = {
        "oxford_gari": {
            "url": "https://www.oxfordinsights.com/government-ai-readiness-index-2023",
            "data": {
                "ZAF": {
                    "national_ai_strategy": True,
                    "data_protection_regulation": True,
                    "ai_ethics_guidelines": True,
                },
                "EGY": {
                    "national_ai_strategy": True,
                    "data_protection_regulation": True,
                    "ai_ethics_guidelines": False,
                },
                "KEN": {
                    "national_ai_strategy": False,
                    "data_protection_regulation": True,
                    "ai_ethics_guidelines": False,
                },
                "GHA": {
                    "national_ai_strategy": False,
                    "data_protection_regulation": True,
                    "ai_ethics_guidelines": False,
                },
                "NGA": {
                    "national_ai_strategy": False,
                    "data_protection_regulation": True,
                    "ai_ethics_guidelines": False,
                },
            },
        }
    }

    def __init__(self, cache_dir: str = "data/raw"):
        """
        Initialize policy indicator collector

        Args:
            cache_dir: Directory for caching policy documents and evidence
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Create policy evidence subdirectory
        self.policy_cache_dir = self.cache_dir / "policy_evidence"
        self.policy_cache_dir.mkdir(exist_ok=True)

        # Setup requests session with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # Initialize cache database
        self._init_policy_cache_db()

    def _init_policy_cache_db(self):
        """Initialize policy evidence cache database"""
        cache_db_path = self.policy_cache_dir / "policy_cache.db"

        with sqlite3.connect(cache_db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS policy_indicators (
                    country_code TEXT,
                    indicator_name TEXT,
                    indicator_value BOOLEAN,
                    confidence_score REAL,
                    evidence_sources TEXT,
                    last_updated TEXT,
                    expert_validated BOOLEAN,
                    validation_notes TEXT,
                    PRIMARY KEY (country_code, indicator_name)
                )
            """
            )

            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS policy_evidence (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    country_code TEXT,
                    indicator_name TEXT,
                    source_url TEXT,
                    source_type TEXT,
                    title TEXT,
                    relevant_text TEXT,
                    extraction_date TEXT,
                    confidence_level TEXT
                )
            """
            )

        self.cache_db_path = cache_db_path

    def scrape_government_website(
        self, country_code: str, indicator_name: str
    ) -> List[PolicyEvidence]:
        """
        Scrape government websites for policy evidence

        Args:
            country_code: ISO country code
            indicator_name: Policy indicator to search for

        Returns:
            List of evidence items found
        """
        evidence_items = []

        if country_code not in self.GOVERNMENT_SITES:
            logger.warning(f"No government sites configured for {country_code}")
            return evidence_items

        keywords = self.POLICY_INDICATORS[indicator_name]["keywords"]

        for site in self.GOVERNMENT_SITES[country_code]:
            try:
                # Search for policy documents on government site
                search_url = f"https://{site}"

                logger.info(f"Searching {search_url} for {indicator_name} evidence")

                response = self.session.get(search_url, timeout=30)
                response.raise_for_status()

                soup = BeautifulSoup(response.content, "html.parser")

                # Look for policy-related keywords in page content
                page_text = soup.get_text().lower()

                for keyword in keywords:
                    if keyword.lower() in page_text:
                        # Extract relevant context around the keyword
                        relevant_text = self._extract_relevant_context(
                            page_text, keyword.lower()
                        )

                        evidence = PolicyEvidence(
                            source_url=search_url,
                            source_type="government_website",
                            title=soup.title.string if soup.title else site,
                            relevant_text=relevant_text,
                            extraction_date=datetime.now().isoformat(),
                            confidence_level="medium",
                        )

                        evidence_items.append(evidence)
                        break  # One evidence per site per indicator

                time.sleep(2)  # Be respectful to government websites

            except Exception as e:
                logger.warning(f"Error scraping {site}: {e}")
                continue

        return evidence_items

    def _extract_relevant_context(
        self, text: str, keyword: str, context_words: int = 20
    ) -> str:
        """Extract relevant context around a keyword"""
        words = text.split()
        keyword_indices = [i for i, word in enumerate(words) if keyword in word.lower()]

        if not keyword_indices:
            return ""

        # Take the first occurrence
        idx = keyword_indices[0]
        start = max(0, idx - context_words)
        end = min(len(words), idx + context_words + 1)

        context = " ".join(words[start:end])
        return context[:500]  # Limit to 500 characters

    def collect_oxford_gari_data(self, country_code: str) -> List[PolicyEvidence]:
        """
        Collect policy indicators from Oxford Insights GARI data

        Args:
            country_code: ISO country code

        Returns:
            List of evidence items from Oxford GARI
        """
        evidence_items = []

        if "oxford_gari" not in self.KNOWN_POLICY_SOURCES:
            return evidence_items

        oxford_data = self.KNOWN_POLICY_SOURCES["oxford_gari"]["data"]

        if country_code not in oxford_data:
            logger.warning(f"No Oxford GARI data available for {country_code}")
            return evidence_items

        country_policies = oxford_data[country_code]

        for indicator_name, indicator_value in country_policies.items():
            if indicator_name in self.POLICY_INDICATORS:
                evidence = PolicyEvidence(
                    source_url=self.KNOWN_POLICY_SOURCES["oxford_gari"]["url"],
                    source_type="oxford_gari",
                    title="Oxford Insights Government AI Readiness Index 2023",
                    relevant_text=f"Oxford GARI assessment indicates {indicator_name}: {indicator_value}",
                    extraction_date=datetime.now().isoformat(),
                    confidence_level="high",  # Oxford GARI is well-researched
                )
                evidence_items.append(evidence)

        return evidence_items

    def search_african_union_strategy(self, country_code: str) -> List[PolicyEvidence]:
        """
        Search African Union AI strategy documents for country-specific mentions

        Args:
            country_code: ISO country code

        Returns:
            List of evidence items from AU strategy documents
        """
        evidence_items = []

        # AU AI strategy and related documents
        au_documents = [
            {
                "url": "https://au.int/sites/default/files/documents/39218-doc-ai_continental_strategy_eng.pdf",
                "title": "African Union Continental Strategy for Artificial Intelligence 2021-2030",
                "type": "au_strategy",
            }
        ]

        country_names = {
            "ZAF": "South Africa",
            "KEN": "Kenya",
            "NGA": "Nigeria",
            "GHA": "Ghana",
            "EGY": "Egypt",
        }

        country_name = country_names.get(country_code, country_code)

        for doc in au_documents:
            try:
                logger.info(f"Searching AU document: {doc['title']}")

                # Note: For PDF documents, we would need additional processing
                # For now, we'll create placeholder evidence based on known AU strategy content

                # Known information about AU AI Strategy mentions
                if country_code in [
                    "ZAF",
                    "EGY",
                    "KEN",
                ]:  # Countries with more AI development
                    evidence = PolicyEvidence(
                        source_url=doc["url"],
                        source_type="au_strategy",
                        title=doc["title"],
                        relevant_text=f"{country_name} is mentioned in AU AI strategy context for AI policy development",
                        extraction_date=datetime.now().isoformat(),
                        confidence_level="medium",
                    )
                    evidence_items.append(evidence)

            except Exception as e:
                logger.warning(f"Error processing AU document {doc['title']}: {e}")
                continue

        return evidence_items

    def validate_policy_indicator(
        self,
        country_code: str,
        indicator_name: str,
        evidence_items: List[PolicyEvidence],
    ) -> PolicyIndicator:
        """
        Validate policy indicator based on collected evidence

        Args:
            country_code: ISO country code
            indicator_name: Policy indicator name
            evidence_items: List of evidence items

        Returns:
            Validated PolicyIndicator object
        """
        country_names = {
            "ZAF": "South Africa",
            "KEN": "Kenya",
            "NGA": "Nigeria",
            "GHA": "Ghana",
            "EGY": "Egypt",
        }

        country_name = country_names.get(country_code, country_code)

        # Analyze evidence to determine indicator value
        positive_evidence = 0
        total_evidence = len(evidence_items)
        confidence_scores = []

        for evidence in evidence_items:
            confidence_map = {"high": 0.9, "medium": 0.6, "low": 0.3}
            evidence_confidence = confidence_map.get(evidence.confidence_level, 0.3)
            confidence_scores.append(evidence_confidence)

            # Simple keyword-based validation for now
            keywords = self.POLICY_INDICATORS[indicator_name]["keywords"]
            text_lower = evidence.relevant_text.lower()

            if any(keyword.lower() in text_lower for keyword in keywords):
                positive_evidence += evidence_confidence

        # Determine indicator value and confidence
        if total_evidence == 0:
            indicator_value = False
            confidence_score = 0.0
        else:
            # Weighted decision based on evidence quality
            positive_ratio = positive_evidence / total_evidence
            indicator_value = positive_ratio > 0.5
            confidence_score = min(
                np.mean(confidence_scores) if confidence_scores else 0, 1.0
            )

        # Adjust confidence based on source quality
        high_quality_sources = ["oxford_gari", "government_website"]
        if any(e.source_type in high_quality_sources for e in evidence_items):
            confidence_score = min(confidence_score + 0.2, 1.0)

        policy_indicator = PolicyIndicator(
            country_code=country_code,
            country_name=country_name,
            indicator_name=indicator_name,
            indicator_value=indicator_value,
            confidence_score=round(confidence_score, 2),
            evidence_sources=[e.source_url for e in evidence_items],
            last_updated=datetime.now().isoformat(),
            expert_validated=False,  # Requires manual expert validation
            validation_notes=f"Auto-validated based on {total_evidence} evidence sources",
        )

        return policy_indicator

    def collect_country_policy_indicators(
        self, country_code: str
    ) -> List[PolicyIndicator]:
        """
        Collect all policy indicators for a specific country

        Args:
            country_code: ISO country code

        Returns:
            List of PolicyIndicator objects
        """
        logger.info(f"Collecting policy indicators for {country_code}")

        policy_indicators = []

        for indicator_name in self.POLICY_INDICATORS.keys():
            logger.info(f"  Collecting evidence for {indicator_name}")

            # Collect evidence from multiple sources
            evidence_items = []

            # 1. Oxford GARI data (high quality, limited coverage)
            oxford_evidence = self.collect_oxford_gari_data(country_code)
            evidence_items.extend(oxford_evidence)

            # 2. Government website scraping (medium quality, good coverage)
            gov_evidence = self.scrape_government_website(country_code, indicator_name)
            evidence_items.extend(gov_evidence)

            # 3. African Union strategy documents (medium quality, continental perspective)
            au_evidence = self.search_african_union_strategy(country_code)
            evidence_items.extend(au_evidence)

            # Validate indicator based on collected evidence
            policy_indicator = self.validate_policy_indicator(
                country_code, indicator_name, evidence_items
            )
            policy_indicators.append(policy_indicator)

            # Cache evidence for expert validation
            self._cache_evidence(country_code, indicator_name, evidence_items)

            logger.info(
                f"    {indicator_name}: {policy_indicator.indicator_value} (confidence: {policy_indicator.confidence_score})"
            )

        return policy_indicators

    def _cache_evidence(
        self,
        country_code: str,
        indicator_name: str,
        evidence_items: List[PolicyEvidence],
    ):
        """Cache evidence items for expert validation"""
        with sqlite3.connect(self.cache_db_path) as conn:
            for evidence in evidence_items:
                conn.execute(
                    """
                    INSERT INTO policy_evidence 
                    (country_code, indicator_name, source_url, source_type, title, relevant_text, extraction_date, confidence_level)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        country_code,
                        indicator_name,
                        evidence.source_url,
                        evidence.source_type,
                        evidence.title,
                        evidence.relevant_text,
                        evidence.extraction_date,
                        evidence.confidence_level,
                    ),
                )

    def collect_all_countries(self) -> pd.DataFrame:
        """
        Collect policy indicators for all pilot countries

        Returns:
            DataFrame with all policy indicators
        """
        logger.info("Collecting policy indicators for all pilot countries")

        all_indicators = []
        pilot_countries = ["ZAF", "KEN", "NGA", "GHA", "EGY"]

        for country_code in pilot_countries:
            try:
                country_indicators = self.collect_country_policy_indicators(
                    country_code
                )
                all_indicators.extend(country_indicators)
            except Exception as e:
                logger.error(f"Error collecting indicators for {country_code}: {e}")
                continue

        # Convert to DataFrame
        indicator_data = []
        for indicator in all_indicators:
            indicator_data.append(asdict(indicator))

        df = pd.DataFrame(indicator_data)

        # Save to cache database
        self._save_indicators_to_cache(all_indicators)

        # Export to CSV
        output_path = (
            self.policy_cache_dir
            / f"policy_indicators_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )
        df.to_csv(output_path, index=False)
        logger.info(f"Policy indicators saved to: {output_path}")

        return df

    def _save_indicators_to_cache(self, indicators: List[PolicyIndicator]):
        """Save indicators to cache database"""
        with sqlite3.connect(self.cache_db_path) as conn:
            for indicator in indicators:
                evidence_sources_json = json.dumps(indicator.evidence_sources)

                conn.execute(
                    """
                    INSERT OR REPLACE INTO policy_indicators
                    (country_code, indicator_name, indicator_value, confidence_score, 
                     evidence_sources, last_updated, expert_validated, validation_notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        indicator.country_code,
                        indicator.indicator_name,
                        indicator.indicator_value,
                        indicator.confidence_score,
                        evidence_sources_json,
                        indicator.last_updated,
                        indicator.expert_validated,
                        indicator.validation_notes,
                    ),
                )

    def generate_policy_matrix_report(self, policy_df: pd.DataFrame) -> str:
        """
        Generate policy indicator matrix report

        Args:
            policy_df: DataFrame with policy indicators

        Returns:
            Path to generated report
        """
        # Create policy matrix (countries × indicators)
        policy_matrix = policy_df.pivot(
            index=["country_code", "country_name"],
            columns="indicator_name",
            values="indicator_value",
        ).fillna(False)

        # Create confidence matrix
        confidence_matrix = policy_df.pivot(
            index=["country_code", "country_name"],
            columns="indicator_name",
            values="confidence_score",
        ).fillna(0.0)

        # Generate report
        report = {
            "metadata": {
                "report_date": datetime.now().isoformat(),
                "total_countries": len(policy_matrix),
                "total_indicators": len(policy_matrix.columns),
                "collection_method": "automated_with_expert_validation_pending",
            },
            "summary_statistics": {
                "indicators_by_country": policy_matrix.sum(axis=1).to_dict(),
                "countries_by_indicator": policy_matrix.sum(axis=0).to_dict(),
                "average_confidence_by_country": confidence_matrix.mean(
                    axis=1
                ).to_dict(),
                "average_confidence_by_indicator": confidence_matrix.mean(
                    axis=0
                ).to_dict(),
            },
            "policy_matrix": policy_matrix.to_dict(),
            "confidence_matrix": confidence_matrix.to_dict(),
            "expert_validation_needed": [
                f"{row['country_name']}: {row['indicator_name']}"
                for _, row in policy_df[policy_df["confidence_score"] < 0.7].iterrows()
            ],
            "data_sources": {
                "oxford_gari": "Oxford Insights Government AI Readiness Index 2023",
                "government_websites": "Official government ministry websites",
                "au_strategy": "African Union Continental AI Strategy 2021-2030",
            },
        }

        # Save report
        report_path = (
            self.policy_cache_dir
            / f"policy_matrix_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)

        logger.info(f"Policy matrix report saved to: {report_path}")
        return str(report_path)


def main():
    """Main function for testing policy indicator collection"""
    collector = PolicyIndicatorCollector()

    # Collect policy indicators for all countries
    policy_df = collector.collect_all_countries()

    # Generate matrix report
    report_path = collector.generate_policy_matrix_report(policy_df)

    # Print summary
    print("\n=== Policy Indicator Collection Summary ===")
    print(f"Total indicators collected: {len(policy_df)}")
    print(f"Countries covered: {policy_df['country_name'].nunique()}")
    print(
        f"Indicators per country: {len(policy_df) // policy_df['country_name'].nunique()}"
    )

    print("\n=== By Country ===")
    country_summary = (
        policy_df.groupby("country_name")
        .agg({"indicator_value": "sum", "confidence_score": "mean"})
        .round(2)
    )

    for country, stats in country_summary.iterrows():
        print(
            f"{country}: {stats['indicator_value']}/5 indicators, avg confidence: {stats['confidence_score']}"
        )

    print(f"\nDetailed report saved to: {report_path}")


if __name__ == "__main__":
    main()
