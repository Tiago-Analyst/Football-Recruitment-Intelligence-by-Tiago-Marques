"""Methodology, provenance and data-quality page."""
import streamlit as st

from app.components.navigation import configure_page, page_header
from app.data import query, require_database
from app.i18n import category, is_portuguese, tr

configure_page(tr("Methodology", "Metodologia"), "📚")
page_header(
    tr("Methodology & Data Quality", "Metodologia e Qualidade dos Dados"),
    tr(
        "Provenance, field availability, transparent formulas and pipeline health.",
        "Proveniência, disponibilidade de campos, fórmulas transparentes e estado do pipeline.",
    ),
)
require_database()

refresh = query("SELECT * FROM powerbi_last_refresh")
quality = query("SELECT rule_name, severity, status, issue_count, checked_at FROM data_quality_results ORDER BY severity, rule_name")
if not refresh.empty:
    st.success(f"{tr('Last refresh', 'Última atualização')}: {refresh.iloc[0].last_refresh} · {tr('Source', 'Fonte')}: {refresh.iloc[0].source_name}")

tabs = st.tabs([
    tr("Sources", "Fontes"),
    tr("Availability", "Disponibilidade"),
    tr("Metrics", "Métricas"),
    tr("Quality", "Qualidade"),
    tr("Matching & licence", "Correspondência e licença"),
])
with tabs[0]:
    st.markdown(tr("**Selected source:** [transfermarkt-datasets](https://github.com/dcaribou/transfermarkt-datasets), a weekly refreshed CC0 DuckDB/CSV publication. OpenFootball and football-data.org were tested but not merged because they do not add transfer/value depth with an entity-safe player bridge.", "**Fonte selecionada:** [transfermarkt-datasets](https://github.com/dcaribou/transfermarkt-datasets), uma publicação DuckDB/CSV CC0 atualizada semanalmente. OpenFootball e football-data.org foram testados, mas não foram combinados porque não acrescentam detalhe de transferências/valores com uma ligação segura entre jogadores."))
with tabs[1]:
    availability = {
        tr("Field area", "Área de dados"): [
            tr("Transfers", "Transferências"), tr("Appearances/minutes", "Jogos/minutos"),
            tr("Valuations", "Avaliações"), tr("Contracts", "Contratos"),
            tr("Loans", "Empréstimos"), tr("Academy origin", "Origem na formação"),
            tr("Liga Portugal 2 player detail", "Detalhe de jogadores da Liga Portugal 2"),
        ],
        tr("Status", "Estado"): [
            tr("Available; type unavailable", "Disponível; tipo indisponível"),
            tr("Available for PO1", "Disponível para PO1"), tr("Available", "Disponível"),
            tr("Current profile only", "Apenas perfil atual"), tr("Unavailable", "Indisponível"),
            tr("Unavailable", "Indisponível"), tr("Unavailable in primary source", "Indisponível na fonte principal"),
        ],
        tr("Impact", "Impacto"): [
            tr("Zero is unknown, never labelled free/loan", "Zero é desconhecido, nunca classificado como livre/empréstimo"),
            tr("Youth usage supported", "Utilização de jovens suportada"),
            tr("Historical trends supported", "Tendências históricas suportadas"),
            tr("Use cautiously", "Utilizar com prudência"), tr("Tracker disabled", "Monitor desativado"),
            tr("Academy metrics disabled", "Métricas de formação desativadas"),
            tr("Not entity-merged", "Sem combinação entre entidades"),
        ],
    }
    st.dataframe(availability, use_container_width=True, hide_index=True)
with tabs[2]:
    st.markdown(tr("""
    - **Reported fees:** strictly positive source values; zero becomes null/unknown.
    - **Age:** completed years on the transfer or match date.
    - **U21/U23 minute share:** youth minutes divided by all recorded club minutes.
    - **Development Index:** 45% U21 minute share + 30% U23 minute share + 25% capped U23-player breadth.
    - **Squad alert thresholds:** 450 meaningful minutes; top-five concentration warning at 55%; position-age warning at 29.
    """, """
    - **Valores declarados:** valores estritamente positivos na fonte; zero torna-se nulo/desconhecido.
    - **Idade:** anos completos na data da transferência ou do jogo.
    - **Percentagem de minutos Sub-21/Sub-23:** minutos dos jovens divididos por todos os minutos registados pelo clube.
    - **Índice de Desenvolvimento:** 45% de minutos Sub-21 + 30% de minutos Sub-23 + 25% da amplitude limitada de jogadores Sub-23.
    - **Limites dos alertas do plantel:** 450 minutos relevantes; alerta de concentração dos cinco principais aos 55%; alerta de idade por posição aos 29 anos.
    """))
with tabs[3]:
    if is_portuguese():
        quality["rule_name"] = quality["rule_name"].map(category)
        quality["severity"] = quality["severity"].map(category)
        quality["status"] = quality["status"].map(category)
        quality = quality.rename(columns={"rule_name": "regra", "severity": "gravidade", "status": "estado", "issue_count": "número_problemas", "checked_at": "verificado_em"})
    st.dataframe(quality, use_container_width=True, hide_index=True)
with tabs[4]:
    st.markdown(tr("Names are normalised only to generate candidates. Automatic player matches require corroboration from date of birth plus nationality/position; ambiguous cases go to `entity_matching_review`. The MVP uses one source, so no cross-source player merge is performed. Dataset code and publication licence: **CC0-1.0**. Users should retain attribution and review upstream terms before commercial deployment.", "Os nomes são normalizados apenas para gerar candidatos. As correspondências automáticas de jogadores exigem confirmação através da data de nascimento e nacionalidade/posição; os casos ambíguos seguem para `entity_matching_review`. O MVP utiliza uma única fonte, pelo que não é feita qualquer combinação de jogadores entre fontes. Código e licença de publicação do conjunto de dados: **CC0-1.0**. Os utilizadores devem manter a atribuição e rever os termos da fonte antes de utilização comercial."))
