"""Loan tracker availability page."""
import streamlit as st

from app.components.navigation import configure_page, page_header, source_caption
from app.data import query, require_database
from app.i18n import tr

configure_page(tr("Loan Player Tracker", "Monitor de Jogadores Emprestados"), "🔁")
page_header(
    tr("Loan Player Tracker", "Monitor de Jogadores Emprestados"),
    tr(
        "A controlled availability state prevents zero-fee transfers from being misclassified as loans.",
        "Um estado de disponibilidade controlado impede que transferências sem valor declarado sejam classificadas incorretamente como empréstimos.",
    ),
)
require_database()

st.markdown(
    '<div class="fri-warning">'
    + tr(
        "Loan tracking is unavailable in this MVP because the selected source does not expose a reliable transfer-type, parent-club, loan-start or loan-end field.",
        "O acompanhamento de empréstimos está indisponível neste MVP porque a fonte selecionada não disponibiliza campos fiáveis para o tipo de transferência, clube detentor, início ou fim do empréstimo.",
    )
    + "</div>",
    unsafe_allow_html=True,
)
st.markdown(tr("""
#### Why this module is disabled

- A zero transfer fee can mean free transfer, loan, undisclosed fee, return, or missing data.
- Inferring a loan from a later reverse transfer would still be ambiguous.
- Usage categories such as “Successful Loan” require a verified loan spell plus minutes, starts and competition level.

The warehouse includes a typed, empty `fact_loans` table so a future licensed source can be added without changing the downstream schema. No player is classified from unsupported evidence.
""", """
#### Porque está este módulo desativado

- Um valor de transferência zero pode significar transferência livre, empréstimo, valor não divulgado, regresso ou dados em falta.
- Inferir um empréstimo através de uma transferência posterior no sentido inverso continuaria a ser ambíguo.
- Categorias de utilização como “Empréstimo bem-sucedido” exigem um empréstimo verificado, minutos, titularidades e nível competitivo.

O armazém de dados inclui uma tabela `fact_loans` tipada e vazia, permitindo adicionar futuramente uma fonte licenciada sem alterar o esquema de dados. Nenhum jogador é classificado com base em evidência não suportada.
"""))
status = query("SELECT availability_note FROM fact_loans")
st.code(tr("Required fields", "Campos necessários") + ": transfer_type, parent_club_id, loan_club_id, loan_start_date, loan_end_date")
source_caption()
