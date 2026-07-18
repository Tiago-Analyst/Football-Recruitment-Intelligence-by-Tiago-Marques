from src.analytics.loans import loan_playing_status


def test_loan_usage_requires_minutes_and_starts():
    assert loan_playing_status(1200, 15, 20) == "Regular Starter"
    assert loan_playing_status(500, 2, 15) == "Rotation Player"
    assert loan_playing_status(20, 0, 2) == "No Meaningful Usage"

