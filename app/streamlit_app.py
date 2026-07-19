"""Bilingual application router."""
from __future__ import annotations

import sys
from pathlib import Path

# Streamlit Community Cloud executes this entrypoint from inside ``app``.
# Add the repository root so absolute ``app.*`` and ``src.*`` imports resolve.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st  # noqa: E402

from app.i18n import language_selector, tr  # noqa: E402

st.set_page_config(
    page_title="Football Recruitment Intelligence",
    page_icon="⚽",
    layout="wide",
)

language_selector()

pages = [
    st.Page("pages/0_home.py", title=tr("Home", "Início"), icon="🏠", url_path="home", default=True),
    st.Page("pages/1_market_overview.py", title=tr("Market overview", "Visão do mercado"), icon="📊", url_path="market_overview"),
    st.Page("pages/2_club_recruitment_strategy.py", title=tr("Club recruitment strategy", "Estratégia de recrutamento"), icon="🎯", url_path="club_recruitment_strategy"),
    st.Page("pages/3_talent_development.py", title=tr("Talent development", "Desenvolvimento de talento"), icon="🌱", url_path="talent_development"),
    st.Page("pages/4_loan_player_tracker.py", title=tr("Loan player tracker", "Monitor de empréstimos"), icon="🔁", url_path="loan_player_tracker"),
    st.Page("pages/5_club_selling_model.py", title=tr("Club selling model", "Modelo de vendas"), icon="💶", url_path="club_selling_model"),
    st.Page("pages/6_squad_planning.py", title=tr("Squad planning", "Planeamento do plantel"), icon="🧩", url_path="squad_planning"),
    st.Page("pages/7_transfer_pathways.py", title=tr("Transfer pathways", "Rotas de transferências"), icon="🕸️", url_path="transfer_pathways"),
    st.Page("pages/8_portuguese_players_abroad.py", title=tr("Portuguese players abroad", "Portugueses no estrangeiro"), icon="🌍", url_path="portuguese_players_abroad"),
    st.Page("pages/9_player_profile.py", title=tr("Player profile", "Perfil do jogador"), icon="👤", url_path="player_profile"),
    st.Page("pages/10_methodology.py", title=tr("Methodology", "Metodologia"), icon="📚", url_path="methodology"),
    st.Page("pages/11_about.py", title=tr("About the author", "Sobre o autor"), icon="🧑‍💻", url_path="about"),
]

navigation = st.navigation(pages)
navigation.run()
