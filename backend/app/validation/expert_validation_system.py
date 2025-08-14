"""
Expert Validation Framework for AHAII
Creates expert survey system for validating uncertain indicators
Implements consensus scoring for policy indicators
Cross-validates AHAII scores against expert country knowledge
Generates validation confidence scores and uncertainty bounds
"""

import json
import logging
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
import pandas as pd
import numpy as np
from statistics import mode, median

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ValidationStatus(Enum):
    """Expert validation status"""

    PENDING = "pending"
    IN_REVIEW = "in_review"
    VALIDATED = "validated"
    DISPUTED = "disputed"
    REJECTED = "rejected"


@dataclass
class ExpertProfile:
    """Expert validator profile"""

    expert_id: str
    name: str
    affiliation: str
    country_expertise: List[str]
    domain_expertise: List[
        str
    ]  # e.g., 'health_informatics', 'ai_policy', 'health_systems'
    years_experience: int
    validation_history: int
    reliability_score: float
    contact_email: str
    registration_date: str


@dataclass
class ValidationRequest:
    """Request for expert validation"""

    request_id: str
    country_code: str
    indicator_name: str
    indicator_type: str  # 'quantitative', 'policy', 'ecosystem'
    current_value: Any
    confidence_score: float
    evidence_provided: List[str]
    validation_question: str
    target_experts: List[str]
    priority_level: str  # 'high', 'medium', 'low'
    deadline: str
    status: ValidationStatus
    creation_date: str


@dataclass
class ExpertResponse:
    """Expert validation response"""

    response_id: str
    request_id: str
    expert_id: str
    validated_value: Any
    confidence_rating: float
    reasoning: str
    additional_evidence: List[str]
    certainty_level: str  # 'very_certain', 'certain', 'uncertain', 'very_uncertain'
    response_date: str


@dataclass
class ValidationConsensus:
    """Consensus result from expert validation"""

    request_id: str
    country_code: str
    indicator_name: str
    original_value: Any
    consensus_value: Any
    consensus_confidence: float
    expert_agreement: float
    response_count: int
    validation_method: str
    final_status: ValidationStatus
    consensus_date: str


