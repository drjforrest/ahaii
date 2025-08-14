#!/usr/bin/env python3
"""
AHAII Data Quality Management System
Advanced validation, cleaning, and enhancement of health AI infrastructure data
"""

import re
import json
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple, Set
from dataclasses import dataclass
from enum import Enum

from loguru import logger
from fuzzywuzzy import fuzz, process
import pycountry

from services.database_service import DatabaseService
from config.database import supabase


class ValidationSeverity(Enum):
    """Data validation issue severity levels"""

    CRITICAL = "critical"  # Prevents data usage
    HIGH = "high"  # Significantly impacts quality
    MEDIUM = "medium"  # Moderate impact
    LOW = "low"  # Minor issue
    INFO = "info"  # Informational only


@dataclass
class ValidationIssue:
    """Represents a data validation issue"""

    severity: ValidationSeverity
    category: str
    description: str
    field_name: Optional[str] = None
    current_value: Optional[Any] = None
    suggested_value: Optional[Any] = None
    record_id: Optional[str] = None
    table_name: Optional[str] = None


class AHAIIDataQualityManager:
    """Comprehensive data quality management for AHAII"""

    def __init__(self):
        self.db_service = DatabaseService()

        # Country name mappings for standardization
        self.country_mappings = self._build_country_mappings()

        # Organization name patterns for standardization
        self.org_patterns = {
            "world health organization": [
                "WHO",
                "World Health Organization",
                "world health org",
            ],
            "african union": ["AU", "African Union", "african development bank"],
            "ministry of health": [
                "ministry of health",
                "health ministry",
                "dept of health",
                "department of health",
            ],
            "world bank": ["World Bank", "world bank group", "WB"],
            "united nations": ["UN", "United Nations", "united nations system"],
        }

        # Health AI keywords for validation
        self.health_ai_keywords = {
            "core_terms": [
                "artificial intelligence",
                "machine learning",
                "deep learning",
                "neural network",
                "computer vision",
                "natural language processing",
                "predictive analytics",
                "clinical decision support",
                "medical imaging ai",
                "diagnostic ai",
            ],
            "health_domains": [
                "radiology",
                "pathology",
                "dermatology",
                "cardiology",
                "oncology",
                "telemedicine",
                "electronic health records",
                "clinical workflow",
                "population health",
                "public health",
                "healthcare analytics",
            ],
        }

        # Data freshness thresholds
        self.freshness_thresholds = {
            "infrastructure_intelligence": timedelta(days=90),  # 3 months
            "infrastructure_indicators": timedelta(days=365),  # 1 year
            "ahaii_scores": timedelta(days=90),  # 3 months
            "health_ai_organizations": timedelta(days=180),  # 6 months
        }

    def _build_country_mappings(self) -> Dict[str, str]:
        """Build comprehensive country name mappings"""
        mappings = {}

        # Add pycountry mappings
        for country in pycountry.countries:
            # Official name
            mappings[country.name.lower()] = country.name

            # Common name if different
            if hasattr(country, "common_name"):
                mappings[country.common_name.lower()] = country.name

            # Alpha-2 and Alpha-3 codes
            mappings[country.alpha_2.lower()] = country.name
            mappings[country.alpha_3.lower()] = country.name

        # Add African country variations
        african_variations = {
            "south africa": "South Africa",
            "democratic republic of congo": "Congo, The Democratic Republic of the",
            "drc": "Congo, The Democratic Republic of the",
            "congo": "Congo",
            "ivory coast": "Côte d'Ivoire",
            "cape verde": "Cabo Verde",
            "swaziland": "Eswatini",
            "gambia": "Gambia",
        }

        mappings.update({k.lower(): v for k, v in african_variations.items()})
        return mappings

    async def run_comprehensive_quality_check(self) -> Dict[str, List[ValidationIssue]]:
        """Run comprehensive data quality validation across all tables"""
        logger.info("🔍 Starting Comprehensive Data Quality Check...")

        all_issues = {
            "infrastructure_intelligence": [],
            "infrastructure_indicators": [],
            "health_ai_organizations": [],
            "ahaii_scores": [],
            "countries": [],
        }

        # 1. Infrastructure Intelligence Quality Check
        intelligence_issues = await self._validate_infrastructure_intelligence()
        all_issues["infrastructure_intelligence"].extend(intelligence_issues)

        # 2. Infrastructure Indicators Quality Check
        indicator_issues = await self._validate_infrastructure_indicators()
        all_issues["infrastructure_indicators"].extend(indicator_issues)

        # 3. Health AI Organizations Quality Check
        org_issues = await self._validate_health_ai_organizations()
        all_issues["health_ai_organizations"].extend(org_issues)

        # 4. AHAII Scores Quality Check
        score_issues = await self._validate_ahaii_scores()
        all_issues["ahaii_scores"].extend(score_issues)

        # 5. Countries Data Quality Check
        country_issues = await self._validate_countries_data()
        all_issues["countries"].extend(country_issues)

        # Generate summary report
        await self._generate_quality_report(all_issues)

        logger.info("✅ Comprehensive Data Quality Check Complete")
        return all_issues

    async def _validate_infrastructure_intelligence(self) -> List[ValidationIssue]:
        """Validate infrastructure intelligence records"""
        issues = []

        try:
            # Get all intelligence records
            result = (
                await supabase.table("infrastructure_intelligence")
                .select("*")
                .execute()
            )
            records = result.data if result.data else []

            logger.info(
                f"Validating {len(records)} infrastructure intelligence records..."
            )

            for record in records:
                record_id = record.get("id")

                # Check required fields
                if not record.get("report_title"):
                    issues.append(
                        ValidationIssue(
                            severity=ValidationSeverity.HIGH,
                            category="missing_required_field",
                            description="Missing report title",
                            field_name="report_title",
                            record_id=record_id,
                            table_name="infrastructure_intelligence",
                        )
                    )

                # Check data freshness
                created_at = record.get("created_at")
                if created_at:
                    created_date = datetime.fromisoformat(
                        created_at.replace("Z", "+00:00")
                    )
                    if (
                        datetime.now() - created_date
                        > self.freshness_thresholds["infrastructure_intelligence"]
                    ):
                        issues.append(
                            ValidationIssue(
                                severity=ValidationSeverity.MEDIUM,
                                category="data_freshness",
                                description="Intelligence record is older than 3 months",
                                field_name="created_at",
                                current_value=created_at,
                                record_id=record_id,
                                table_name="infrastructure_intelligence",
                            )
                        )

                # Validate health AI relevance
                key_findings = record.get("key_findings", {})
                if isinstance(key_findings, dict):
                    ai_score = key_findings.get("health_ai_relevance_score", 0)
                    if ai_score < 0.2:
                        issues.append(
                            ValidationIssue(
                                severity=ValidationSeverity.LOW,
                                category="relevance_threshold",
                                description="Low health AI relevance score",
                                field_name="key_findings.health_ai_relevance_score",
                                current_value=ai_score,
                                record_id=record_id,
                                table_name="infrastructure_intelligence",
                            )
                        )

                # Validate country association
                if not record.get("country_id"):
                    # Check if we can infer country from content
                    title = record.get("report_title", "").lower()
                    summary = record.get("report_summary", "").lower()
                    content = f"{title} {summary}"

                    suggested_country = self._infer_country_from_text(content)
                    if suggested_country:
                        issues.append(
                            ValidationIssue(
                                severity=ValidationSeverity.MEDIUM,
                                category="missing_country_association",
                                description="Missing country association but country can be inferred",
                                field_name="country_id",
                                suggested_value=suggested_country,
                                record_id=record_id,
                                table_name="infrastructure_intelligence",
                            )
                        )
                    else:
                        issues.append(
                            ValidationIssue(
                                severity=ValidationSeverity.HIGH,
                                category="missing_country_association",
                                description="Missing country association and cannot infer",
                                field_name="country_id",
                                record_id=record_id,
                                table_name="infrastructure_intelligence",
                            )
                        )

                # Validate URL format
                source_url = record.get("source_url")
                if source_url and not self._is_valid_url(source_url):
                    issues.append(
                        ValidationIssue(
                            severity=ValidationSeverity.MEDIUM,
                            category="invalid_format",
                            description="Invalid URL format",
                            field_name="source_url",
                            current_value=source_url,
                            record_id=record_id,
                            table_name="infrastructure_intelligence",
                        )
                    )

        except Exception as e:
            logger.error(f"Error validating infrastructure intelligence: {e}")
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.CRITICAL,
                    category="validation_error",
                    description=f"Failed to validate infrastructure intelligence: {str(e)}",
                    table_name="infrastructure_intelligence",
                )
            )

        return issues

    async def _validate_infrastructure_indicators(self) -> List[ValidationIssue]:
        """Validate infrastructure indicators"""
        issues = []

        try:
            result = (
                await supabase.table("infrastructure_indicators").select("*").execute()
            )
            records = result.data if result.data else []

            logger.info(f"Validating {len(records)} infrastructure indicators...")

            # Valid pillar names
            valid_pillars = {
                "human_capital",
                "physical_infrastructure",
                "regulatory_framework",
                "economic_market",
            }

            for record in records:
                record_id = record.get("id")

                # Validate pillar
                pillar = record.get("pillar")
                if pillar not in valid_pillars:
                    # Try to map to valid pillar
                    suggested_pillar = self._map_to_valid_pillar(pillar)
                    issues.append(
                        ValidationIssue(
                            severity=ValidationSeverity.HIGH,
                            category="invalid_pillar",
                            description=f"Invalid pillar: {pillar}",
                            field_name="pillar",
                            current_value=pillar,
                            suggested_value=suggested_pillar,
                            record_id=record_id,
                            table_name="infrastructure_indicators",
                        )
                    )

                # Validate indicator value ranges
                indicator_value = record.get("indicator_value")
                indicator_unit = record.get("indicator_unit")

                if indicator_value is not None:
                    if indicator_unit == "percentage" and (
                        indicator_value < 0 or indicator_value > 100
                    ):
                        issues.append(
                            ValidationIssue(
                                severity=ValidationSeverity.HIGH,
                                category="invalid_range",
                                description="Percentage value out of valid range (0-100)",
                                field_name="indicator_value",
                                current_value=indicator_value,
                                record_id=record_id,
                                table_name="infrastructure_indicators",
                            )
                        )

                    if indicator_value < 0:
                        issues.append(
                            ValidationIssue(
                                severity=ValidationSeverity.HIGH,
                                category="invalid_range",
                                description="Negative indicator value",
                                field_name="indicator_value",
                                current_value=indicator_value,
                                record_id=record_id,
                                table_name="infrastructure_indicators",
                            )
                        )

                # Validate confidence score
                confidence_score = record.get("confidence_score")
                if confidence_score is not None and (
                    confidence_score < 0 or confidence_score > 1
                ):
                    issues.append(
                        ValidationIssue(
                            severity=ValidationSeverity.MEDIUM,
                            category="invalid_range",
                            description="Confidence score out of valid range (0-1)",
                            field_name="confidence_score",
                            current_value=confidence_score,
                            record_id=record_id,
                            table_name="infrastructure_indicators",
                        )
                    )

                # Check for required country association
                if not record.get("country_id"):
                    issues.append(
                        ValidationIssue(
                            severity=ValidationSeverity.CRITICAL,
                            category="missing_required_field",
                            description="Missing country association",
                            field_name="country_id",
                            record_id=record_id,
                            table_name="infrastructure_indicators",
                        )
                    )

                # Validate data year
                data_year = record.get("data_year")
                current_year = datetime.now().year
                if data_year and (data_year < 2000 or data_year > current_year + 1):
                    issues.append(
                        ValidationIssue(
                            severity=ValidationSeverity.MEDIUM,
                            category="invalid_range",
                            description="Data year out of reasonable range",
                            field_name="data_year",
                            current_value=data_year,
                            record_id=record_id,
                            table_name="infrastructure_indicators",
                        )
                    )

        except Exception as e:
            logger.error(f"Error validating infrastructure indicators: {e}")
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.CRITICAL,
                    category="validation_error",
                    description=f"Failed to validate infrastructure indicators: {str(e)}",
                    table_name="infrastructure_indicators",
                )
            )

        return issues

    async def _validate_health_ai_organizations(self) -> List[ValidationIssue]:
        """Validate health AI organizations"""
        issues = []

        try:
            result = (
                await supabase.table("health_ai_organizations").select("*").execute()
            )
            records = result.data if result.data else []

            logger.info(f"Validating {len(records)} health AI organizations...")

            for record in records:
                record_id = record.get("id")

                # Check required fields
                if not record.get("name"):
                    issues.append(
                        ValidationIssue(
                            severity=ValidationSeverity.CRITICAL,
                            category="missing_required_field",
                            description="Missing organization name",
                            field_name="name",
                            record_id=record_id,
                            table_name="health_ai_organizations",
                        )
                    )

                # Validate website URL
                website = record.get("website")
                if website and not self._is_valid_url(website):
                    issues.append(
                        ValidationIssue(
                            severity=ValidationSeverity.MEDIUM,
                            category="invalid_format",
                            description="Invalid website URL format",
                            field_name="website",
                            current_value=website,
                            record_id=record_id,
                            table_name="health_ai_organizations",
                        )
                    )

                # Validate funding amounts
                total_funding = record.get("total_funding_usd")
                if total_funding is not None and total_funding < 0:
                    issues.append(
                        ValidationIssue(
                            severity=ValidationSeverity.HIGH,
                            category="invalid_range",
                            description="Negative funding amount",
                            field_name="total_funding_usd",
                            current_value=total_funding,
                            record_id=record_id,
                            table_name="health_ai_organizations",
                        )
                    )

                # Validate employee count
                employee_count = record.get("employee_count")
                if employee_count is not None and employee_count < 0:
                    issues.append(
                        ValidationIssue(
                            severity=ValidationSeverity.MEDIUM,
                            category="invalid_range",
                            description="Negative employee count",
                            field_name="employee_count",
                            current_value=employee_count,
                            record_id=record_id,
                            table_name="health_ai_organizations",
                        )
                    )

                # Check country association
                if not record.get("country_id"):
                    issues.append(
                        ValidationIssue(
                            severity=ValidationSeverity.HIGH,
                            category="missing_required_field",
                            description="Missing country association",
                            field_name="country_id",
                            record_id=record_id,
                            table_name="health_ai_organizations",
                        )
                    )

        except Exception as e:
            logger.error(f"Error validating health AI organizations: {e}")

        return issues

    async def _validate_ahaii_scores(self) -> List[ValidationIssue]:
        """Validate AHAII scores"""
        issues = []

        try:
            result = await supabase.table("ahaii_scores").select("*").execute()
            records = result.data if result.data else []

            logger.info(f"Validating {len(records)} AHAII scores...")

            for record in records:
                record_id = record.get("id")

                # Validate score ranges (0-100)
                score_fields = [
                    "total_score",
                    "human_capital_score",
                    "physical_infrastructure_score",
                    "regulatory_infrastructure_score",
                    "economic_market_score",
                ]

                for field in score_fields:
                    score = record.get(field)
                    if score is not None and (score < 0 or score > 100):
                        issues.append(
                            ValidationIssue(
                                severity=ValidationSeverity.CRITICAL,
                                category="invalid_range",
                                description=f"Score out of valid range (0-100): {field}",
                                field_name=field,
                                current_value=score,
                                record_id=record_id,
                                table_name="ahaii_scores",
                            )
                        )

                # Validate confidence scores (0-1)
                confidence_fields = ["overall_confidence_score"]
                for field in confidence_fields:
                    confidence = record.get(field)
                    if confidence is not None and (confidence < 0 or confidence > 1):
                        issues.append(
                            ValidationIssue(
                                severity=ValidationSeverity.HIGH,
                                category="invalid_range",
                                description=f"Confidence score out of valid range (0-1): {field}",
                                field_name=field,
                                current_value=confidence,
                                record_id=record_id,
                                table_name="ahaii_scores",
                            )
                        )

                # Check required country association
                if not record.get("country_id"):
                    issues.append(
                        ValidationIssue(
                            severity=ValidationSeverity.CRITICAL,
                            category="missing_required_field",
                            description="Missing country association",
                            field_name="country_id",
                            record_id=record_id,
                            table_name="ahaii_scores",
                        )
                    )

        except Exception as e:
            logger.error(f"Error validating AHAII scores: {e}")

        return issues

    async def _validate_countries_data(self) -> List[ValidationIssue]:
        """Validate countries reference data"""
        issues = []

        try:
            result = await supabase.table("countries").select("*").execute()
            records = result.data if result.data else []

            logger.info(f"Validating {len(records)} countries...")

            for record in records:
                record_id = record.get("id")

                # Validate ISO codes
                iso_alpha3 = record.get("iso_code_alpha3")
                if iso_alpha3 and len(iso_alpha3) != 3:
                    issues.append(
                        ValidationIssue(
                            severity=ValidationSeverity.HIGH,
                            category="invalid_format",
                            description="ISO Alpha-3 code must be 3 characters",
                            field_name="iso_code_alpha3",
                            current_value=iso_alpha3,
                            record_id=record_id,
                            table_name="countries",
                        )
                    )

                iso_alpha2 = record.get("iso_code_alpha2")
                if iso_alpha2 and len(iso_alpha2) != 2:
                    issues.append(
                        ValidationIssue(
                            severity=ValidationSeverity.HIGH,
                            category="invalid_format",
                            description="ISO Alpha-2 code must be 2 characters",
                            field_name="iso_code_alpha2",
                            current_value=iso_alpha2,
                            record_id=record_id,
                            table_name="countries",
                        )
                    )

                # Validate population
                population = record.get("population")
                if population is not None and population < 0:
                    issues.append(
                        ValidationIssue(
                            severity=ValidationSeverity.HIGH,
                            category="invalid_range",
                            description="Negative population value",
                            field_name="population",
                            current_value=population,
                            record_id=record_id,
                            table_name="countries",
                        )
                    )

        except Exception as e:
            logger.error(f"Error validating countries: {e}")

        return issues

    def _infer_country_from_text(self, text: str) -> Optional[str]:
        """Infer country from text content"""
        text_lower = text.lower()

        # Look for country mentions
        for country_variation, standard_name in self.country_mappings.items():
            if country_variation in text_lower:
                return standard_name

        return None

    def _is_valid_url(self, url: str) -> bool:
        """Validate URL format"""
        url_pattern = re.compile(
            r"^https?://"  # http:// or https://
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"  # domain...
            r"localhost|"  # localhost...
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
            r"(?::\d+)?"  # optional port
            r"(?:/?|[/?]\S+)$",
            re.IGNORECASE,
        )

        return url_pattern.match(url) is not None

    def _map_to_valid_pillar(self, pillar: str) -> str:
        """Map invalid pillar to valid pillar name"""
        pillar_mappings = {
            "human capital": "human_capital",
            "physical": "physical_infrastructure",
            "infrastructure": "physical_infrastructure",
            "regulatory": "regulatory_framework",
            "regulation": "regulatory_framework",
            "economic": "economic_market",
            "market": "economic_market",
        }

        if pillar:
            pillar_lower = pillar.lower().strip()
            return pillar_mappings.get(pillar_lower, "unknown")

        return "unknown"

    async def _generate_quality_report(
        self, all_issues: Dict[str, List[ValidationIssue]]
    ) -> Dict[str, Any]:
        """Generate comprehensive quality report"""

        # Calculate summary statistics
        total_issues = sum(len(issues) for issues in all_issues.values())
        severity_counts = {severity.value: 0 for severity in ValidationSeverity}
        category_counts = {}

        for table_issues in all_issues.values():
            for issue in table_issues:
                severity_counts[issue.severity.value] += 1
                category_counts[issue.category] = (
                    category_counts.get(issue.category, 0) + 1
                )

        # Calculate quality score (0-100)
        critical_weight = severity_counts["critical"] * 10
        high_weight = severity_counts["high"] * 5
        medium_weight = severity_counts["medium"] * 2
        low_weight = severity_counts["low"] * 1

        total_weight = critical_weight + high_weight + medium_weight + low_weight
        quality_score = max(0, 100 - min(100, total_weight))  # Cap at 0-100

        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_issues": total_issues,
                "quality_score": quality_score,
                "severity_breakdown": severity_counts,
                "category_breakdown": category_counts,
            },
            "table_breakdown": {
                table: len(issues) for table, issues in all_issues.items()
            },
            "recommendations": self._generate_quality_recommendations(
                all_issues, quality_score
            ),
        }

        # Log summary
        logger.info("📊 Data Quality Report Generated")
        logger.info(f"   Overall Quality Score: {quality_score}/100")
        logger.info(f"   Total Issues: {total_issues}")
        logger.info(
            f"   Critical: {severity_counts['critical']}, High: {severity_counts['high']}"
        )
        logger.info(
            f"   Medium: {severity_counts['medium']}, Low: {severity_counts['low']}"
        )

        return report

    def _generate_quality_recommendations(
        self, all_issues: Dict[str, List[ValidationIssue]], quality_score: float
    ) -> List[str]:
        """Generate actionable quality improvement recommendations"""
        recommendations = []

        # Critical issues
        critical_count = sum(
            1
            for issues in all_issues.values()
            for issue in issues
            if issue.severity == ValidationSeverity.CRITICAL
        )
        if critical_count > 0:
            recommendations.append(
                f"🚨 URGENT: Fix {critical_count} critical data quality issues immediately"
            )

        # Missing country associations
        missing_countries = sum(
            1
            for issues in all_issues.values()
            for issue in issues
            if issue.category == "missing_country_association"
        )
        if missing_countries > 0:
            recommendations.append(
                f"🌍 Improve country detection: {missing_countries} records need country associations"
            )

        # URL validation issues
        url_issues = sum(
            1
            for issues in all_issues.values()
            for issue in issues
            if issue.category == "invalid_format" and "url" in issue.field_name.lower()
        )
        if url_issues > 0:
            recommendations.append(f"🔗 Fix {url_issues} invalid URL formats")

        # Data freshness
        freshness_issues = sum(
            1
            for issues in all_issues.values()
            for issue in issues
            if issue.category == "data_freshness"
        )
        if freshness_issues > 0:
            recommendations.append(f"⏰ Update {freshness_issues} stale data records")

        # Overall quality score recommendations
        if quality_score < 70:
            recommendations.append(
                "📈 Overall data quality is below acceptable threshold - implement data validation pipeline"
            )
        elif quality_score < 85:
            recommendations.append(
                "🔧 Good data quality but room for improvement - focus on high-severity issues"
            )
        else:
            recommendations.append(
                "✅ Excellent data quality - maintain current standards"
            )

        return recommendations

    async def auto_fix_issues(
        self, issues: List[ValidationIssue], dry_run: bool = True
    ) -> Dict[str, int]:
        """Automatically fix certain types of validation issues"""
        logger.info(f"🔧 Auto-fixing validation issues (dry_run={dry_run})...")

        fix_counts = {"fixed": 0, "skipped": 0, "failed": 0}

        for issue in issues:
            try:
                if (
                    issue.category == "missing_country_association"
                    and issue.suggested_value
                ):
                    # Auto-fix missing country associations where we have suggestions
                    if not dry_run:
                        # Look up country ID
                        country_result = (
                            await supabase.table("countries")
                            .select("id")
                            .eq("name", issue.suggested_value)
                            .execute()
                        )
                        if country_result.data:
                            country_id = country_result.data[0]["id"]
                            # Update the record
                            await supabase.table(issue.table_name).update(
                                {"country_id": country_id}
                            ).eq("id", issue.record_id).execute()
                            fix_counts["fixed"] += 1
                        else:
                            fix_counts["failed"] += 1
                    else:
                        fix_counts["fixed"] += 1  # Would fix in real run

                elif issue.category == "invalid_pillar" and issue.suggested_value:
                    # Auto-fix invalid pillar names
                    if not dry_run:
                        await supabase.table(issue.table_name).update(
                            {"pillar": issue.suggested_value}
                        ).eq("id", issue.record_id).execute()
                        fix_counts["fixed"] += 1
                    else:
                        fix_counts["fixed"] += 1  # Would fix in real run

                else:
                    fix_counts["skipped"] += 1

            except Exception as e:
                logger.error(f"Failed to fix issue {issue.description}: {e}")
                fix_counts["failed"] += 1

        logger.info(
            f"Auto-fix results: {fix_counts['fixed']} fixed, {fix_counts['skipped']} skipped, {fix_counts['failed']} failed"
        )
        return fix_counts


async def run_data_quality_check():
    """Main entry point for data quality validation"""
    quality_manager = AHAIIDataQualityManager()
    issues = await quality_manager.run_comprehensive_quality_check()
    return issues


if __name__ == "__main__":
    issues = asyncio.run(run_data_quality_check())
    print(f"\n🔍 Data Quality Check Complete!")
    print(
        f"Total Issues Found: {sum(len(table_issues) for table_issues in issues.values())}"
    )
