"""Portuguese players abroad monitor."""
import plotly.express as px
import streamlit as st

from app.components.cards import compact_number, metric_row
from app.components.charts import style
from app.components.navigation import configure_page, page_header, source_caption
from app.data import query, require_database
from app.i18n import category, country_label, is_portuguese, tr

configure_page(tr("Portuguese Players Abroad", "Jogadores Portugueses no Estrangeiro"), "🌍")
page_header(
    tr("Portuguese Players Abroad", "Jogadores Portugueses no Estrangeiro"),
    tr(
        "Current-source player profiles outside Portugal, with usage indicators where a covered competition provides minutes.",
        "Perfis atuais de jogadores fora de Portugal, com indicadores de utilização quando existem minutos numa competição coberta.",
    ),
)
require_database()

frame = query("SELECT * FROM portuguese_players_abroad")
u23_only = st.sidebar.checkbox(tr("U23 only", "Apenas Sub-23"))
status = st.sidebar.multiselect(
    tr("Usage status", "Estado de utilização"),
    sorted(frame.usage_status.dropna().unique().tolist()),
    format_func=category,
)
if u23_only:
    frame = frame[frame.age < 23]
if status:
    frame = frame[frame.usage_status.isin(status)]
metric_row([
    (tr("Players", "Jogadores"), compact_number(len(frame)), None),
    (tr("Countries", "Países"), compact_number(frame.country.nunique()), None),
    (tr("U23", "Sub-23"), compact_number((frame.age < 23).sum()), None),
    (tr("Known market value", "Valor de mercado conhecido"), compact_number(frame.market_value_eur.sum(), True), None),
])

country = frame.groupby("country", dropna=False).size().rename("players").reset_index()
country["country_label"] = country["country"].map(country_label)
c1, c2 = st.columns(2)
c1.plotly_chart(style(px.choropleth(country.dropna(), locations="country", locationmode="country names", color="players", color_continuous_scale="Teal", title=tr("Geographic distribution", "Distribuição geográfica"), labels={"players": tr("Players", "Jogadores")})), use_container_width=True)
c2.plotly_chart(style(px.bar(country.sort_values("players").tail(15), x="players", y="country_label", orientation="h", title=tr("Largest country groups", "Principais grupos por país"), labels={"players": tr("Players", "Jogadores"), "country_label": tr("Country", "País")})), use_container_width=True)
player_table = frame[["player", "club", "country", "competition_id", "age", "position", "minutes", "appearances", "market_value_eur", "usage_status"]].sort_values("market_value_eur", ascending=False)
if is_portuguese():
    player_table["position"] = player_table["position"].map(category)
    player_table["usage_status"] = player_table["usage_status"].map(category)
    player_table["country"] = player_table["country"].map(country_label)
    player_table = player_table.rename(columns={"player": "jogador", "club": "clube", "country": "país", "competition_id": "competição", "age": "idade", "position": "posição", "minutes": "minutos", "appearances": "jogos", "market_value_eur": "valor_mercado_eur", "usage_status": "estado_utilização"})
else:
    player_table["country"] = player_table["country"].map(country_label)
st.dataframe(player_table, use_container_width=True, hide_index=True)
st.info(tr("Potential return suitability is not asserted: financial, tactical and contractual feasibility are outside the available evidence.", "Não é avaliada a adequação de um possível regresso: a viabilidade financeira, tática e contratual está fora da evidência disponível."))
source_caption()
