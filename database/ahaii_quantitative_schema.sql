-- AHAII Quantitative Assessment Database Schema
-- African Health AI Infrastructure Index - Enhanced with Phase 2 Quantitative Data Models

-- Main AHAII assessment tracking table
CREATE TABLE IF NOT EXISTS ahaii_assessments (
    id SERIAL PRIMARY KEY,
    assessment_id VARCHAR(50) UNIQUE NOT NULL,
    assessment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    methodology_version VARCHAR(10) DEFAULT '1.0' NOT NULL,
    
    -- Assessment metadata
    countries_assessed JSONB,
    total_countries INTEGER NOT NULL,
    data_collection_status VARCHAR(20) DEFAULT 'pending',
    scoring_status VARCHAR(20) DEFAULT 'pending',
    validation_status VARCHAR(20) DEFAULT 'pending',
    report_status VARCHAR(20) DEFAULT 'pending',
    
    -- Overall statistics
    regional_average_score FLOAT,
    data_quality_grade CHAR(1),
    expert_validation_coverage FLOAT,
    
    -- Indexes
    CONSTRAINT chk_data_collection_status CHECK (data_collection_status IN ('pending', 'in_progress', 'completed', 'failed')),
    CONSTRAINT chk_scoring_status CHECK (scoring_status IN ('pending', 'in_progress', 'completed', 'failed')),
    CONSTRAINT chk_validation_status CHECK (validation_status IN ('pending', 'in_progress', 'completed', 'failed')),
    CONSTRAINT chk_report_status CHECK (report_status IN ('pending', 'in_progress', 'completed', 'failed')),
    CONSTRAINT chk_data_quality_grade CHECK (data_quality_grade IN ('A', 'B', 'C', 'D', 'F'))
);

CREATE INDEX IF NOT EXISTS idx_assessment_date ON ahaii_assessments(assessment_date);
CREATE INDEX IF NOT EXISTS idx_assessment_status ON ahaii_assessments(data_collection_status, scoring_status);

-- Country scores for each assessment
CREATE TABLE IF NOT EXISTS ahaii_country_scores (
    id SERIAL PRIMARY KEY,
    assessment_id VARCHAR(50) REFERENCES ahaii_assessments(assessment_id) ON DELETE CASCADE,
    country_code CHAR(3) NOT NULL,
    country_name VARCHAR(100) NOT NULL,
    
    -- Core scores
    total_score FLOAT NOT NULL,
    overall_confidence FLOAT NOT NULL,
    tier_classification INTEGER NOT NULL,
    regional_rank INTEGER,
    
    -- Confidence intervals
    confidence_interval_lower FLOAT,
    confidence_interval_upper FLOAT,
    confidence_level FLOAT DEFAULT 0.95,
    
    -- Data quality metrics
    data_quality_grade CHAR(1),
    data_completeness_pct FLOAT,
    expert_validation_status VARCHAR(50),
    
    -- Timestamps
    calculation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT chk_tier_classification CHECK (tier_classification IN (1, 2, 3)),
    CONSTRAINT chk_total_score CHECK (total_score >= 0 AND total_score <= 100),
    CONSTRAINT chk_confidence CHECK (overall_confidence >= 0 AND overall_confidence <= 1),
    CONSTRAINT chk_country_quality_grade CHECK (data_quality_grade IN ('A', 'B', 'C', 'D', 'F'))
);

CREATE INDEX IF NOT EXISTS idx_country_assessment ON ahaii_country_scores(assessment_id, country_code);
CREATE INDEX IF NOT EXISTS idx_country_score ON ahaii_country_scores(total_score);
CREATE INDEX IF NOT EXISTS idx_country_tier ON ahaii_country_scores(tier_classification);

