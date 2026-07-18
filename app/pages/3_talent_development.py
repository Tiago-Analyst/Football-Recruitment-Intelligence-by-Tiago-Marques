"""Talent development monitor."""
import plotly.express as px
import streamlit as st

from app.components.cards import metric_row
from app.components.charts import style
from app.components.navigation import configure_page, page_header, source_caption
from app.data import query, require_database
from app.i18n import is_portuguese, tr

configure_page(tr("Talent Development", "Desenvolvimento de Talento"), "🌱")
page_header(
    tr("Talent Development Monitor", "Monitor de Desenvolvimento de Talento"),
    tr(
        "Youth exposure and minutes-based development indicators. Academy origin and club-spell value growth are not available.",
        "Exposição de jovens e indicadores de desenvolvimento baseados em minutos. A origem na formação e o crescimento de valor por passagem no clube não estão disponíveis.",
    ),
)
require_database()

seasons = query("SELECT DISTINCT season FROM fact_player_development ORDER BY season DESC")["season"].tolist()
season = st.sidebar.selectbox(tr("Season", "Época"), seasons)
frame = query("SELECT d.*, c.club_name FROM fact_player_development d JOIN dim_clubs c USING(club_key) WHERE season=? ORDER BY development_index DESC", (season,))
if frame.empty:
    st.warning(tr("No development data for this season.", "Não existem dados de desenvolvimento para esta época."))
    st.stop()
leader = frame.iloc[0]
metric_row([
    (tr("Leading club", "Clube líder"), leader.club_name, None),
    (tr("Development Index", "Índice de Desenvolvimento"), f"{leader.development_index:.1f}", tr("Directional, configurable youth-usage index", "Índice direcional e configurável de utilização de jovens")),
    (tr("U21 minute share", "Percentagem de minutos Sub-21"), f"{leader.u21_minutes_share:.1%}", None),
    (tr("U23 players used", "Jogadores Sub-23 utilizados"), f"{leader.u23_players_used:,}", None),
])

st.plotly_chart(style(px.bar(frame, x="development_index", y="club_name", orientation="h", color="u21_minutes_share", title=tr("Club Development Index", "Índice de Desenvolvimento por Clube"), labels={"development_index": tr("Development Index", "Índice de Desenvolvimento"), "club_name": tr("Club", "Clube"), "u21_minutes_share": tr("U21 minute share", "Minutos Sub-21")}), 520), use_container_width=True)
c1, c2 = st.columns(2)
c1.plotly_chart(style(px.scatter(frame, x="u23_players_used", y="u23_minutes_share", size="total_minutes", hover_name="club_name", title=tr("Youth breadth vs exposure", "Amplitude de jovens vs exposição"), labels={"u23_players_used": tr("U23 players used", "Jogadores Sub-23 utilizados"), "u23_minutes_share": tr("U23 minute share", "Percentagem de minutos Sub-23")})), use_container_width=True)
table = frame[["club_name", "u19_players_used", "u21_players_used", "u23_players_used", "u21_minutes_share", "minutes_weighted_age"]]
if is_portuguese():
    table = table.rename(columns={"club_name": "clube", "u19_players_used": "jogadores_sub19", "u21_players_used": "jogadores_sub21", "u23_players_used": "jogadores_sub23", "u21_minutes_share": "percentagem_minutos_sub21", "minutes_weighted_age": "idade_ponderada_por_minutos"})
c2.dataframe(table, use_container_width=True, hide_index=True)
st.caption(tr("Index = 45% U21 minute share + 30% U23 minute share + 25% capped U23 player count. It is a directional analytical tool, not an objective universal ranking.", "Índice = 45% da percentagem de minutos Sub-21 + 30% da percentagem de minutos Sub-23 + 25% do número limitado de jogadores Sub-23. É uma ferramenta analítica direcional, não uma classificação universal objetiva."))
source_caption()
