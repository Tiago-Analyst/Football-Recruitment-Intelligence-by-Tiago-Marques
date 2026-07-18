import pandas as pd

from src.analytics.squad_planning import minute_concentration, position_depth_alerts


def test_minute_concentration():
    assert minute_concentration(pd.Series([100, 50, 25]), top_n=1) == 100 / 175


def test_position_depth_alert():
    frame = pd.DataFrame({"club": ["A", "A", "A"], "position": ["GK", "GK", "DF"], "minutes": [900, 10, 800]})
    result = position_depth_alerts(frame)
    assert set(result.position) == {"GK", "DF"}