-- Pillar scores breakdown
CREATE TABLE IF NOT EXISTS ahaii_pillar_scores (
    id SERIAL PRIMARY KEY,
    country_score_id INTEGER REFERENCES ahaii_country_scores(id) ON DELETE CASCADE,
    pillar_name VARCHAR(30) NOT NULL,
    
    -- Pillar performance
    score FLOAT NOT NULL,
    confidence FLOAT NOT NULL,
    weight FLOAT NOT NULL,
    
    -- Sub-component breakdown
    sub_components JSONB,
    normalized_indicators JSONB,
    
    -- Analysis
    improvement_potential FLOAT,
    key_constraints JSONB,
    proxy_applications JSONB,
    
    -- Regional context
    regional_percentile FLOAT,
    regional_tier VARCHAR(20),
    
    -- Constraints
    CONSTRAINT chk_pillar_name CHECK (pillar_name IN ('human_capital', 'physical_infrastructure', 'regulatory_framework', 'economic_market')),
    CONSTRAINT chk_pillar_score CHECK (score >= 0 AND score <= 100),
    CONSTRAINT chk_pillar_confidence CHECK (confidence >= 0 AND confidence <= 1),
    CONSTRAINT chk_pillar_weight CHECK (weight >= 0 AND weight <= 1)
);

CREATE INDEX IF NOT EXISTS idx_pillar_country ON ahaii_pillar_scores(country_score_id, pillar_name);
CREATE INDEX IF NOT EXISTS idx_pillar_score ON ahaii_pillar_scores(pillar_name, score);

-- Individual indicator values
CREATE TABLE IF NOT EXISTS ahaii_indicator_values (
    id SERIAL PRIMARY KEY,
    country_score_id INTEGER REFERENCES ahaii_country_scores(id) ON DELETE CASCADE,
    
    -- Indicator identification
    indicator_code VARCHAR(50) NOT NULL,
    indicator_name VARCHAR(100) NOT NULL,
    indicator_type VARCHAR(20) NOT NULL,
    pillar_name VARCHAR(30) NOT NULL,
    
    -- Values
    raw_value FLOAT,
    normalized_value FLOAT,
    confidence_score FLOAT NOT NULL,
    
    -- Data provenance
    data_source VARCHAR(50) NOT NULL,
    collection_date TIMESTAMP NOT NULL,
    year INTEGER,
    
    -- Validation
    expert_validated BOOLEAN DEFAULT FALSE,
    validation_confidence FLOAT,
    is_proxy_value BOOLEAN DEFAULT FALSE,
    proxy_source_indicator VARCHAR(100),
    
    -- Constraints
    CONSTRAINT chk_indicator_type CHECK (indicator_type IN ('quantitative', 'policy', 'ecosystem')),
    CONSTRAINT chk_indicator_pillar CHECK (pillar_name IN ('human_capital', 'physical_infrastructure', 'regulatory_framework', 'economic_market')),
    CONSTRAINT chk_normalized_value CHECK (normalized_value IS NULL OR (normalized_value >= 0 AND normalized_value <= 100)),
    CONSTRAINT chk_indicator_confidence CHECK (confidence_score >= 0 AND confidence_score <= 1)
);

CREATE INDEX IF NOT EXISTS idx_indicator_country ON ahaii_indicator_values(country_score_id, indicator_code);
CREATE INDEX IF NOT EXISTS idx_indicator_type ON ahaii_indicator_values(indicator_type, pillar_name);
CREATE INDEX IF NOT EXISTS idx_indicator_source ON ahaii_indicator_values(data_source);

