"""Conservative entity matching for future hybrid-source extensions."""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from datetime import date


def normalise_name(value: str) -> str:
    """Normalise accents, case and punctuation without deciding identity."""
    ascii_value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", ascii_value.lower()).strip()


@dataclass(frozen=True)
class MatchCandidate:
    """An auditable entity-match proposal."""

    source_id: str
    target_id: str
    confidence: float
    decision: str
    reason: str


def match_player(
    source: dict[str, object], target: dict[str, object], auto_threshold: float = 0.95
) -> MatchCandidate:
    """Score identity using name plus corroborating fields; never name alone."""
    name_equal = normalise_name(str(source.get("name", ""))) == normalise_name(
        str(target.get("name", ""))
    )
    dob_equal = bool(source.get("date_of_birth")) and source.get("date_of_birth") == target.get(
        "date_of_birth"
    )
    nationality_equal = bool(source.get("nationality")) and source.get("nationality") == target.get(
        "nationality"
    )
    position_equal = bool(source.get("position")) and source.get("position") == target.get("position")
    confidence = (
        0.45 * name_equal + 0.35 * dob_equal + 0.10 * nationality_equal + 0.10 * position_equal
    )
    corroborators = sum((dob_equal, nationality_equal, position_equal))
    decision = "auto_match" if confidence >= auto_threshold and corroborators >= 2 else "review"
    return MatchCandidate(
        str(source.get("source_id", "")),
        str(target.get("source_id", "")),
        confidence,
        decision,
        f"name={name_equal};dob={dob_equal};nationality={nationality_equal};position={position_equal}",
    )
