"""Plotly defaults and chart builders."""
from __future__ import annotations

import plotly.express as px
import plotly.graph_objects as go

COLORS = ["#10a37f", "#1677ff", "#ffb020", "#e64980", "#6750a4", "#5b7083"]


def style(figure: go.Figure, height: int = 380) -> go.Figure:
    """Apply the shared visual language."""
    text_color = "#26394d"
    figure.update_layout(
        height=height,
        margin=dict(l=10, r=10, t=50, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        colorway=COLORS,
        legend_title_text="",
        font=dict(color=text_color),
        title_font=dict(color="#132238"),
        legend=dict(font=dict(color=text_color), title_font=dict(color=text_color)),
        coloraxis_colorbar=dict(
            tickfont=dict(color=text_color),
            title_font=dict(color=text_color),
        ),
    )
    figure.update_xaxes(
        color=text_color,
        tickfont=dict(color=text_color),
        title_font=dict(color=text_color),
        gridcolor="#d9e1ea",
        linecolor="#8391a2",
    )
    figure.update_yaxes(
        color=text_color,
        tickfont=dict(color=text_color),
        title_font=dict(color=text_color),
        gridcolor="#d9e1ea",
        linecolor="#8391a2",
    )
    figure.update_annotations(font=dict(color=text_color))
    return figure


def bar(frame, x: str, y: str, title: str, horizontal: bool = False):
    """Create a consistently styled bar chart."""
    figure = px.bar(frame, x=x, y=y, title=title, orientation="h" if horizontal else "v")
    return style(figure)
