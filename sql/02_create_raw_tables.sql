CREATE TABLE raw.players AS SELECT * FROM source.players;
CREATE TABLE raw.clubs AS SELECT * FROM source.clubs;
CREATE TABLE raw.competitions AS SELECT * FROM source.competitions;
CREATE TABLE raw.countries AS SELECT * FROM source.countries;
CREATE TABLE raw.transfers AS SELECT * FROM source.transfers;
CREATE TABLE raw.games AS SELECT * FROM source.games WHERE competition_id = 'PO1';
CREATE TABLE raw.appearances AS SELECT * FROM source.appearances WHERE competition_id = 'PO1';
CREATE TABLE raw.game_events AS
SELECT e.* FROM source.game_events e
JOIN raw.games g ON e.game_id = g.game_id;
CREATE TABLE raw.player_valuations AS
SELECT v.*
FROM source.player_valuations v
WHERE v.player_id IN (
    SELECT player_id FROM source.players
    WHERE current_club_domestic_competition_id = 'PO1'
       OR country_of_citizenship = 'Portugal'
    UNION
    SELECT player_id FROM source.appearances WHERE competition_id = 'PO1'
    UNION
    SELECT player_id FROM source.transfers t
    WHERE CAST(t.from_club_id AS VARCHAR) IN (
        SELECT club_id FROM source.clubs WHERE domestic_competition_id = 'PO1'
    ) OR CAST(t.to_club_id AS VARCHAR) IN (
        SELECT club_id FROM source.clubs WHERE domestic_competition_id = 'PO1'
    )
);
