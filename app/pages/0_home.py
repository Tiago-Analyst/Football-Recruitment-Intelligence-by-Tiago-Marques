"""Bilingual landing page."""
from __future__ import annotations

import streamlit as st

from app.components.navigation import configure_page, page_header
from app.data import query, require_database
from app.i18n import tr

configure_page(tr("Home", "Início"))
page_header(
    tr(
        "Football Recruitment & Development Intelligence",
        "Inteligência de Recrutamento e Desenvolvimento no Futebol",
    ),
    tr(
        "A decision-support product for understanding how Portuguese clubs recruit, develop, value and sell players.",
        "Um produto de apoio à decisão para compreender como os clubes portugueses recrutam, desenvolvem, valorizam e vendem jogadores.",
    ),
)
require_database()

refresh = query("SELECT * FROM powerbi_last_refresh")
clubs = query("SELECT COUNT(*) AS n FROM dim_clubs WHERE domestic_competition_id='PO1'").iloc[0, 0]
players = query("SELECT COUNT(DISTINCT player_key) AS n FROM fact_player_appearances").iloc[0, 0]
transfers = query("SELECT COUNT(*) AS n FROM fact_transfers WHERE transfer_date<=CURRENT_DATE").iloc[0, 0]

c1, c2, c3 = st.columns(3)
c1.metric(tr("Portuguese clubs tracked", "Clubes portugueses acompanhados"), f"{clubs:,}")
c2.metric(tr("Players observed", "Jogadores observados"), f"{players:,}")
c3.metric(tr("Transfers in scope", "Transferências analisadas"), f"{transfers:,}")

st.markdown(tr("### What this product answers", "### Perguntas a que este produto responde"))
st.markdown(
    tr(
        """
- Which markets, positions and age bands does each club recruit from?
- Which clubs give meaningful first-team minutes to young players?
- Where do Portuguese clubs sell, and which pathways carry the most reported value?
- Where are Portuguese players abroad, and how much current-source usage do they have?
- Where do squad age, depth and minute concentration create planning risk?
        """,
        """
- Em que mercados, posições e faixas etárias recruta cada clube?
- Que clubes dão minutos relevantes na equipa principal a jogadores jovens?
- Para onde vendem os clubes portugueses e que rotas geram mais valor declarado?
- Onde jogam os portugueses no estrangeiro e qual é o seu nível de utilização?
- Onde é que a idade, profundidade e concentração de minutos criam risco no plantel?
        """,
    )
)
st.info(
    tr(
        "Use the navigation to explore each module. Loan analysis is disabled because the source has no reliable loan-type field.",
        "Utilize a navegação para explorar cada módulo. A análise de empréstimos está desativada porque a fonte não possui um campo fiável para o tipo de empréstimo.",
    )
)
if not refresh.empty:
    st.caption(
        tr("Latest pipeline refresh", "Última atualização do pipeline")
        + f": {refresh.iloc[0]['last_refresh']} · "
        + tr("Source", "Fonte")
        + f": {refresh.iloc[0]['source_name']}"
    )
