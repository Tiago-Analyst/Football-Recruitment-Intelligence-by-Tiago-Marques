# Limitations

The primary dataset is a transparent third-party publication derived from Transfermarkt. Its CC0 repository licence supports portfolio reuse, but upstream provenance and applicable terms should be reviewed before commercial deployment.

No explicit loan/free/permanent flag exists. `fact_loans` is empty and zero fees are unknown. Academy provenance is absent. Transfer histories do not reliably identify a single continuous club spell, so purchase-to-sale return and value created “by” a club are excluded. Liga Portugal 2 has no detailed player/appearance coverage in the primary artifact. Current player club and contract fields are snapshots and can be stale relative to a recently completed transfer. Country pathways are incomplete where transfer-only clubs cannot be mapped to a competition.

Appearances cover selected competitions and begin later than some transfer/valuation histories. “Starts” are not directly available in appearances; the model exposes an explicitly named estimated-start count based on at least 60 minutes and does not use it for loan decisions. Market value is an estimate and must never be read as a realised fee.

