from datetime import date

from src.data.matching import match_player, normalise_name


def test_name_normalisation_handles_accents():
    assert normalise_name("João Félix") == "joao felix"


def test_name_only_never_auto_matches():
    left = {"source_id": "a", "name": "João Silva"}
    right = {"source_id": "b", "name": "Joao Silva"}
    assert match_player(left, right).decision == "review"


def test_corroborated_identity_auto_matches():
    left = {"source_id": "a", "name": "João Silva", "date_of_birth": date(2002, 1, 1), "nationality": "Portugal", "position": "Attack"}
    right = {"source_id": "b", "name": "Joao Silva", "date_of_birth": date(2002, 1, 1), "nationality": "Portugal", "position": "Attack"}
    assert match_player(left, right).decision == "auto_match"

