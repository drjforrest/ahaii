#!/usr/bin/env python3
"""
AHAII Health AI Infrastructure Snowball Sampler
Enhanced citation discovery and reference extraction for health AI infrastructure intelligence
"""

import asyncio
import re
import json
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass
from enum import Enum

import aiohttp
from bs4 import BeautifulSoup
from loguru import logger

from services.database_service import DatabaseService
from config.database import supabase


class SamplingStrategy(Enum):
    """Different snowball sampling strategies"""

    BREADTH_FIRST = "breadth_first"
    DEPTH_FIRST = "depth_first"
    PRIORITY_BASED = "priority_based"
    HEALTH_AI_FOCUSED = "health_ai_focused"  # AHAII-specific


class CitationType(Enum):
    """Types of citations for health AI infrastructure"""

    ACADEMIC_PAPER = "academic_paper"
    HEALTH_AI_REPORT = "health_ai_report"
    POLICY_DOCUMENT = "policy_document"
    NEWS_ARTICLE = "news_article"
    CLINICAL_STUDY = "clinical_study"
    REGULATORY_FILING = "regulatory_filing"
    COMPANY_WEBSITE = "company_website"
    GITHUB_REPO = "github_repo"
    UNKNOWN = "unknown"


@dataclass
class SamplingConfig:
    """Configuration for health AI snowball sampling"""

    max_depth: int = 4
    max_citations_per_batch: int = 25
    min_confidence_threshold: float = 0.6
    strategy: SamplingStrategy = SamplingStrategy.HEALTH_AI_FOCUSED

    # Rate limiting for respectful scraping
    delay_between_requests: float = 3.0
    max_requests_per_minute: int = 15

    # Health AI quality filters
    require_health_relevance: bool = True
    require_ai_relevance: bool = True
    require_african_connection: bool = True
    min_health_ai_score: float = 0.4

    # Government document handling (IMPORTANT)
    government_domains_allowed: Set[str] = None
    respect_robots_txt: bool = True
    max_government_docs_per_country: int = 3

    def __post_init__(self):
        if self.government_domains_allowed is None:
            # Conservative list of clearly public government domains
            self.government_domains_allowed = {
                "who.int",  # WHO is international
                "africa.who.int",  # WHO Africa regional office
                "afro.who.int",  # WHO Africa
                "data.gov.ng",  # Nigeria open data (public)
                "data.gov.za",  # South Africa open data (public)
                "opendata.gov.rw",  # Rwanda open data (public)
                "data.gov.ke",  # Kenya open data (public)
                "data.gov.gh",  # Ghana open data (public)
                # Add more as needed, but be conservative
            }


@dataclass
class HealthAICitation:
    """Health AI infrastructure citation with enhanced metadata"""

    id: str
    title: str
    url: Optional[str]
    citation_text: str
    confidence_score: float
    citation_type: CitationType
    discovered_at: datetime
    source_document_id: str

    # Health AI specific fields
    health_ai_relevance_score: float = 0.0
    african_relevance_score: float = 0.0
    infrastructure_pillar: Optional[str] = (
        None  # human_capital, physical, regulatory, economic
    )
    mentioned_countries: List[str] = None
    mentioned_organizations: List[str] = None
    regulatory_signals: List[str] = None
    funding_mentions: List[Dict[str, Any]] = None

    # Reference extraction
    reference_links: List[str] = None
    citation_count: int = 0

    def __post_init__(self):
        if self.mentioned_countries is None:
            self.mentioned_countries = []
        if self.mentioned_organizations is None:
            self.mentioned_organizations = []
        if self.regulatory_signals is None:
            self.regulatory_signals = []
        if self.funding_mentions is None:
            self.funding_mentions = []
        if self.reference_links is None:
            self.reference_links = []


