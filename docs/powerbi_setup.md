# Power BI setup

Import CSVs or Parquet files from `output/powerbi/`. Prefer Parquet for fact tables and CSV for small dimensions.

## Star schema relationships

| From (one) | To (many) | Key | Direction |
|---|---|---|---|
| dim_players | fact_transfers | player_key | Single |
| dim_players | fact_player_appearances/statistics/valuations | player_key | Single |
| dim_clubs | fact_transfers | from_club_key (active) | Single |
| dim_clubs | fact_transfers | to_club_key (inactive or role-playing copy) | Single |
| dim_clubs | recruitment/development/sales/squad facts | club_key | Single |
| dim_competitions | facts | source competition ID bridge | Single |
| dim_dates | transfers/appearances/valuations | date_key | Single |

Use role-playing copies `From Club` and `To Club` for the cleanest transfer model. Avoid bidirectional filters unless a specific visual requires them.

## Recommended measures

```DAX
Transfers = COUNTROWS(fact_transfers)
Known Fees = SUM(fact_transfers[transfer_fee_eur])
Known Fee Coverage = DIVIDE(COUNT(fact_transfers[transfer_fee_eur]), [Transfers])
Average Transfer Age = AVERAGE(fact_transfers[age_at_transfer])
U21 Minute Share = DIVIDE(SUM(fact_player_development[u21_minutes]), SUM(fact_player_development[total_minutes]))
```

Recommended visuals: transfer timeline, club age/market small multiples, recruitment-country bars, selling-destination matrix, Development Index scatter, squad age pyramid, pathway Sankey, and quality status matrix. Recommended slicers: season, club, country, position, age group, fee availability and direction.

Refresh the folder after the Python pipeline succeeds. For incremental refresh, partition transfers by `transfer_date`, appearances by `date`, and valuations by `date`; retain a full refresh for dimensions because current-profile attributes can change. `last_refresh.csv` and `data_quality_summary.csv` should be visible on a methodology page.
