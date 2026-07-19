"""Detailed player profile."""
import plotly.express as px
import streamlit as st

from app.components.charts import style
from app.components.navigation import configure_page, page_header, source_caption
from app.data import query, require_database
from app.i18n import category, is_portuguese, tr

configure_page(tr("Player Profile", "Perfil do Jogador"), "👤")
page_header(
    tr("Player Profile", "Perfil do Jogador"),
    tr(
        "Identity, season usage, transfer history and market-value trajectory from a single stable source ID.",
        "Identidade, utilização por época, histórico de transferências e evolução do valor de mercado através de um identificador estável.",
    ),
)
require_database()

search = st.sidebar.text_input(tr("Search player", "Pesquisar jogador"), "")
if len(search) >= 2:
    players = query("SELECT player_key, name, current_club_name FROM dim_players WHERE name ILIKE ? ORDER BY name LIMIT 100", (f"%{search}%",))
else:
    players = query("""
        SELECT DISTINCT p.player_key, p.name, p.current_club_name,
               p.market_value_in_eur
        FROM fact_squad_snapshots s
        JOIN dim_players p USING(player_key)
        ORDER BY p.market_value_in_eur DESC NULLS LAST, p.name
        LIMIT 500
    """)
if players.empty:
    st.warning(tr("No player found.", "Nenhum jogador encontrado."))
    st.stop()
label = st.sidebar.selectbox(
    tr("Player", "Jogador"),
    [f"{r.name} · {r.current_club_name or tr('No current club', 'Sem clube atual')} · #{r.player_key}" for r in players.itertuples()],
)
player_key = int(label.rsplit("#", 1)[1])
profile = query("SELECT * FROM dim_players WHERE player_key=?", (player_key,)).iloc[0]

c1, c2 = st.columns([1, 3])
with c1:
    if profile.image_url:
        st.image(profile.image_url, width=180)
with c2:
    st.subheader(profile["name"])
    unavailable = tr("Unavailable", "Indisponível")
    st.write(
        f"**{tr('Club', 'Clube')}:** {profile.current_club_name or unavailable}  \n"
        f"**{tr('Nationality', 'Nacionalidade')}:** {profile.nationality or unavailable}  \n"
        f"**{tr('Position', 'Posição')}:** {category(profile.position) or unavailable} / {profile.sub_position or unavailable}  \n"
        f"**{tr('Date of birth', 'Data de nascimento')}:** {profile.date_of_birth or unavailable}  \n"
        f"**{tr('Foot', 'Pé preferido')}:** {category(profile.foot) or unavailable} · "
        f"**{tr('Height', 'Altura')}:** {profile.height_in_cm or unavailable} cm"
    )

stats = query("SELECT season, club_name, appearances, minutes, goals, assists FROM clean_player_statistics WHERE player_key=? ORDER BY season", (player_key,))
valuations = query("SELECT date, market_value_eur FROM fact_player_valuations WHERE player_key=? ORDER BY date", (player_key,))
transfers = query("SELECT transfer_date, from_club, to_club, transfer_fee_eur, market_value_at_transfer_eur, fee_status FROM clean_transfers WHERE player_key=? ORDER BY transfer_date", (player_key,))
c1, c2 = st.columns(2)
c1.plotly_chart(style(px.bar(stats, x="season", y="minutes", color="club_name", title=tr("Minutes by season", "Minutos por época"), labels={"season": tr("Season", "Época"), "minutes": tr("Minutes", "Minutos"), "club_name": tr("Club", "Clube")})), use_container_width=True)
c2.plotly_chart(style(px.line(valuations, x="date", y="market_value_eur", title=tr("Market-value history", "Histórico do valor de mercado"), labels={"date": tr("Date", "Data"), "market_value_eur": tr("Market value (EUR)", "Valor de mercado (EUR)")})), use_container_width=True)
if is_portuguese():
    transfers = transfers.rename(columns={"transfer_date": "data_transferência", "from_club": "clube_origem", "to_club": "clube_destino", "transfer_fee_eur": "valor_transferência_eur", "market_value_at_transfer_eur": "valor_mercado_na_transferência_eur", "fee_status": "estado_valor"})
    stats = stats.rename(columns={"season": "época", "club_name": "clube", "appearances": "jogos", "minutes": "minutos", "goals": "golos", "assists": "assistências"})
st.subheader(tr("Transfer history", "Histórico de transferências"))
st.dataframe(transfers, use_container_width=True, hide_index=True)
st.subheader(tr("Appearance history", "Histórico de jogos"))
st.dataframe(stats, use_container_width=True, hide_index=True)
st.caption(tr("Loan history is unavailable because transfer nature is not exposed by the source.", "O histórico de empréstimos está indisponível porque a natureza da transferência não é fornecida pela fonte."))
source_caption()
