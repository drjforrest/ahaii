"""
Health AI Infrastructure Academic Scraper for AHAII
Specialized ETL for academic publications related to African health AI infrastructure
"""

import asyncio
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from urllib.parse import quote

import aiohttp
import feedparser
from config.settings import settings
from loguru import logger
from pydantic import BaseModel


class HealthAIPaper(BaseModel):
    """Pydantic model for Health AI Infrastructure paper data"""
    paper_id: str
    title: str
    authors: List[str]
    abstract: str
    url: str
    published_date: datetime
    updated_date: datetime
    categories: List[str]
    keywords: List[str]
    
    # AHAII-specific scoring
    african_relevance_score: float
    african_entities: List[str]  # Countries, institutions, etc.
    health_ai_infrastructure_score: float  # How relevant to health AI infrastructure
    pillar_relevance: Dict[str, float]  # Relevance to each AHAII pillar
    
    # Infrastructure indicators extracted from paper
    infrastructure_signals: List[Dict[str, Any]]


class HealthAIInfrastructureClassifier:
    """Classifier for determining health AI infrastructure relevance and extracting signals"""
    
    def __init__(self):
        self.human_capital_keywords = [
            'medical education', 'clinical training', 'health informatics education',
            'biomedical informatics curriculum', 'AI medical training', 'clinical decision support training',
            'health data science programs', 'medical AI workforce', 'clinical informatics competency'
        ]
        
        self.physical_infrastructure_keywords = [
            'EMR implementation', 'electronic medical records', 'hospital information systems',
            'medical device integration', 'PACS deployment', 'healthcare interoperability',
            'clinical data networks', 'telemedicine infrastructure', 'health data centers',
            'medical imaging systems', 'hospital digitization'
        ]
        
        self.regulatory_keywords = [
            'medical AI regulation', 'health AI governance', 'clinical AI validation',
            'medical device approval', 'health data privacy', 'clinical trial regulation',
            'medical AI ethics', 'health AI compliance', 'FDA medical device', 'CE mark'
        ]
        
        self.economic_keywords = [
            'health AI investment', 'medical AI funding', 'healthcare digital transformation',
            'clinical AI adoption costs', 'health AI reimbursement', 'medical AI market',
            'healthcare technology economics', 'digital health business model'
        ]
    
    def classify_infrastructure_relevance(self, title: str, abstract: str) -> Dict[str, float]:
        """Calculate relevance scores for each AHAII pillar"""
        text = f"{title} {abstract}".lower()
        
        scores = {
            'human_capital': self._calculate_keyword_relevance(text, self.human_capital_keywords),
            'physical_infrastructure': self._calculate_keyword_relevance(text, self.physical_infrastructure_keywords),
            'regulatory': self._calculate_keyword_relevance(text, self.regulatory_keywords),
            'economic': self._calculate_keyword_relevance(text, self.economic_keywords)
        }
        
        return scores
    
    def _calculate_keyword_relevance(self, text: str, keywords: List[str]) -> float:
        """Calculate relevance score based on keyword presence and frequency"""
        score = 0.0
        word_count = len(text.split())
        
        for keyword in keywords:
            occurrences = text.count(keyword.lower())
            if occurrences > 0:
                # Base score for presence + bonus for frequency
                keyword_score = 10.0 + (occurrences * 5.0)
                score += keyword_score
        
        # Normalize by text length and keyword set size
        if word_count > 0:
            score = (score / word_count) * 100
            score = min(score, 100.0)  # Cap at 100
            
        return round(score, 2)
    
    def extract_infrastructure_signals(self, title: str, abstract: str) -> List[Dict[str, Any]]:
        """Extract specific infrastructure signals/indicators from the paper"""
        signals = []
        text = f"{title} {abstract}".lower()
        
        # EMR adoption signals
        if any(term in text for term in ['emr adoption', 'electronic medical record implementation', 'ehr deployment']):
            signals.append({
                'signal_type': 'emr_adoption',
                'indicator_name': 'emr_adoption_rate',
                'confidence': 0.7,
                'extracted_text': self._extract_relevant_sentence(text, ['emr', 'electronic medical record'])
            })
        
        # Training program signals
        if any(term in text for term in ['training program', 'medical education', 'clinical training']):
            signals.append({
                'signal_type': 'training_programs',
                'indicator_name': 'clinical_ai_certification_programs',
                'confidence': 0.6,
                'extracted_text': self._extract_relevant_sentence(text, ['training', 'education'])
            })
        
        # Infrastructure development signals
        if any(term in text for term in ['infrastructure development', 'system implementation', 'digital transformation']):
            signals.append({
                'signal_type': 'infrastructure_development',
                'indicator_name': 'digital_health_infrastructure',
                'confidence': 0.8,
                'extracted_text': self._extract_relevant_sentence(text, ['infrastructure', 'implementation'])
            })
        
        return signals
    
    def _extract_relevant_sentence(self, text: str, keywords: List[str]) -> str:
        """Extract the most relevant sentence containing the keywords"""
        sentences = text.split('.')
        best_sentence = ""
        max_keyword_count = 0
        
        for sentence in sentences:
            keyword_count = sum(1 for keyword in keywords if keyword in sentence)
            if keyword_count > max_keyword_count:
                max_keyword_count = keyword_count
                best_sentence = sentence.strip()
        
        return best_sentence[:200]  # Truncate for storage


