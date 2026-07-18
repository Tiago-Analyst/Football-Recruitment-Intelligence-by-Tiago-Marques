CREATE TABLE fact_club_recruitment AS
SELECT to_club_key AS club_key, transfer_season,
       COUNT(*) AS players_recruited,
       AVG(age_at_transfer) AS average_recruitment_age,
       MEDIAN(age_at_transfer) AS median_recruitment_age,
       SUM(transfer_fee_eur) AS known_spending_eur,
       AVG(transfer_fee_eur) AS average_known_fee_eur,
       COUNT(transfer_fee_eur) AS transfers_with_known_fee,
       AVG(CASE WHEN age_at_transfer < 21 THEN 1.0 ELSE 0.0 END) AS u21_share,
       AVG(CASE WHEN age_at_transfer < 23 THEN 1.0 ELSE 0.0 END) AS u23_share,
       AVG(CASE WHEN from_country = 'Portugal' THEN 1.0 ELSE 0.0 END) AS domestic_share,
       AVG(CASE WHEN from_country IS NOT NULL AND from_country <> 'Portugal' THEN 1.0 ELSE 0.0 END) AS international_share
FROM fact_transfers
WHERE to_competition_id = 'PO1' AND transfer_date <= CURRENT_DATE
GROUP BY ALL;

CREATE TABLE fact_club_sales AS
SELECT from_club_key AS club_key, transfer_season,
       COUNT(*) AS sales_count, SUM(transfer_fee_eur) AS known_sales_eur,
       AVG(transfer_fee_eur) AS average_known_sale_eur,
       MEDIAN(transfer_fee_eur) AS median_known_sale_eur,
       AVG(age_at_transfer) AS average_sale_age,
       AVG(CASE WHEN age_at_transfer < 23 THEN 1.0 ELSE 0.0 END) AS u23_sale_share,
       AVG(CASE WHEN to_country IS NOT NULL AND to_country <> 'Portugal' THEN 1.0 ELSE 0.0 END) AS international_share
FROM fact_transfers
WHERE from_competition_id = 'PO1' AND transfer_date <= CURRENT_DATE
GROUP BY ALL;

CREATE TABLE fact_player_development AS
WITH usage AS (
    SELECT club_key, season,
           COUNT(DISTINCT CASE WHEN age_on_match_date < 19 AND minutes_played > 0 THEN player_key END) AS u19_players_used,
           COUNT(DISTINCT CASE WHEN age_on_match_date < 21 AND minutes_played > 0 THEN player_key END) AS u21_players_used,
           COUNT(DISTINCT CASE WHEN age_on_match_date < 23 AND minutes_played > 0 THEN player_key END) AS u23_players_used,
           SUM(CASE WHEN age_on_match_date < 21 THEN minutes_played ELSE 0 END) AS u21_minutes,
           SUM(CASE WHEN age_on_match_date < 23 THEN minutes_played ELSE 0 END) AS u23_minutes,
           SUM(minutes_played) AS total_minutes,
           SUM(age_on_match_date * minutes_played) / NULLIF(SUM(minutes_played), 0) AS minutes_weighted_age
    FROM fact_player_appearances GROUP BY ALL
)
SELECT *, u21_minutes / NULLIF(total_minutes, 0) AS u21_minutes_share,
       u23_minutes / NULLIF(total_minutes, 0) AS u23_minutes_share,
       ROUND(100 * (
           0.45 * LEAST(u21_minutes / NULLIF(total_minutes, 0), 1) +
           0.30 * LEAST(u23_minutes / NULLIF(total_minutes, 0), 1) +
           0.25 * LEAST(u23_players_used / 10.0, 1)
       ), 2) AS development_index,
       'Youth-usage index only; academy and club-spell value growth unavailable' AS index_scope
FROM usage;

CREATE TABLE transfer_pathways AS
SELECT COALESCE(from_country, 'Unknown') AS source_country,
       COALESCE(to_country, 'Unknown') AS destination_country,
       COALESCE(from_competition_id, 'Unknown') AS source_competition_id,
       COALESCE(to_competition_id, 'Unknown') AS destination_competition_id,
       COUNT(*) AS transfer_count, AVG(age_at_transfer) AS average_age,
       AVG(transfer_fee_eur) AS average_known_fee_eur,
       COUNT(transfer_fee_eur) AS transfers_with_known_fee
FROM fact_transfers
WHERE transfer_date <= CURRENT_DATE
GROUP BY ALL;

