CREATE VIEW clean_transfers AS
SELECT t.*, p.name AS player_name, p.position, p.nationality,
       fc.club_name AS from_club, tc.club_name AS to_club
FROM fact_transfers t
LEFT JOIN dim_players p USING (player_key)
LEFT JOIN dim_clubs fc ON t.from_club_key = fc.club_key
LEFT JOIN dim_clubs tc ON t.to_club_key = tc.club_key;

CREATE VIEW clean_player_statistics AS
SELECT s.*, p.name AS player_name, p.position, p.nationality, c.club_name
FROM fact_player_season_statistics s
LEFT JOIN dim_players p USING (player_key)
LEFT JOIN dim_clubs c USING (club_key);

