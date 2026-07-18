# Source research and validation

Research was completed on 18 July 2026. Three candidates were accessed directly and unchanged samples were saved under `data/raw/source_validation/` (the 205 MB DuckDB artifact is gitignored). No prohibited scraping, private endpoint or login circumvention is used.

## Decision summary

| Criterion | transfermarkt-datasets | OpenFootball Europe | football-data.org v4 |
|---|---|---|---|
| Official project URL | https://github.com/dcaribou/transfermarkt-datasets | https://github.com/openfootball/europe | https://www.football-data.org/ |
| Access | Public DuckDB / compressed CSV | Public GitHub text files | Documented REST API |
| Authentication | None | None | None for competition list; token for useful match endpoints |
| Format | DuckDB, CSV.gz | Football.TXT | JSON |
| Portugal | Liga Portugal player/game detail | Primeira Liga, Liga 2 fixtures/results | Primeira Liga free; broader Portuguese competitions listed by tiers |
| Measured seasons | PO1 2012/13–2025/26 | Files 2018/19–2026/27 at validation | API reports per-competition available-season counts |
| Latest measured date | Games 2026-07-06; PO1 2026-05-16; valuations 2026-02-27 | 2025/26 sample present; future schedule files also listed | Competition metadata accessed 2026-07-18 |
| Update frequency | Weekly, documented | Community repository commits | Provider-managed/current API |
| Player fields | Stable ID, identity, DOB, nationality, position, foot, height, current club/value/contract | None | Squad/person resources, plan-dependent |
| Club fields | Stable ID, competition, squad metadata, stadium | Team names only in fixtures | Stable API IDs and team resources |
| Transfers | Player/from/to/date/season/fee/value; no reliable type | None | None |
| Appearances/minutes | Game-level appearances, goals, assists, minutes | None | Person/match fields are tier/endpoint dependent |
| Market values | Current and history | None | None |
| Loans | No explicit type/parent/loan dates | None | None |
| Contracts | Current profile expiry when present | None | Limited/provider-dependent |
| Licence/terms | Repository declares CC0-1.0 | CC0/public domain | Provider terms and attribution/rate policies |
| Stable identifiers | Player, club, game, competition | No player IDs | API entity IDs |
| Automation | Excellent: single versioned artifact, no key | Good for match results | Good with secret token and rate limiting |
| Portfolio suitability | Strong, with upstream provenance caveat | Strong for results projects | Suitable under provider terms |
| Reliability concerns | Third-party publication derived from Transfermarkt; zero fee semantics; coverage is selected competitions | Community-maintained, uneven seasons, no player facts | Free tier/plan constraints; metadata `lastUpdated` can lag; no transfers/values |
| Known limitations | No academy flag, explicit loan type, reliable free-transfer type or PO2 player detail | Results only | Not a recruitment/value dataset |

## Real sample results

Selected artifact SHA-256 for the validated run: `1217a880b61d9abe9ac6a822ebeed64dee5d47eecf463b0178e818216cbfb208`; source commit `59fa295c51fc23466f3a71542f8bf3d1335daa83`.

| Table | Records |
|---|---:|
| appearances | 1,894,350 |
| clubs | 796 |
| competitions | 65 |
| countries | 124 |
| games | 88,958 |
| player_valuations | 507,815 |
| players | 50,149 |
| transfers | 35,139 |

Portuguese validation found 4,152 PO1 games and 119,936 appearances from 2012-08-17 to 2026-05-16, 1,899 transfer records touching historically PO1-classified clubs, and 348 current Portuguese player profiles abroad. Future-dated transfers exist and are retained with `is_future_dated`; completed-date analytics exclude them.

## Source-to-target field map

| Source | Field | Warehouse target | Transformation / caveat |
|---|---|---|---|
| players | player_id | dim_players.source_player_id/player_key | Preserved; internal stable key |
| players | date_of_birth | dim_players.date_of_birth | Used for event-date age |
| players | position/sub_position | dim_players | Broad and detailed positions |
| players | contract_expiration_date | dim_players | Current profile only |
| clubs | club_id | dim_clubs.source_club_id/club_key | Cast to bigint; transfer-only clubs unioned |
| competitions | competition_id | dim_competitions.source_competition_id | `PO1` is initial scope |
| transfers | transfer_date/from/to | fact_transfers | Future flag; Portugal-touching records only |
| transfers | transfer_fee | fact_transfers.transfer_fee_eur | Values `<=0` become null/unknown |
| transfers | market_value_in_eur | fact_transfers.market_value_at_transfer_eur | Estimate, not fee |
| appearances | appearance_id/game/player/club | fact_player_appearances | PO1 game-level facts |
| appearances | minutes/goals/assists | appearance and season-stat facts | No fabricated starts; `estimated_starts` is explicitly minutes-based |
| player_valuations | date/value/player | fact_player_valuations | Relevant-player subset |

## Realistic MVP

Implemented: market overview, recruitment patterns, youth minutes, configurable development indicator, selling model, squad snapshots/alerts, transfer pathways, Portuguese players abroad, player histories, quality monitoring, exports and refresh automation.

Excluded: actual loan categories, academy integration, reliable free/permanent classification, club-spell transfer ROI, Liga Portugal 2 player detail, and “realistic return target” claims. Adding them requires explicit transfer nature/loan dates, academy provenance, reliable purchase-club spell attribution, and entity-safe PO2 player statistics.

