# Architecture

The project separates extraction, validation, transformation, analytics, services and presentation. `src/data/adapters` owns external contracts; raw artifacts are immutable and hash-addressable through run logs. SQL builds a star-like DuckDB warehouse. Python analytics contain small testable rules; Streamlit and Power BI consume only warehouse relations.

Internal keys remain stable because the selected source's numeric entity identifiers are adopted as surrogate keys while also being preserved in explicit `source_*_id` columns. Transfer-only clubs and players are added to dimensions rather than dropped. A future hybrid source must write uncertain candidate matches to `entity_matching_review`.

The warehouse copies only analytical scope from the 205 MB source: all player/club/competition reference tables, all transfers needed to identify Portugal-touching movement, PO1 appearances/games, and valuations for relevant players. This keeps refreshes fast while the immutable source remains the audit record.

