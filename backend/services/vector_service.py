"""
Vector Database Service for AHAII
Pinecone integration for Dense inference-enabled index with multilingual-e5-large
Adapted from TAIFA-FIALA for African Health AI Infrastructure Index
"""

import asyncio
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from config.settings import settings
from loguru import logger
from pinecone import Pinecone
from pydantic import BaseModel


class VectorDocument(BaseModel):
    """Document for vector storage"""

    id: str
    content: str
    metadata: Dict[str, Any]


class SearchResult(BaseModel):
    """Vector search result"""

    id: str
    score: float
    metadata: Dict[str, Any]
    content: Optional[str] = None


class VectorService:
    """Service for vector operations using Pinecone Dense inference index"""

    def __init__(self):
        self.pc = None
        self.index = None
        self.index_name = settings.PINECONE_INDEX

    async def initialize(self):
        """Initialize Pinecone client"""
        try:
            # Initialize Pinecone client
            self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)

            # Get index reference
            self.index = self.pc.Index(self.index_name)

            logger.info(f"Vector service initialized with index: {self.index_name}")

        except Exception as e:
            logger.error(f"Error initializing vector service: {e}")
            raise

    def prepare_text(self, text: str) -> str:
        """Clean and prepare text for Pinecone"""
        try:
            cleaned_text = text.strip()
            if not cleaned_text:
                return ""

            # Truncate if too long (multilingual-e5-large has limits)
            max_length = 8192  # Conservative limit for multilingual models
            if len(cleaned_text) > max_length:
                cleaned_text = cleaned_text[:max_length] + "..."

            return cleaned_text

        except Exception as e:
            logger.error(f"Error preparing text: {e}")
            return ""

    async def embed_text(self, text: str) -> List[float]:
        """Generate embedding using Pinecone's inference API"""
        try:
            if not self.index:
                await self.initialize()

            # Use Pinecone's inference to embed text
            response = self.pc.inference.embed(
                model="multilingual-e5-large",
                inputs=[text],
                parameters={"input_type": "passage"},
            )

            if response and len(response) > 0:
                return response[0]["values"]
            else:
                logger.error("Empty embedding response from Pinecone")
                return []

        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return []

    async def upsert_documents(self, documents: List[VectorDocument]) -> bool:
        """Upsert documents to Pinecone using embeddings"""
        try:
            if not self.index:
                await self.initialize()

            # Process documents in batches
            batch_size = 100
            success_count = 0

            for i in range(0, len(documents), batch_size):
                batch = documents[i : i + batch_size]
                vectors_to_upsert = []

                for doc in batch:
                    prepared_text = self.prepare_text(doc.content)
                    if not prepared_text:
                        logger.warning(f"Skipping document {doc.id} - no content")
                        continue

                    # Generate embedding
                    embedding = await self.embed_text(prepared_text)
                    if not embedding:
                        logger.warning(f"Skipping document {doc.id} - embedding failed")
                        continue

                    # Prepare vector for upsert
                    vector = {
                        "id": doc.id,
                        "values": embedding,
                        "metadata": {
                            **doc.metadata,
                            "text": prepared_text[
                                :1000
                            ],  # Store truncated text for retrieval
                        },
                    }
                    vectors_to_upsert.append(vector)

                # Upsert batch
                if vectors_to_upsert:
                    try:
                        self.index.upsert(vectors=vectors_to_upsert)
                        success_count += len(vectors_to_upsert)
                        logger.info(
                            f"Upserted batch {i // batch_size + 1}/{(len(documents) - 1) // batch_size + 1} - {len(vectors_to_upsert)} vectors"
                        )
                    except Exception as batch_error:
                        logger.error(f"Batch upsert failed: {batch_error}")
                        continue

                # Small delay between batches
                if len(documents) > batch_size:
                    await asyncio.sleep(0.2)

            logger.info(
                f"Successfully upserted {success_count}/{len(documents)} documents"
            )
            return success_count > 0

        except Exception as e:
            logger.error(f"Error upserting documents: {e}")
            return False

    async def search_similar(
        self,
        query: str,
        top_k: int = 10,
        filter_metadata: Optional[Dict[str, Any]] = None,
    ) -> List[SearchResult]:
        """Search for similar documents using query embedding"""
        try:
            if not self.index:
                await self.initialize()

            query_text = self.prepare_text(query)
            if not query_text:
                return []

            # Generate query embedding
            query_embedding = await self.embed_text(query_text)
            if not query_embedding:
                logger.error("Failed to generate query embedding")
                return []

            # Perform vector search
            search_response = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True,
                filter=filter_metadata,
            )

            # Parse results
            results = []
            for match in search_response.matches:
                result = SearchResult(
                    id=match.id,
                    score=match.score,
                    metadata=match.metadata,
                    content=match.metadata.get(
                        "text", match.metadata.get("content", "")
                    ),
                )
                results.append(result)

            logger.info(
                f"Found {len(results)} similar documents for query: {query[:50]}..."
            )
            return results

        except Exception as e:
            logger.error(f"Error searching similar documents: {e}")
            return []

    async def search_innovations(
        self,
        query: str,
        innovation_type: Optional[str] = None,
        country: Optional[str] = None,
        top_k: int = 20,
    ) -> List[SearchResult]:
        """Search for innovations with filters"""
        filter_dict = {"document_type": "innovation"}

        if innovation_type:
            filter_dict["innovation_type"] = innovation_type

        if country:
            filter_dict["country"] = country

        return await self.search_similar(query, top_k, filter_dict)

    async def search_publications(
        self,
        query: str,
        publication_type: Optional[str] = None,
        year_from: Optional[int] = None,
        top_k: int = 20,
    ) -> List[SearchResult]:
        """Search for publications with filters"""
        filter_dict = {"document_type": "publication"}

        if publication_type:
            filter_dict["publication_type"] = publication_type

        if year_from:
            filter_dict["year"] = {"$gte": year_from}

        return await self.search_similar(query, top_k, filter_dict)

    async def add_innovation(
        self,
        innovation_id: UUID,
        title: str,
        description: str,
        innovation_type: str,
        country: str,
        additional_metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Add innovation to vector database"""
        combined_text = f"{title}. {description}"

        metadata = {
            "document_type": "innovation",
            "innovation_id": str(innovation_id),
            "title": title,
            "innovation_type": innovation_type,
            "country": country,
            "timestamp": str(asyncio.get_event_loop().time()),
        }

        if additional_metadata:
            metadata.update(additional_metadata)

        document = VectorDocument(
            id=f"innovation_{innovation_id}", content=combined_text, metadata=metadata
        )

        return await self.upsert_documents([document])

    async def add_publication(
        self,
        publication_id: UUID,
        title: str,
        abstract: str,
        publication_type: str,
        authors: List[str],
        year: Optional[int] = None,
        additional_metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Add publication to vector database"""
        authors_text = ", ".join(authors) if authors else ""
        combined_text = f"{title}. {abstract}. Authors: {authors_text}"

        metadata = {
            "document_type": "publication",
            "publication_id": str(publication_id),
            "title": title,
            "publication_type": publication_type,
            "authors": authors,
            "timestamp": str(asyncio.get_event_loop().time()),
        }

        if year:
            metadata["year"] = year

        if additional_metadata:
            metadata.update(additional_metadata)

        document = VectorDocument(
            id=f"publication_{publication_id}", content=combined_text, metadata=metadata
        )

        return await self.upsert_documents([document])

    async def add_news_article(
        self,
        article_id: UUID,
        title: str,
        content: str,
        source: str,
        relevance_scores: Dict[str, float],
        additional_metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Add news article to vector database"""
        combined_text = f"{title}. {content[:2000]}"

        metadata = {
            "document_type": "news_article",
            "article_id": str(article_id),
            "title": title,
            "source": source,
            "ai_relevance_score": relevance_scores.get("ai_relevance_score", 0.0),
            "african_relevance_score": relevance_scores.get(
                "african_relevance_score", 0.0
            ),
            "timestamp": str(asyncio.get_event_loop().time()),
        }

        if additional_metadata:
            metadata.update(additional_metadata)

        document = VectorDocument(
            id=f"article_{article_id}", content=combined_text, metadata=metadata
        )

        return await self.upsert_documents([document])

    # =============================================================================
    # AHAII-SPECIFIC VECTOR OPERATIONS FOR HEALTH AI INFRASTRUCTURE
    # =============================================================================

    async def add_infrastructure_intelligence(
        self,
        intelligence_id: str,
        title: str,
        summary: str,
        source_type: str,
        country_code: str,
        pillar_impacts: Dict[str, bool],
        significance: str = "low",
        additional_metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Add infrastructure intelligence to vector database"""
        combined_text = f"{title}. {summary}"

        metadata = {
            "document_type": "infrastructure_intelligence",
            "intelligence_id": intelligence_id,
            "title": title,
            "source_type": source_type,  # 'academic_paper', 'news_article', 'government_report'
            "country_code": country_code,
            "affects_human_capital": pillar_impacts.get("human_capital", False),
            "affects_physical_infrastructure": pillar_impacts.get(
                "physical_infrastructure", False
            ),
            "affects_regulatory_framework": pillar_impacts.get(
                "regulatory_framework", False
            ),
            "affects_economic_market": pillar_impacts.get("economic_market", False),
            "impact_significance": significance,
            "timestamp": str(asyncio.get_event_loop().time()),
        }

        if additional_metadata:
            metadata.update(additional_metadata)

        document = VectorDocument(
            id=f"intel_{intelligence_id}", content=combined_text, metadata=metadata
        )

        return await self.upsert_documents([document])

    async def add_health_ai_organization(
        self,
        org_id: str,
        name: str,
        description: str,
        organization_type: str,
        country_code: str,
        focus_areas: List[str],
        additional_metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Add health AI organization to vector database"""
        focus_text = ", ".join(focus_areas) if focus_areas else ""
        combined_text = f"{name}. {description}. Focus areas: {focus_text}"

        metadata = {
            "document_type": "health_ai_organization",
            "organization_id": org_id,
            "name": name,
            "organization_type": organization_type,
            "country_code": country_code,
            "focus_areas": focus_areas,
            "timestamp": str(asyncio.get_event_loop().time()),
        }

        if additional_metadata:
            metadata.update(additional_metadata)

        document = VectorDocument(
            id=f"org_{org_id}", content=combined_text, metadata=metadata
        )

        return await self.upsert_documents([document])

    async def search_by_infrastructure_pillar(
        self,
        query: str,
        pillar: str,  # 'human_capital', 'physical_infrastructure', 'regulatory_framework', 'economic_market'
        country_code: Optional[str] = None,
        top_k: int = 20,
    ) -> List[SearchResult]:
        """Search for documents affecting a specific infrastructure pillar"""
        filter_dict = {f"affects_{pillar}": True}

        if country_code:
            filter_dict["country_code"] = country_code

        return await self.search_similar(query, top_k, filter_dict)

    async def search_health_ai_organizations(
        self,
        query: str,
        organization_type: Optional[str] = None,
        country_code: Optional[str] = None,
        top_k: int = 20,
    ) -> List[SearchResult]:
        """Search for health AI organizations"""
        filter_dict = {"document_type": "health_ai_organization"}

        if organization_type:
            filter_dict["organization_type"] = organization_type

        if country_code:
            filter_dict["country_code"] = country_code

        return await self.search_similar(query, top_k, filter_dict)

    async def search_infrastructure_intelligence(
        self,
        query: str,
        source_type: Optional[str] = None,
        significance: Optional[str] = None,
        country_code: Optional[str] = None,
        top_k: int = 20,
    ) -> List[SearchResult]:
        """Search for infrastructure intelligence reports"""
        filter_dict = {"document_type": "infrastructure_intelligence"}

        if source_type:
            filter_dict["source_type"] = source_type

        if significance:
            filter_dict["impact_significance"] = significance

        if country_code:
            filter_dict["country_code"] = country_code

        return await self.search_similar(query, top_k, filter_dict)

    async def find_similar_by_country(
        self,
        query: str,
        country_code: str,
        top_k: int = 20,
    ) -> List[SearchResult]:
        """Find documents similar to query for a specific country"""
        filter_dict = {"country_code": country_code}
        return await self.search_similar(query, top_k, filter_dict)

    async def get_pillar_insights(
        self,
        pillar: str,
        country_code: Optional[str] = None,
        limit: int = 50,
    ) -> Dict[str, Any]:
        """Get insights for a specific infrastructure pillar"""
        try:
            # Search for high-impact documents for this pillar
            filter_dict = {f"affects_{pillar}": True, "impact_significance": "high"}

            if country_code:
                filter_dict["country_code"] = country_code

            # Use a broad query to get pillar-relevant documents
            pillar_queries = {
                "human_capital": "medical training clinical education health informatics AI curriculum",
                "physical_infrastructure": "hospital system EMR implementation data center telemedicine platform",
                "regulatory_framework": "medical device approval health regulation AI governance clinical validation",
                "economic_market": "health AI funding medical AI investment digital health budget",
            }

            query = pillar_queries.get(pillar, pillar)
            results = await self.search_similar(query, limit, filter_dict)

            # Analyze results
            source_types = {}
            countries = {}
            significance_counts = {"high": 0, "medium": 0, "low": 0}

            for result in results:
                # Count source types
                source_type = result.metadata.get("source_type", "unknown")
                source_types[source_type] = source_types.get(source_type, 0) + 1

                # Count countries
                country = result.metadata.get("country_code", "unknown")
                countries[country] = countries.get(country, 0) + 1

                # Count significance
                sig = result.metadata.get("impact_significance", "low")
                if sig in significance_counts:
                    significance_counts[sig] += 1

            return {
                "pillar": pillar,
                "total_documents": len(results),
                "source_type_breakdown": source_types,
                "country_breakdown": countries,
                "significance_breakdown": significance_counts,
                "recent_insights": [
                    {
                        "title": result.metadata.get("title", "Unknown"),
                        "score": result.score,
                        "source_type": result.metadata.get("source_type", "unknown"),
                        "country_code": result.metadata.get("country_code", "unknown"),
                        "significance": result.metadata.get(
                            "impact_significance", "low"
                        ),
                    }
                    for result in results[:10]  # Top 10 results
                ],
            }

        except Exception as e:
            logger.error(f"Error getting pillar insights for {pillar}: {e}")
            return {"error": str(e)}

    async def find_similar_innovations(
        self, innovation_id: UUID, top_k: int = 5
    ) -> List[SearchResult]:
        """Find innovations similar to a given innovation"""
        try:
            # First, get the innovation's content
            fetch_response = self.index.fetch(ids=[f"innovation_{innovation_id}"])

            if (
                not fetch_response.vectors
                or f"innovation_{innovation_id}" not in fetch_response.vectors
            ):
                logger.warning(
                    f"Innovation {innovation_id} not found in vector database"
                )
                return []

            innovation_metadata = fetch_response.vectors[
                f"innovation_{innovation_id}"
            ].metadata
            innovation_text = innovation_metadata.get(
                "text", innovation_metadata.get("title", "")
            )

            if not innovation_text:
                logger.warning(f"No text content found for innovation {innovation_id}")
                return []

            # Search for similar innovations
            search_results = await self.search_similar(
                query=innovation_text,
                top_k=top_k + 1,  # +1 to account for the original
                filter_metadata={"document_type": "innovation"},
            )

            # Filter out the original innovation
            similar_results = [
                result
                for result in search_results
                if result.id != f"innovation_{innovation_id}"
            ]

            return similar_results[:top_k]

        except Exception as e:
            logger.error(f"Error finding similar innovations: {e}")
            return []

    async def get_stats(self) -> Dict[str, Any]:
        """Get vector database statistics"""
        try:
            if not self.index:
                await self.initialize()

            stats = self.index.describe_index_stats()

            return {
                "total_vectors": stats.total_vector_count,
                "index_fullness": stats.index_fullness,
                "dimension": getattr(stats, "dimension", 1024),
                "namespaces": stats.namespaces,
            }

        except Exception as e:
            logger.error(f"Error getting vector database stats: {e}")
            return {}

    async def delete_document(self, document_id: str) -> bool:
        """Delete a document from vector database"""
        try:
            if not self.index:
                await self.initialize()

            self.index.delete(ids=[document_id])
            logger.info(f"Deleted document: {document_id}")
            return True

        except Exception as e:
            logger.error(f"Error deleting document {document_id}: {e}")
            return False


# Global vector service instance
vector_service = VectorService()


async def get_vector_service() -> VectorService:
    """Get initialized vector service"""
    if not vector_service.index:
        await vector_service.initialize()
    return vector_service


if __name__ == "__main__":
    # Test the vector service
    async def test_vector_service():
        service = await get_vector_service()

        # Test adding a document
        success = await service.add_innovation(
            innovation_id=uuid4(),
            title="AI-Powered Crop Disease Detection",
            description="Mobile app using computer vision to identify crop diseases in Kenya",
            innovation_type="AgriTech",
            country="Kenya",
        )

        print(f"Document added: {success}")

        # Test search
        results = await service.search_innovations("crop disease detection Kenya")
        print(f"Search results: {len(results)}")

        for result in results:
            print(
                f"- {result.metadata.get('title', 'No title')} (score: {result.score:.3f})"
            )

    asyncio.run(test_vector_service())
