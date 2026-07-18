CREATE VIEW powerbi_fact_player_statistics AS SELECT * FROM fact_player_season_statistics;
CREATE VIEW powerbi_last_refresh AS
SELECT MAX(extraction_timestamp) AS last_refresh, ANY_VALUE(source_name) AS source_name,
       ANY_VALUE(source_file_hash) AS source_file_hash
FROM source_ingestion_log;

