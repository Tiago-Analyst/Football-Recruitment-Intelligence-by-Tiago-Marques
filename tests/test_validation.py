from datetime import date

import pandas as pd
import pytest

from src.data.validation import (
    CriticalDataQualityError,
    assert_no_critical_failures,
    inspect_source_database,
    is_stale,
)


def test_invalid_source_file_fails(runtime_path):
    path = runtime_path / "bad.duckdb"
    path.write_text("not a database")
    with pytest.raises(CriticalDataQualityError):
        inspect_source_database(path, ["players"])


def test_critical_result_stops_pipeline():
    results = pd.DataFrame([{"rule_name": "duplicates", "severity": "critical", "status": "FAIL"}])
    with pytest.raises(CriticalDataQualityError):
        assert_no_critical_failures(results)


def test_stale_threshold():
    assert is_stale(date(2025, 1, 1), date(2025, 1, 20), 14)
    assert not is_stale(date(2025, 1, 10), date(2025, 1, 20), 14)
