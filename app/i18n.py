"""Lightweight English and European Portuguese localisation helpers."""
from __future__ import annotations

import streamlit as st

LANGUAGE_KEY = "dashboard_language"


def language() -> str:
    """Return the active language code, defaulting to English."""
    return st.session_state.get(LANGUAGE_KEY, "en")


def is_portuguese() -> bool:
    """Return whether European Portuguese is active."""
    return language() == "pt"


def tr(english: str, portuguese: str) -> str:
    """Return one of two supplied translations for the active language."""
    return portuguese if is_portuguese() else english


CATEGORY_TRANSLATIONS = {
    "All": "Todos",
    "Incoming": "Entradas",
    "Outgoing": "Saídas",
    "unknown_or_zero": "desconhecida_ou_zero",
    "reported_positive": "valor_positivo_declarado",
    "High usage": "Utilização elevada",
    "Regular usage": "Utilização regular",
    "Limited usage": "Utilização limitada",
    "No current-source minutes": "Sem minutos atuais na fonte",
    "Young talent recruiter": "Recrutador de jovens talentos",
    "Domestic-market recruiter": "Recrutador no mercado nacional",
    "International-market recruiter": "Recrutador no mercado internacional",
    "Development-focused recruiter": "Recrutador orientado para o desenvolvimento",
    "Balanced recruiter": "Recrutador equilibrado",
    "High-volume seller": "Vendedor de grande volume",
    "Young-player seller": "Vendedor de jogadores jovens",
    "International exporter": "Exportador internacional",
    "Elite-talent seller": "Vendedor de talento de elite",
    "Balanced seller": "Vendedor equilibrado",
    "Attack": "Ataque",
    "Defender": "Defesa",
    "Goalkeeper": "Guarda-redes",
    "Midfield": "Meio-campo",
    "right": "direito",
    "left": "esquerdo",
    "both": "ambos",
    "Unknown": "Desconhecido",
    "Limited position depth": "Profundidade limitada na posição",
    "High position age": "Idade elevada na posição",
    "Excessive minute concentration": "Concentração excessiva de minutos",
    "Only one player reached 450 minutes in this broad position.": "Apenas um jogador atingiu 450 minutos nesta posição geral.",
    "Minutes-weighted age is at least 29 in this broad position.": "A idade ponderada por minutos é de pelo menos 29 anos nesta posição geral.",
    "The five highest-usage players account for at least 55% of recorded minutes.": "Os cinco jogadores mais utilizados representam pelo menos 55% dos minutos registados.",
    "Expires within 12 months": "Expira nos próximos 12 meses",
    "Beyond 12 months": "Além de 12 meses",
    "Unavailable": "Indisponível",
    "warning": "aviso",
    "critical": "crítico",
    "PASS": "APROVADO",
    "FAIL": "FALHOU",
    "missing_player_id": "identificador de jogador em falta",
    "duplicate_player_id": "identificador de jogador duplicado",
    "missing_club_id": "identificador de clube em falta",
    "duplicate_club_id": "identificador de clube duplicado",
    "negative_transfer_fee": "valor de transferência negativo",
    "transfer_before_birth": "transferência anterior ao nascimento",
    "negative_minutes": "minutos negativos",
    "duplicate_appearance": "jogo de jogador duplicado",
    "negative_market_value": "valor de mercado negativo",
    "future_transfer": "transferência com data futura",
    "unknown_transfer_fee": "valor de transferência desconhecido",
    "unavailable_loan_type": "tipo de empréstimo indisponível",
    "England": "Inglaterra",
    "Spain": "Espanha",
    "France": "França",
    "Italy": "Itália",
    "Germany": "Alemanha",
    "Brazil": "Brasil",
    "Netherlands": "Países Baixos",
    "Belgium": "Bélgica",
    "Switzerland": "Suíça",
    "Austria": "Áustria",
    "Greece": "Grécia",
    "Turkey": "Turquia",
    "Scotland": "Escócia",
    "Wales": "País de Gales",
    "Ireland": "Irlanda",
    "Northern Ireland": "Irlanda do Norte",
    "United States": "Estados Unidos",
    "Saudi Arabia": "Arábia Saudita",
    "United Arab Emirates": "Emirados Árabes Unidos",
    "Czech Republic": "República Checa",
    "South Korea": "Coreia do Sul",
    "Cape Verde": "Cabo Verde",
    "Guinea-Bissau": "Guiné-Bissau",
    "Morocco": "Marrocos",
    "Egypt": "Egito",
    "Sweden": "Suécia",
    "Norway": "Noruega",
    "Denmark": "Dinamarca",
    "Poland": "Polónia",
    "Romania": "Roménia",
    "Russia": "Rússia",
    "Ukraine": "Ucrânia",
    "Japan": "Japão",
    "China": "China",
    "Australia": "Austrália",
}


def category(value: object) -> object:
    """Translate a known categorical value while preserving source data."""
    if not is_portuguese() or value is None:
        return value
    return CATEGORY_TRANSLATIONS.get(str(value), value)


def country_label(value: object) -> str:
    """Return a presentation label for a country, grouping unmapped values as Other."""
    if value is None or str(value).strip() in {"", "Unknown", "nan", "None"}:
        return tr("Other", "Outros")
    return str(category(value))


def language_selector() -> None:
    """Render the persistent bilingual language control."""
    if LANGUAGE_KEY not in st.session_state:
        st.session_state[LANGUAGE_KEY] = "en"
    st.sidebar.selectbox(
        "Language / Idioma",
        options=["en", "pt"],
        format_func=lambda code: "English" if code == "en" else "Português (Portugal)",
        key=LANGUAGE_KEY,
    )
