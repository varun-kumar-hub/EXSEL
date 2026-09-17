from typing import List, Dict, Any, Callable, Optional
from nicegui import ui
import plotly.graph_objects as go


def create_plotly_figure(
    points: List[Dict[str, Any]],
    y_label: str = "Water Level (%)",
    line_color: str = "#2563EB",
    min_threshold: Optional[float] = 30.0,
    max_threshold: Optional[float] = 80.0,
    y_range: Optional[List[float]] = None,
) -> go.Figure:
    """Create a clean, minimalist Plotly telemetry line chart matching PRD"""
    x_vals = [p.get("timestamp", "") for p in points]
    y_vals = [p.get("value", 0.0) for p in points]

    fig = go.Figure()

    # Telemetry line with subtle fill
    fig.add_trace(
        go.Scatter(
            x=x_vals,
            y=y_vals,
            mode="lines",
            name=y_label,
            line=dict(color=line_color, width=2.5, shape="spline"),
            fill="tozeroy",
            fillcolor="rgba(37, 99, 235, 0.06)",
            hovertemplate="<b>%{x}</b><br>Value: %{y:.1f}<extra></extra>",
        )
    )

    # Dashed threshold reference lines
    if min_threshold is not None:
        fig.add_hline(
            y=min_threshold,
            line_dash="dash",
            line_color="#F59E0B",
            line_width=1.5,
            annotation_text=f"Min ({min_threshold})",
            annotation_position="bottom right",
            annotation_font=dict(size=10, color="#D97706"),
        )

    if max_threshold is not None:
        fig.add_hline(
            y=max_threshold,
            line_dash="dash",
            line_color="#DC2626",
            line_width=1.5,
            annotation_text=f"Max ({max_threshold})",
            annotation_position="top right",
            annotation_font=dict(size=10, color="#DC2626"),
        )

    # Layout styling: Minimal, clean, no flashy gradients, responsive
    fig.update_layout(
        margin=dict(l=36, r=20, t=20, b=30),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font=dict(family="Inter, sans-serif", size=11, color="#6B7280"),
        xaxis=dict(
            showgrid=True,
            gridcolor="#F3F4F6",
            zeroline=False,
            showline=True,
            linecolor="#E5E7EB",
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#F3F4F6",
            zeroline=False,
            showline=True,
            linecolor="#E5E7EB",
            range=y_range,
        ),
        showlegend=False,
        hovermode="x unified",
        height=260,
    )
    return fig


def create_chart_card(
    title: str,
    points: List[Dict[str, Any]],
    y_label: str = "Value",
    line_color: str = "#2563EB",
    min_threshold: Optional[float] = None,
    max_threshold: Optional[float] = None,
    on_range_change: Optional[Callable[[str], None]] = None,
    active_range: str = "24H",
) -> ui.card:
    """
    Standard Chart Card with Time Filter Buttons (1H | 6H | 24H | 7D)
    """
    with ui.card().classes("sw-card p-5 w-full") as card:
        # Header + Range Switchers
        with ui.row().classes("w-full items-center justify-between mb-3"):
            ui.label(title).classes("text-sm font-semibold text-[#111827]")

            with ui.row().classes("items-center gap-1 bg-[#F3F4F6] p-0.5 rounded-md"):
                for r in ["1H", "6H", "24H", "7D"]:
                    is_active = (r == active_range)
                    btn_cls = "bg-white text-[#2563EB] shadow-xs font-semibold" if is_active else "text-[#6B7280] hover:text-[#111827]"

                    def make_handler(rg=r):
                        async def handler():
                            if on_range_change:
                                await on_range_change(rg)
                        return handler

                    ui.button(r, on_click=make_handler()).classes(
                        f"px-2.5 py-0.5 text-xs rounded {btn_cls} transition-all"
                    ).props("flat dense")

        fig = create_plotly_figure(
            points=points,
            y_label=y_label,
            line_color=line_color,
            min_threshold=min_threshold,
            max_threshold=max_threshold,
        )
        plot = ui.plotly(fig).classes("w-full")
        card.plot = plot

    return card
