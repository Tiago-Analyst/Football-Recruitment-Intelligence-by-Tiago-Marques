import pandas as pd

from src.analytics.development import development_index, youth_minutes_share


def test_youth_minute_share():
    assert youth_minutes_share(pd.Series([900, 100]), pd.Series([20, 30]), 20) == 0.9


def test_development_index_is_bounded_and_deterministic():
    assert development_index(1, 1, 20) == 100.0
    assert development_index(0, 0, 0) == 0.0