class HealthAIAcademicScraper:
    """Academic scraper for African Health AI Infrastructure research papers"""

    def __init__(self):
        self.session = None
        self.african_countries = set(settings.AFRICAN_COUNTRIES)
        self.african_institutions = set(settings.AFRICAN_MEDICAL_INSTITUTIONS)
        self.health_ai_keywords = settings.HEALTH_AI_INFRASTRUCTURE_KEYWORDS
        self.classifier = HealthAIInfrastructureClassifier()
        
        # Academic sources with health AI focus
        self.sources = {
            'arxiv': settings.ARXIV_BASE_URL,
            'pubmed': settings.PUBMED_BASE_URL,
            'crossref': settings.CROSSREF_BASE_URL
        }

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=settings.CRAWL4AI_TIMEOUT)
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def build_health_ai_search_query(self, source: str = 'arxiv', max_results: int = 50, 
                                   days_back: int = 30) -> str:
        """Build health AI infrastructure search query for different academic sources"""
        
        if source == 'arxiv':
            return self._build_arxiv_query(max_results, days_back)
        elif source == 'pubmed':
            return self._build_pubmed_query(max_results, days_back)
        else:
            logger.warning(f"Unsupported source: {source}")
            return ""
    
    def _build_arxiv_query(self, max_results: int, days_back: int) -> str:
        """Build ArXiv search query focused on health AI infrastructure"""
        
        # Combine health AI infrastructure keywords
        health_ai_terms = [
            'health artificial intelligence', 'medical AI', 'clinical AI',
            'healthcare machine learning', 'medical informatics', 
            'electronic medical records', 'telemedicine', 'digital health'
        ]
        
        keyword_query = " OR ".join([f'all:"{term}"' for term in health_ai_terms[:8]])  # Limit to avoid URL issues
        
        # Add African context
        african_terms = []
        for country in list(self.african_countries)[:8]:  # Limit to key countries
            african_terms.append(f'all:"{country}"')
        
        # Add major African medical institutions
        for institution in ['University of Cape Town', 'Cairo University', 'University of Nairobi']:
            african_terms.append(f'all:"{institution}"')
            
        african_query = " OR ".join(african_terms)
        
        # Combine queries
        full_query = f"({keyword_query}) AND ({african_query})"
        
        # Build URL parameters
        params = {
            'search_query': full_query,
            'start': 0,
            'max_results': max_results,
            'sortBy': 'lastUpdatedDate',
            'sortOrder': 'descending'
        }
        
        query_string = "&".join([f"{k}={quote(str(v))}" for k, v in params.items()])
        return f"{self.sources['arxiv']}?{query_string}"
    
    def _build_pubmed_query(self, max_results: int, days_back: int) -> str:
        """Build PubMed search query for health AI infrastructure papers"""
        
        # PubMed specific search terms
        search_terms = [
            "health artificial intelligence[MeSH]",
            "medical informatics[MeSH]", 
            "electronic health records[MeSH]",
            "telemedicine[MeSH]",
            "Africa[MeSH]"
        ]
        
        query = " AND ".join(search_terms[:3]) + f" AND ({' OR '.join(self.african_countries[:10])})"
        
        params = {
            'db': 'pubmed',
            'term': query,
            'retmax': max_results,
            'sort': 'date',
            'rettype': 'xml'
        }
        
        query_string = "&".join([f"{k}={quote(str(v))}" for k, v in params.items()])
        return f"{self.sources['pubmed']}/esearch.fcgi?{query_string}"

    async def scrape_health_ai_papers(self, source: str = 'arxiv', max_results: int = 50) -> List[Dict[str, Any]]:
        """Scrape health AI infrastructure papers from academic sources"""
        
        query_url = self.build_health_ai_search_query(source, max_results)
        if not query_url:
            return []
        
        logger.info(f"Scraping {source} for health AI infrastructure papers: {max_results} results")
        
        try:
            papers = await self.fetch_papers(query_url, source)
            processed_papers = []
            
            for paper_data in papers:
                try:
                    processed_paper = self.process_health_ai_paper(paper_data)
                    if processed_paper and self.is_relevant_to_ahaii(processed_paper):
                        processed_papers.append(processed_paper)
                except Exception as e:
                    logger.error(f"Error processing paper: {e}")
                    continue
            
            logger.info(f"Successfully processed {len(processed_papers)} relevant health AI papers")
            return processed_papers
            
        except Exception as e:
            logger.error(f"Error scraping {source}: {e}")
            return []

    async def fetch_papers(self, query_url: str, source: str) -> List[Dict[str, Any]]:
        """Fetch papers from academic API"""
        try:
            async with self.session.get(query_url) as response:
                if response.status == 200:
                    content = await response.text()
                    if source == 'arxiv':
                        return self.parse_arxiv_response(content)
                    elif source == 'pubmed':
                        return self.parse_pubmed_response(content)
                    else:
                        return []
                else:
                    logger.error(f"{source} API error: {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Error fetching from {source}: {e}")
            return []

    def parse_arxiv_response(self, xml_content: str) -> List[Dict[str, Any]]:
        """Parse ArXiv XML response"""
        papers = []
        
        try:
            feed = feedparser.parse(xml_content)
            
            for entry in feed.entries:
                try:
                    paper_data = self.extract_arxiv_paper_data(entry)
                    if paper_data:
                        papers.append(paper_data)
                except Exception as e:
                    logger.error(f"Error parsing ArXiv entry: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error parsing ArXiv response: {e}")
            
        return papers

    def extract_arxiv_paper_data(self, entry) -> Optional[Dict[str, Any]]:
        """Extract paper data from ArXiv entry"""
        try:
            title = getattr(entry, 'title', '').replace('\n', ' ').strip()
            abstract = getattr(entry, 'summary', '').replace('\n', ' ').strip()
            
            if not title or not abstract or not hasattr(entry, 'id'):
                return None
                
            # Extract ArXiv ID
            paper_id = entry.id.split('/')[-1]
            
            # Extract authors
            authors = []
            if hasattr(entry, 'authors') and entry.authors:
                authors = [getattr(author, 'name', str(author)) for author in entry.authors]
            
            # Extract dates
            try:
                published_date = datetime.strptime(entry.published, '%Y-%m-%dT%H:%M:%SZ')
            except (ValueError, AttributeError):
                published_date = datetime.now()
                
            try:
                updated_date = datetime.strptime(entry.updated, '%Y-%m-%dT%H:%M:%SZ')
            except (ValueError, AttributeError):
                updated_date = published_date
                
            # Extract categories
            categories = []
            if hasattr(entry, 'tags') and entry.tags:
                categories = [getattr(tag, 'term', str(tag)) for tag in entry.tags]
            
            return {
                'paper_id': paper_id,
                'title': title,
                'authors': authors,
                'abstract': abstract,
                'url': entry.id,
                'published_date': published_date,
                'updated_date': updated_date,
                'categories': categories,
                'source': 'arxiv'
            }
            
        except Exception as e:
            logger.error(f"Error extracting ArXiv paper data: {e}")
            return None

    def process_health_ai_paper(self, paper_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process paper with AHAII-specific analysis"""
        try:
            title = paper_data.get('title', '')
            abstract = paper_data.get('abstract', '')
            authors = paper_data.get('authors', [])
            
            # Calculate African relevance
            african_score, african_entities = self.calculate_african_relevance(title, abstract, authors)
            
            # Calculate health AI infrastructure relevance
            pillar_scores = self.classifier.classify_infrastructure_relevance(title, abstract)
            health_ai_infra_score = sum(pillar_scores.values()) / len(pillar_scores)
            
            # Extract infrastructure signals
            infrastructure_signals = self.classifier.extract_infrastructure_signals(title, abstract)
            
            # Generate keywords
            keywords = self.extract_keywords(title, abstract)
            
            return {
                **paper_data,
                'keywords': keywords,
                'african_relevance_score': african_score,
                'african_entities': african_entities,
                'health_ai_infrastructure_score': health_ai_infra_score,
                'pillar_relevance': pillar_scores,
                'infrastructure_signals': infrastructure_signals
            }
            
        except Exception as e:
            logger.error(f"Error processing health AI paper: {e}")
            return None

    def calculate_african_relevance(self, title: str, abstract: str, authors: List[str]) -> tuple[float, List[str]]:
        """Calculate African relevance score and extract African entities"""
        text = f"{title} {abstract} {' '.join(authors)}".lower()
        
        african_entities = []
        country_matches = 0
        institution_matches = 0
        
        # Check for African countries
        for country in self.african_countries:
            if country.lower() in text:
                african_entities.append(country)
                country_matches += 1
        
        # Check for African institutions
        for institution in self.african_institutions:
            if any(word in text for word in institution.lower().split()[:3]):  # Check first 3 words
                african_entities.append(institution)
                institution_matches += 1
        
        # Calculate score (0-100)
        score = (country_matches * 20) + (institution_matches * 30)
        score = min(score, 100.0)
        
        return round(score, 2), list(set(african_entities))

    def is_relevant_to_ahaii(self, paper_data: Dict[str, Any]) -> bool:
        """Determine if paper is relevant to AHAII assessment"""
        african_score = paper_data.get('african_relevance_score', 0)
        health_ai_score = paper_data.get('health_ai_infrastructure_score', 0)
        
        # Require minimum African relevance and health AI infrastructure relevance
        return african_score >= 10.0 and health_ai_score >= 15.0

    def extract_keywords(self, title: str, abstract: str) -> List[str]:
        """Extract relevant keywords from title and abstract"""
        text = f"{title} {abstract}".lower()
        keywords = []
        
        # Extract health AI infrastructure keywords that appear in text
        for keyword in self.health_ai_keywords:
            if keyword.lower() in text:
                keywords.append(keyword)
        
        return list(set(keywords))[:20]  # Limit to 20 most relevant

    def parse_pubmed_response(self, xml_content: str) -> List[Dict[str, Any]]:
        """Parse PubMed XML response (simplified implementation)"""
        # This would require more sophisticated XML parsing for PubMed
        # For now, return empty list - can be expanded later
        logger.info("PubMed parsing not yet implemented")
        return []


async def scrape_health_ai_infrastructure_papers(max_results: int = 50) -> List[Dict[str, Any]]:
    """Main function to scrape health AI infrastructure papers"""
    
    async with HealthAIAcademicScraper() as scraper:
        papers = await scraper.scrape_health_ai_papers('arxiv', max_results)
        
        logger.info(f"Scraped {len(papers)} health AI infrastructure papers")
        
        return papers


if __name__ == "__main__":
    # Test the scraper
    import asyncio
    
    async def test_scraper():
        papers = await scrape_health_ai_infrastructure_papers(10)
        
        for paper in papers:
            print(f"Title: {paper['title']}")
            print(f"African Relevance: {paper['african_relevance_score']}")
            print(f"Health AI Infrastructure Score: {paper['health_ai_infrastructure_score']}")
            print(f"Pillar Scores: {paper['pillar_relevance']}")
            print(f"Infrastructure Signals: {len(paper['infrastructure_signals'])}")
            print("---")
    
    asyncio.run(test_scraper())