-- Data collection run tracking
CREATE TABLE IF NOT EXISTS data_collection_runs (
    id SERIAL PRIMARY KEY,
    assessment_id VARCHAR(50) REFERENCES ahaii_assessments(assessment_id) ON DELETE CASCADE,
    run_id VARCHAR(50) UNIQUE NOT NULL,
    
    -- Run metadata
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    status VARCHAR(20) DEFAULT 'running',
    
    -- Collection components
    world_bank_status VARCHAR(20) DEFAULT 'pending',
    policy_indicators_status VARCHAR(20) DEFAULT 'pending',
    ecosystem_mapping_status VARCHAR(20) DEFAULT 'pending',
    
    -- Results summary
    total_data_points_collected INTEGER DEFAULT 0,
    world_bank_indicators INTEGER DEFAULT 0,
    policy_indicators INTEGER DEFAULT 0,
    ecosystem_organizations INTEGER DEFAULT 0,
    
    -- Error tracking
    error_count INTEGER DEFAULT 0,
    error_details JSONB,
    
    -- Constraints
    CONSTRAINT chk_run_status CHECK (status IN ('running', 'completed', 'failed')),
    CONSTRAINT chk_wb_status CHECK (world_bank_status IN ('pending', 'running', 'completed', 'failed')),
    CONSTRAINT chk_policy_status CHECK (policy_indicators_status IN ('pending', 'running', 'completed', 'failed')),
    CONSTRAINT chk_ecosystem_status CHECK (ecosystem_mapping_status IN ('pending', 'running', 'completed', 'failed'))
);

CREATE INDEX IF NOT EXISTS idx_collection_run_status ON data_collection_runs(status);
CREATE INDEX IF NOT EXISTS idx_collection_run_time ON data_collection_runs(start_time);

-- Expert validation results
CREATE TABLE IF NOT EXISTS expert_validation_results (
    id SERIAL PRIMARY KEY,
    validation_request_id VARCHAR(50) UNIQUE NOT NULL,
    
    -- Request details
    country_code CHAR(3) NOT NULL,
    indicator_name VARCHAR(100) NOT NULL,
    indicator_type VARCHAR(20) NOT NULL,
    
    -- Original vs validated values
    original_value TEXT,
    consensus_value TEXT,
    consensus_confidence FLOAT,
    
    -- Expert consensus
    expert_agreement FLOAT,
    response_count INTEGER,
    validation_method VARCHAR(50),
    
    -- Status
    final_status VARCHAR(20),
    consensus_date TIMESTAMP,
    
    -- Evidence and reasoning
    evidence_sources JSONB,
    expert_reasoning TEXT,
    
    -- Constraints
    CONSTRAINT chk_validation_type CHECK (indicator_type IN ('quantitative', 'policy', 'ecosystem')),
    CONSTRAINT chk_validation_status CHECK (final_status IN ('validated', 'disputed', 'pending', 'rejected')),
    CONSTRAINT chk_consensus_confidence CHECK (consensus_confidence IS NULL OR (consensus_confidence >= 0 AND consensus_confidence <= 1)),
    CONSTRAINT chk_expert_agreement CHECK (expert_agreement IS NULL OR (expert_agreement >= 0 AND expert_agreement <= 1))
);

CREATE INDEX IF NOT EXISTS idx_validation_country ON expert_validation_results(country_code, indicator_name);
CREATE INDEX IF NOT EXISTS idx_validation_status ON expert_validation_results(final_status);

-- Regional benchmarks table
CREATE TABLE IF NOT EXISTS ahaii_regional_benchmarks (
    id SERIAL PRIMARY KEY,
    region VARCHAR(50) NOT NULL,
    indicator_name VARCHAR(100) NOT NULL,
    
    -- Benchmark statistics
    mean_value FLOAT,
    median_value FLOAT,
    percentile_75 FLOAT,
    percentile_25 FLOAT,
    
    -- Data quality
    countries_with_data INTEGER,
    total_countries INTEGER,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(region, indicator_name)
);

CREATE INDEX IF NOT EXISTS idx_regional_benchmark ON ahaii_regional_benchmarks(region, indicator_name);

-- Views for common queries

-- Country ranking view
CREATE OR REPLACE VIEW ahaii_country_rankings AS
SELECT 
    cs.assessment_id,
    cs.country_code,
    cs.country_name,
    cs.total_score,
    cs.tier_classification,
    cs.regional_rank,
    cs.overall_confidence,
    cs.data_quality_grade,
    a.assessment_date
