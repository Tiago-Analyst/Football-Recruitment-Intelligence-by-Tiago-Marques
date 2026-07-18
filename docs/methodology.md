# Methodology

Completed-date metrics filter `transfer_date <= CURRENT_DATE`. A transfer touches Portuguese football when its source or destination club is classified by the selected source under `PO1`; this includes historically covered clubs, not just the current league membership.

Age is completed years on the event date. Youth groups use age on each match date, avoiding the common error of using current age for historical appearances. Positive fees are reported separately from record counts; zero-coded fees become null because the source cannot distinguish free moves, loans, undisclosed fees and missing values.

The Development Index is configurable in `config/development_weights.yaml`. The current implementation is a 0–100 directional youth-usage indicator: 45% U21 minute share, 30% U23 minute share and 25% capped U23-player breadth (ten players reaches the cap). It excludes academy origin and club-spell value growth. It must not be interpreted as a universal measure of development quality.

Recruitment and selling profiles use explicit thresholds in SQL/Python. They describe observed patterns, not club intent. Squad alerts are screening rules: 450 minutes defines meaningful positional usage, a top-five share of 55% flags concentration, and minutes-weighted position age of 29 flags age exposure.

