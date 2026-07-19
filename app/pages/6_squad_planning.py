"""Squad planning and age structure."""
import plotly.express as px
import streamlit as st

from app.components.cards import compact_number, metric_row
from app.components.charts import style
from app.components.navigation import configure_page, page_header, source_caption
from app.data import query, require_database
from app.i18n import category, is_portuguese, tr

configure_page(tr("Squad Planning", "Planeamento do Plantel"), "🧩")
page_header(
    tr("Squad Planning & Age Structure", "Planeamento do Plantel e Estrutura Etária"),
    tr(
        "Latest-source roster age/value structure plus recent minutes-based depth and concentration alerts.",
        "Estrutura de idade e valor do plantel na versão mais recente da fonte, com alertas recentes de profundidade e concentração baseados em minutos.",
    ),
)
require_database()

clubs = query("SELECT DISTINCT s.club_key, c.club_name FROM fact_squad_snapshots s JOIN dim_clubs c USING(club_key) ORDER BY club_name")
club_name = st.sidebar.selectbox(tr("Club", "Clube"), clubs.club_name.tolist())
club_key = int(clubs.loc[clubs.club_name == club_name, "club_key"].iloc[0])
squad = query("SELECT s.*, p.name player FROM fact_squad_snapshots s JOIN dim_players p USING(player_key) WHERE club_key=?", (club_key,))
alerts = query("SELECT context, alert_type, alert_message, severity FROM squad_alerts WHERE club_key=?", (club_key,))

metric_row([
    (tr("Squad size", "Tamanho do plantel"), compact_number(len(squad)), None),
    (tr("Average age", "Idade média"), f"{squad.age.mean():.1f}" if not squad.empty else tr("Unavailable", "Indisponível"), None),
    (tr("U23 players", "Jogadores Sub-23"), compact_number((squad.age < 23).sum()), None),
    (tr("Market value", "Valor de mercado"), compact_number(squad.market_value_eur.sum(), True), None),
    (tr("Alerts", "Alertas"), compact_number(len(alerts)), None),
])

c1, c2 = st.columns(2)
squad["position_label"] = squad["position"].map(category)
c1.plotly_chart(style(px.histogram(squad, x="age", color="position_label", nbins=18, title=tr("Squad age distribution", "Distribuição etária do plantel"), labels={"age": tr("Age", "Idade"), "count": tr("Count", "Número"), "position_label": tr("Position", "Posição")})), use_container_width=True)
value = squad.groupby("position", dropna=False).agg(players=("player_key", "count"), market_value_eur=("market_value_eur", "sum")).reset_index()
value["position_label"] = value["position"].map(category)
c2.plotly_chart(style(px.bar(value, x="position_label", y="market_value_eur", color="players", title=tr("Market value by position", "Valor de mercado por posição"), labels={"position_label": tr("Position", "Posição"), "market_value_eur": tr("Market value (EUR)", "Valor de mercado (EUR)"), "players": tr("Players", "Jogadores")})), use_container_width=True)
st.subheader(tr("Squad alerts", "Alertas do plantel"))
if alerts.empty:
    st.success(tr("No configured alerts triggered for the latest observed season.", "Nenhum alerta configurado foi acionado na última época observada."))
else:
    if is_portuguese():
        alerts["alert_type"] = alerts["alert_type"].map(category)
        alerts["alert_message"] = alerts["alert_message"].map(category)
        alerts["severity"] = alerts["severity"].map(category)
        alerts = alerts.rename(columns={"context": "contexto", "alert_type": "tipo_alerta", "alert_message": "mensagem_alerta", "severity": "gravidade"})
    st.dataframe(alerts, use_container_width=True, hide_index=True)
st.subheader(tr("Latest-source roster snapshot", "Retrato do plantel na fonte mais recente"))
squad_table = squad[["player", "age", "position_label", "sub_position", "market_value_eur", "contract_expiration_date", "contract_status"]].sort_values(["position_label", "age"])
if is_portuguese():
    squad_table["contract_status"] = squad_table["contract_status"].map(category)
    squad_table = squad_table.rename(columns={"player": "jogador", "age": "idade", "position_label": "posição", "sub_position": "subposição", "market_value_eur": "valor_mercado_eur", "contract_expiration_date": "fim_contrato", "contract_status": "estado_contrato"})
st.dataframe(squad_table, use_container_width=True, hide_index=True)
st.caption(tr(
    "The roster includes players and clubs whose last source season matches the latest available season.",
    "O plantel inclui jogadores e clubes cuja última época na fonte corresponde à época mais recente disponível.",
))
st.caption(tr("Contract status uses the source's current profile field. It is not historical and should be revalidated before operational decisions.", "O estado contratual utiliza o campo atual do perfil na fonte. Não é histórico e deve ser novamente validado antes de decisões operacionais."))
source_caption()
