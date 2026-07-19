# Public deployment and automatic data refresh

The public app uses two independent GitHub-hosted components:

1. Streamlit Community Cloud deploys the application code from the default branch.
2. `Refresh football data` builds and publishes the latest validated DuckDB warehouse.

No personal computer or self-hosted runner is required.

## Refresh lifecycle

Every Monday at 06:20 UTC, or whenever it is started manually, the refresh workflow:

1. Downloads the current CC0 `transfermarkt-datasets` DuckDB artifact.
2. Rebuilds the analytics warehouse and Power BI exports.
3. Runs the configured data-quality gates.
4. Verifies that the warehouse contains the core application tables.
5. Replaces the `football_recruitment.duckdb` asset in the `data-latest` GitHub Release.
6. Creates `database/latest.json` with the release URL, size and SHA-256 checksum.
7. Commits that manifest to the default branch, prompting the hosted app to refresh.

If extraction, transformation or validation fails, the release and manifest are not changed.
The deployed app therefore continues to use the last successfully published warehouse.

## One-time GitHub setup

In the repository, open `Settings > Actions > General > Workflow permissions`, select
`Read and write permissions`, and save. The workflow needs this repository-scoped permission
to replace the release asset and commit the small version manifest.

Commit and push the production-deployment changes, then open `Actions > Refresh football data`
and choose `Run workflow`. A successful first run creates:

- the `data-latest` release;
- its `football_recruitment.duckdb` asset;
- `database/latest.json` on the default branch.

## Streamlit Community Cloud

Create a public app from the GitHub repository using:

- Branch: `main`
- Main file path: `app/streamlit_app.py`
- Python: `3.12`

No Streamlit secret is required for the public CC0 source or the public release asset.

On a cloud start, the app reads `database/latest.json`, downloads the versioned warehouse to
ephemeral storage, verifies its checksum and required tables, and only then serves queries.
Local development continues to prefer `database/football_recruitment.duckdb` when it exists.

## Operations

- Green refresh workflow: the latest validated warehouse was published.
- Failed refresh workflow: inspect the failed step; the previous public database remains active.
- Manual refresh: use `Actions > Refresh football data > Run workflow`.
- Scheduled workflows in inactive public repositories may be disabled by GitHub after 60 days;
  re-enable the workflow from the Actions page if necessary.
