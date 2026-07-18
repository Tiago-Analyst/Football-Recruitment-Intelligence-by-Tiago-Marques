# Data dictionary

## Dimensions

| Relation | Grain | Key fields |
|---|---|---|
| dim_players | One source player | player_key, source_player_id, identity, position, current profile fields |
| dim_clubs | One source or transfer-only club | club_key, source_club_id, domestic competition, country |
| dim_competitions | One competition | competition_key, source_competition_id, type, country |
| dim_countries | One country | country_key, code, confederation |
| dim_seasons | One PO1 source season | season_key, start/end year, label |
| dim_positions | One broad position | position_key, position_name |
| dim_dates | One calendar date | date_key, date attributes |
| dim_transfer_types | One source-semantics state | nature unavailable / positive-fee nature unavailable |

## Facts and analytics

| Relation | Grain | Notes |
|---|---|---|
| fact_transfers | One Portugal-touching source transfer | Positive known fee or null; future flag |
| fact_player_appearances | One PO1 player-game appearance | Minutes, goals, assists, match-date age |
| fact_player_season_statistics | Player-club-season | Aggregated usage |
| fact_player_valuations | Player valuation date | Third-party market estimate |
| fact_game_events | One event in a PO1 game | Goals/cards/substitutions when supplied |
| fact_loans | One verified loan | Typed empty relation in MVP |
| fact_squad_snapshots | Current player profile snapshot | Age/value/contract fields |
| fact_club_recruitment | Club-transfer season | Incoming strategy measures |
| fact_player_development | Club-season | Youth usage and Development Index |
| fact_club_sales | Club-transfer season | Outgoing strategy measures |
| transfer_pathways | Country/competition route | Count, age, known-fee coverage |
| portuguese_players_abroad | Current Portuguese player abroad | Current profile plus latest covered usage |
| squad_alerts | One club/context alert | Transparent screening rule |

Operational tables record pipeline runs, source ingestion, data quality, schema change and entity review.