class HealthAISnowballSampler:
    """Enhanced snowball sampler for health AI infrastructure intelligence"""

    def __init__(self, config: SamplingConfig = None):
        self.config = config or SamplingConfig()
        self.db_service = DatabaseService()
        self.processed_urls: Set[str] = set()
        self.session_id = (
            f"health_ai_snowball_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )

        # Health AI patterns for extraction
        self.health_ai_patterns = {
            "health_terms": [
                "health",
                "healthcare",
                "medical",
                "clinical",
                "hospital",
                "patient",
                "diagnosis",
                "treatment",
                "therapy",
                "pharmaceutical",
                "biomedical",
                "epidemiology",
                "public health",
                "telemedicine",
                "telehealth",
            ],
            "ai_terms": [
                "artificial intelligence",
                "machine learning",
                "deep learning",
                "ai",
                "ml",
                "neural network",
                "computer vision",
                "nlp",
                "natural language",
                "predictive analytics",
                "algorithm",
                "automated",
                "intelligent",
            ],
            "infrastructure_terms": [
                "infrastructure",
                "system",
                "platform",
                "implementation",
                "deployment",
                "capacity",
                "framework",
                "architecture",
                "ecosystem",
                "network",
            ],
        }

        # African countries for relevance scoring
        self.african_countries = {
            "nigeria",
            "kenya",
            "south africa",
            "ghana",
            "egypt",
            "morocco",
            "rwanda",
            "uganda",
            "tanzania",
            "ethiopia",
            "senegal",
            "tunisia",
            "algeria",
            "cameroon",
            "ivory coast",
            "zambia",
            "zimbabwe",
            "botswana",
            "namibia",
            "malawi",
            "mozambique",
            "madagascar",
            "angola",
            "sudan",
            "mali",
            "burkina faso",
            "niger",
            "chad",
            "libya",
            "mauritania",
            "somalia",
            "eritrea",
            "djibouti",
            "gambia",
            "guinea",
            "sierra leone",
            "liberia",
            "togo",
            "benin",
            "gabon",
            "equatorial guinea",
            "central african republic",
            "democratic republic congo",
            "republic of congo",
            "lesotho",
            "swaziland",
            "comoros",
            "seychelles",
            "mauritius",
            "cape verde",
            "sao tome and principe",
        }

    async def run_sampling_session(self) -> Dict[str, Any]:
        """Run a complete health AI snowball sampling session"""

        logger.info(f"🔬 Starting Health AI Snowball Sampling: {self.session_id}")

        session_stats = {
            "session_id": self.session_id,
            "start_time": datetime.now(),
            "citations_processed": 0,
            "health_ai_discoveries": 0,
            "reference_links_extracted": 0,
            "government_docs_processed": 0,
            "african_relevant_findings": 0,
            "failed_extractions": 0,
            "depth_reached": 0,
            "discoveries_by_depth": {},
            "quality_scores": [],
            "pillar_distribution": {
                "human_capital": 0,
                "physical_infrastructure": 0,
                "regulatory": 0,
                "economic": 0,
            },
        }

        try:
            # Get initial seed from infrastructure intelligence
            discovery_queue = await self._create_health_ai_discovery_queue()

            if not discovery_queue:
                logger.info("No health AI citations available for snowball sampling")
                return session_stats

            logger.info(f"📊 Initial discovery queue: {len(discovery_queue)} citations")

            # Process by depth with health AI focus
            current_depth = 0
            current_queue = discovery_queue

            while current_queue and current_depth < self.config.max_depth:
                logger.info(
                    f"🔍 Processing depth {current_depth} with {len(current_queue)} items"
                )

                depth_results = await self._process_depth_level(
                    current_queue, current_depth
                )

                # Update session stats
                session_stats["citations_processed"] += depth_results["processed_count"]
                session_stats["health_ai_discoveries"] += depth_results[
                    "discoveries_count"
                ]
                session_stats["reference_links_extracted"] += depth_results[
                    "references_extracted"
                ]
                session_stats["government_docs_processed"] += depth_results[
                    "government_docs_count"
                ]
                session_stats["african_relevant_findings"] += depth_results[
                    "african_relevant_count"
                ]
                session_stats["failed_extractions"] += depth_results["failed_count"]
                session_stats["discoveries_by_depth"][current_depth] = depth_results[
                    "discoveries_count"
                ]
                session_stats["quality_scores"].extend(depth_results["quality_scores"])

                # Update pillar distribution
                for pillar, count in depth_results.get("pillar_counts", {}).items():
                    session_stats["pillar_distribution"][pillar] += count

                # Prepare next depth queue
                current_queue = depth_results["next_depth_queue"]
                current_depth += 1
                session_stats["depth_reached"] = current_depth

                # Rate limiting between depths
                if current_queue:
                    await asyncio.sleep(self.config.delay_between_requests * 2)

            # Calculate final statistics
            session_stats["end_time"] = datetime.now()
            session_stats["duration_seconds"] = (
                session_stats["end_time"] - session_stats["start_time"]
            ).total_seconds()
            session_stats["average_quality"] = (
                sum(session_stats["quality_scores"])
                / len(session_stats["quality_scores"])
                if session_stats["quality_scores"]
                else 0
            )

            # Store session results
            await self._store_session_results(session_stats)

            logger.info(
                f"🎉 Snowball sampling completed: {session_stats['health_ai_discoveries']} new health AI discoveries"
            )

        except Exception as e:
            logger.error(f"❌ Snowball sampling session failed: {e}")
            session_stats["error"] = str(e)
            session_stats["end_time"] = datetime.now()

        return session_stats

    async def _create_health_ai_discovery_queue(self) -> List[Dict[str, Any]]:
        """Create discovery queue from existing intelligence and citations"""

        discovery_queue = []

        # Get recent infrastructure intelligence with URLs
        intelligence_result = (
            await supabase.table("infrastructure_intelligence")
            .select("*")
            .not_("source_url", "is", "null")
            .gte("created_at", (datetime.now() - timedelta(days=30)).isoformat())
            .order("created_at", desc=True)
            .limit(50)
            .execute()
        )

        for record in intelligence_result.data or []:
            source_url = record.get("source_url")
            if source_url and source_url not in self.processed_urls:

                # Calculate priority based on health AI relevance
                key_findings = record.get("key_findings", {})
                health_ai_score = key_findings.get("health_ai_relevance_score", 0)
                african_score = key_findings.get("african_relevance_score", 0)

                priority_score = health_ai_score * 0.6 + african_score * 0.4

                if priority_score >= self.config.min_confidence_threshold:
                    discovery_item = {
                        "citation_id": record["id"],
                        "title": record["report_title"],
                        "url": source_url,
                        "priority_score": priority_score,
                        "citation_type": "infrastructure_intelligence",
                        "discovery_method": "existing_intelligence",
                        "health_ai_score": health_ai_score,
                        "african_score": african_score,
                    }
                    discovery_queue.append(discovery_item)

        # Sort by priority score
        discovery_queue.sort(key=lambda x: x["priority_score"], reverse=True)

        logger.info(
            f"📋 Created health AI discovery queue with {len(discovery_queue)} high-quality items"
        )
        return discovery_queue[: self.config.max_citations_per_batch]

    async def _process_depth_level(
        self, queue: List[Dict[str, Any]], depth: int
    ) -> Dict[str, Any]:
        """Process all citations at a specific depth level"""

        results = {
            "processed_count": 0,
            "discoveries_count": 0,
            "references_extracted": 0,
            "government_docs_count": 0,
            "african_relevant_count": 0,
            "failed_count": 0,
            "quality_scores": [],
            "next_depth_queue": [],
            "pillar_counts": {
                "human_capital": 0,
                "physical_infrastructure": 0,
                "regulatory": 0,
                "economic": 0,
            },
        }

        for citation_item in queue:
            try:
                citation_results = await self._process_single_citation(
                    citation_item, depth
                )

                results["processed_count"] += 1

                if citation_results["success"]:
                    results["discoveries_count"] += citation_results[
                        "discoveries_count"
                    ]
                    results["references_extracted"] += citation_results[
                        "references_extracted"
                    ]
                    results["government_docs_count"] += citation_results[
                        "government_docs_count"
                    ]
                    results["african_relevant_count"] += citation_results[
                        "african_relevant_count"
                    ]
                    results["quality_scores"].append(
                        citation_results["average_quality"]
                    )

                    # Update pillar counts
                    for pillar in citation_results.get("pillars_found", []):
                        if pillar in results["pillar_counts"]:
                            results["pillar_counts"][pillar] += 1

                    # Add high-quality references to next depth queue
                    for ref_citation in citation_results["reference_citations"]:
                        if self._should_include_in_next_depth(ref_citation):
                            results["next_depth_queue"].append(ref_citation)
                else:
                    results["failed_count"] += 1

                # Respectful rate limiting
                await asyncio.sleep(self.config.delay_between_requests)

            except Exception as e:
                logger.error(
                    f"Failed to process citation {citation_item.get('citation_id')}: {e}"
                )
                results["failed_count"] += 1

        return results

    async def _process_single_citation(
        self, citation_item: Dict[str, Any], depth: int
    ) -> Dict[str, Any]:
        """Process a single citation for health AI snowball sampling"""

        result = {
            "success": False,
            "discoveries_count": 0,
            "references_extracted": 0,
            "government_docs_count": 0,
            "african_relevant_count": 0,
            "average_quality": 0.0,
            "reference_citations": [],
            "pillars_found": [],
        }

        citation_url = citation_item.get("url")
        citation_id = citation_item.get("citation_id")

        if not citation_url or citation_url in self.processed_urls:
            return result

        # Check if this is a government domain and apply restrictions
        if self._is_government_domain(citation_url):
            if not self._should_process_government_doc(citation_url):
                logger.info(
                    f"⚠️ Skipping government document (policy restrictions): {citation_url}"
                )
                return result
            else:
                result["government_docs_count"] = 1
                logger.info(
                    f"🏛️ Processing approved government document: {citation_url}"
                )

        try:
            self.processed_urls.add(citation_url)

            # Fetch content with respect to robots.txt
            content = await self._fetch_citation_content_respectfully(citation_url)

            if content:
                # Extract health AI relevant information
                health_ai_citation = await self._extract_health_ai_info(
                    content, citation_item, depth
                )

                if (
                    health_ai_citation
                    and health_ai_citation.confidence_score
                    >= self.config.min_confidence_threshold
                ):
                    # Extract reference links (the key feature!)
                    reference_links = await self._extract_reference_links(
                        content, citation_url
                    )
                    health_ai_citation.reference_links = reference_links
                    result["references_extracted"] = len(reference_links)

                    # Store the enhanced citation
                    stored_citation = await self._store_health_ai_citation(
                        health_ai_citation
                    )

                    if stored_citation:
                        result["success"] = True
                        result["discoveries_count"] = 1
                        result["average_quality"] = health_ai_citation.confidence_score

                        if health_ai_citation.african_relevance_score > 0.3:
                            result["african_relevant_count"] = 1

                        if health_ai_citation.infrastructure_pillar:
                            result["pillars_found"].append(
                                health_ai_citation.infrastructure_pillar
                            )

                        # Create citations for reference links
                        for ref_link in reference_links:
                            ref_citation = {
                                "citation_id": f"ref_{len(result['reference_citations'])}_{depth}",
                                "title": f"Reference from {health_ai_citation.title[:50]}...",
                                "url": ref_link,
                                "priority_score": health_ai_citation.confidence_score
                                * 0.8,  # Slightly lower
                                "citation_type": "reference_link",
                                "discovery_method": f"reference_extraction_depth_{depth}",
                                "parent_citation_id": citation_id,
                            }
                            result["reference_citations"].append(ref_citation)

                        logger.info(
                            f"✅ Processed health AI citation: {health_ai_citation.title[:50]}... ({len(reference_links)} refs)"
                        )

        except Exception as e:
            logger.error(f"Error processing citation {citation_id}: {e}")

        return result

    async def _fetch_citation_content_respectfully(self, url: str) -> Optional[str]:
        """Fetch content while respecting robots.txt and rate limits"""

        # Check robots.txt if enabled
        if self.config.respect_robots_txt and not await self._check_robots_txt(url):
            logger.info(f"🤖 Robots.txt disallows access: {url}")
            return None

        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "User-Agent": "AHAII-Research-Bot/1.0 (+https://ahaii.org/research) - Academic research on African health AI infrastructure"
                }

                async with session.get(
                    url, timeout=aiohttp.ClientTimeout(total=15), headers=headers
                ) as response:
                    if response.status == 200:
                        content = await response.text()

                        # Filter out very short or clearly non-content pages
                        if len(content.strip()) < 500:
                            return None

                        return content[:25000]  # Reasonable limit

                    elif response.status == 403:
                        logger.warning(f"🚫 Access denied: {url}")
                        return None

                    elif response.status == 429:
                        logger.warning(f"⏰ Rate limited: {url}")
                        await asyncio.sleep(30)  # Back off significantly
                        return None

                    else:
                        logger.warning(f"⚠️ HTTP {response.status}: {url}")
                        return None

        except Exception as e:
            logger.warning(f"Failed to fetch {url}: {e}")
            return None

    async def _check_robots_txt(self, url: str) -> bool:
        """Check robots.txt for the domain (simplified)"""
        try:
            from urllib.parse import urljoin, urlparse

            parsed_url = urlparse(url)
            robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    robots_url, timeout=aiohttp.ClientTimeout(total=5)
                ) as response:
                    if response.status == 200:
                        robots_content = await response.text()

                        # Very basic robots.txt parsing
                        if (
                            "Disallow: /" in robots_content
                            and "User-agent: *" in robots_content
                        ):
                            return False

                        # Check for specific disallows that might affect our path
                        lines = robots_content.lower().split("\n")
                        for line in lines:
                            if "disallow:" in line and parsed_url.path in line:
                                return False

            return True  # Allow if can't determine or no robots.txt

        except Exception:
            return True  # Allow if can't check

    def _is_government_domain(self, url: str) -> bool:
        """Check if URL is from a government domain"""
        from urllib.parse import urlparse

        try:
            domain = urlparse(url).netloc.lower()

            # Check against allowed government domains
            for allowed_domain in self.config.government_domains_allowed:
                if allowed_domain in domain:
                    return True

            # Check for obvious government patterns (be conservative)
            government_patterns = [
                ".gov.",  # But not .gov.com etc
                ".govt.",
                "ministry",
                "parliament",
                "senate",
                "president",
            ]

            for pattern in government_patterns:
                if pattern in domain:
                    return True

            return False

        except Exception:
            return False

    def _should_process_government_doc(self, url: str) -> bool:
        """Determine if we should process this government document"""

        # Only process from explicitly allowed domains
        from urllib.parse import urlparse

        domain = urlparse(url).netloc.lower()

        for allowed_domain in self.config.government_domains_allowed:
            if allowed_domain in domain:
                return True

        return False

    async def _extract_health_ai_info(
        self, content: str, citation_item: Dict[str, Any], depth: int
    ) -> Optional[HealthAICitation]:
        """Extract health AI infrastructure information from content"""

        # Create soup for parsing
        soup = BeautifulSoup(content, "html.parser")

        # Extract text content
        text_content = soup.get_text()
        text_lower = text_content.lower()

        # Calculate health AI relevance scores
        health_score = self._calculate_health_relevance(text_lower)
        ai_score = self._calculate_ai_relevance(text_lower)
        african_score = self._calculate_african_relevance(text_lower)
        infrastructure_score = self._calculate_infrastructure_relevance(text_lower)

        # Overall confidence score
        confidence = (
            health_score * 0.3
            + ai_score * 0.3
            + african_score * 0.2
            + infrastructure_score * 0.2
        )

        if confidence < self.config.min_confidence_threshold:
            return None

        # Extract title
        title = citation_item.get("title", "")
        if soup.title:
            title = soup.title.get_text().strip()[:200]

        # Determine infrastructure pillar
        pillar = self._determine_infrastructure_pillar(text_lower)

        # Extract countries and organizations
        countries = self._extract_mentioned_countries(text_lower)
        organizations = self._extract_health_organizations(text_content)

        # Extract regulatory signals
        regulatory_signals = self._extract_regulatory_signals(text_content)

        # Extract funding mentions
        funding_mentions = self._extract_funding_mentions(text_content)

        citation = HealthAICitation(
            id=f"snowball_{citation_item.get('citation_id')}_{depth}_{datetime.now().timestamp()}",
            title=title,
            url=citation_item.get("url"),
            citation_text=text_content[:1000],  # First 1000 chars as excerpt
            confidence_score=confidence,
            citation_type=self._determine_citation_type(citation_item.get("url", "")),
            discovered_at=datetime.now(),
            source_document_id=citation_item.get("citation_id", ""),
            health_ai_relevance_score=health_score,
            african_relevance_score=african_score,
            infrastructure_pillar=pillar,
            mentioned_countries=countries,
            mentioned_organizations=organizations,
            regulatory_signals=regulatory_signals,
            funding_mentions=funding_mentions,
        )

        return citation

    async def _extract_reference_links(self, content: str, base_url: str) -> List[str]:
        """Extract reference links from academic papers and reports (KEY FEATURE)"""

        soup = BeautifulSoup(content, "html.parser")
        reference_links = []

        # Common patterns for reference sections
        reference_patterns = [
            "references",
            "bibliography",
            "citations",
            "sources",
            "further reading",
            "related work",
            "see also",
            "additional resources",
        ]

        # Find reference sections
        reference_sections = []

        for pattern in reference_patterns:
            # Look for headings with reference-like text
            headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
            for heading in headings:
                if pattern in heading.get_text().lower():
                    # Get content after this heading
                    reference_sections.append(heading.find_next_siblings())

        # Also look for common reference list patterns
        reference_lists = soup.find_all(
            ["ol", "ul"], class_=re.compile(r"ref|citation|bibliography", re.I)
        )
        reference_sections.extend(reference_lists)

        # Extract links from reference sections
        for section in reference_sections:
            if isinstance(section, list):
                for element in section:
                    links = (
                        element.find_all("a", href=True)
                        if hasattr(element, "find_all")
                        else []
                    )
                    for link in links:
                        href = link.get("href")
                        if self._is_academic_reference(href):
                            reference_links.append(href)
            else:
                links = (
                    section.find_all("a", href=True)
                    if hasattr(section, "find_all")
                    else []
                )
                for link in links:
                    href = link.get("href")
                    if self._is_academic_reference(href):
                        reference_links.append(href)

        # Extract DOI links from anywhere in the document
        doi_pattern = r'https?://(?:dx\.)?doi\.org/[^\s\'"<>]+'
        doi_matches = re.findall(doi_pattern, content, re.IGNORECASE)
        reference_links.extend(doi_matches)

        # Extract PubMed links
        pubmed_pattern = r'https?://(?:www\.)?pubmed\.ncbi\.nlm\.nih\.gov/[^\s\'"<>]+'
        pubmed_matches = re.findall(pubmed_pattern, content, re.IGNORECASE)
        reference_links.extend(pubmed_matches)

        # Extract ArXiv links
        arxiv_pattern = r'https?://(?:www\.)?arxiv\.org/[^\s\'"<>]+'
        arxiv_matches = re.findall(arxiv_pattern, content, re.IGNORECASE)
        reference_links.extend(arxiv_matches)

        # Clean and deduplicate links
        cleaned_links = []
        seen_links = set()

        for link in reference_links:
            # Make absolute URLs
            from urllib.parse import urljoin

            absolute_link = (
                urljoin(base_url, link) if not link.startswith("http") else link
            )

            # Clean up common suffixes
            absolute_link = absolute_link.rstrip(".,);")

            if absolute_link not in seen_links and len(absolute_link) > 10:
                seen_links.add(absolute_link)
                cleaned_links.append(absolute_link)

        return cleaned_links[:20]  # Limit to 20 references per document

    def _is_academic_reference(self, href: str) -> bool:
        """Check if a link appears to be an academic reference"""
        if not href:
            return False

        academic_domains = [
            "doi.org",
            "pubmed",
            "arxiv.org",
            "scholar.google",
            "researchgate.net",
            "academia.edu",
            "jstor.org",
            "springer.com",
            "wiley.com",
            "elsevier.com",
            "nature.com",
            "science.org",
            "plos.org",
            "bmj.com",
            "nejm.org",
            "thelancet.com",
            "cell.com",
            "frontiersin.org",
            "mdpi.com",
        ]

        href_lower = href.lower()

        return any(domain in href_lower for domain in academic_domains)

    def _calculate_health_relevance(self, text: str) -> float:
        """Calculate health relevance score"""
        score = 0.0
        word_count = len(text.split())

        for term in self.health_ai_patterns["health_terms"]:
            count = text.count(term.lower())
            score += count * 0.1

        return min(score / (word_count / 100) if word_count > 0 else score, 1.0)

    def _calculate_ai_relevance(self, text: str) -> float:
        """Calculate AI relevance score"""
        score = 0.0
        word_count = len(text.split())

        for term in self.health_ai_patterns["ai_terms"]:
            count = text.count(term.lower())
            if term in ["artificial intelligence", "machine learning", "deep learning"]:
                score += count * 0.3
            elif term in ["ai", "ml"]:
                score += count * 0.2
            else:
                score += count * 0.1

        return min(score / (word_count / 100) if word_count > 0 else score, 1.0)

    def _calculate_african_relevance(self, text: str) -> float:
        """Calculate African relevance score"""
        score = 0.0

        for country in self.african_countries:
            if country in text:
                score += 0.3

        african_terms = ["africa", "african", "sub-saharan", "continental"]
        for term in african_terms:
            if term in text:
                score += 0.2

        return min(score, 1.0)

    def _calculate_infrastructure_relevance(self, text: str) -> float:
        """Calculate infrastructure relevance score"""
        score = 0.0
        word_count = len(text.split())

        for term in self.health_ai_patterns["infrastructure_terms"]:
            count = text.count(term.lower())
            score += count * 0.05

        return min(score / (word_count / 100) if word_count > 0 else score, 1.0)

    def _determine_infrastructure_pillar(self, text: str) -> Optional[str]:
        """Determine which infrastructure pillar this content relates to"""

        pillar_keywords = {
            "human_capital": [
                "training",
                "education",
                "skills",
                "workforce",
                "capacity building",
                "curriculum",
                "certification",
                "competency",
                "expertise",
                "talent",
            ],
            "physical_infrastructure": [
                "hardware",
                "server",
                "network",
                "connectivity",
                "bandwidth",
                "data center",
                "cloud",
                "system",
                "platform",
                "infrastructure",
            ],
            "regulatory": [
                "regulation",
                "policy",
                "governance",
                "compliance",
                "standard",
                "law",
                "legal",
                "approval",
                "certification",
                "framework",
            ],
            "economic": [
                "funding",
                "investment",
                "economic",
                "financial",
                "cost",
                "budget",
                "resource",
                "market",
                "commercial",
                "revenue",
            ],
        }

        pillar_scores = {}

        for pillar, keywords in pillar_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text)
            if score > 0:
                pillar_scores[pillar] = score

        if pillar_scores:
            return max(pillar_scores, key=pillar_scores.get)

        return None

    def _extract_mentioned_countries(self, text: str) -> List[str]:
        """Extract mentioned African countries"""
        mentioned = []

        for country in self.african_countries:
            if country in text:
                mentioned.append(country.title())

        return list(set(mentioned))[:10]  # Limit and deduplicate

    def _extract_health_organizations(self, text: str) -> List[str]:
        """Extract health organization mentions"""

        org_patterns = [
            r"(?:ministry|department) of health",
            r"world health organization|WHO",
            r"(?:hospital|medical center|health system)",
            r"(?:university|college) of medicine",
            r"medical association",
            r"health(?:\s+\w+)*\s+(?:organization|agency|institute)",
        ]

        organizations = []
        for pattern in org_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            organizations.extend(matches)

        return list(set(organizations))[:10]

    def _extract_regulatory_signals(self, text: str) -> List[str]:
        """Extract regulatory signals"""

        regulatory_patterns = [
            r"approved by \w+",
            r"regulatory \w+",
            r"compliance with \w+",
            r"policy \w+",
            r"guidance \w+",
        ]

        signals = []
        for pattern in regulatory_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            signals.extend(matches)

        return list(set(signals))[:5]

    def _extract_funding_mentions(self, text: str) -> List[Dict[str, Any]]:
        """Extract funding mentions"""

        funding_patterns = [
            r"\$(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(million|billion|thousand)",
            r"(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(million|billion|thousand)\s*dollars",
        ]

        funding_mentions = []
        for pattern in funding_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    amount = float(match[0].replace(",", ""))
                    unit = match[1].lower()

                    if unit == "billion":
                        amount *= 1000000000
                    elif unit == "million":
                        amount *= 1000000
                    elif unit == "thousand":
                        amount *= 1000

                    funding_mentions.append(
                        {
                            "amount": amount,
                            "currency": "USD",
                            "context": match[0] + " " + match[1],
                        }
                    )
                except ValueError:
                    continue

        return funding_mentions[:3]

    def _determine_citation_type(self, url: str) -> CitationType:
        """Determine citation type from URL"""

        url_lower = url.lower()

        if "doi.org" in url_lower or "pubmed" in url_lower or "arxiv" in url_lower:
            return CitationType.ACADEMIC_PAPER
        elif any(domain in url_lower for domain in ["who.int", ".gov"]):
            return CitationType.POLICY_DOCUMENT
        elif "github.com" in url_lower:
            return CitationType.GITHUB_REPO
        elif any(domain in url_lower for domain in ["news", "techcrunch", "reuters"]):
            return CitationType.NEWS_ARTICLE
        else:
            return CitationType.UNKNOWN

    async def _store_health_ai_citation(
        self, citation: HealthAICitation
    ) -> Optional[str]:
        """Store health AI citation in database"""

        try:
            citation_data = {
                "id": citation.id,
                "title": citation.title,
                "url": citation.url,
                "citation_text": citation.citation_text,
                "confidence_score": citation.confidence_score,
                "citation_type": citation.citation_type.value,
                "discovered_at": citation.discovered_at.isoformat(),
                "source_document_id": citation.source_document_id,
                "health_ai_relevance_score": citation.health_ai_relevance_score,
                "african_relevance_score": citation.african_relevance_score,
                "infrastructure_pillar": citation.infrastructure_pillar,
                "mentioned_countries": citation.mentioned_countries,
                "mentioned_organizations": citation.mentioned_organizations,
                "regulatory_signals": citation.regulatory_signals,
                "funding_mentions": citation.funding_mentions,
                "reference_links": citation.reference_links,
                "citation_count": len(citation.reference_links),
                "processed": False,
            }

            # Store in infrastructure_intelligence table as a discovery
            intelligence_data = {
                "report_type": "snowball_discovery",
                "report_title": citation.title,
                "report_summary": citation.citation_text[:500],
                "key_findings": {
                    "health_ai_relevance_score": citation.health_ai_relevance_score,
                    "african_relevance_score": citation.african_relevance_score,
                    "infrastructure_pillar": citation.infrastructure_pillar,
                    "mentioned_countries": citation.mentioned_countries,
                    "mentioned_organizations": citation.mentioned_organizations,
                    "regulatory_signals": citation.regulatory_signals,
                    "funding_mentions": citation.funding_mentions,
                    "reference_links_count": len(citation.reference_links),
                },
                "source_type": "snowball_sampling",
                "source_url": citation.url,
                "confidence_score": citation.confidence_score,
                "verification_status": "auto_discovered",
            }

            # Try to associate with a country
            if citation.mentioned_countries:
                country_name = citation.mentioned_countries[0]
                country_result = (
                    await supabase.table("countries")
                    .select("id")
                    .ilike("name", f"%{country_name}%")
                    .execute()
                )
                if country_result.data:
                    intelligence_data["country_id"] = country_result.data[0]["id"]

            result = await self.db_service.insert_infrastructure_intelligence(
                intelligence_data
            )

            if result:
                return result.get("id")

        except Exception as e:
            logger.error(f"Failed to store health AI citation: {e}")

        return None

    def _should_include_in_next_depth(self, citation: Dict[str, Any]) -> bool:
        """Determine if citation should be included in next depth iteration"""

        priority_score = citation.get("priority_score", 0)
        citation_type = citation.get("citation_type", "")

        # Higher threshold for deeper levels
        min_threshold = self.config.min_confidence_threshold + (
            0.1 * len(self.processed_urls) / 100
        )

        return (
            priority_score >= min_threshold
            and citation_type
            in ["academic_paper", "policy_document", "health_ai_report"]
            and citation.get("url") not in self.processed_urls
        )

    async def _store_session_results(self, session_stats: Dict[str, Any]) -> None:
        """Store snowball sampling session results"""

        try:
            # Convert datetime objects to ISO strings
            session_data = session_stats.copy()
            for key in ["start_time", "end_time"]:
                if key in session_data and session_data[key]:
                    session_data[key] = session_data[key].isoformat()

            # Store as infrastructure intelligence
            intelligence_data = {
                "report_type": "snowball_session_summary",
                "report_title": f"Health AI Snowball Sampling Session {session_stats['session_id']}",
                "report_summary": f"Automated discovery session processed {session_stats['citations_processed']} citations and discovered {session_stats['health_ai_discoveries']} new health AI resources.",
                "key_findings": session_data,
                "source_type": "snowball_sampling",
                "confidence_score": session_stats.get("average_quality", 0.0),
                "verification_status": "system_generated",
            }

            await self.db_service.insert_infrastructure_intelligence(intelligence_data)

            logger.info(
                f"📊 Stored snowball session results: {session_stats['session_id']}"
            )

        except Exception as e:
            logger.error(f"Failed to store session results: {e}")


