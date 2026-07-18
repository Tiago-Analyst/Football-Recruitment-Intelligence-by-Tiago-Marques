import pandas as pd

from src.analytics.selling_model import selling_profile
from src.analytics.transfers import aggregate_pathways, fee_status, transfer_window


def test_transfer_fee_and_window_classification():
    assert fee_status(0) == "unknown_or_zero"
    assert fee_status(1_000_000) == "reported_positive"
    assert transfer_window(7) == "Summer"
    assert transfer_window(1) == "Winter"


def test_pathway_aggregation():
    frame = pd.DataFrame({"source_country": ["Portugal", "Portugal"], "destination_country": ["England", "England"], "player_key": [1, 2], "transfer_fee_eur": [10.0, 20.0]})
    result = aggregate_pathways(frame).iloc[0]
    assert result.transfer_count == 2
    assert result.average_fee_eur == 15


def test_selling_profile_rules():
    row = pd.Series({"sales_count": 12, "average_sale_age": 22, "international_share": .7, "known_sales_eur": 60_000_000})
    labels = selling_profile(row)
    assert "High-volume seller" in labels and "Elite-talent seller" in labels