class ExpertValidationSystem:
    """
    Expert validation framework for AHAII indicators
    """

    # Domain expertise categories
    DOMAIN_EXPERTISE = {
        "health_informatics": "Health informatics and medical AI",
        "ai_policy": "AI policy and governance",
        "health_systems": "Health systems and infrastructure",
        "digital_health": "Digital health and telemedicine",
        "biomedical_engineering": "Biomedical engineering and technology",
        "public_health": "Public health and epidemiology",
        "health_economics": "Health economics and financing",
    }

    # Validation thresholds
    CONSENSUS_THRESHOLDS = {
        "agreement_threshold": 0.75,  # 75% expert agreement required
        "minimum_responses": 3,  # Minimum expert responses needed
        "confidence_threshold": 0.7,  # Minimum consensus confidence
    }

    # Known expert network (would be expanded in real implementation)
    EXPERT_NETWORK = {
        "expert_001": {
            "name": "Dr. Sarah Johnson",
            "affiliation": "University of Cape Town - Health Informatics",
            "country_expertise": ["ZAF", "SSA_region"],
            "domain_expertise": ["health_informatics", "digital_health"],
            "years_experience": 12,
            "reliability_score": 0.92,
        },
        "expert_002": {
            "name": "Prof. Ahmed Hassan",
            "affiliation": "Cairo University - Biomedical Engineering",
            "country_expertise": ["EGY", "MENA_region"],
            "domain_expertise": ["biomedical_engineering", "medical_ai"],
            "years_experience": 15,
            "reliability_score": 0.89,
        },
        "expert_003": {
            "name": "Dr. Grace Wanjiku",
            "affiliation": "University of Nairobi - Public Health",
            "country_expertise": ["KEN", "EAC_region"],
            "domain_expertise": ["public_health", "health_systems"],
            "years_experience": 10,
            "reliability_score": 0.85,
        },
        "expert_004": {
            "name": "Dr. Kwame Asante",
            "affiliation": "Ghana Health Service - Digital Health",
            "country_expertise": ["GHA", "WAF_region"],
            "domain_expertise": ["digital_health", "ai_policy"],
            "years_experience": 8,
            "reliability_score": 0.88,
        },
        "expert_005": {
            "name": "Prof. Adaora Okonkwo",
            "affiliation": "University of Lagos - Health Economics",
            "country_expertise": ["NGA", "WAF_region"],
            "domain_expertise": ["health_economics", "health_systems"],
            "years_experience": 14,
            "reliability_score": 0.91,
        },
    }

    def __init__(self, validation_dir: str = "data/processed"):
        """
        Initialize expert validation system

        Args:
            validation_dir: Directory for validation data and results
        """
        self.validation_dir = Path(validation_dir)
        self.validation_dir.mkdir(parents=True, exist_ok=True)

        # Create validation subdirectory
        self.expert_cache_dir = self.validation_dir / "expert_validation"
        self.expert_cache_dir.mkdir(exist_ok=True)

        # Initialize validation database
        self._init_validation_db()

    def _init_validation_db(self):
        """Initialize expert validation database"""
        cache_db_path = self.expert_cache_dir / "validation_cache.db"

        with sqlite3.connect(cache_db_path) as conn:
            # Expert profiles table
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS expert_profiles (
                    expert_id TEXT PRIMARY KEY,
                    name TEXT,
                    affiliation TEXT,
                    country_expertise TEXT,
                    domain_expertise TEXT,
                    years_experience INTEGER,
                    validation_history INTEGER,
                    reliability_score REAL,
                    contact_email TEXT,
                    registration_date TEXT
                )
            """
            )

            # Validation requests table
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS validation_requests (
                    request_id TEXT PRIMARY KEY,
                    country_code TEXT,
                    indicator_name TEXT,
                    indicator_type TEXT,
                    current_value TEXT,
                    confidence_score REAL,
                    evidence_provided TEXT,
                    validation_question TEXT,
                    target_experts TEXT,
                    priority_level TEXT,
                    deadline TEXT,
                    status TEXT,
                    creation_date TEXT
                )
            """
            )

            # Expert responses table
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS expert_responses (
                    response_id TEXT PRIMARY KEY,
                    request_id TEXT,
                    expert_id TEXT,
                    validated_value TEXT,
                    confidence_rating REAL,
                    reasoning TEXT,
                    additional_evidence TEXT,
                    certainty_level TEXT,
                    response_date TEXT
                )
            """
            )

            # Consensus results table
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS validation_consensus (
                    request_id TEXT PRIMARY KEY,
                    country_code TEXT,
                    indicator_name TEXT,
                    original_value TEXT,
                    consensus_value TEXT,
                    consensus_confidence REAL,
                    expert_agreement REAL,
                    response_count INTEGER,
                    validation_method TEXT,
                    final_status TEXT,
                    consensus_date TEXT
                )
            """
            )

        self.cache_db_path = cache_db_path

    def create_validation_requests(
        self, policy_data: pd.DataFrame, ecosystem_metrics: pd.DataFrame
    ) -> List[ValidationRequest]:
        """
        Create validation requests for uncertain indicators

        Args:
            policy_data: DataFrame with policy indicators
            ecosystem_metrics: DataFrame with ecosystem metrics

        Returns:
            List of validation requests
        """
        logger.info("Creating expert validation requests for uncertain indicators")

        validation_requests = []

        # Identify policy indicators needing validation (low confidence)
        uncertain_policies = policy_data[policy_data["confidence_score"] < 0.7]

        for _, row in uncertain_policies.iterrows():
            request = self._create_policy_validation_request(row)
            validation_requests.append(request)

        # Identify ecosystem metrics needing validation
        uncertain_ecosystem = ecosystem_metrics[
            ecosystem_metrics["confidence_score"] < 0.8
        ]

        for _, row in uncertain_ecosystem.iterrows():
            request = self._create_ecosystem_validation_request(row)
            validation_requests.append(request)

        # Cache requests
        self._cache_validation_requests(validation_requests)

        logger.info(f"Created {len(validation_requests)} validation requests")
        return validation_requests

    def _create_policy_validation_request(
        self, policy_row: pd.Series
    ) -> ValidationRequest:
        """Create validation request for policy indicator"""
        request_id = f"policy_{policy_row['country_code']}_{policy_row['indicator_name']}_{int(datetime.now().timestamp())}"

        # Select appropriate experts
        target_experts = self._select_experts_for_indicator(
            policy_row["country_code"], "policy", policy_row["indicator_name"]
        )

        # Create validation question
        validation_question = f"""
        Please validate the existence of '{policy_row['indicator_name']}' in {policy_row['country_name']}.
        
        Current assessment: {'YES' if policy_row['indicator_value'] else 'NO'}
        Confidence: {policy_row['confidence_score']:.2f}
        
        Based on your expertise, does this country have this policy/framework in place?
        Please provide your assessment and supporting evidence.
        """

        request = ValidationRequest(
            request_id=request_id,
            country_code=policy_row["country_code"],
            indicator_name=policy_row["indicator_name"],
            indicator_type="policy",
            current_value=policy_row["indicator_value"],
            confidence_score=policy_row["confidence_score"],
            evidence_provided=policy_row.get("evidence_sources", []),
            validation_question=validation_question,
            target_experts=target_experts,
            priority_level="high" if policy_row["confidence_score"] < 0.5 else "medium",
            deadline=(datetime.now() + timedelta(days=14)).isoformat(),
            status=ValidationStatus.PENDING,
            creation_date=datetime.now().isoformat(),
        )

        return request

    def _create_ecosystem_validation_request(
        self, ecosystem_row: pd.Series
    ) -> ValidationRequest:
        """Create validation request for ecosystem metric"""
        request_id = f"ecosystem_{ecosystem_row['country_code']}_maturity_{int(datetime.now().timestamp())}"

        target_experts = self._select_experts_for_indicator(
            ecosystem_row["country_code"], "ecosystem", "ecosystem_maturity"
        )

        validation_question = f"""
        Please validate the health AI ecosystem maturity assessment for {ecosystem_row['country_name']}.
        
        Current assessment:
        - Total organizations: {ecosystem_row['total_organizations']}
        - Universities with programs: {ecosystem_row['universities_with_programs']}
        - Active startups: {ecosystem_row['active_startups']}
        - Ecosystem maturity score: {ecosystem_row['estimated_ecosystem_maturity']:.1f}/100
        
        Based on your knowledge of the health AI ecosystem in this country, 
        do these numbers seem reasonable? Are there major organizations or initiatives missing?
        """

        request = ValidationRequest(
            request_id=request_id,
            country_code=ecosystem_row["country_code"],
            indicator_name="ecosystem_maturity",
            indicator_type="ecosystem",
            current_value=ecosystem_row["estimated_ecosystem_maturity"],
            confidence_score=ecosystem_row["confidence_score"],
            evidence_provided=[],
            validation_question=validation_question,
            target_experts=target_experts,
            priority_level="medium",
            deadline=(datetime.now() + timedelta(days=21)).isoformat(),
            status=ValidationStatus.PENDING,
            creation_date=datetime.now().isoformat(),
        )

        return request

    def _select_experts_for_indicator(
        self, country_code: str, indicator_type: str, indicator_name: str
    ) -> List[str]:
        """Select appropriate experts for validation request"""
        suitable_experts = []

        for expert_id, expert_info in self.EXPERT_NETWORK.items():
            # Check country expertise
            country_match = country_code in expert_info["country_expertise"] or any(
                region in expert_info["country_expertise"]
                for region in ["SSA_region", "WAF_region", "EAC_region", "MENA_region"]
            )

            # Check domain expertise
            domain_match = False
            if indicator_type == "policy":
                domain_match = any(
                    domain in expert_info["domain_expertise"]
                    for domain in ["ai_policy", "digital_health", "health_systems"]
                )
            elif indicator_type == "ecosystem":
                domain_match = any(
                    domain in expert_info["domain_expertise"]
                    for domain in [
                        "health_informatics",
                        "digital_health",
                        "biomedical_engineering",
                    ]
                )

            # Check reliability
            reliability_match = expert_info["reliability_score"] > 0.8

            if country_match and domain_match and reliability_match:
                suitable_experts.append(expert_id)

        # Return top 3-5 experts
        return suitable_experts[:5]

    def simulate_expert_responses(
        self, validation_requests: List[ValidationRequest]
    ) -> List[ExpertResponse]:
        """
        Simulate expert responses for validation requests
        (In real implementation, this would be replaced by actual expert survey system)

        Args:
            validation_requests: List of validation requests

        Returns:
            List of simulated expert responses
        """
        logger.info("Simulating expert responses for validation")

        expert_responses = []

        for request in validation_requests:
            # Simulate 3-5 responses per request
            num_responses = np.random.randint(3, 6)

            for i in range(num_responses):
                if i < len(request.target_experts):
                    expert_id = request.target_experts[i]
                else:
                    expert_id = np.random.choice(list(self.EXPERT_NETWORK.keys()))

                response = self._simulate_expert_response(request, expert_id)
                expert_responses.append(response)

        # Cache responses
        self._cache_expert_responses(expert_responses)

        logger.info(f"Generated {len(expert_responses)} expert responses")
        return expert_responses

    def _simulate_expert_response(
        self, request: ValidationRequest, expert_id: str
    ) -> ExpertResponse:
        """Simulate individual expert response"""
        expert_info = self.EXPERT_NETWORK[expert_id]
        expert_reliability = expert_info["reliability_score"]

        response_id = f"response_{request.request_id}_{expert_id}_{int(datetime.now().timestamp())}"

        if request.indicator_type == "policy":
            # Simulate policy validation
            original_value = request.current_value

            # Expert tends to agree with high-confidence assessments
            if request.confidence_score > 0.8:
                validated_value = original_value
                confidence_rating = 0.85 + (expert_reliability - 0.8) * 0.15
            else:
                # Some variation for low-confidence assessments
                agreement_probability = 0.6 + (expert_reliability - 0.8) * 0.4
                validated_value = (
                    original_value
                    if np.random.random() < agreement_probability
                    else not original_value
                )
                confidence_rating = 0.7 + np.random.random() * 0.2

            reasoning = f"Based on my knowledge of {request.country_code} policy landscape and {expert_info['years_experience']} years of experience."

        else:  # ecosystem validation
            original_value = request.current_value

            # Expert assessment varies within reasonable bounds
            expert_adjustment = np.random.normal(0, 10) * (1 - expert_reliability)
            validated_value = max(0, min(100, original_value + expert_adjustment))
            confidence_rating = 0.75 + (expert_reliability - 0.8) * 0.25

            reasoning = f"Assessment based on knowledge of health AI ecosystem in {request.country_code}."

        # Determine certainty level
        if confidence_rating > 0.9:
            certainty_level = "very_certain"
        elif confidence_rating > 0.75:
            certainty_level = "certain"
        elif confidence_rating > 0.6:
            certainty_level = "uncertain"
        else:
            certainty_level = "very_uncertain"

        response = ExpertResponse(
            response_id=response_id,
            request_id=request.request_id,
            expert_id=expert_id,
            validated_value=validated_value,
            confidence_rating=confidence_rating,
            reasoning=reasoning,
            additional_evidence=[],
            certainty_level=certainty_level,
            response_date=datetime.now().isoformat(),
        )

        return response

    def calculate_consensus(
        self,
        validation_requests: List[ValidationRequest],
        expert_responses: List[ExpertResponse],
    ) -> List[ValidationConsensus]:
        """
        Calculate consensus from expert responses

        Args:
            validation_requests: List of validation requests
            expert_responses: List of expert responses

        Returns:
            List of validation consensus results
        """
        logger.info("Calculating expert consensus for validation requests")

        consensus_results = []

        # Group responses by request
        responses_by_request = {}
        for response in expert_responses:
            if response.request_id not in responses_by_request:
                responses_by_request[response.request_id] = []
            responses_by_request[response.request_id].append(response)

        for request in validation_requests:
            if request.request_id in responses_by_request:
                responses = responses_by_request[request.request_id]
                consensus = self._calculate_request_consensus(request, responses)
                consensus_results.append(consensus)

        # Cache consensus results
        self._cache_consensus_results(consensus_results)

        logger.info(f"Generated {len(consensus_results)} consensus results")
        return consensus_results

    def _calculate_request_consensus(
        self, request: ValidationRequest, responses: List[ExpertResponse]
    ) -> ValidationConsensus:
        """Calculate consensus for individual request"""
        if len(responses) < self.CONSENSUS_THRESHOLDS["minimum_responses"]:
            # Insufficient responses
            return ValidationConsensus(
                request_id=request.request_id,
                country_code=request.country_code,
                indicator_name=request.indicator_name,
                original_value=request.current_value,
                consensus_value=request.current_value,
                consensus_confidence=request.confidence_score,
                expert_agreement=0.0,
                response_count=len(responses),
                validation_method="insufficient_responses",
                final_status=ValidationStatus.PENDING,
                consensus_date=datetime.now().isoformat(),
            )

        # Calculate consensus based on indicator type
        if request.indicator_type == "policy":
            consensus_value, agreement = self._calculate_binary_consensus(responses)
        else:
            consensus_value, agreement = self._calculate_numeric_consensus(responses)

        # Calculate weighted confidence
        expert_weights = []
        confidence_scores = []

        for response in responses:
            expert_info = self.EXPERT_NETWORK.get(
                response.expert_id, {"reliability_score": 0.8}
            )
            weight = expert_info["reliability_score"]
            expert_weights.append(weight)
            confidence_scores.append(response.confidence_rating)

        total_weight = sum(expert_weights)
        consensus_confidence = (
            sum(c * w for c, w in zip(confidence_scores, expert_weights)) / total_weight
        )

        # Determine final status
        if (
            agreement >= self.CONSENSUS_THRESHOLDS["agreement_threshold"]
            and consensus_confidence
            >= self.CONSENSUS_THRESHOLDS["confidence_threshold"]
        ):
            final_status = ValidationStatus.VALIDATED
        elif agreement < 0.5:
            final_status = ValidationStatus.DISPUTED
        else:
            final_status = ValidationStatus.IN_REVIEW

        consensus = ValidationConsensus(
            request_id=request.request_id,
            country_code=request.country_code,
            indicator_name=request.indicator_name,
            original_value=request.current_value,
            consensus_value=consensus_value,
            consensus_confidence=round(consensus_confidence, 2),
            expert_agreement=round(agreement, 2),
            response_count=len(responses),
            validation_method="expert_consensus",
            final_status=final_status,
            consensus_date=datetime.now().isoformat(),
        )

        return consensus

    def _calculate_binary_consensus(
        self, responses: List[ExpertResponse]
    ) -> Tuple[bool, float]:
        """Calculate consensus for binary (policy) indicators"""
        values = [response.validated_value for response in responses]

        # Mode (most common value)
        try:
            consensus_value = mode(values)
            agreement = values.count(consensus_value) / len(values)
        except:
            # No clear mode, use majority
            true_count = sum(values)
            false_count = len(values) - true_count

            if true_count > false_count:
                consensus_value = True
                agreement = true_count / len(values)
            else:
                consensus_value = False
                agreement = false_count / len(values)

        return consensus_value, agreement

    def _calculate_numeric_consensus(
        self, responses: List[ExpertResponse]
    ) -> Tuple[float, float]:
        """Calculate consensus for numeric indicators"""
        values = [response.validated_value for response in responses]

        # Use median as consensus value
        consensus_value = median(values)

        # Calculate agreement as inverse of coefficient of variation
        mean_val = np.mean(values)
        std_val = np.std(values)

        if mean_val > 0:
            cv = std_val / mean_val
            agreement = max(0, 1 - cv)  # Higher agreement = lower variation
        else:
            agreement = 1.0 if std_val == 0 else 0.5

        return consensus_value, agreement

    def _cache_validation_requests(self, requests: List[ValidationRequest]):
        """Cache validation requests to database"""
        with sqlite3.connect(self.cache_db_path) as conn:
            for request in requests:
                evidence_json = json.dumps(request.evidence_provided)
                target_experts_json = json.dumps(request.target_experts)

                conn.execute(
                    """
                    INSERT INTO validation_requests 
                    (request_id, country_code, indicator_name, indicator_type, current_value,
                     confidence_score, evidence_provided, validation_question, target_experts,
                     priority_level, deadline, status, creation_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        request.request_id,
                        request.country_code,
                        request.indicator_name,
                        request.indicator_type,
                        str(request.current_value),
                        request.confidence_score,
                        evidence_json,
                        request.validation_question,
                        target_experts_json,
                        request.priority_level,
                        request.deadline,
                        request.status.value,
                        request.creation_date,
                    ),
                )

    def _cache_expert_responses(self, responses: List[ExpertResponse]):
        """Cache expert responses to database"""
        with sqlite3.connect(self.cache_db_path) as conn:
            for response in responses:
                evidence_json = json.dumps(response.additional_evidence)

                conn.execute(
                    """
                    INSERT INTO expert_responses 
                    (response_id, request_id, expert_id, validated_value, confidence_rating,
                     reasoning, additional_evidence, certainty_level, response_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        response.response_id,
                        response.request_id,
                        response.expert_id,
                        str(response.validated_value),
                        response.confidence_rating,
                        response.reasoning,
                        evidence_json,
                        response.certainty_level,
                        response.response_date,
                    ),
                )

    def _cache_consensus_results(self, consensus_results: List[ValidationConsensus]):
        """Cache consensus results to database"""
        with sqlite3.connect(self.cache_db_path) as conn:
            for consensus in consensus_results:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO validation_consensus 
                    (request_id, country_code, indicator_name, original_value, consensus_value,
                     consensus_confidence, expert_agreement, response_count, validation_method,
                     final_status, consensus_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        consensus.request_id,
                        consensus.country_code,
                        consensus.indicator_name,
                        str(consensus.original_value),
                        str(consensus.consensus_value),
                        consensus.consensus_confidence,
                        consensus.expert_agreement,
                        consensus.response_count,
                        consensus.validation_method,
                        consensus.final_status.value,
                        consensus.consensus_date,
                    ),
                )

    def generate_validation_report(
        self,
        validation_requests: List[ValidationRequest],
        expert_responses: List[ExpertResponse],
        consensus_results: List[ValidationConsensus],
    ) -> str:
        """
        Generate comprehensive expert validation report

        Args:
            validation_requests: List of validation requests
            expert_responses: List of expert responses
            consensus_results: List of consensus results

        Returns:
            Path to generated report
        """
        # Calculate summary statistics
        total_requests = len(validation_requests)
        total_responses = len(expert_responses)
        validated_indicators = len(
            [
                c
                for c in consensus_results
                if c.final_status == ValidationStatus.VALIDATED
            ]
        )
        disputed_indicators = len(
            [
                c
                for c in consensus_results
                if c.final_status == ValidationStatus.DISPUTED
            ]
        )

        # Average expert agreement
        avg_agreement = (
            np.mean([c.expert_agreement for c in consensus_results])
            if consensus_results
            else 0
        )

        # Response rate by expert
        expert_response_counts = {}
        for response in expert_responses:
            if response.expert_id not in expert_response_counts:
                expert_response_counts[response.expert_id] = 0
            expert_response_counts[response.expert_id] += 1

        report = {
            "metadata": {
                "report_date": datetime.now().isoformat(),
                "validation_period": f"{datetime.now().strftime('%Y-%m-%d')}",
                "expert_network_size": len(self.EXPERT_NETWORK),
                "validation_methodology": "consensus_based_expert_validation",
            },
            "summary_statistics": {
                "total_validation_requests": total_requests,
                "total_expert_responses": total_responses,
                "average_responses_per_request": (
                    total_responses / total_requests if total_requests > 0 else 0
                ),
                "validated_indicators": validated_indicators,
                "disputed_indicators": disputed_indicators,
                "average_expert_agreement": round(avg_agreement, 2),
                "validation_completion_rate": (
                    len(consensus_results) / total_requests if total_requests > 0 else 0
                ),
            },
            "expert_participation": {
                "active_experts": len(expert_response_counts),
                "responses_by_expert": expert_response_counts,
                "expert_network": {
                    eid: info["name"] + " - " + info["affiliation"]
                    for eid, info in self.EXPERT_NETWORK.items()
                },
            },
            "validation_results": {
                "consensus_outcomes": [asdict(c) for c in consensus_results],
                "high_confidence_validations": [
                    asdict(c)
                    for c in consensus_results
                    if c.consensus_confidence > 0.8
                    and c.final_status == ValidationStatus.VALIDATED
                ],
                "disputed_indicators": [
                    asdict(c)
                    for c in consensus_results
                    if c.final_status == ValidationStatus.DISPUTED
                ],
            },
            "quality_assurance": {
                "consensus_thresholds": self.CONSENSUS_THRESHOLDS,
                "expert_reliability_scores": {
                    eid: info["reliability_score"]
                    for eid, info in self.EXPERT_NETWORK.items()
                },
                "validation_confidence_distribution": {
                    "high_confidence": len(
                        [c for c in consensus_results if c.consensus_confidence > 0.8]
                    ),
                    "medium_confidence": len(
                        [
                            c
                            for c in consensus_results
                            if 0.6 <= c.consensus_confidence <= 0.8
                        ]
                    ),
                    "low_confidence": len(
                        [c for c in consensus_results if c.consensus_confidence < 0.6]
                    ),
                },
            },
            "recommendations": [
                "Continue expert validation for disputed indicators with additional evidence",
                "Expand expert network to include more regional specialists",
                "Implement systematic evidence collection for low-confidence indicators",
                "Establish quarterly expert review cycles for ongoing validation",
                "Create expert feedback mechanism for methodology improvements",
            ],
        }

        # Save report
        report_path = (
            self.expert_cache_dir
            / f"expert_validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)

        logger.info(f"Expert validation report saved to: {report_path}")
        return str(report_path)


def main():
    """Main function for testing expert validation system"""
    from src.data_collection.policy_indicator_collector import PolicyIndicatorCollector
    from src.data_collection.health_ai_ecosystem_mapper import HealthAIEcosystemMapper

    # Collect data for validation
    policy_collector = PolicyIndicatorCollector()
    policy_data = policy_collector.collect_all_countries()

    ecosystem_mapper = HealthAIEcosystemMapper()
    _, ecosystem_metrics = ecosystem_mapper.map_all_countries()

    # Initialize validation system
    validation_system = ExpertValidationSystem()

    # Create validation requests
    validation_requests = validation_system.create_validation_requests(
        policy_data, ecosystem_metrics
    )

    # Simulate expert responses
    expert_responses = validation_system.simulate_expert_responses(validation_requests)

    # Calculate consensus
    consensus_results = validation_system.calculate_consensus(
        validation_requests, expert_responses
    )

    # Generate validation report
    report_path = validation_system.generate_validation_report(
        validation_requests, expert_responses, consensus_results
    )

    # Print summary
    print("\n=== Expert Validation Summary ===")
    print(f"Validation requests created: {len(validation_requests)}")
    print(f"Expert responses received: {len(expert_responses)}")
    print(f"Consensus achieved: {len(consensus_results)}")

    validated_count = len(
        [c for c in consensus_results if c.final_status == ValidationStatus.VALIDATED]
    )
    disputed_count = len(
        [c for c in consensus_results if c.final_status == ValidationStatus.DISPUTED]
    )

    print(f"Validated indicators: {validated_count}")
    print(f"Disputed indicators: {disputed_count}")

    if consensus_results:
        avg_agreement = np.mean([c.expert_agreement for c in consensus_results])
        print(f"Average expert agreement: {avg_agreement:.2f}")

    print(f"\nDetailed validation report saved to: {report_path}")


if __name__ == "__main__":
    main()
