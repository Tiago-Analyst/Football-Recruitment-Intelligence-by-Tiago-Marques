CREATE TABLE fact_transfers AS
SELECT ROW_NUMBER() OVER (ORDER BY t.transfer_date, t.player_id, t.from_club_id, t.to_club_id) AS transfer_key,
       t.player_id AS player_key, t.transfer_date,
       CAST(strftime(t.transfer_date, '%Y%m%d') AS INTEGER) AS date_key,
       t.transfer_season, t.from_club_id AS from_club_key, t.to_club_id AS to_club_key,
       t.from_club_name, t.to_club_name,
       CASE WHEN t.transfer_fee > 0 THEN CAST(t.transfer_fee AS DOUBLE) END AS transfer_fee_eur,
       CAST(t.market_value_in_eur AS DOUBLE) AS market_value_at_transfer_eur,
       CASE WHEN t.transfer_fee > 0 THEN 2 ELSE 1 END AS transfer_type_key,
       CASE WHEN t.transfer_fee > 0 THEN 'reported_positive' ELSE 'unknown_or_zero' END AS fee_status,
       CASE WHEN MONTH(t.transfer_date) IN (6,7,8,9) THEN 'Summer'
            WHEN MONTH(t.transfer_date) IN (1,2) THEN 'Winter' ELSE 'Outside main windows' END AS transfer_window,
       DATE_DIFF('year', p.date_of_birth, t.transfer_date) -
           CASE WHEN (MONTH(t.transfer_date), DAY(t.transfer_date)) <
                     (MONTH(p.date_of_birth), DAY(p.date_of_birth)) THEN 1 ELSE 0 END AS age_at_transfer,
       fc.domestic_competition_id AS from_competition_id,
       tc.domestic_competition_id AS to_competition_id,
       fc.country_name AS from_country, tc.country_name AS to_country,
       t.transfer_date > CURRENT_DATE AS is_future_dated
FROM raw.transfers t
LEFT JOIN dim_players p ON t.player_id = p.player_key
LEFT JOIN dim_clubs fc ON t.from_club_id = fc.club_key
LEFT JOIN dim_clubs tc ON t.to_club_id = tc.club_key
WHERE fc.domestic_competition_id = 'PO1' OR tc.domestic_competition_id = 'PO1';

CREATE TABLE fact_player_appearances AS
SELECT a.appearance_id, a.player_id AS player_key, a.player_club_id AS club_key,
       a.game_id, a.date, CAST(strftime(a.date, '%Y%m%d') AS INTEGER) AS date_key,
       a.competition_id, g.season, a.yellow_cards, a.red_cards, a.goals, a.assists,
       a.minutes_played,
       DATE_DIFF('year', p.date_of_birth, a.date) -
           CASE WHEN (MONTH(a.date), DAY(a.date)) <
                     (MONTH(p.date_of_birth), DAY(p.date_of_birth)) THEN 1 ELSE 0 END AS age_on_match_date
FROM raw.appearances a
JOIN raw.games g ON TRY_CAST(g.game_id AS BIGINT) = a.game_id
LEFT JOIN dim_players p ON a.player_id = p.player_key;

CREATE TABLE fact_player_season_statistics AS
SELECT player_key, club_key, competition_id, season,
       COUNT(DISTINCT game_id) AS appearances, SUM(minutes_played) AS minutes,
       SUM(goals) AS goals, SUM(assists) AS assists,
       SUM(CASE WHEN minutes_played >= 60 THEN 1 ELSE 0 END) AS estimated_starts,
       CAST(SUM(age_on_match_date * minutes_played) / NULLIF(SUM(minutes_played), 0) AS DOUBLE) AS minutes_weighted_age
FROM fact_player_appearances
GROUP BY ALL;

CREATE TABLE fact_player_valuations AS
SELECT ROW_NUMBER() OVER (ORDER BY player_id, date) AS valuation_key,
       player_id AS player_key, date,
       CAST(strftime(date, '%Y%m%d') AS INTEGER) AS date_key,
       market_value_in_eur AS market_value_eur, current_club_id AS club_key,
       current_club_name, player_club_domestic_competition_id AS competition_id
FROM raw.player_valuations;

CREATE TABLE fact_game_events AS
SELECT game_event_id, date, TRY_CAST(game_id AS BIGINT) AS game_id,
       minute, type AS event_type, club_id AS club_key, club_name,
       player_id AS player_key, description, player_in_id, player_assist_id
FROM raw.game_events;

CREATE TABLE fact_loans AS
SELECT CAST(NULL AS BIGINT) AS loan_key, CAST(NULL AS BIGINT) AS player_key,
       CAST(NULL AS BIGINT) AS parent_club_key, CAST(NULL AS BIGINT) AS loan_club_key,
       CAST(NULL AS DATE) AS loan_start_date, CAST(NULL AS DATE) AS loan_end_date,
       CAST(NULL AS VARCHAR) AS playing_time_status,
       CAST('Unavailable: source has no reliable loan flag' AS VARCHAR) AS availability_note
WHERE FALSE;

CREATE TABLE fact_club_season_summary AS
WITH club_matches AS (
    SELECT season, home_club_id AS club_key, home_club_goals AS goals_for,
           away_club_goals AS goals_against, CASE WHEN home_club_goals > away_club_goals THEN 1 ELSE 0 END AS wins
    FROM raw.games
    UNION ALL
    SELECT season, away_club_id, away_club_goals, home_club_goals,
           CASE WHEN away_club_goals > home_club_goals THEN 1 ELSE 0 END
    FROM raw.games
)
SELECT season, club_key, COUNT(*) AS matches, SUM(wins) AS wins,
       SUM(goals_for) AS goals_for, SUM(goals_against) AS goals_against
FROM club_matches GROUP BY ALL;

CREATE TABLE fact_squad_snapshots AS
SELECT CURRENT_DATE AS snapshot_date, p.current_club_key AS club_key, p.player_key,
       p.position, p.sub_position,
       DATE_DIFF('year', p.date_of_birth, CURRENT_DATE) -
           CASE WHEN (MONTH(CURRENT_DATE), DAY(CURRENT_DATE)) <
                     (MONTH(p.date_of_birth), DAY(p.date_of_birth)) THEN 1 ELSE 0 END AS age,
       p.market_value_in_eur AS market_value_eur, p.contract_expiration_date,
       CASE WHEN p.contract_expiration_date IS NULL THEN 'Unavailable'
            WHEN p.contract_expiration_date <= CURRENT_DATE + INTERVAL 365 DAY THEN 'Expires within 12 months'
            ELSE 'Beyond 12 months' END AS contract_status
FROM dim_players p
WHERE p.current_club_domestic_competition_id = 'PO1';