CREATE TABLE portuguese_players_abroad AS
WITH latest_stats AS (
    SELECT player_key, club_key, season, appearances, minutes, goals, assists,
           ROW_NUMBER() OVER (PARTITION BY player_key ORDER BY CAST(season AS INTEGER) DESC) AS rn
    FROM fact_player_season_statistics
)
SELECT p.player_key, p.name AS player, p.date_of_birth,
       DATE_DIFF('year', p.date_of_birth, CURRENT_DATE) -
           CASE WHEN (MONTH(CURRENT_DATE), DAY(CURRENT_DATE)) <
                     (MONTH(p.date_of_birth), DAY(p.date_of_birth)) THEN 1 ELSE 0 END AS age,
       p.position, p.sub_position, p.current_club_name AS club,
       p.current_club_domestic_competition_id AS competition_id,
       c.country_name AS country, p.market_value_in_eur AS market_value_eur,
       s.season AS latest_observed_season, s.appearances, s.minutes, s.goals, s.assists,
       CASE WHEN s.minutes >= 1800 THEN 'High usage'
            WHEN s.minutes >= 900 THEN 'Regular usage'
            WHEN s.minutes > 0 THEN 'Limited usage'
            ELSE 'No current-source minutes' END AS usage_status,
       'Indicator only; financial and contract feasibility not assessed' AS return_indicator_note
FROM dim_players p
LEFT JOIN dim_clubs c ON p.current_club_key = c.club_key
LEFT JOIN latest_stats s ON p.player_key = s.player_key AND s.rn = 1
WHERE p.nationality = 'Portugal'
  AND COALESCE(p.current_club_domestic_competition_id, '') <> 'PO1'
  AND p.current_club_key IS NOT NULL;

CREATE TABLE squad_alerts AS
WITH latest AS (SELECT MAX(CAST(season AS INTEGER))::VARCHAR AS season FROM fact_player_season_statistics),
depth AS (
    SELECT s.club_key, p.position, COUNT(*) AS players_with_meaningful_minutes,
           AVG(s.minutes_weighted_age) AS weighted_age
    FROM fact_player_season_statistics s
    JOIN dim_players p USING (player_key), latest l
    WHERE s.season = l.season AND s.minutes >= 450
    GROUP BY ALL
), concentration AS (
    SELECT club_key, SUM(CASE WHEN rn <= 5 THEN minutes ELSE 0 END) / NULLIF(SUM(minutes), 0) AS top_five_minutes_share
    FROM (
        SELECT club_key, minutes, ROW_NUMBER() OVER (PARTITION BY club_key ORDER BY minutes DESC) AS rn
        FROM fact_player_season_statistics s, latest l WHERE s.season = l.season
    ) x GROUP BY club_key
), alerts AS (
    SELECT club_key, position AS context, 'Limited position depth' AS alert_type,
           'Only one player reached 450 minutes in this broad position.' AS alert_message,
           'warning' AS severity
    FROM depth WHERE players_with_meaningful_minutes <= 1
    UNION ALL
    SELECT club_key, position, 'High position age',
           'Minutes-weighted age is at least 29 in this broad position.', 'warning'
    FROM depth WHERE weighted_age >= 29
    UNION ALL
    SELECT club_key, 'Squad', 'Excessive minute concentration',
           'The five highest-usage players account for at least 55% of recorded minutes.', 'warning'
    FROM concentration WHERE top_five_minutes_share >= 0.55
)
SELECT ROW_NUMBER() OVER () AS alert_key, * FROM alerts;

CREATE TABLE club_profiles AS
WITH r AS (
    SELECT club_key,
       CASE
         WHEN AVG(average_recruitment_age) < 23 THEN 'Young talent recruiter'
         WHEN AVG(domestic_share) >= 0.60 THEN 'Domestic-market recruiter'
         WHEN AVG(international_share) >= 0.60 THEN 'International-market recruiter'
         ELSE 'Balanced recruiter' END AS recruitment_profile
    FROM fact_club_recruitment GROUP BY club_key
), s AS (
    SELECT club_key,
       CASE
         WHEN SUM(known_sales_eur) >= 50000000 THEN 'Elite-talent seller'
         WHEN AVG(average_sale_age) < 24 THEN 'Young-player seller'
         WHEN AVG(international_share) >= 0.60 THEN 'International exporter'
         ELSE 'Balanced seller' END AS selling_profile
    FROM fact_club_sales GROUP BY club_key
)
SELECT c.club_key, c.club_name, r.recruitment_profile, s.selling_profile,
       'Profiles use documented thresholds and available fields only.' AS profile_note
FROM dim_clubs c LEFT JOIN r USING (club_key) LEFT JOIN s USING (club_key)
WHERE c.domestic_competition_id = 'PO1';

