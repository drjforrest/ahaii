"""
AHAII Data Models
SQLAlchemy models for AHAII quantitative assessment data
"""

from datetime import datetime
from typing import Dict, Any, Optional
from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime, JSON, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from enum import Enum

Base = declarative_base()

class AHAIITier(Enum):
    """AHAII Infrastructure Readiness Tiers"""
    IMPLEMENTATION_READY = 1  # 70+ points
    FOUNDATION_BUILDING = 2   # 40-69 points  
    DEVELOPMENT = 3           # 0-39 points

class PillarName(Enum):
    """AHAII Infrastructure Pillars"""
    HUMAN_CAPITAL = "human_capital"
    PHYSICAL_INFRASTRUCTURE = "physical_infrastructure"
    REGULATORY_FRAMEWORK = "regulatory_framework"
    ECONOMIC_MARKET = "economic_market"

# SQLAlchemy Models

class AHAIIAssessment(Base):
    """
    Main AHAII assessment record
    """
    __tablename__ = "ahaii_assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(String(50), unique=True, index=True, nullable=False)
    assessment_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    methodology_version = Column(String(10), default="1.0", nullable=False)
    
    # Assessment metadata
    countries_assessed = Column(JSON)  # List of country codes
    total_countries = Column(Integer, nullable=False)
    data_collection_status = Column(String(20), default="pending")  # pending, in_progress, completed, failed
    scoring_status = Column(String(20), default="pending")
    validation_status = Column(String(20), default="pending")
    report_status = Column(String(20), default="pending")
    
    # Overall statistics
    regional_average_score = Column(Float)
    data_quality_grade = Column(String(1))  # A, B, C, D, F
    expert_validation_coverage = Column(Float)  # Percentage of indicators validated
    
    # Relationships
    country_scores = relationship("AHAIICountryScore", back_populates="assessment", cascade="all, delete-orphan")
    data_collection_runs = relationship("DataCollectionRun", back_populates="assessment", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('idx_assessment_date', 'assessment_date'),
        Index('idx_assessment_status', 'data_collection_status', 'scoring_status'),
    )

class AHAIICountryScore(Base):
    """
    AHAII scores for individual countries
    """
    __tablename__ = "ahaii_country_scores"
    
    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(String(50), ForeignKey("ahaii_assessments.assessment_id"), nullable=False)
    country_code = Column(String(3), nullable=False)
    country_name = Column(String(100), nullable=False)
    
    # Core scores
    total_score = Column(Float, nullable=False)
    overall_confidence = Column(Float, nullable=False)
    tier_classification = Column(Integer, nullable=False)  # 1, 2, or 3
    regional_rank = Column(Integer)
    
    # Confidence intervals
    confidence_interval_lower = Column(Float)
    confidence_interval_upper = Column(Float)
    confidence_level = Column(Float, default=0.95)
    
    # Data quality metrics
    data_quality_grade = Column(String(1))
    data_completeness_pct = Column(Float)
    expert_validation_status = Column(String(50))
    
    # Timestamps
    calculation_date = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    assessment = relationship("AHAIIAssessment", back_populates="country_scores")
    pillar_scores = relationship("AHAIIPillarScore", back_populates="country_score", cascade="all, delete-orphan")
    indicators = relationship("AHAIIIndicatorValue", back_populates="country_score", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('idx_country_assessment', 'assessment_id', 'country_code'),
        Index('idx_country_score', 'total_score'),
        Index('idx_country_tier', 'tier_classification'),
    )

class AHAIIPillarScore(Base):
    """
    Individual pillar scores for countries
    """
    __tablename__ = "ahaii_pillar_scores"
    
    id = Column(Integer, primary_key=True, index=True)
    country_score_id = Column(Integer, ForeignKey("ahaii_country_scores.id"), nullable=False)
    pillar_name = Column(String(30), nullable=False)
    
    # Pillar performance
    score = Column(Float, nullable=False)
    confidence = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    
    # Sub-component breakdown
    sub_components = Column(JSON)  # Dict of sub-component scores
    normalized_indicators = Column(JSON)  # Dict of normalized indicator values
    
    # Analysis
    improvement_potential = Column(Float)
    key_constraints = Column(JSON)  # List of key constraint descriptions
    proxy_applications = Column(JSON)  # List of proxy indicators used
    
    # Regional context
    regional_percentile = Column(Float)
    regional_tier = Column(String(20))
    
    # Relationships
    country_score = relationship("AHAIICountryScore", back_populates="pillar_scores")
    
    # Indexes
    __table_args__ = (
        Index('idx_pillar_country', 'country_score_id', 'pillar_name'),
        Index('idx_pillar_score', 'pillar_name', 'score'),
    )

