from app import i18n


def test_english_translation_branch(monkeypatch):
    monkeypatch.setattr(i18n, "is_portuguese", lambda: False)
    assert i18n.tr("Club", "Clube") == "Club"
    assert i18n.category("Incoming") == "Incoming"


def test_portuguese_translation_branch(monkeypatch):
    monkeypatch.setattr(i18n, "is_portuguese", lambda: True)
    assert i18n.tr("Club", "Clube") == "Clube"
    assert i18n.category("Incoming") == "Entradas"


def test_unknown_source_value_is_preserved(monkeypatch):
    monkeypatch.setattr(i18n, "is_portuguese", lambda: True)
    assert i18n.category("SL Benfica") == "SL Benfica"


def test_unmapped_country_is_grouped_as_other(monkeypatch):
    monkeypatch.setattr(i18n, "is_portuguese", lambda: False)
    assert i18n.country_label("Unknown") == "Other"
    monkeypatch.setattr(i18n, "is_portuguese", lambda: True)
    assert i18n.country_label(None) == "Outros"
