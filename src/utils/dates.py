"""Date helpers used by metrics and validation."""
from __future__ import annotations

from datetime import date


def age_on(birth_date: date | None, on_date: date | None) -> int | None:
    """Calculate completed age, returning None when dates are missing or invalid."""
    if birth_date is None or on_date is None or on_date < birth_date:
        return None
    return on_date.year - birth_date.year - (
        (on_date.month, on_date.day) < (birth_date.month, birth_date.day)
    )