class AHAIIIndicatorValue(Base):
    """
    Individual indicator values used in AHAII calculation
    """
    __tablename__ = "ahaii_indicator_values"
    
    id = Column(Integer, primary_key=True, index=True)
    country_score_id = Column(Integer, ForeignKey("ahaii_country_scores.id"), nullable=False)
    
    # Indicator identification
    indicator_code = Column(String(50), nullable=False)
    indicator_name = Column(String(100), nullable=False)
    indicator_type = Column(String(20), nullable=False)  # quantitative, policy, ecosystem
    pillar_name = Column(String(30), nullable=False)
    
    # Values
    raw_value = Column(Float)
    normalized_value = Column(Float)
    confidence_score = Column(Float, nullable=False)
    
    # Data provenance
    data_source = Column(String(50), nullable=False)
    collection_date = Column(DateTime, nullable=False)
    year = Column(Integer)  # Data year (may differ from collection date)
    
    # Validation
    expert_validated = Column(Boolean, default=False)
    validation_confidence = Column(Float)
    is_proxy_value = Column(Boolean, default=False)
    proxy_source_indicator = Column(String(100))
    
    # Relationships
    country_score = relationship("AHAIICountryScore", back_populates="indicators")
    
    # Indexes
    __table_args__ = (
        Index('idx_indicator_country', 'country_score_id', 'indicator_code'),
        Index('idx_indicator_type', 'indicator_type', 'pillar_name'),
        Index('idx_indicator_source', 'data_source'),
    )

class DataCollectionRun(Base):
    """
    Data collection execution tracking
    """
    __tablename__ = "data_collection_runs"
    
    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(String(50), ForeignKey("ahaii_assessments.assessment_id"), nullable=False)
    run_id = Column(String(50), unique=True, nullable=False)
    
    # Run metadata
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    status = Column(String(20), default="running")  # running, completed, failed
    
    # Collection components
    world_bank_status = Column(String(20), default="pending")
    policy_indicators_status = Column(String(20), default="pending")
    ecosystem_mapping_status = Column(String(20), default="pending")
    
    # Results summary
    total_data_points_collected = Column(Integer, default=0)
    world_bank_indicators = Column(Integer, default=0)
    policy_indicators = Column(Integer, default=0)
    ecosystem_organizations = Column(Integer, default=0)
    
    # Error tracking
    error_count = Column(Integer, default=0)
    error_details = Column(JSON)
    
    # Relationships
    assessment = relationship("AHAIIAssessment", back_populates="data_collection_runs")
    
    # Indexes
    __table_args__ = (
        Index('idx_collection_run_status', 'status'),
        Index('idx_collection_run_time', 'start_time'),
    )

class ExpertValidationResult(Base):
    """
    Expert validation results for uncertain indicators
    """
    __tablename__ = "expert_validation_results"
    
    id = Column(Integer, primary_key=True, index=True)
    validation_request_id = Column(String(50), unique=True, nullable=False)
    
    # Request details
    country_code = Column(String(3), nullable=False)
    indicator_name = Column(String(100), nullable=False)
    indicator_type = Column(String(20), nullable=False)
    
    # Original vs validated values
    original_value = Column(String(100))
    consensus_value = Column(String(100))
    consensus_confidence = Column(Float)
    
    # Expert consensus
    expert_agreement = Column(Float)
    response_count = Column(Integer)
    validation_method = Column(String(50))
    
    # Status
    final_status = Column(String(20))  # validated, disputed, pending
    consensus_date = Column(DateTime)
    
    # Evidence and reasoning
    evidence_sources = Column(JSON)
    expert_reasoning = Column(Text)
    
    # Indexes
    __table_args__ = (
        Index('idx_validation_country', 'country_code', 'indicator_name'),
        Index('idx_validation_status', 'final_status'),
    )

# Pydantic Models for API

