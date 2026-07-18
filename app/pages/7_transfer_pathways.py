"""Transfer pathway Sankey analysis."""
import plotly.graph_objects as go
import streamlit as st

from app.components.charts import style
from app.components.navigation import configure_page, page_header, source_caption
from app.data import query, require_database
from app.i18n import country_label, is_portuguese, tr

configure_page(tr("Transfer Pathways", "Rotas de Transferências"), "🕸️")
page_header(
    tr("Transfer Pathways", "Rotas de Transferências"),
    tr(
        "How players move between Portugal and international markets, aggregated without uncertain entity joins.",
        "Como os jogadores se movimentam entre Portugal e os mercados internacionais, sem associações incertas entre entidades.",
    ),
)
require_database()

minimum = st.sidebar.slider(tr("Minimum transfers per route", "Mínimo de transferências por rota"), 1, 25, 3)
frame = query("SELECT source_country, destination_country, SUM(transfer_count) transfer_count, AVG(average_age) average_age, SUM(transfers_with_known_fee) known_fee_records FROM transfer_pathways GROUP BY source_country, destination_country HAVING SUM(transfer_count)>=? ORDER BY transfer_count DESC", (minimum,))
frame["source_country"] = frame["source_country"].map(country_label)
frame["destination_country"] = frame["destination_country"].map(country_label)
labels = sorted(set(frame.source_country.tolist()) | set(frame.destination_country.tolist()))
index = {name: idx for idx, name in enumerate(labels)}
figure = go.Figure(go.Sankey(
    node=dict(label=labels, pad=14, thickness=16, color="#0b1f33"),
    link=dict(source=[index[x] for x in frame.source_country], target=[index[x] for x in frame.destination_country], value=frame.transfer_count, color="rgba(16,163,127,.25)")
))
figure.update_layout(title=tr("Country-to-country transfer routes", "Rotas de transferências entre países"))
st.plotly_chart(style(figure, 600), use_container_width=True)
if is_portuguese():
    frame = frame.rename(columns={"source_country": "país_origem", "destination_country": "país_destino", "transfer_count": "número_transferências", "average_age": "idade_média", "known_fee_records": "registos_valor_conhecido"})
st.dataframe(frame, use_container_width=True, hide_index=True)
st.caption(tr(
    "Unmapped club-country records are displayed as Other and are not inferred from club names.",
    "Os registos sem associação entre clube e país são apresentados como Outros e não são inferidos através do nome do clube.",
))
source_caption()
