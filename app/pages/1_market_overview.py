"""Transfer market overview."""
import plotly.express as px
import streamlit as st

from app.components.cards import compact_number, metric_row
from app.components.charts import style
from app.components.navigation import configure_page, page_header, source_caption
from app.data import query, require_database
from app.i18n import category, tr

configure_page(tr("Market Overview", "Visão do Mercado"), "📊")
page_header(
    tr("Transfer Market Overview", "Visão Geral do Mercado de Transferências"),
    tr(
        "Movement into and out of Portuguese top-flight clubs, using only completed dates and reported positive fees.",
        "Movimentos de entrada e saída dos clubes da primeira divisão portuguesa, considerando apenas datas concluídas e valores positivos declarados.",
    ),
)
require_database()

seasons = query("SELECT DISTINCT transfer_season FROM fact_transfers WHERE transfer_date<=CURRENT_DATE ORDER BY transfer_season DESC")["transfer_season"].tolist()
selected = st.sidebar.multiselect(tr("Season", "Época"), seasons, default=seasons[:5])
direction = st.sidebar.radio(
    tr("Direction", "Direção"),
    ["All", "Incoming", "Outgoing"],
    horizontal=True,
    format_func=category,
)
clauses = ["transfer_date<=CURRENT_DATE"]
params: list[object] = []
if selected:
    clauses.append(f"transfer_season IN ({','.join(['?'] * len(selected))})")
    params.extend(selected)
if direction == "Incoming":
    clauses.append("to_competition_id='PO1'")
elif direction == "Outgoing":
    clauses.append("from_competition_id='PO1'")
where = " AND ".join(clauses)

kpi = query(f"SELECT COUNT(*) transfers, COUNT(transfer_fee_eur) known_fee_records, SUM(transfer_fee_eur) known_fees, AVG(age_at_transfer) avg_age, MEDIAN(age_at_transfer) median_age FROM fact_transfers WHERE {where}", tuple(params)).iloc[0]
metric_row([
    (tr("Transfers", "Transferências"), compact_number(kpi.transfers), tr("Unique source transfer records", "Registos únicos de transferências na fonte")),
    (tr("Known-fee records", "Registos com valor conhecido"), compact_number(kpi.known_fee_records), tr("Strictly positive fees only", "Apenas valores estritamente positivos")),
    (tr("Reported fees", "Valores declarados"), compact_number(kpi.known_fees, True), tr("Not an estimate for unknown zero-coded fees", "Não estima valores desconhecidos registados como zero")),
    (tr("Average age", "Idade média"), f"{kpi.avg_age:.1f}" if kpi.avg_age else tr("Unavailable", "Indisponível"), None),
    (tr("Median age", "Idade mediana"), f"{kpi.median_age:.1f}" if kpi.median_age else tr("Unavailable", "Indisponível"), None),
])

timeline = query(
    f"SELECT DATE_TRUNC('month', transfer_date) AS transfer_month, "
    f"COUNT(*) AS transfers FROM fact_transfers WHERE {where} "
    "GROUP BY transfer_month ORDER BY transfer_month",
    tuple(params),
)
types = query(f"SELECT fee_status, COUNT(*) transfers FROM fact_transfers WHERE {where} GROUP BY fee_status", tuple(params))
types["fee_status_label"] = types["fee_status"].map(category)
c1, c2 = st.columns([2, 1])
c1.plotly_chart(style(px.line(timeline, x="transfer_month", y="transfers", markers=True, title=tr("Transfer activity over time", "Atividade de transferências ao longo do tempo"), labels={"transfer_month": tr("Month", "Mês"), "transfers": tr("Transfers", "Transferências")})), use_container_width=True)
c2.plotly_chart(style(px.pie(types, names="fee_status_label", values="transfers", hole=.55, title=tr("Fee availability", "Disponibilidade dos valores"))), use_container_width=True)

clubs = query(f"SELECT COALESCE(c.club_name, 'Unknown') club, COUNT(*) transfers FROM fact_transfers t LEFT JOIN dim_clubs c ON CASE WHEN t.to_competition_id='PO1' THEN t.to_club_key ELSE t.from_club_key END=c.club_key WHERE {where} GROUP BY club ORDER BY transfers DESC LIMIT 12", tuple(params))
ages = query(f"SELECT age_at_transfer age, COUNT(*) transfers FROM fact_transfers WHERE {where} AND age_at_transfer BETWEEN 15 AND 45 GROUP BY age ORDER BY age", tuple(params))
c1, c2 = st.columns(2)
c1.plotly_chart(style(px.bar(clubs, x="transfers", y="club", orientation="h", title=tr("Most active clubs", "Clubes mais ativos"), labels={"transfers": tr("Transfers", "Transferências"), "club": tr("Club", "Clube")})), use_container_width=True)
c2.plotly_chart(style(px.bar(ages, x="age", y="transfers", title=tr("Transfer age distribution", "Distribuição da idade nas transferências"), labels={"age": tr("Age", "Idade"), "transfers": tr("Transfers", "Transferências")})), use_container_width=True)
source_caption()
