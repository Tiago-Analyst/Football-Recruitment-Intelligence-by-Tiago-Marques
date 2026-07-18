"""Club selling model page."""
import plotly.express as px
import streamlit as st

from app.components.cards import compact_number, metric_row
from app.components.charts import style
from app.components.navigation import configure_page, page_header, source_caption
from app.data import query, require_database
from app.i18n import category, country_label, is_portuguese, tr

configure_page(tr("Club Selling Model", "Modelo de Vendas do Clube"), "💶")
page_header(
    tr("Club Selling Model", "Modelo de Vendas do Clube"),
    tr(
        "Outgoing transfer volume, reported proceeds, sale age and destination markets.",
        "Volume de saídas, receitas declaradas, idade de venda e mercados de destino.",
    ),
)
require_database()

clubs = query("SELECT club_key, club_name FROM dim_clubs WHERE domestic_competition_id='PO1' ORDER BY club_name")
club_name = st.sidebar.selectbox(tr("Club", "Clube"), clubs.club_name.tolist())
club_key = int(clubs.loc[clubs.club_name == club_name, "club_key"].iloc[0])
profile = query("SELECT selling_profile FROM club_profiles WHERE club_key=?", (club_key,))
profile_label = category(profile.iloc[0, 0]) if not profile.empty else tr("Insufficient data", "Dados insuficientes")
st.info(f"{tr('Rule-based profile', 'Perfil baseado em regras')}: **{profile_label}**")

summary = query("SELECT SUM(sales_count) sales, SUM(known_sales_eur) proceeds, AVG(average_sale_age) avg_age, AVG(u23_sale_share) u23_share, AVG(international_share) intl_share FROM fact_club_sales WHERE club_key=?", (club_key,)).iloc[0]
metric_row([
    (tr("Outgoing records", "Registos de saída"), compact_number(summary.sales), None),
    (tr("Reported proceeds", "Receitas declaradas"), compact_number(summary.proceeds, True), tr("Positive reported fees only", "Apenas valores positivos declarados")),
    (tr("Average sale age", "Idade média de venda"), f"{summary.avg_age:.1f}" if summary.avg_age else tr("Unavailable", "Indisponível"), None),
    (tr("U23 sale share", "Percentagem de vendas Sub-23"), f"{summary.u23_share:.0%}" if summary.u23_share is not None else tr("Unavailable", "Indisponível"), None),
    (tr("International share", "Percentagem internacional"), f"{summary.intl_share:.0%}" if summary.intl_share is not None else tr("Unavailable", "Indisponível"), None),
])

by_season = query("SELECT * FROM fact_club_sales WHERE club_key=? ORDER BY transfer_season", (club_key,))
destinations = query("SELECT COALESCE(to_country,'Unknown') destination, COUNT(*) transfers, SUM(transfer_fee_eur) known_fees FROM fact_transfers WHERE from_club_key=? AND transfer_date<=CURRENT_DATE GROUP BY destination ORDER BY transfers DESC LIMIT 12", (club_key,))
destinations["destination"] = destinations["destination"].map(country_label)
c1, c2 = st.columns(2)
c1.plotly_chart(style(px.bar(by_season, x="transfer_season", y="known_sales_eur", title=tr("Reported sales by season", "Vendas declaradas por época"), labels={"transfer_season": tr("Season", "Época"), "known_sales_eur": tr("Known sales (EUR)", "Vendas conhecidas (EUR)")})), use_container_width=True)
c2.plotly_chart(style(px.bar(destinations, x="transfers", y="destination", orientation="h", title=tr("Destination markets", "Mercados de destino"), labels={"transfers": tr("Transfers", "Transferências"), "destination": tr("Destination", "Destino")})), use_container_width=True)

sales = query("SELECT transfer_date, player_name, position, age_at_transfer, to_club, to_country, transfer_fee_eur FROM clean_transfers WHERE from_club_key=? AND transfer_date<=CURRENT_DATE ORDER BY transfer_fee_eur DESC NULLS LAST", (club_key,))
if is_portuguese():
    sales["to_country"] = sales["to_country"].map(country_label)
    sales = sales.rename(columns={"transfer_date": "data_transferência", "player_name": "jogador", "position": "posição", "age_at_transfer": "idade_na_transferência", "to_club": "clube_destino", "to_country": "país_destino", "transfer_fee_eur": "valor_transferência_eur"})
else:
    sales["to_country"] = sales["to_country"].map(country_label)
st.subheader(tr("Major reported sales", "Principais vendas declaradas"))
st.dataframe(sales.head(30), use_container_width=True, hide_index=True)
source_caption()