async def run_health_ai_snowball_sampling(
    config: SamplingConfig = None,
) -> Dict[str, Any]:
    """Main entry point for health AI snowball sampling"""

    sampler = HealthAISnowballSampler(config)
    return await sampler.run_sampling_session()


if __name__ == "__main__":
    # Test the snowball sampler
    async def test_snowball_sampling():
        # Create conservative configuration
        config = SamplingConfig(
            max_depth=2,  # Conservative depth
            max_citations_per_batch=5,  # Small batch for testing
            delay_between_requests=5.0,  # Respectful delay
            max_requests_per_minute=10,  # Conservative rate
            government_domains_allowed={
                "who.int",
                "afro.who.int",
            },  # Only international orgs
        )

        results = await run_health_ai_snowball_sampling(config)

        print(f"\n🔬 Health AI Snowball Sampling Results:")
        print(f"Session ID: {results['session_id']}")
        print(f"Citations Processed: {results['citations_processed']}")
        print(f"Health AI Discoveries: {results['health_ai_discoveries']}")
        print(f"Reference Links Extracted: {results['reference_links_extracted']}")
        print(f"Government Docs Processed: {results['government_docs_processed']}")
        print(f"African Relevant Findings: {results['african_relevant_findings']}")
        print(f"Average Quality Score: {results.get('average_quality', 0):.2f}")
        print(f"Pillar Distribution: {results['pillar_distribution']}")

    asyncio.run(test_snowball_sampling())
