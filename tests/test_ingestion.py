import duckdb

from src.data.ingestion import schema_signature, signature_json


def test_schema_signature_is_stable(runtime_path):
    database = runtime_path / "source.duckdb"
    with duckdb.connect(str(database)) as connection:
        connection.execute("CREATE TABLE players(player_id INTEGER, name VARCHAR)")
    signature = schema_signature(database, ["players"])
    assert signature["players"] == [("player_id", "INTEGER"), ("name", "VARCHAR")]
    assert signature_json(signature) == signature_json(signature)
