CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE pipeline_run_log (
    pipeline_run_id VARCHAR PRIMARY KEY,
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    status VARCHAR,
    duration_seconds DOUBLE,
    error_message VARCHAR
);

CREATE TABLE source_ingestion_log (
    pipeline_run_id VARCHAR,
    source_name VARCHAR,
    source_url VARCHAR,
    extraction_timestamp TIMESTAMPTZ,
    source_updated_at TIMESTAMPTZ,
    source_file_name VARCHAR,
    source_file_hash VARCHAR,
    season VARCHAR,
    competition VARCHAR,
    record_count BIGINT,
    load_type VARCHAR,
    status VARCHAR,
    duration_seconds DOUBLE,
    error_message VARCHAR
);

CREATE TABLE data_quality_results (
    pipeline_run_id VARCHAR,
    rule_name VARCHAR,
    severity VARCHAR,
    status VARCHAR,
    issue_count BIGINT,
    checked_at TIMESTAMPTZ
);

CREATE TABLE entity_matching_review (
    review_id BIGINT,
    source_name VARCHAR,
    source_entity_id VARCHAR,
    candidate_entity_key BIGINT,
    confidence DOUBLE,
    decision VARCHAR,
    reason VARCHAR,
    created_at TIMESTAMPTZ
);

CREATE TABLE schema_change_log (
    pipeline_run_id VARCHAR,
    source_name VARCHAR,
    detected_at TIMESTAMPTZ,
    table_name VARCHAR,
    change_type VARCHAR,
    details VARCHAR
);

