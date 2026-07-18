# Automation

## GitHub Actions

`tests.yml` runs Ruff and pytest on pushes and pull requests. `refresh_data.yml` runs every Monday at 06:20 UTC and can be triggered manually. It downloads the latest source, validates required tables and non-empty counts, rebuilds DuckDB, writes Power BI files and quality reports, and uploads outputs as workflow artifacts. Raw source databases and credentials are not committed.

## Windows Task Scheduler

1. Create a basic task and choose a weekly trigger.
2. Program: the absolute path to the virtual environment's `python.exe`.
3. Arguments: `scripts\10_run_full_pipeline.py`.
4. Start in: the repository root.
5. Enable “Run task as soon as possible after a scheduled start is missed”.
6. Review `output/logs/pipeline.log` and `output/reports/data_quality_report.csv`.

No API key is required by the selected source. If a future source needs one, store it in `.env` locally and GitHub Secrets in CI. Never place secrets in YAML.

The source's weekly cadence makes incremental loads unnecessary for this MVP; each 205 MB artifact is immutable, hashed and rebuilt quickly. Snapshot retention should follow storage policy rather than committing raw files to Git.