class AHAIIAssessmentRequest(BaseModel):
    """Request model for AHAII assessment"""
    countries: list[str] = ["ZAF", "KEN", "NGA", "GHA", "EGY"]
    include_policy_indicators: bool = True
    include_ecosystem_mapping: bool = True
    include_expert_validation: bool = True
    generate_report: bool = True
    methodology_version: str = "1.0"

class AHAIICountryScoreResponse(BaseModel):
    """Response model for country scores"""
    country_code: str
    country_name: str
    total_score: float
    tier: int
    regional_rank: Optional[int]
    pillar_scores: Dict[str, float]
    confidence_score: float
    confidence_interval: Optional[tuple[float, float]]
    data_quality_grade: Optional[str]
    
    class Config:
        from_attributes = True

class AHAIIPillarScoreResponse(BaseModel):
    """Response model for pillar scores"""
    pillar_name: str
    score: float
    confidence: float
    weight: float
    sub_components: Dict[str, float]
    improvement_potential: Optional[float]
    key_constraints: Optional[list[str]]
    regional_percentile: Optional[float]
    
    class Config:
        from_attributes = True

class AHAIIAssessmentResponse(BaseModel):
    """Response model for complete assessment"""
    assessment_id: str
    assessment_date: str
    methodology_version: str
    countries_assessed: list[str]
    total_countries: int
    regional_average_score: Optional[float]
    data_quality_grade: Optional[str]
    country_scores: list[AHAIICountryScoreResponse]
    
    class Config:
        from_attributes = True

class DataCollectionStatusResponse(BaseModel):
    """Response model for data collection status"""
    run_id: str
    status: str
    start_time: str
    world_bank_status: str
    policy_indicators_status: str
    ecosystem_mapping_status: str
    total_data_points_collected: int
    error_count: int
    
    class Config:
        from_attributes = True

class AHAIIIndicatorResponse(BaseModel):
    """Response model for individual indicators"""
    indicator_code: str
    indicator_name: str
    indicator_type: str
    pillar_name: str
    raw_value: Optional[float]
    normalized_value: Optional[float]
    confidence_score: float
    data_source: str
    year: Optional[int]
    expert_validated: bool
    is_proxy_value: bool
    
    class Config:
        from_attributes = True

# Database helper functions

def create_ahaii_tables(engine):
    """Create all AHAII tables"""
    Base.metadata.create_all(bind=engine)

def get_latest_assessment(db_session) -> Optional[AHAIIAssessment]:
    """Get the most recent AHAII assessment"""
    return db_session.query(AHAIIAssessment).order_by(
        AHAIIAssessment.assessment_date.desc()
    ).first()

def get_country_scores_by_assessment(db_session, assessment_id: str) -> list[AHAIICountryScore]:
    """Get all country scores for a specific assessment"""
    return db_session.query(AHAIICountryScore).filter(
        AHAIICountryScore.assessment_id == assessment_id
    ).order_by(AHAIICountryScore.total_score.desc()).all()

def get_pillar_scores_by_country(db_session, country_score_id: int) -> list[AHAIIPillarScore]:
    """Get all pillar scores for a specific country"""
    return db_session.query(AHAIIPillarScore).filter(
        AHAIIPillarScore.country_score_id == country_score_id
    ).all()

def get_indicators_by_country(db_session, country_score_id: int) -> list[AHAIIIndicatorValue]:
    """Get all indicators for a specific country"""
    return db_session.query(AHAIIIndicatorValue).filter(
        AHAIIIndicatorValue.country_score_id == country_score_id
    ).order_by(AHAIIIndicatorValue.pillar_name, AHAIIIndicatorValue.indicator_name).all()

def get_assessment_history(db_session, country_code: str, limit: int = 10) -> list[AHAIICountryScore]:
    """Get assessment history for a specific country"""
    return db_session.query(AHAIICountryScore).filter(
        AHAIICountryScore.country_code == country_code
    ).order_by(AHAIICountryScore.calculation_date.desc()).limit(limit).all()

def get_regional_rankings(db_session, assessment_id: str) -> list[tuple]:
    """Get regional rankings for an assessment"""
    return db_session.query(
        AHAIICountryScore.country_name,
        AHAIICountryScore.total_score,
        AHAIICountryScore.tier_classification,
        AHAIICountryScore.regional_rank
    ).filter(
        AHAIICountryScore.assessment_id == assessment_id
    ).order_by(AHAIICountryScore.regional_rank).all()