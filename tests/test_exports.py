import duckdb

from src.data import export as export_module


def test_powerbi_export_uses_utf8_and_parquet(runtime_path, monkeypatch):
    database = runtime_path / "warehouse.duckdb"
    with duckdb.connect(str(database)) as connection:
        connection.execute("CREATE TABLE dim_players(player_key INTEGER, name VARCHAR)")
        connection.execute("INSERT INTO dim_players VALUES (1, 'João')")
        connection.execute("CREATE TABLE data_quality_results(severity VARCHAR, status VARCHAR, issue_count INTEGER)")
        connection.execute("INSERT INTO data_quality_results VALUES ('critical','PASS',0)")
        connection.execute("CREATE VIEW powerbi_last_refresh AS SELECT CURRENT_TIMESTAMP last_refresh, 'test' source_name, 'abc' source_file_hash")
    monkeypatch.setattr(export_module, "EXPORTS", {"dim_players": "dim_players"})
    written = export_module.export_powerbi(database, runtime_path / "out")
    assert (runtime_path / "out" / "dim_players.csv").read_text(encoding="utf-8").find("João") > 0
    assert (runtime_path / "out" / "dim_players.parquet") in written
