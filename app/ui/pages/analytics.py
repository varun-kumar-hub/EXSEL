from nicegui import ui
import plotly.graph_objects as go
from app.ui.layout import app_layout
from app.ui.components.stat_card import create_stat_card
from app.ui.components.chart_card import create_plotly_figure
from app.services.analytics_service import analytics_service


def register_analytics_page():
    @ui.page("/analytics")
    async def analytics_page():
        active_filter = "7D"

        with app_layout(page_title="Hydraulic Analytics", subtitle="Long-term Trends & Resource Optimization", current_path="/analytics"):
            # Header with Date Filter Toolbar
            with ui.row().classes("w-full items-center justify-between mb-6"):
                with ui.column().classes("gap-0"):
                    ui.label("Performance Analytics & Water Conservation").classes("text-base font-bold text-[#111827]")
                    ui.label("Statistical modeling computed via Pandas and NumPy aggregation engines.").classes("text-xs text-[#6B7280]")

                # Filter buttons
                filter_row = ui.row().classes("items-center gap-1 bg-white border border-[#E5E7EB] p-1 rounded-md")

            kpi_container = ui.element("div").classes("w-full grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6")
            charts_container = ui.element("div").classes("w-full grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6")

            async def load_analytics(date_filter: str):
                nonlocal active_filter
                active_filter = date_filter
                data = await analytics_service.get_analytics(date_filter)

                # Render Filter Row
                filter_row.clear()
                with filter_row:
                    for f in ["Today", "7D", "30D"]:
                        is_active = (f == active_filter)
                        btn_cls = "sw-btn-primary" if is_active else "sw-btn-secondary"
                        ui.button(f, on_click=lambda filter_name=f: load_analytics(filter_name)).classes(
                            f"px-3 py-1 text-xs font-semibold {btn_cls}"
                        )

                # Render KPIs
                kpi_container.clear()
                with kpi_container:
                    s = data["summary"]
                    create_stat_card(
                        title="Average Water Level",
                        value=f"{s['avg_water_level']}%",
                        status_label="Nominal",
                        subtext="Mean reservoir capacity",
                        icon="water",
                    )
                    create_stat_card(
                        title="Peak Flow Rate",
                        value=f"{s['max_flow_rate']}",
                        unit="L/min",
                        status_label="Peak Load",
                        subtext=f"Min flow: {s['min_flow_rate']} L/min",
                        icon="speed",
                    )
                    create_stat_card(
                        title="Total Gate Actions",
                        value=str(s["total_gate_operations"]),
                        status_label="Operations",
                        subtext="Dispatched in period",
                        icon="door_front",
                    )
                    create_stat_card(
                        title="Estimated Water Loss",
                        value=f"{s['estimated_water_loss_liters']}",
                        unit="L",
                        status_label="Conservation",
                        subtext="Efficiency rate: 98.4%",
                        icon="opacity",
                    )

                # Render Trend Charts
                charts_container.clear()
                with charts_container:
                    # Water Level Trend
                    with ui.card().classes("sw-card p-5 w-full"):
                        ui.label("Water Level Fluctuations").classes("text-sm font-semibold text-[#111827] mb-3")
                        fig_wl = create_plotly_figure(
                            data["water_level_trend"],
                            y_label="Water Level (%)",
                            line_color="#2563EB",
                            min_threshold=30.0,
                            max_threshold=80.0,
                        )
                        ui.plotly(fig_wl).classes("w-full")

                    # Daily Gate Operations Bar Chart
                    with ui.card().classes("sw-card p-5 w-full"):
                        ui.label("Daily Gate Operations Activity").classes("text-sm font-semibold text-[#111827] mb-3")
                        ops = data["gate_operations_daily"]
                        fig_ops = go.Figure(
                            data=[
                                go.Bar(
                                    x=[o["date"] for o in ops],
                                    y=[o["count"] for o in ops],
                                    marker_color="#2563EB",
                                    hovertemplate="<b>%{x}</b><br>Operations: %{y}<extra></extra>",
                                )
                            ]
                        )
                        fig_ops.update_layout(
                            margin=dict(l=30, r=20, t=20, b=30),
                            plot_bgcolor="#FFFFFF",
                            paper_bgcolor="#FFFFFF",
                            font=dict(family="Inter, sans-serif", size=11, color="#6B7280"),
                            xaxis=dict(gridcolor="#F3F4F6", showline=True, linecolor="#E5E7EB"),
                            yaxis=dict(gridcolor="#F3F4F6", showline=True, linecolor="#E5E7EB"),
                            height=260,
                        )
                        ui.plotly(fig_ops).classes("w-full")

            await load_analytics(active_filter)
