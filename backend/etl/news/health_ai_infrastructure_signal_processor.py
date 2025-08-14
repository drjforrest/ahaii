"""
Health AI Infrastructure Signal Processor for AHAII
Classifies news articles by infrastructure pillar impact and significance
"""

import re
from typing import Dict, Any, List, Optional


class HealthAIInfrastructureSignalProcessor:
    """Classify news articles by health AI infrastructure pillar impact"""

    def __init__(self):
        self.infrastructure_keywords = {
            "human_capital": [
                "medical training",
                "clinical education",
                "health informatics curriculum",
                "ai medical training",
                "clinical ai literacy",
                "medical ai workforce",
                "health data science programs",
                "clinical decision support training",
                "biomedical informatics education",
                "health ai capacity building",
                "medical informatics certification",
                "clinical ai competency",
                "health ai skills development",
                "medical ai education program",
            ],
            "physical_infrastructure": [
                "hospital emr implementation",
                "medical imaging systems deployment",
                "healthcare data center",
                "clinical data network",
                "telemedicine platform",
                "pacs implementation",
                "health information system",
                "hospital it infrastructure",
                "clinical decision support system",
                "electronic health record",
                "medical device connectivity",
                "healthcare cloud infrastructure",
                "hospital digital transformation",
                "clinical data integration platform",
                "health information exchange",
                "medical iot deployment",
            ],
            "regulatory": [
                "medical ai regulation",
                "health ai governance framework",
                "clinical ai validation",
                "medical device ai approval",
                "fda ai guidance",
                "health data privacy regulation",
                "clinical trial ai oversight",
                "medical ai safety standard",
                "health ai ethics committee",
                "medical device regulation",
                "clinical ai certification",
                "health ai compliance framework",
                "medical ai audit requirement",
                "clinical ai quality assurance",
                "health ai regulatory pathway",
            ],
            "economic": [
                "health ai funding",
                "medical ai investment",
                "healthtech venture capital",
                "digital health funding round",
                "clinical ai market analysis",
                "health ai reimbursement",
                "medical ai cost effectiveness",
                "healthtech ipo",
                "digital health merger",
                "clinical ai roi",
                "health ai market valuation",
                "medical ai budget allocation",
                "healthtech acquisition",
                "digital health economic impact",
            ],
        }

        self.organization_patterns = [
            r"(?:ministry|department)\s+of\s+health",
            r"world health organization|who",
            r"africa\s+cdc|african\s+union",
            r"(?:hospital|medical\s+center|health\s+system)",
            r"(?:university|college)\s+(?:of\s+)?medicine",
            r"medical\s+association",
            r"health\s+(?:ministry|department|agency)",
            r"clinical\s+research\s+(?:center|institute)",
            r"medical\s+(?:school|college)",
            r"health\s+(?:insurance|fund|plan)",
        ]

        self.funding_indicators = [
            r"\$\d+(?:\.\d+)?\s*(?:million|billion|thousand|k)\b",
            r"funding\s+(?:of|worth)\s+\$?\d+(?:\.\d+)?\s*(?:million|billion|k)",
            r"investment\s+(?:of|worth)\s+\$?\d+(?:\.\d+)?\s*(?:million|billion|k)",
            r"raised\s+\$?\d+(?:\.\d+)?\s*(?:million|billion|k)",
            r"grant\s+(?:of|worth)\s+\$?\d+(?:\.\d+)?\s*(?:million|billion|k)",
            r"budget\s+(?:of|allocation)\s+\$?\d+(?:\.\d+)?\s*(?:million|billion|k)",
        ]

        self.regulatory_signals = [
            r"approved\s+(?:by|for)\s+(?:fda|regulatory|authority)",
            r"regulatory\s+(?:approval|clearance|authorization)",
            r"clinical\s+trial\s+(?:approval|authorization)",
            r"medical\s+device\s+(?:approval|clearance|registration)",
            r"health\s+(?:policy|regulation|guideline)\s+(?:announced|published|updated)",
            r"compliance\s+with\s+(?:health|medical|data)\s+(?:regulation|standard)",
            r"ethical\s+(?:approval|clearance|review)",
            r"quality\s+assurance\s+(?:standard|certification|audit)",
        ]

    def classify_infrastructure_signal(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """Classify news article by infrastructure pillar impact"""
        title = article.get("title", "").lower()
        summary = article.get("summary", "").lower()
        content = article.get("content", "").lower()

        full_text = f"{title} {summary} {content}"

        classification = {
            "human_capital": False,
            "physical_infrastructure": False,
            "regulatory": False,
            "economic": False,
            "significance": "low",
            "confidence_score": 0.0,
            "pillar_scores": {},
            "infrastructure_indicators": [],
            "health_organizations": [],
            "regulatory_signals": [],
            "funding_mentions": [],
        }

        # Analyze each pillar
        pillar_scores = {}
        for pillar, keywords in self.infrastructure_keywords.items():
            score = self._calculate_pillar_score(full_text, keywords)
            pillar_scores[pillar] = score
            if score > 0.3:  # Threshold for pillar activation
                classification[pillar] = True

        classification["pillar_scores"] = pillar_scores

        # Extract infrastructure indicators
        classification["infrastructure_indicators"] = (
            self._extract_infrastructure_indicators(full_text)
        )

        # Extract health organizations
        classification["health_organizations"] = self._extract_health_organizations(
            full_text
        )

        # Extract regulatory signals
        classification["regulatory_signals"] = self._extract_regulatory_signals(
            full_text
        )

        # Extract funding mentions
        classification["funding_mentions"] = self._extract_funding_mentions(full_text)

        # Calculate overall significance
        active_pillars = sum(
            classification[pillar]
            for pillar in [
                "human_capital",
                "physical_infrastructure",
                "regulatory",
                "economic",
            ]
        )
        max_pillar_score = max(pillar_scores.values()) if pillar_scores else 0

        if active_pillars >= 3 or max_pillar_score > 0.7:
            classification["significance"] = "high"
        elif active_pillars >= 2 or max_pillar_score > 0.5:
            classification["significance"] = "medium"
        else:
            classification["significance"] = "low"

        # Calculate confidence score
        classification["confidence_score"] = self._calculate_confidence_score(
            pillar_scores,
            classification["infrastructure_indicators"],
            classification["regulatory_signals"],
            classification["funding_mentions"],
        )

        return classification

    def _calculate_pillar_score(self, text: str, keywords: List[str]) -> float:
        """Calculate score for a specific infrastructure pillar"""
        score = 0.0
        text_length = len(text.split())

        for keyword in keywords:
            # Count exact phrase matches
            phrase_count = len(
                re.findall(rf"\b{re.escape(keyword)}\b", text, re.IGNORECASE)
            )
            if phrase_count > 0:
                # Weight longer, more specific phrases higher
                phrase_weight = min(len(keyword.split()) * 0.1, 0.5)
                score += phrase_count * phrase_weight

        # Normalize by text length
        if text_length > 0:
            score = score / (text_length / 100)  # per 100 words

        return min(score, 1.0)

    def _extract_infrastructure_indicators(self, text: str) -> List[Dict[str, Any]]:
        """Extract specific infrastructure indicators from text"""
        indicators = []

        # Quantitative indicators patterns
        patterns = {
            "emr_adoption_rate": r"(\d+(?:\.\d+)?)%?\s*(?:of\s+)?(?:hospitals|facilities|clinics)\s*(?:have|use|implemented|adopted)\s*(?:emr|electronic medical record|electronic health record)",
            "ai_training_programs": r"(\d+)\s*(?:new\s+)?(?:ai|artificial intelligence)\s*(?:training|certification|education)\s*programs?",
            "telemedicine_capability": r"(\d+(?:\.\d+)?)%?\s*(?:of\s+)?(?:hospitals|facilities)\s*(?:offer|provide|support)\s*(?:telemedicine|telehealth)",
            "health_data_centers": r"(\d+)\s*(?:new\s+)?(?:health|medical)\s*(?:data\s+centers?|cloud\s+facilities)",
            "medical_devices_connected": r"(\d+(?:,\d{3})*)\s*(?:medical\s+devices?|iot\s+devices?)\s*(?:connected|networked)",
            "clinical_ai_implementations": r"(\d+)\s*(?:clinical\s+ai|medical\s+ai|health\s+ai)\s*(?:implementations?|deployments?|systems?)",
            "health_ai_budget": r"\$(\d+(?:\.\d+)?)\s*(?:million|billion|thousand|k)\s*(?:allocated|budgeted|invested)\s*(?:for|in|on)\s*(?:health\s+ai|medical\s+ai|digital\s+health)",
            "medical_staff_trained": r"(\d+(?:,\d{3})*)\s*(?:medical\s+staff|healthcare\s+workers|clinicians)\s*(?:trained|certified)\s*(?:in|on)\s*(?:ai|digital\s+health|health\s+informatics)",
        }

        for indicator_type, pattern in patterns.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    value = match.group(1).replace(",", "")
                    if "%" in match.group(0):
                        value_type = "percentage"
                    elif "$" in match.group(0):
                        value_type = "currency"
                    else:
                        value_type = "count"

                    indicators.append(
                        {
                            "indicator_name": indicator_type,
                            "value": float(value),
                            "value_type": value_type,
                            "context": text[
                                max(0, match.start() - 30) : match.end() + 30
                            ],
                            "confidence": 0.8,
                        }
                    )
                except (ValueError, IndexError):
                    continue

        return indicators[:10]  # Limit to top 10

    def _extract_health_organizations(self, text: str) -> List[str]:
        """Extract health organization mentions"""
        organizations = set()

        for pattern in self.organization_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                org_name = match.group(0).strip()
                if len(org_name) > 5:
                    organizations.add(org_name.title())

        return list(organizations)[:15]

    def _extract_regulatory_signals(self, text: str) -> List[Dict[str, Any]]:
        """Extract regulatory signals and approvals"""
        signals = []

        for pattern in self.regulatory_signals:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                signals.append(
                    {
                        "signal_type": "regulatory_action",
                        "description": match.group(0),
                        "context": text[max(0, match.start() - 40) : match.end() + 40],
                        "confidence": 0.7,
                    }
                )

        return signals[:8]

    def _extract_funding_mentions(self, text: str) -> List[Dict[str, Any]]:
        """Extract funding and investment mentions"""
        funding_mentions = []

        for pattern in self.funding_indicators:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    # Extract amount and convert to standard format
                    amount_match = re.search(r"(\d+(?:\.\d+)?)", match.group(0))
                    if amount_match:
                        amount = float(amount_match.group(1))

                        # Determine multiplier
                        text_match = match.group(0).lower()
                        if "billion" in text_match or "b" == text_match[-1]:
                            amount *= 1_000_000_000
                        elif "million" in text_match or "m" == text_match[-1]:
                            amount *= 1_000_000
                        elif "thousand" in text_match or "k" in text_match:
                            amount *= 1_000

                        funding_mentions.append(
                            {
                                "amount": amount,
                                "formatted_amount": match.group(0),
                                "context": text[
                                    max(0, match.start() - 50) : match.end() + 50
                                ],
                                "confidence": 0.8,
                            }
                        )
                except (ValueError, IndexError):
                    continue

        return funding_mentions[:5]

    def _calculate_confidence_score(
        self,
        pillar_scores: Dict[str, float],
        indicators: List[Dict],
        regulatory_signals: List[Dict],
        funding_mentions: List[Dict],
    ) -> float:
        """Calculate overall confidence score for the classification"""

        # Base score from pillar analysis
        max_pillar_score = max(pillar_scores.values()) if pillar_scores else 0
        avg_pillar_score = (
            sum(pillar_scores.values()) / len(pillar_scores) if pillar_scores else 0
        )

        confidence = max_pillar_score * 0.4 + avg_pillar_score * 0.3

        # Boost confidence with specific indicators
        if indicators:
            confidence += min(len(indicators) * 0.05, 0.2)

        if regulatory_signals:
            confidence += min(len(regulatory_signals) * 0.03, 0.1)

        if funding_mentions:
            confidence += min(len(funding_mentions) * 0.04, 0.1)

        return min(confidence, 1.0)

    def get_primary_pillar(self, classification: Dict[str, Any]) -> Optional[str]:
        """Determine the primary infrastructure pillar for this article"""
        pillar_scores = classification.get("pillar_scores", {})
        if not pillar_scores:
            return None

        max_pillar = max(pillar_scores, key=pillar_scores.get)
        if pillar_scores[max_pillar] > 0.3:
            return max_pillar

        return None

    def is_significant_infrastructure_signal(
        self, classification: Dict[str, Any]
    ) -> bool:
        """Determine if this article represents a significant infrastructure signal"""
        significance = classification.get("significance", "low")
        confidence = classification.get("confidence_score", 0.0)

        return significance in ["high", "medium"] and confidence > 0.5


# Example usage and testing
if __name__ == "__main__":
    processor = HealthAIInfrastructureSignalProcessor()

    # Test article
    test_article = {
        "title": "South African Hospital Implements AI-Powered EMR System",
        "summary": "Major teaching hospital in Cape Town announces deployment of AI-enhanced electronic medical records system, training 500 medical staff on new digital health platform.",
        "content": "The University of Cape Town teaching hospital has successfully implemented a $2.5 million AI-powered electronic medical records system. The deployment includes training 500 medical staff members on the new digital health platform. The system received regulatory approval from the South African Health Products Regulatory Authority and will improve clinical decision support for doctors treating patients across multiple departments.",
    }

    classification = processor.classify_infrastructure_signal(test_article)

    print("Classification Results:")
    print(f"Primary Pillar: {processor.get_primary_pillar(classification)}")
    print(f"Significance: {classification['significance']}")
    print(f"Confidence: {classification['confidence_score']:.2f}")
    print(
        f"Active Pillars: {[k for k, v in classification.items() if k in ['human_capital', 'physical_infrastructure', 'regulatory', 'economic'] and v]}"
    )
    print(
        f"Infrastructure Indicators: {len(classification['infrastructure_indicators'])}"
    )
    print(f"Health Organizations: {classification['health_organizations']}")
    print(f"Funding Mentions: {len(classification['funding_mentions'])}")