FROM ahaii_country_scores cs
JOIN ahaii_assessments a ON cs.assessment_id = a.assessment_id
ORDER BY cs.total_score DESC;

-- Latest assessment view
CREATE OR REPLACE VIEW ahaii_latest_assessment AS
SELECT 
    cs.*,
    a.assessment_date,
    a.methodology_version
FROM ahaii_country_scores cs
JOIN ahaii_assessments a ON cs.assessment_id = a.assessment_id
WHERE a.assessment_date = (
    SELECT MAX(assessment_date) 
    FROM ahaii_assessments 
    WHERE data_collection_status = 'completed' 
    AND scoring_status = 'completed'
);

-- Pillar performance summary view
CREATE OR REPLACE VIEW ahaii_pillar_summary AS
SELECT 
    ps.country_score_id,
    cs.country_code,
    cs.country_name,
    cs.assessment_id,
    ps.pillar_name,
    ps.score,
    ps.confidence,
    ps.regional_percentile,
    ps.improvement_potential
FROM ahaii_pillar_scores ps
JOIN ahaii_country_scores cs ON ps.country_score_id = cs.id;

-- Data quality summary view
CREATE OR REPLACE VIEW ahaii_data_quality_summary AS
SELECT 
    cs.assessment_id,
    cs.country_code,
    cs.country_name,
    cs.data_quality_grade,
    cs.data_completeness_pct,
    COUNT(iv.id) as total_indicators,
    COUNT(CASE WHEN iv.expert_validated = TRUE THEN 1 END) as validated_indicators,
    COUNT(CASE WHEN iv.is_proxy_value = TRUE THEN 1 END) as proxy_indicators,
    AVG(iv.confidence_score) as avg_confidence
FROM ahaii_country_scores cs
LEFT JOIN ahaii_indicator_values iv ON cs.id = iv.country_score_id
GROUP BY cs.id, cs.assessment_id, cs.country_code, cs.country_name, cs.data_quality_grade, cs.data_completeness_pct;

-- Functions for common operations

-- Function to get latest country score
CREATE OR REPLACE FUNCTION get_latest_country_score(p_country_code CHAR(3))
RETURNS TABLE(
    country_code CHAR(3),
    country_name VARCHAR(100),
    total_score FLOAT,
    tier_classification INTEGER,
    regional_rank INTEGER,
    assessment_date TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        cs.country_code,
        cs.country_name,
        cs.total_score,
        cs.tier_classification,
        cs.regional_rank,
        a.assessment_date
    FROM ahaii_country_scores cs
    JOIN ahaii_assessments a ON cs.assessment_id = a.assessment_id
    WHERE cs.country_code = p_country_code
    ORDER BY a.assessment_date DESC
    LIMIT 1;
END;
$$ LANGUAGE plpgsql;

-- Function to calculate regional averages
CREATE OR REPLACE FUNCTION calculate_regional_averages(p_assessment_id VARCHAR(50))
RETURNS TABLE(
    pillar_name VARCHAR(30),
    regional_average FLOAT,
    country_count INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        ps.pillar_name,
        AVG(ps.score) as regional_average,
        COUNT(DISTINCT ps.country_score_id)::INTEGER as country_count
    FROM ahaii_pillar_scores ps
    JOIN ahaii_country_scores cs ON ps.country_score_id = cs.id
    WHERE cs.assessment_id = p_assessment_id
    GROUP BY ps.pillar_name;
END;
$$ LANGUAGE plpgsql;

-- Insert sample data for testing (commented out for production)
-- This would be populated by the AHAII assessment pipeline

-- Sample assessment
-- INSERT INTO ahaii_assessments (assessment_id, countries_assessed, total_countries, data_collection_status, scoring_status) 
-- VALUES ('ahaii_pilot_2024', '["ZAF", "KEN", "NGA", "GHA", "EGY"]', 5, 'completed', 'completed');

-- Grant permissions (adjust as needed for your environment)
-- GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO ahaii_user;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO ahaii_user;