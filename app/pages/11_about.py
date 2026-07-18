"""Bilingual author and project background page."""
from __future__ import annotations

from pathlib import Path

import streamlit as st

from app.components.navigation import configure_page, page_header
from app.i18n import tr

configure_page(tr("About the Author", "Sobre o Autor"), "🧑‍💻")
page_header(
    tr("About the Author", "Sobre o Autor"),
    tr(
        "The professional background and motivation behind Football Recruitment Intelligence.",
        "O percurso profissional e a motivação por detrás do Football Recruitment Intelligence.",
    ),
)

profile, project = st.columns([1, 1.8], gap="large")

with profile:
    st.markdown(
        """
        <style>
        [data-testid="stImage"] img {
            border: 1px solid #e1e8ef;
            border-radius: 14px;
            box-shadow: 0 4px 14px rgba(11,31,51,.08);
        }
        .fri-email-card {
            background: #ffffff;
            border: 1px solid #e1e8ef;
            border-radius: 10px;
            color: #52657a;
            font-size: .9rem;
            padding: .7rem .8rem;
            text-align: center;
        }
        .fri-email-card a {
            color: #0f806b;
            font-weight: 600;
            text-decoration: none;
            overflow-wrap: anywhere;
        }
        .fri-email-card a:hover { text-decoration: underline; }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.image(
        Path(__file__).resolve().parents[1] / "assets" / "tiago_marques.png",
        width="stretch",
    )
    st.markdown(
        f"""
        <div class="fri-card">
            <div class="fri-eyebrow">{tr("PROJECT AUTHOR", "AUTOR DO PROJETO")}</div>
            <h2 style="color:#0b1f33;margin:.35rem 0 .15rem;">Tiago Marques</h2>
            <p style="color:#52657a;margin:0 0 1rem;">
                Data Engineer · Business Intelligence
            </p>
            <p style="color:#26394d;margin:0;">
                SQL · ETL · Data Modelling · Power BI · Python · DuckDB
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.link_button(
        tr("View LinkedIn profile", "Ver perfil no LinkedIn"),
        "https://www.linkedin.com/in/tiagomarques-/",
        use_container_width=True,
        type="primary",
    )
    st.markdown(
        '<div class="fri-email-card">✉&nbsp; '
        '<a href="mailto:tiagoamarcolino@gmail.com">tiagoamarcolino@gmail.com</a>'
        "</div>",
        unsafe_allow_html=True,
    )

with project:
    st.markdown(tr("### Professional profile", "### Perfil profissional"))
    st.write(
        tr(
            "I am Tiago Marques, a Data Engineer and Business Intelligence professional with experience in SQL, ETL processes, data modelling, Power BI and the development of analytical solutions that support better decision-making.",
            "Sou o Tiago Marques, Data Engineer e profissional de Business Intelligence, com experiência em SQL, processos ETL, modelação de dados, Power BI e desenvolvimento de soluções analíticas de apoio à decisão.",
        )
    )
    st.write(
        tr(
            "I have a strong interest in football analytics, scouting and performance analysis, and I aim to combine my technical background with my passion for football.",
            "Tenho um forte interesse por football analytics, scouting e análise de desempenho, procurando aliar o meu percurso técnico à minha paixão pelo futebol.",
        )
    )

    st.markdown(tr("### About this project", "### Sobre este projeto"))
    st.write(
        tr(
            "Football Recruitment Intelligence was developed as a personal portfolio project to explore recruitment, player development, loans and transfer patterns, transforming data into useful information for scouting and sporting-management contexts.",
            "O Football Recruitment Intelligence foi desenvolvido como um projeto pessoal de portefólio para explorar padrões de recrutamento, desenvolvimento de jogadores, empréstimos e transferências, transformando dados em informação útil para contextos de scouting e direção desportiva.",
        )
    )
    st.write(
        tr(
            "The project brings together Python, SQL, DuckDB, data modelling, automation and data visualisation. It is designed as an evolving analytical product and as part of my continued learning in football data analytics.",
            "O projeto reúne competências de Python, SQL, DuckDB, modelação de dados, automatização e visualização. Foi concebido como um produto analítico em evolução e como parte do meu percurso contínuo de aprendizagem na área de dados aplicada ao futebol.",
        )
    )

st.divider()
st.caption(
    tr(
        "Built with a focus on transparent methodology, reproducibility and decision-ready analysis.",
        "Desenvolvido com foco na transparência metodológica, reprodutibilidade e análise orientada à decisão.",
    )
)
