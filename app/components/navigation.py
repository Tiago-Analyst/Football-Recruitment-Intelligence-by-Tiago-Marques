"""Brand and page-shell helpers."""
from __future__ import annotations

import streamlit as st

from app.i18n import tr


def configure_page(title: str, icon: str = "⚽") -> None:
    """Configure a consistent professional page shell."""
    st.set_page_config(page_title=f"{title} | FRI", page_icon=icon, layout="wide")
    st.markdown(
        """
        <style>
        .stApp {background: #f6f8fb; color: #132238;}
        [data-testid="stSidebar"] {background: #0b1f33; color: #ecf2f8;}
        [data-testid="stSidebar"] [data-testid="stWidgetLabel"] *,
        [data-testid="stSidebar"] [data-testid="stSidebarNav"] span,
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
            color: #ecf2f8 !important;
        }
        [data-testid="stSidebar"] [data-baseweb="select"] > div,
        [data-testid="stSidebar"] [data-baseweb="input"] > div,
        [data-testid="stSidebar"] [data-baseweb="base-input"] {
            background: #ffffff !important;
            border-color: #cbd5e1 !important;
        }
        [data-testid="stSidebar"] [data-baseweb="select"] span,
        [data-testid="stSidebar"] [data-baseweb="select"] div,
        [data-testid="stSidebar"] input,
        [data-testid="stSidebar"] textarea {
            color: #132238 !important;
            -webkit-text-fill-color: #132238 !important;
            opacity: 1 !important;
        }
        [data-testid="stSidebar"] input::placeholder,
        [data-testid="stSidebar"] textarea::placeholder {
            color: #64748b !important;
            -webkit-text-fill-color: #64748b !important;
            opacity: 1 !important;
        }
        [data-testid="stSidebar"] [data-baseweb="select"] svg,
        [data-testid="stSidebar"] [data-baseweb="input"] svg {
            fill: #334155 !important;
            color: #334155 !important;
        }
        [role="listbox"],
        [data-baseweb="popover"] [role="listbox"],
        [data-baseweb="menu"] {
            background: #ffffff !important;
            max-height: min(240px, calc(100vh - 32px)) !important;
            overflow-y: auto !important;
            overscroll-behavior: contain;
            scrollbar-gutter: stable;
            padding-bottom: 8px !important;
        }
        [role="listbox"] [role="option"],
        [role="listbox"] [role="option"] *,
        [data-baseweb="popover"] [role="option"],
        [data-baseweb="popover"] [role="option"] *,
        [data-baseweb="menu"] li,
        [data-baseweb="menu"] li * {
            color: #132238 !important;
            -webkit-text-fill-color: #132238 !important;
        }
        [data-baseweb="popover"] [aria-selected="true"],
        [data-baseweb="menu"] li:hover {
            background: #e8f5f1 !important;
        }
        [role="listbox"]::-webkit-scrollbar,
        [data-baseweb="popover"] [role="listbox"]::-webkit-scrollbar,
        [data-baseweb="menu"]::-webkit-scrollbar {
            width: 9px;
        }
        [role="listbox"]::-webkit-scrollbar-thumb,
        [data-baseweb="popover"] [role="listbox"]::-webkit-scrollbar-thumb,
        [data-baseweb="menu"]::-webkit-scrollbar-thumb {
            background: #94a3b8;
            border: 2px solid #ffffff;
            border-radius: 999px;
        }
        .fri-eyebrow {color:#10a37f;font-size:.76rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;}
        .fri-title {font-size:2.15rem;font-weight:780;line-height:1.1;margin:.2rem 0 .4rem;color:#0b1f33;}
        .fri-subtitle {color:#52657a;max-width:850px;margin-bottom:1.35rem;}
        .fri-card {background:white;border:1px solid #e1e8ef;border-radius:12px;padding:1rem 1.1rem;box-shadow:0 2px 8px rgba(11,31,51,.04);}
        div[data-testid="stMetric"] {background:white;border:1px solid #e1e8ef;border-radius:12px;padding:1rem;}
        div[data-testid="stMetric"] [data-testid="stMetricLabel"] p,
        div[data-testid="stMetric"] [data-testid="stMetricValue"] {
            color: #132238 !important;
            opacity: 1 !important;
        }
        div[data-testid="stAlert"] *,
        div[data-baseweb="notification"] * {
            color: #26394d !important;
            opacity: 1 !important;
        }
        .fri-warning {
            background: #fff8cc;
            border: 1px solid #eadf84;
            border-radius: 10px;
            color: #4b4300 !important;
            font-weight: 600;
            padding: 1rem 1.1rem;
            margin: .5rem 0 1.5rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_header(title: str, subtitle: str) -> None:
    """Render the standard title treatment."""
    st.markdown(
        '<div class="fri-eyebrow">'
        + tr("Football Recruitment Intelligence", "Inteligência de Recrutamento no Futebol")
        + "</div>",
        unsafe_allow_html=True,
    )
    st.markdown(f'<div class="fri-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="fri-subtitle">{subtitle}</div>', unsafe_allow_html=True)


def source_caption() -> None:
    """Keep provenance visible on analytical pages."""
    st.caption(
        tr(
            "Source: transfermarkt-datasets (CC0) · Positive reported fees only · Last refresh shown in Methodology",
            "Fonte: transfermarkt-datasets (CC0) · Apenas valores positivos declarados · Última atualização apresentada na Metodologia",
        )
    )
