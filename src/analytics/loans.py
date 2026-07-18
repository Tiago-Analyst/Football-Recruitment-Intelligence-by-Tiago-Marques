"""Loan status rules, activated only when actual loan fields exist."""
from __future__ import annotations


def loan_playing_status(minutes: int, starts: int, matches: int) -> str:
    """Classify usage from observed playing time, never valuation alone."""
    if matches <= 0 or minutes < 90:
        return "No Meaningful Usage"
    start_share = starts / matches
    if minutes >= 900 and start_share >= 0.60:
        return "Regular Starter"
    if minutes >= 450:
        return "Rotation Player"
    return "Limited Minutes"

