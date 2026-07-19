from datetime import datetime, timedelta, timezone

from app.components.cards import format_refresh_time


def test_refresh_time_is_normalised_to_utc_without_microseconds():
    value = datetime(2026, 7, 19, 1, 12, 30, 999999, tzinfo=timezone(timedelta(hours=1)))

    assert format_refresh_time(value) == "2026-07-19 00:12 UTC"
