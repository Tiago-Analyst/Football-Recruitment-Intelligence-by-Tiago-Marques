"""Club recruitment strategy page."""
import plotly.express as px
import streamlit as st

from app.components.cards import compact_number, metric_row
from app.components.charts import style
from app.components.navigation import configure_page, page_header, source_caption
from app.data import query, require_database
from app.i18n import category, country_label, is_portuguese, tr

configure_page(tr("Club Recruitment", "Recrutamento do Clube"), "🎯")
page_header(
    tr("Club Recruitment Strategy", "Estratégia de Recrutamento do Clube"),
    tr(
        "Compare age, origin market and known-fee patterns for incoming players.",
        "Compare a idade, mercados de origem e padrões de valores conhecidos dos jogadores contratados.",
    ),
)
require_database()

clubs = query("SELECT club_key, club_name FROM dim_clubs WHERE domestic_competition_id='PO1' ORDER BY club_name")
club_name = st.sidebar.selectbox(tr("Club", "Clube"), clubs.club_name.tolist())
club_key = int(clubs.loc[clubs.club_name == club_name, "club_key"].iloc[0])
profile = query("SELECT recruitment_profile FROM club_profiles WHERE club_key=?", (club_key,))
profile_label = category(profile.iloc[0, 0]) if not profile.empty else tr("Insufficient data", "Dados insuficientes")
st.info(f"{tr('Rule-based profile', 'Perfil baseado em regras')}: **{profile_label}**")

summary = query("SELECT SUM(players_recruited) recruited, AVG(average_recruitment_age) avg_age, SUM(known_spending_eur) spending, AVG(u23_share) u23_share, AVG(international_share) intl_share FROM fact_club_recruitment WHERE club_key=?", (club_key,)).iloc[0]
metric_row([
    (tr("Recruited", "Contratados"), compact_number(summary.recruited), None),
    (tr("Average age", "Idade média"), f"{summary.avg_age:.1f}" if summary.avg_age else tr("Unavailable", "Indisponível"), None),
    (tr("Known spending", "Despesa conhecida"), compact_number(summary.spending, True), tr("Positive reported fees only", "Apenas valores positivos declarados")),
    (tr("U23 share", "Percentagem Sub-23"), f"{summary.u23_share:.0%}" if summary.u23_share is not None else tr("Unavailable", "Indisponível"), None),
    (tr("International share", "Percentagem internacional"), f"{summary.intl_share:.0%}" if summary.intl_share is not None else tr("Unavailable", "Indisponível"), None),
])

by_season = query("SELECT * FROM fact_club_recruitment WHERE club_key=? ORDER BY transfer_season", (club_key,))
markets = query("SELECT COALESCE(from_country,'Unknown') market, COUNT(*) players FROM fact_transfers WHERE to_club_key=? AND transfer_date<=CURRENT_DATE GROUP BY market ORDER BY players DESC LIMIT 12", (club_key,))
markets["market"] = markets["market"].map(country_label)
c1, c2 = st.columns(2)
c1.plotly_chart(style(px.line(by_season, x="transfer_season", y="average_recruitment_age", markers=True, title=tr("Recruitment age by season", "Idade de recrutamento por época"), labels={"transfer_season": tr("Season", "Época"), "average_recruitment_age": tr("Average age", "Idade média")})), use_container_width=True)
c2.plotly_chart(style(px.bar(markets, x="players", y="market", orientation="h", title=tr("Source markets", "Mercados de origem"), labels={"players": tr("Players", "Jogadores"), "market": tr("Market", "Mercado")})), use_container_width=True)

players = query("SELECT transfer_date, player_name, position, age_at_transfer, from_club, from_country, transfer_fee_eur, fee_status FROM clean_transfers WHERE to_club_key=? AND transfer_date<=CURRENT_DATE ORDER BY transfer_date DESC", (club_key,))
if is_portuguese():
    players["from_country"] = players["from_country"].map(country_label)
    players = players.rename(columns={"transfer_date": "data_transferência", "player_name": "jogador", "position": "posição", "age_at_transfer": "idade_na_transferência", "from_club": "clube_origem", "from_country": "país_origem", "transfer_fee_eur": "valor_transferência_eur", "fee_status": "estado_valor"})
else:
    players["from_country"] = players["from_country"].map(country_label)
st.subheader(tr("Recruitment ledger", "Registo de recrutamento"))
st.dataframe(players, use_container_width=True, hide_index=True)
source_caption()
