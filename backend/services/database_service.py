"""
Supabase Database Service for AHAII
Provides reusable database operations using Supabase client for Row Level Security
Adapted from TAIFA-FIALA for African Health AI Infrastructure Index
"""

from datetime import date, datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4

from config.database import supabase
from loguru import logger


class DatabaseService:
    """Centralized database service using Supabase client for RLS compliance"""

    def __init__(self):
        self.client = supabase

    def serialize_date(self, date_obj):
        """Helper function to serialize dates for JSON compatibility"""
        if date_obj is None:
            return None
        elif isinstance(date_obj, datetime):
            return date_obj.isoformat()
        elif isinstance(date_obj, date):
            return date_obj.isoformat()
        elif isinstance(date_obj, str):
            return date_obj
        else:
            return str(date_obj)

    # PUBLICATIONS
    async def create_publication(
        self, publication_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Create a new publication record"""
        try:
            # Prepare publication data according to current schema
            publication_date = publication_data.get("publication_date")
            pub_record = {
                "id": str(uuid4()),
                "title": publication_data.get("title", ""),
                "abstract": publication_data.get("abstract"),
                "publication_type": publication_data.get(
                    "publication_type", "journal_paper"
                ),
                "publication_date": self.serialize_date(publication_date),
                "year": publication_data.get("year")
                or (
                    publication_date.year if hasattr(publication_date, "year") else None
                ),
                "doi": publication_data.get("doi"),
                "url": publication_data.get("url"),
                "pdf_url": publication_data.get("pdf_url"),
                "journal": publication_data.get("journal")
                or publication_data.get("venue"),
                "venue": publication_data.get("venue"),
                "citation_count": publication_data.get("citation_count", 0),
                "project_domain": publication_data.get("project_domain"),
                "ai_techniques": publication_data.get("ai_techniques"),
                "geographic_scope": publication_data.get("geographic_scope"),
                "funding_source": publication_data.get("funding_source"),
                "key_outcomes": publication_data.get("key_outcomes"),
                "african_relevance_score": publication_data.get(
                    "african_relevance_score", 0.0
                ),
                "ai_relevance_score": publication_data.get("ai_relevance_score", 0.0),
                "african_entities": publication_data.get("african_entities", []),
                "keywords": publication_data.get("keywords", []),
                "source": publication_data.get("source", "systematic_review"),
                "source_id": publication_data.get("source_id")
                or publication_data.get("arxiv_id")
                or publication_data.get("pubmed_id"),
                "data_type": publication_data.get("data_type", "Academic Paper"),
                "processed_at": datetime.utcnow().isoformat(),
                "verification_status": publication_data.get(
                    "verification_status", "pending"
                ),
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
            }

            # Remove None values
            pub_record = {k: v for k, v in pub_record.items() if v is not None}

            result = self.client.table("publications").insert(pub_record).execute()

            if result.data:
                logger.info(
                    f"✅ Created publication: {publication_data.get('title', 'Unknown')[:50]}..."
                )
                return result.data[0]
            else:
                logger.error(f"❌ Failed to create publication: {result}")
                return None

        except Exception as e:
            logger.error(f"❌ Error creating publication: {e}")
            return None

    async def bulk_create_publications(
        self, publications: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Bulk create multiple publications"""
        created_publications = []

        for pub_data in publications:
            result = await self.create_publication(pub_data)
            if result:
                created_publications.append(result)

        logger.info(
            f"✅ Bulk created {len(created_publications)}/{len(publications)} publications"
        )
        return created_publications

    # INNOVATIONS
    async def create_innovation(
        self, innovation_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Create a new innovation record"""
        try:
            innovation_record = {
                "id": str(uuid4()),
                "title": innovation_data.get("title", ""),
                "description": innovation_data.get("description", ""),
                "innovation_type": innovation_data.get("innovation_type", "software"),
                "domain": innovation_data.get("domain", "other"),
                "ai_techniques_used": innovation_data.get("ai_techniques_used", []),
                "target_beneficiaries": innovation_data.get("target_beneficiaries"),
                "problem_addressed": innovation_data.get("problem_addressed")
                or innovation_data.get("problem_solved"),
                "solution_approach": innovation_data.get("solution_approach"),
                "development_stage": innovation_data.get(
                    "development_stage", "concept"
                ),
                "technology_stack": innovation_data.get("technology_stack", [])
                or innovation_data.get("tech_stack", []),
                "programming_languages": innovation_data.get(
                    "programming_languages", []
                ),
                "datasets_used": innovation_data.get("datasets_used", []),
                "countries_deployed": innovation_data.get("countries_deployed", []),
                "target_countries": innovation_data.get("target_countries", []),
                "users_reached": innovation_data.get("users_reached", 0),
                "impact_metrics": innovation_data.get("impact_metrics", {}),
                "verification_status": innovation_data.get(
                    "verification_status", "pending"
                ),
                "visibility": innovation_data.get("visibility", "public"),
                "demo_url": innovation_data.get("demo_url"),
                "github_url": innovation_data.get("github_url"),
                "documentation_url": innovation_data.get("documentation_url")
                or innovation_data.get("website_url"),
                "video_url": innovation_data.get("video_url"),
                "image_urls": innovation_data.get("image_urls", []),
                "creation_date": self.serialize_date(
                    innovation_data.get("creation_date")
                ),
                "last_updated_date": self.serialize_date(
                    innovation_data.get("last_updated_date")
                ),
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
            }

            # Remove None values
            innovation_record = {
                k: v for k, v in innovation_record.items() if v is not None
            }

            result = (
                self.client.table("innovations").insert(innovation_record).execute()
            )

            if result.data:
                logger.info(
                    f"✅ Created innovation: {innovation_data.get('title', 'Unknown')[:50]}..."
                )
                return result.data[0]
            else:
                logger.error(f"❌ Failed to create innovation: {result}")
                return None

        except Exception as e:
            logger.error(f"❌ Error creating innovation: {e}")
            return None

    # ORGANIZATIONS
    async def create_organization(
        self, org_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Create a new organization record"""
        try:
            org_record = {
                "id": str(uuid4()),
                "name": org_data.get("name", ""),
                "organization_type": org_data.get("organization_type", "unknown"),
                "country": org_data.get("country", ""),
                "website": org_data.get("website"),
                "description": org_data.get("description"),
                "founded_date": self.serialize_date(org_data.get("founded_date")),
                "contact_email": org_data.get("contact_email"),
                "logo_url": org_data.get("logo_url"),
                "verification_status": org_data.get("verification_status", "pending"),
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
            }

            # Remove None values
            org_record = {k: v for k, v in org_record.items() if v is not None}

            result = self.client.table("organizations").insert(org_record).execute()

            if result.data:
                logger.info(
                    f"✅ Created organization: {org_data.get('name', 'Unknown')}"
                )
                return result.data[0]
            else:
                logger.error(f"❌ Failed to create organization: {result}")
                return None

        except Exception as e:
            logger.error(f"❌ Error creating organization: {e}")
            return None

    # INDIVIDUALS
    async def create_individual(
        self, individual_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Create a new individual record"""
        try:
            individual_record = {
                "id": str(uuid4()),
                "name": individual_data.get("name", ""),
                "email": individual_data.get("email"),
                "role": individual_data.get("role"),
                "bio": individual_data.get("bio"),
                "country": individual_data.get("country"),
                "organization_id": individual_data.get("organization_id"),
                "linkedin_url": individual_data.get("linkedin_url"),
                "twitter_url": individual_data.get("twitter_url")
                or individual_data.get("twitter_handle"),
                "website_url": individual_data.get("website_url")
                or individual_data.get("website"),
                "orcid_id": individual_data.get("orcid_id"),
                "profile_image_url": individual_data.get("profile_image_url"),
                "expertise_areas": individual_data.get("expertise_areas", []),
                "verification_status": individual_data.get(
                    "verification_status", "pending"
                ),
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
            }

            # Remove None values
            individual_record = {
                k: v for k, v in individual_record.items() if v is not None
            }

            result = (
                self.client.table("individuals").insert(individual_record).execute()
            )

            if result.data:
                logger.info(
                    f"✅ Created individual: {individual_data.get('name', 'Unknown')}"
                )
                return result.data[0]
            else:
                logger.error(f"❌ Failed to create individual: {result}")
                return None

        except Exception as e:
            logger.error(f"❌ Error creating individual: {e}")
            return None

    # FUNDING
    async def create_funding(
        self, funding_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Create a new funding record"""
        try:
            funding_record = {
                "id": str(uuid4()),
                "innovation_id": funding_data.get("innovation_id"),
                "funder_org_id": funding_data.get("funder_org_id"),
                "funding_type": funding_data.get("funding_type", "grant"),
                "amount": funding_data.get("amount"),
                "currency": funding_data.get("currency", "USD"),
                "funding_date": funding_data.get("funding_date"),
                "duration_months": funding_data.get("duration_months"),
                "description": funding_data.get("description")
                or funding_data.get("notes"),
                "funding_program": funding_data.get("funding_program")
                or funding_data.get("funding_round"),
                "verification_status": funding_data.get(
                    "verification_status", "pending"
                ),
                "verified": funding_data.get("verified", False),
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
            }

            # Remove None values
            funding_record = {k: v for k, v in funding_record.items() if v is not None}

            result = self.client.table("fundings").insert(funding_record).execute()

            if result.data:
                logger.info("✅ Created funding record")
                return result.data[0]
            else:
                logger.error(f"❌ Failed to create funding: {result}")
                return None

        except Exception as e:
            logger.error(f"❌ Error creating funding: {e}")
            return None

    # QUERY METHODS
    async def get_publications(
        self, limit: int = 100, filters: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """Get publications with optional filters"""
        try:
            query = self.client.table("publications").select("*")

            if filters:
                for key, value in filters.items():
                    query = query.eq(key, value)

            result = query.limit(limit).execute()
            return result.data if result.data else []

        except Exception as e:
            logger.error(f"❌ Error fetching publications: {e}")
            return []

    async def get_innovations(
        self, limit: int = 100, filters: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """Get innovations with optional filters"""
        try:
            query = self.client.table("innovations").select("*")

            if filters:
                for key, value in filters.items():
                    query = query.eq(key, value)

            result = query.limit(limit).execute()
            return result.data if result.data else []

        except Exception as e:
            logger.error(f"❌ Error fetching innovations: {e}")
            return []

    async def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
        try:
            stats = {}

            # Count publications
            pub_result = (
                self.client.table("publications").select("id", count="exact").execute()
            )
            stats["total_publications"] = pub_result.count if pub_result.count else 0

            # Count innovations
            innov_result = (
                self.client.table("innovations").select("id", count="exact").execute()
            )
            stats["total_innovations"] = innov_result.count if innov_result.count else 0

            # Count organizations
            org_result = (
                self.client.table("organizations").select("id", count="exact").execute()
            )
            stats["total_organizations"] = org_result.count if org_result.count else 0

            # Count individuals
            ind_result = (
                self.client.table("individuals").select("id", count="exact").execute()
            )
            stats["total_individuals"] = ind_result.count if ind_result.count else 0

            # Count fundings
            fund_result = (
                self.client.table("fundings").select("id", count="exact").execute()
            )
            stats["total_fundings"] = fund_result.count if fund_result.count else 0

            return stats

        except Exception as e:
            logger.error(f"❌ Error fetching statistics: {e}")
            return {}

    # SEARCH METHODS
    async def search_publications(
        self, query: str, limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Search publications by title, abstract, or keywords"""
        try:
            result = (
                self.client.table("publications")
                .select("*")
                .or_(f"title.ilike.%{query}%,abstract.ilike.%{query}%")
                .limit(limit)
                .execute()
            )

            return result.data if result.data else []

        except Exception as e:
            logger.error(f"❌ Error searching publications: {e}")
            return []

    async def search_innovations(
        self, query: str, limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Search innovations by title or description"""
        try:
            result = (
                self.client.table("innovations")
                .select("*")
                .or_(f"title.ilike.%{query}%,description.ilike.%{query}%")
                .limit(limit)
                .execute()
            )

            return result.data if result.data else []

        except Exception as e:
            logger.error(f"❌ Error searching innovations: {e}")
            return []

    # RELATIONSHIP METHODS
    async def link_publication_to_innovation(
        self,
        publication_id: str,
        innovation_id: str,
        relationship_type: str = "related",
    ) -> bool:
        """Link a publication to an innovation"""
        try:
            link_record = {
                "publication_id": publication_id,
                "innovation_id": innovation_id,
                "relationship_type": relationship_type,
            }

            result = (
                self.client.table("innovation_publications")
                .insert(link_record)
                .execute()
            )

            if result.data:
                logger.info(
                    f"✅ Linked publication {publication_id} to innovation {innovation_id}"
                )
                return True
            else:
                logger.error(f"❌ Failed to link publication to innovation: {result}")
                return False

        except Exception as e:
            logger.error(f"❌ Error linking publication to innovation: {e}")
            return False

    # =============================================================================
    # AHAII-SPECIFIC METHODS FOR HEALTH AI INFRASTRUCTURE
    # =============================================================================

    async def insert_infrastructure_indicator(
        self, indicator_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Insert infrastructure indicator into AHAII schema"""
        try:
            indicator_record = {
                "id": str(uuid4()),
                "country_id": indicator_data.get("country_id"),
                "pillar": indicator_data.get("pillar"),  # 'human_capital', 'physical', 'regulatory', 'economic'
                "indicator_name": indicator_data.get("indicator_name"),
                "indicator_value": indicator_data.get("indicator_value"),
                "indicator_unit": indicator_data.get("indicator_unit"),
                "data_year": indicator_data.get("data_year"),
                "data_quarter": indicator_data.get("data_quarter"),
                "data_source": indicator_data.get("data_source", "unknown"),
                "data_source_type": indicator_data.get("data_source_type", "unknown"),
                "data_collection_method": indicator_data.get("data_collection_method"),
                "sample_size": indicator_data.get("sample_size"),
                "geographic_coverage": indicator_data.get("geographic_coverage", "national"),
                "verification_status": indicator_data.get("verification_status", "unverified"),
                "confidence_level": indicator_data.get("confidence_level", "medium"),
                "confidence_score": indicator_data.get("confidence_score"),
                "validation_notes": indicator_data.get("validation_notes"),
                "global_benchmark_available": indicator_data.get("global_benchmark_available", False),
                "global_percentile": indicator_data.get("global_percentile"),
                "african_percentile": indicator_data.get("african_percentile"),
                "regional_percentile": indicator_data.get("regional_percentile"),
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
            }
            
            # Remove None values
            indicator_record = {k: v for k, v in indicator_record.items() if v is not None}
            
            result = self.client.table("infrastructure_indicators").insert(indicator_record).execute()
            
            if result.data:
                logger.info(
                    f"✅ Created infrastructure indicator: {indicator_data.get('indicator_name', 'Unknown')} for {indicator_data.get('pillar', 'Unknown')}"
                )
                return result.data[0]
            else:
                logger.error(f"❌ Failed to create infrastructure indicator: {result}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Error creating infrastructure indicator: {e}")
            return None

    async def update_ahaii_scores(
        self, country_id: str, scores: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Update AHAII scores for a country"""
        try:
            score_record = {
                "country_id": country_id,
                "assessment_year": scores.get("assessment_year"),
                "assessment_quarter": scores.get("assessment_quarter"),
                "total_score": scores.get("total_score"),
                "global_ranking": scores.get("global_ranking"),
                "regional_ranking": scores.get("regional_ranking"),
                "sub_regional_ranking": scores.get("sub_regional_ranking"),
                
                # Pillar scores
                "human_capital_score": scores.get("human_capital_score"),
                "human_capital_clinical_literacy": scores.get("human_capital_clinical_literacy"),
                "human_capital_informatics_capacity": scores.get("human_capital_informatics_capacity"),
                "human_capital_workforce_pipeline": scores.get("human_capital_workforce_pipeline"),
                
                "physical_infrastructure_score": scores.get("physical_infrastructure_score"),
                "physical_digitization_level": scores.get("physical_digitization_level"),
                "physical_computational_capacity": scores.get("physical_computational_capacity"),
                "physical_connectivity_reliability": scores.get("physical_connectivity_reliability"),
                
                "regulatory_infrastructure_score": scores.get("regulatory_infrastructure_score"),
                "regulatory_approval_pathways": scores.get("regulatory_approval_pathways"),
                "regulatory_data_governance": scores.get("regulatory_data_governance"),
                "regulatory_market_access": scores.get("regulatory_market_access"),
                
                "economic_market_score": scores.get("economic_market_score"),
                "economic_market_maturity": scores.get("economic_market_maturity"),
                "economic_financial_sustainability": scores.get("economic_financial_sustainability"),
                "economic_research_funding": scores.get("economic_research_funding"),
                
                "readiness_tier": scores.get("readiness_tier"),
                "tier_justification": scores.get("tier_justification"),
                "overall_confidence_score": scores.get("overall_confidence_score"),
                "data_completeness_percentage": scores.get("data_completeness_percentage"),
                "expert_validation_score": scores.get("expert_validation_score"),
                "peer_review_status": scores.get("peer_review_status", "pending"),
                
                "development_trajectory": scores.get("development_trajectory"),
                "key_strengths": scores.get("key_strengths", []),
                "priority_improvement_areas": scores.get("priority_improvement_areas", []),
                "assessment_methodology_version": scores.get("assessment_methodology_version", "1.0"),
                
                "created_at": datetime.utcnow().isoformat(),
            }
            
            # Remove None values
            score_record = {k: v for k, v in score_record.items() if v is not None}
            
            # Try to update existing record first
            existing = (
                self.client.table("ahaii_scores")
                .select("id")
                .eq("country_id", country_id)
                .eq("assessment_year", scores.get("assessment_year"))
                .eq("assessment_quarter", scores.get("assessment_quarter") or 1)
                .execute()
            )
            
            if existing.data:
                # Update existing record
                result = (
                    self.client.table("ahaii_scores")
                    .update(score_record)
                    .eq("id", existing.data[0]["id"])
                    .execute()
                )
                logger.info(f"✅ Updated AHAII scores for country {country_id}")
            else:
                # Insert new record
                score_record["id"] = str(uuid4())
                result = self.client.table("ahaii_scores").insert(score_record).execute()
                logger.info(f"✅ Created AHAII scores for country {country_id}")
            
            if result.data:
                return result.data[0]
            else:
                logger.error(f"❌ Failed to update AHAII scores: {result}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Error updating AHAII scores: {e}")
            return None

    async def insert_health_ai_organization(
        self, org_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Insert health AI organization"""
        try:
            org_record = {
                "id": str(uuid4()),
                "name": org_data.get("name", ""),
                "organization_type": org_data.get("organization_type", "unknown"),
                "country_id": org_data.get("country_id"),
                "city": org_data.get("city"),
                "founding_year": org_data.get("founding_year"),
                "employee_count": org_data.get("employee_count"),
                "website": org_data.get("website"),
                "description": org_data.get("description"),
                
                # Health AI specific fields
                "primary_health_ai_focus": org_data.get("primary_health_ai_focus", []),
                "clinical_partnerships": org_data.get("clinical_partnerships", []),
                "regulatory_approvals": org_data.get("regulatory_approvals", []),
                
                # Funding and investment
                "total_funding_usd": org_data.get("total_funding_usd"),
                "latest_funding_round_usd": org_data.get("latest_funding_round_usd"),
                "latest_funding_date": self.serialize_date(org_data.get("latest_funding_date")),
                "funding_sources": org_data.get("funding_sources", []),
                
                # Clinical implementation
                "active_clinical_deployments": org_data.get("active_clinical_deployments", 0),
                "countries_with_deployments": org_data.get("countries_with_deployments", []),
                "validated_clinical_outcomes": org_data.get("validated_clinical_outcomes", False),
                "peer_reviewed_publications": org_data.get("peer_reviewed_publications", 0),
                
                # International recognition
                "who_collaboration": org_data.get("who_collaboration", False),
                "international_partnerships": org_data.get("international_partnerships", []),
                "global_health_initiatives": org_data.get("global_health_initiatives", []),
                
                # Infrastructure contributions
                "contributes_to_human_capital": org_data.get("contributes_to_human_capital", False),
                "contributes_to_physical_infra": org_data.get("contributes_to_physical_infra", False),
                "contributes_to_regulatory_framework": org_data.get("contributes_to_regulatory_framework", False),
                "contributes_to_market_development": org_data.get("contributes_to_market_development", False),
                
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
            }
            
            # Remove None values
            org_record = {k: v for k, v in org_record.items() if v is not None}
            
            result = self.client.table("health_ai_organizations").insert(org_record).execute()
            
            if result.data:
                logger.info(
                    f"✅ Created health AI organization: {org_data.get('name', 'Unknown')}"
                )
                return result.data[0]
            else:
                logger.error(f"❌ Failed to create health AI organization: {result}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Error creating health AI organization: {e}")
            return None

    async def insert_infrastructure_intelligence(
        self, intelligence_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Insert infrastructure intelligence from ETL pipeline"""
        try:
            intelligence_record = {
                "id": str(uuid4()),
                "report_type": intelligence_data.get("report_type"),  # 'academic_scan', 'news_monitoring', etc.
                "country_id": intelligence_data.get("country_id"),
                "report_title": intelligence_data.get("report_title", ""),
                "report_summary": intelligence_data.get("report_summary"),
                "key_findings": intelligence_data.get("key_findings", {}),
                
                # Source information
                "source_type": intelligence_data.get("source_type"),
                "source_url": intelligence_data.get("source_url"),
                "source_publication": intelligence_data.get("source_publication"),
                "publication_date": self.serialize_date(intelligence_data.get("publication_date")),
                
                # Infrastructure impact
                "affects_human_capital": intelligence_data.get("affects_human_capital", False),
                "affects_physical_infrastructure": intelligence_data.get("affects_physical_infrastructure", False),
                "affects_regulatory_framework": intelligence_data.get("affects_regulatory_framework", False),
                "affects_economic_market": intelligence_data.get("affects_economic_market", False),
                
                "impact_significance": intelligence_data.get("impact_significance", "low"),
                
                # Processing metadata
                "processed_by_ai": intelligence_data.get("processed_by_ai", True),
                "confidence_score": intelligence_data.get("confidence_score"),
                "verification_status": intelligence_data.get("verification_status", "pending"),
                
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
            }
            
            # Remove None values
            intelligence_record = {k: v for k, v in intelligence_record.items() if v is not None}
            
            result = self.client.table("infrastructure_intelligence").insert(intelligence_record).execute()
            
            if result.data:
                logger.info(
                    f"✅ Created infrastructure intelligence: {intelligence_data.get('report_title', 'Unknown')[:50]}..."
                )
                return result.data[0]
            else:
                logger.error(f"❌ Failed to create infrastructure intelligence: {result}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Error creating infrastructure intelligence: {e}")
            return None

    # AHAII-specific query methods
    async def get_country_by_iso_code(self, iso_code: str) -> Optional[Dict[str, Any]]:
        """Get country by ISO code"""
        try:
            result = (
                self.client.table("countries")
                .select("*")
                .eq("iso_code_alpha3", iso_code.upper())
                .execute()
            )
            
            if result.data:
                return result.data[0]
            else:
                return None
                
        except Exception as e:
            logger.error(f"❌ Error fetching country by ISO code {iso_code}: {e}")
            return None

    async def get_latest_ahaii_scores(self, country_id: str) -> Optional[Dict[str, Any]]:
        """Get latest AHAII scores for a country"""
        try:
            result = (
                self.client.table("ahaii_scores")
                .select("*")
                .eq("country_id", country_id)
                .order("assessment_year.desc")
                .order("assessment_quarter.desc")
                .limit(1)
                .execute()
            )
            
            if result.data:
                return result.data[0]
            else:
                return None
                
        except Exception as e:
            logger.error(f"❌ Error fetching latest AHAII scores for {country_id}: {e}")
            return None

    async def get_infrastructure_indicators_by_pillar(
        self, country_id: str, pillar: str, data_year: int = None
    ) -> List[Dict[str, Any]]:
        """Get infrastructure indicators by pillar for a country"""
        try:
            query = (
                self.client.table("infrastructure_indicators")
                .select("*")
                .eq("country_id", country_id)
                .eq("pillar", pillar)
            )
            
            if data_year:
                query = query.eq("data_year", data_year)
            
            result = query.execute()
            return result.data if result.data else []
            
        except Exception as e:
            logger.error(f"❌ Error fetching infrastructure indicators: {e}")
            return []

    async def get_ahaii_statistics(self) -> Dict[str, Any]:
        """Get AHAII database statistics"""
        try:
            stats = {}
            
            # Count countries
            country_result = (
                self.client.table("countries").select("id", count="exact").execute()
            )
            stats["total_countries"] = country_result.count if country_result.count else 0
            
            # Count infrastructure indicators
            indicator_result = (
                self.client.table("infrastructure_indicators").select("id", count="exact").execute()
            )
            stats["total_infrastructure_indicators"] = indicator_result.count if indicator_result.count else 0
            
            # Count health AI organizations
            org_result = (
                self.client.table("health_ai_organizations").select("id", count="exact").execute()
            )
            stats["total_health_ai_organizations"] = org_result.count if org_result.count else 0
            
            # Count infrastructure intelligence
            intel_result = (
                self.client.table("infrastructure_intelligence").select("id", count="exact").execute()
            )
            stats["total_infrastructure_intelligence"] = intel_result.count if intel_result.count else 0
            
            # Count AHAII scores
            scores_result = (
                self.client.table("ahaii_scores").select("id", count="exact").execute()
            )
            stats["total_ahaii_assessments"] = scores_result.count if scores_result.count else 0
            
            return stats
            
        except Exception as e:
            logger.error(f"❌ Error fetching AHAII statistics: {e}")
            return {}


# Global database service instance
db_service = DatabaseService()
