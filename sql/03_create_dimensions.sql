CREATE TABLE dim_countries AS
SELECT CAST(country_id AS BIGINT) AS country_key,
       CAST(country_id AS VARCHAR) AS source_country_id,
       country_name, country_code, confederation
FROM raw.countries;

CREATE TABLE dim_competitions AS
SELECT ROW_NUMBER() OVER (ORDER BY competition_id) AS competition_key,
       competition_id AS source_competition_id,
       competition_code, name AS competition_name, sub_type, type AS competition_type,
       country_id AS source_country_id, country_name, confederation
FROM raw.competitions;

CREATE TABLE dim_clubs AS
WITH source_clubs AS (
    SELECT TRY_CAST(club_id AS BIGINT) AS source_club_id, name AS club_name,
           domestic_competition_id, squad_size, average_age, stadium_name, last_season,
           ROW_NUMBER() OVER (PARTITION BY TRY_CAST(club_id AS BIGINT) ORDER BY name) AS rn
    FROM raw.clubs
), transfer_clubs AS (
    SELECT source_club_id, ANY_VALUE(club_name) AS club_name
    FROM (
        SELECT from_club_id AS source_club_id, from_club_name AS club_name FROM raw.transfers
        UNION ALL
        SELECT to_club_id AS source_club_id, to_club_name AS club_name FROM raw.transfers
    ) t
    GROUP BY source_club_id
), all_clubs AS (
    SELECT * FROM source_clubs
    UNION ALL
    SELECT t.source_club_id, t.club_name, NULL, NULL, NULL, NULL, NULL, 1
    FROM transfer_clubs t
    WHERE NOT EXISTS (
        SELECT 1 FROM source_clubs c
        WHERE c.source_club_id = t.source_club_id
    )
)
SELECT source_club_id AS club_key, source_club_id, club_name, domestic_competition_id,
       c.country_name, squad_size, average_age, stadium_name, last_season
FROM all_clubs a
LEFT JOIN raw.competitions c ON a.domestic_competition_id = c.competition_id
WHERE rn = 1 AND source_club_id IS NOT NULL;

CREATE TABLE dim_players AS
WITH player_base AS (
    SELECT player_id, last_season, name, first_name, last_name, CAST(date_of_birth AS DATE) AS date_of_birth,
           country_of_birth, country_of_citizenship, position, sub_position, foot, height_in_cm,
           TRY_CAST(current_club_id AS BIGINT) AS current_club_id,
           current_club_name, current_club_domestic_competition_id,
           CAST(contract_expiration_date AS DATE) AS contract_expiration_date,
           market_value_in_eur, highest_market_value_in_eur, image_url, url
    FROM raw.players
), transfer_only AS (
    SELECT t.player_id, NULL, ANY_VALUE(t.player_name), NULL, NULL, NULL, NULL, NULL, NULL, NULL,
           NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL
    FROM raw.transfers t
    WHERE NOT EXISTS (SELECT 1 FROM player_base p WHERE p.player_id = t.player_id)
    GROUP BY t.player_id
)
SELECT player_id AS player_key, player_id AS source_player_id, last_season, name, first_name, last_name,
       date_of_birth, country_of_birth, country_of_citizenship AS nationality,
       position, sub_position, foot, height_in_cm, current_club_id AS current_club_key,
       current_club_name, current_club_domestic_competition_id,
       contract_expiration_date, market_value_in_eur, highest_market_value_in_eur,
       image_url, url
FROM (SELECT * FROM player_base UNION ALL SELECT * FROM transfer_only);

CREATE TABLE dim_seasons AS
SELECT ROW_NUMBER() OVER (ORDER BY season) AS season_key,
       season AS source_season, CAST(season AS INTEGER) AS start_year,
       CAST(season AS INTEGER) + 1 AS end_year,
       season || '/' || RIGHT(CAST(CAST(season AS INTEGER) + 1 AS VARCHAR), 2) AS season_label
FROM (SELECT DISTINCT season FROM raw.games);

CREATE TABLE dim_positions AS
SELECT ROW_NUMBER() OVER (ORDER BY position) AS position_key, position AS position_name
FROM (SELECT DISTINCT COALESCE(position, 'Unknown') AS position FROM dim_players);

CREATE TABLE dim_transfer_types AS
SELECT * FROM (VALUES
    (1, 'Nature unavailable', 'The source has no reliable permanent/free/loan flag.'),
    (2, 'Reported positive fee; nature unavailable', 'A positive fee is reported, but transfer nature is not.')
) AS t(transfer_type_key, transfer_type_name, definition);

CREATE TABLE dim_dates AS
SELECT CAST(strftime(d, '%Y%m%d') AS INTEGER) AS date_key, d AS full_date,
       YEAR(d) AS year, MONTH(d) AS month, MONTHNAME(d) AS month_name,
       QUARTER(d) AS quarter, DAYOFWEEK(d) AS day_of_week
FROM generate_series(DATE '1990-01-01', DATE '2040-12-31', INTERVAL 1 DAY) t(d);
