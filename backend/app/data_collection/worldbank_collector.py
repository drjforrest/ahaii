"""
World Bank API Data Collection Pipeline for AHAII
African Health AI Infrastructure Index

Collects 12 priority World Bank indicators for 5 pilot countries
Handles missing data gracefully with confidence scoring
Stores in PostgreSQL with data quality metadata
Implements caching to avoid API rate limits
"""

import json
import logging
import sqlite3
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WorldBankCollector:
    """
    Automated data collection system for World Bank indicators
    """

    # Key indicators for health AI infrastructure assessment
    KEY_INDICATORS = {
        "EG.ELC.ACCS.ZS": "electricity_access_pct",
        "IT.CEL.SETS.P2": "mobile_subscriptions_per_100",
        "IT.NET.USER.ZS": "internet_users_pct",
        "GB.XPD.RSDV.GD.ZS": "rd_expenditure_pct_gdp",
        "SH.MED.BEDS.ZS": "hospital_beds_per_1000",
        "SH.XPD.CHEX.GD.ZS": "current_health_expenditure_pct_gdp",
        "SE.TER.ENRR": "tertiary_education_enrollment_rate",
        "IT.MLT.MAIN.P2": "fixed_broadband_subscriptions_per_100",
        "SH.MED.PHYS.ZS": "physicians_per_1000",
        "NY.GDP.PCAP.CD": "gdp_per_capita_current_usd",
        "SP.POP.TOTL": "total_population",
        "SE.XPD.TOTL.GD.ZS": "government_expenditure_on_education_pct_gdp",
    }

    # Pilot countries for initial assessment
    PILOT_COUNTRIES = ["ZAF", "KEN", "NGA", "GHA", "EGY"]

    # Country name mapping
    COUNTRY_NAMES = {
        "ZAF": "South Africa",
        "KEN": "Kenya",
        "NGA": "Nigeria",
        "GHA": "Ghana",
        "EGY": "Egypt",
    }

    def __init__(self, cache_dir: str = "data/raw", db_path: Optional[str] = None):
        """
        Initialize World Bank data collector

        Args:
            cache_dir: Directory for caching downloaded data
            db_path: Path to database connection (if None, uses local cache)
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = db_path

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

        # Initialize local cache database
        self._init_cache_db()

    def _init_cache_db(self):
        """Initialize local SQLite cache database"""
        cache_db_path = self.cache_dir / "worldbank_cache.db"

        with sqlite3.connect(cache_db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS indicator_data (
                    country_code TEXT,
                    indicator_code TEXT,
                    year INTEGER,
                    value REAL,
                    confidence_score REAL,
                    data_source TEXT,
                    collection_date TEXT,
                    PRIMARY KEY (country_code, indicator_code, year)
                )
            """
            )

            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS collection_metadata (
                    country_code TEXT,
                    indicator_code TEXT,
                    last_updated TEXT,
                    success_rate REAL,
                    total_requests INTEGER,
                    PRIMARY KEY (country_code, indicator_code)
                )
            """
            )

        self.cache_db_path = cache_db_path

    def _check_cache(
        self, country_code: str, indicator_code: str, max_age_days: int = 7
    ) -> Optional[pd.DataFrame]:
        """
        Check if data exists in cache and is recent enough

        Args:
            country_code: ISO country code
            indicator_code: World Bank indicator code
            max_age_days: Maximum age of cached data in days

        Returns:
            Cached data if available and recent, None otherwise
        """
        cutoff_date = (datetime.now() - timedelta(days=max_age_days)).isoformat()

        with sqlite3.connect(self.cache_db_path) as conn:
            query = """
                SELECT country_code, indicator_code, year, value, confidence_score, data_source
                FROM indicator_data 
                WHERE country_code = ? AND indicator_code = ? AND collection_date > ?
                ORDER BY year
            """

            df = pd.read_sql_query(
                query, conn, params=(country_code, indicator_code, cutoff_date)
            )

            if len(df) > 0:
                logger.info(f"Using cached data for {country_code} - {indicator_code}")
                return df

        return None

    def _cache_data(self, data: pd.DataFrame, country_code: str, indicator_code: str):
        """
        Cache data to local database

        Args:
            data: DataFrame with indicator data
            country_code: ISO country code
            indicator_code: World Bank indicator code
        """
        data_to_cache = data.copy()
        data_to_cache["collection_date"] = datetime.now().isoformat()

        with sqlite3.connect(self.cache_db_path) as conn:
            # Insert/replace data
            data_to_cache.to_sql(
                "indicator_data", conn, if_exists="replace", index=False, method="multi"
            )

            # Update metadata
            success_rate = (
                len(data_to_cache[data_to_cache["value"].notna()]) / len(data_to_cache)
                if len(data_to_cache) > 0
                else 0
            )

            conn.execute(
                """
                INSERT OR REPLACE INTO collection_metadata 
                (country_code, indicator_code, last_updated, success_rate, total_requests)
                VALUES (?, ?, ?, ?, ?)
            """,
                (
                    country_code,
                    indicator_code,
                    datetime.now().isoformat(),
                    success_rate,
                    len(data_to_cache),
                ),
            )

    def fetch_indicator_data(
        self,
        country_code: str,
        indicator_code: str,
        start_year: int = 2020,
        end_year: int = 2023,
        use_cache: bool = True,
    ) -> pd.DataFrame:
        """
        Fetch data for a specific indicator and country from World Bank API

        Args:
            country_code: ISO country code (e.g., 'ZAF')
            indicator_code: World Bank indicator code (e.g., 'EG.ELC.ACCS.ZS')
            start_year: Starting year for data collection
            end_year: Ending year for data collection
            use_cache: Whether to use cached data if available

        Returns:
            DataFrame with indicator data including confidence scores
        """
        # Check cache first
        if use_cache:
            cached_data = self._check_cache(country_code, indicator_code)
            if cached_data is not None:
                return cached_data

        logger.info(f"Fetching {indicator_code} for {country_code} from World Bank API")

        # World Bank API endpoint
        url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator_code}"

        params = {
            "date": f"{start_year}:{end_year}",
            "format": "json",
            "per_page": 1000,
        }

        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()

            # Handle API response format
            if len(data) < 2 or data[1] is None:
                logger.warning(
                    f"No data returned for {indicator_code} in {country_code}"
                )
                return self._create_empty_dataframe(
                    country_code, indicator_code, start_year, end_year
                )

            # Process API response
            records = []
            for item in data[1]:
                if item["value"] is not None:
                    records.append(
                        {
                            "country_code": country_code,
                            "indicator_code": indicator_code,
                            "year": int(item["date"]),
                            "value": float(item["value"]),
                            "confidence_score": 1.0,  # High confidence for direct API data
                            "data_source": "world_bank_api",
                        }
                    )
                else:
                    # Add record for missing data with low confidence
                    records.append(
                        {
                            "country_code": country_code,
                            "indicator_code": indicator_code,
                            "year": int(item["date"]),
                            "value": None,
                            "confidence_score": 0.0,
                            "data_source": "world_bank_api_missing",
                        }
                    )

            df = pd.DataFrame(records)

            # Apply data quality assessment
            df = self._assess_data_quality(df)

            # Cache the results
            if use_cache:
                self._cache_data(df, country_code, indicator_code)

            time.sleep(0.5)  # Rate limiting - be respectful to API

            return df

        except requests.exceptions.RequestException as e:
            logger.error(
                f"Error fetching data for {indicator_code} in {country_code}: {e}"
            )
            return self._create_empty_dataframe(
                country_code, indicator_code, start_year, end_year
            )

    def _create_empty_dataframe(
        self, country_code: str, indicator_code: str, start_year: int, end_year: int
    ) -> pd.DataFrame:
        """Create empty dataframe for missing data"""
        years = list(range(start_year, end_year + 1))
        return pd.DataFrame(
            {
                "country_code": [country_code] * len(years),
                "indicator_code": [indicator_code] * len(years),
                "year": years,
                "value": [None] * len(years),
                "confidence_score": [0.0] * len(years),
                "data_source": ["api_error"] * len(years),
            }
        )

    def _assess_data_quality(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Assess data quality and adjust confidence scores

        Args:
            df: DataFrame with indicator data

        Returns:
            DataFrame with updated confidence scores
        """
        df = df.copy()

        # Adjust confidence based on data completeness
        total_years = len(df)
        available_years = len(df[df["value"].notna()])
        completeness_ratio = available_years / total_years if total_years > 0 else 0

        # Reduce confidence for incomplete datasets
        if completeness_ratio < 0.5:
            df.loc[df["value"].notna(), "confidence_score"] *= 0.8
        elif completeness_ratio < 0.75:
            df.loc[df["value"].notna(), "confidence_score"] *= 0.9

        # Check for outliers (values > 3 standard deviations from mean)
        if available_years > 2:
            mean_val = df["value"].mean()
            std_val = df["value"].std()

            if std_val > 0:
                outlier_mask = abs(df["value"] - mean_val) > 3 * std_val
                df.loc[outlier_mask, "confidence_score"] *= 0.7

        return df

    def collect_all_indicators(
        self, start_year: int = 2020, end_year: int = 2023
    ) -> pd.DataFrame:
        """
        Collect all priority indicators for all pilot countries

        Args:
            start_year: Starting year for data collection
            end_year: Ending year for data collection

        Returns:
            Complete DataFrame with all indicator data
        """
        logger.info("Starting comprehensive World Bank data collection for AHAII")

        all_data = []
        total_requests = len(self.PILOT_COUNTRIES) * len(self.KEY_INDICATORS)
        completed_requests = 0

        for country_code in self.PILOT_COUNTRIES:
            country_name = self.COUNTRY_NAMES[country_code]
            logger.info(f"Collecting data for {country_name} ({country_code})")

            for indicator_code, indicator_name in self.KEY_INDICATORS.items():
                logger.info(f"  Fetching {indicator_name} ({indicator_code})")

                df = self.fetch_indicator_data(
                    country_code=country_code,
                    indicator_code=indicator_code,
                    start_year=start_year,
                    end_year=end_year,
                )

                # Add indicator name for easier analysis
                df["indicator_name"] = indicator_name
                df["country_name"] = country_name

                all_data.append(df)
                completed_requests += 1

                progress = (completed_requests / total_requests) * 100
                logger.info(
                    f"  Progress: {progress:.1f}% ({completed_requests}/{total_requests})"
                )

        # Combine all data
        combined_df = pd.concat(all_data, ignore_index=True)

        # Save raw data
        output_path = (
            self.cache_dir
            / f"worldbank_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )
        combined_df.to_csv(output_path, index=False)
        logger.info(f"Raw data saved to: {output_path}")

        return combined_df

    def generate_data_completeness_report(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate comprehensive data completeness report

        Args:
            data: DataFrame with collected indicator data

        Returns:
            Dictionary with completeness statistics
        """
        report = {
            "collection_summary": {
                "total_countries": len(data["country_code"].unique()),
                "total_indicators": len(data["indicator_code"].unique()),
                "total_data_points": len(data),
                "available_data_points": len(data[data["value"].notna()]),
                "overall_completeness": len(data[data["value"].notna()])
                / len(data)
                * 100,
            },
            "by_country": {},
            "by_indicator": {},
            "by_year": {},
            "confidence_analysis": {},
        }

        # By country analysis
        for country in data["country_code"].unique():
            country_data = data[data["country_code"] == country]
            total = len(country_data)
            available = len(country_data[country_data["value"].notna()])

            report["by_country"][country] = {
                "country_name": country_data["country_name"].iloc[0],
                "total_data_points": total,
                "available_data_points": available,
                "completeness_pct": (available / total * 100) if total > 0 else 0,
                "avg_confidence": country_data[country_data["value"].notna()][
                    "confidence_score"
                ].mean(),
            }

        # By indicator analysis
        for indicator in data["indicator_code"].unique():
            indicator_data = data[data["indicator_code"] == indicator]
            total = len(indicator_data)
            available = len(indicator_data[indicator_data["value"].notna()])

            report["by_indicator"][indicator] = {
                "indicator_name": indicator_data["indicator_name"].iloc[0],
                "total_data_points": total,
                "available_data_points": available,
                "completeness_pct": (available / total * 100) if total > 0 else 0,
                "avg_confidence": indicator_data[indicator_data["value"].notna()][
                    "confidence_score"
                ].mean(),
            }

        # By year analysis
        for year in sorted(data["year"].unique()):
            year_data = data[data["year"] == year]
            total = len(year_data)
            available = len(year_data[year_data["value"].notna()])

            report["by_year"][year] = {
                "total_data_points": total,
                "available_data_points": available,
                "completeness_pct": (available / total * 100) if total > 0 else 0,
                "avg_confidence": year_data[year_data["value"].notna()][
                    "confidence_score"
                ].mean(),
            }

        # Confidence analysis
        available_data = data[data["value"].notna()]
        if len(available_data) > 0:
            report["confidence_analysis"] = {
                "mean_confidence": available_data["confidence_score"].mean(),
                "median_confidence": available_data["confidence_score"].median(),
                "min_confidence": available_data["confidence_score"].min(),
                "max_confidence": available_data["confidence_score"].max(),
                "high_confidence_pct": len(
                    available_data[available_data["confidence_score"] >= 0.8]
                )
                / len(available_data)
                * 100,
            }

        # Save report
        report_path = (
            self.cache_dir
            / f"data_completeness_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)

        logger.info(f"Data completeness report saved to: {report_path}")

        return report


def main():
    """Main function for testing the World Bank collector"""
    collector = WorldBankCollector()

    # Collect all data
    data = collector.collect_all_indicators()

    # Generate completeness report
    report = collector.generate_data_completeness_report(data)

    # Print summary
    print("\n=== World Bank Data Collection Summary ===")
    print(f"Total data points: {report['collection_summary']['total_data_points']}")
    print(
        f"Available data points: {report['collection_summary']['available_data_points']}"
    )
    print(
        f"Overall completeness: {report['collection_summary']['overall_completeness']:.1f}%"
    )

    print("\n=== By Country ===")
    for country_code, stats in report["by_country"].items():
        print(f"{stats['country_name']}: {stats['completeness_pct']:.1f}% complete")

    print("\n=== By Indicator ===")
    for indicator_code, stats in report["by_indicator"].items():
        print(f"{stats['indicator_name']}: {stats['completeness_pct']:.1f}% complete")


if __name__ == "__main__":
    main()
