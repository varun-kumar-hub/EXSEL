from nicegui import ui, app
from app.ui.layout import app_layout
from app.ui.components.stat_card import create_stat_card
from app.ui.components.chart_card import create_chart_card, create_plotly_figure
from app.ui.components.gate_card import create_gate_card
from app.ui.components.alert_card import create_alert_card
from app.ui.components.toast import show_toast
from app.services.dashboard_service import dashboard_service
from app.services.gate_service import gate_service
from app.services.alert_service import alert_service
from app.auth.permissions import permissions


def register_dashboard_page():
    @ui.page("/")
    @ui.page("/dashboard")
    async def dashboard_page():
        user = app.storage.user.get("user") or {
            "full_name": "Chief Operator",
            "email": "operator@smartwater.io",
            "role": "operator",
        }
        user_role = user.get("role", "operator")

        # Initial state fetch
        overview = await dashboard_service.get_overview()
        active_range_wl = "24H"
        active_range_fl = "24H"
        wl_points = await dashboard_service.get_chart_data("water_level", active_range_wl)
        fl_points = await dashboard_service.get_chart_data("flow_rate", active_range_fl)

        with app_layout(page_title="Smart Water Distribution", subtitle="System Overview", current_path="/dashboard"):
            # 1. Four Summary Cards Grid (Responsive: 1-col mobile, 2-col tablet, 4-col desktop)
            stat_cards_container = ui.element("div").classes("w-full grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6")

            def render_stat_cards(cards_data):
                stat_cards_container.clear()
                with stat_cards_container:
                    wl = cards_data["water_level"]
                    create_stat_card(
                        title="Water Level",
                        value=f"{wl['value']}%",
                        status_label=wl["status_label"],
                        status_color=wl["status_color"],
                        subtext=wl["subtext"],
                        progress_pct=wl["progress_pct"],
                        icon="water_drop",
                    )

                    fl = cards_data["flow_rate"]
                    create_stat_card(
                        title="Flow Rate",
                        value=f"{fl['value']}",
                        unit=fl["unit"],
                        status_label=fl["status_label"],
                        subtext=fl["subtext"],
                        icon="speed",
                    )

                    wg = cards_data["water_gates"]
                    create_stat_card(
                        title="Water Gates",
                        value=wg["value"],
                        status_label=wg["status_label"],
                        status_color=wg["status_color"],
                        subtext=wg["subtext"],
                        icon="door_front",
                    )

                    pmp = cards_data["pump"]
                    create_stat_card(
                        title="Primary Pump",
                        value=pmp["value"],
                        status_label=pmp["status_label"],
                        status_color=pmp["status_color"],
                        subtext=pmp["subtext"],
                        icon="settings_power",
                    )

            render_stat_cards(overview["summary_cards"])

            # 2. Middle Row: Water Level & Flow Rate Charts (70% width) + Recent Alerts (30% width)
            with ui.row().classes("w-full grid grid-cols-1 lg:grid-cols-12 gap-6 mb-6 items-start"):
                # Left Column: Charts (8 cols on desktop)
                with ui.column().classes("lg:col-span-8 w-full gap-6"):
                    # Water Level Chart
                    async def change_wl_range(new_range: str):
                        nonlocal active_range_wl
                        active_range_wl = new_range
                        pts = await dashboard_service.get_chart_data("water_level", new_range)
                        wl_chart_card.plot.figure = create_plotly_figure(
                            points=pts,
                            y_label="Water Level (%)",
                            line_color="#2563EB",
                            min_threshold=30.0,
                            max_threshold=80.0,
                        )
                        wl_chart_card.plot.update()

                    wl_chart_card = create_chart_card(
                        title="Reservoir Water Level Trend",
                        points=wl_points,
                        y_label="Water Level (%)",
                        line_color="#2563EB",
                        min_threshold=30.0,
                        max_threshold=80.0,
                        on_range_change=change_wl_range,
                        active_range=active_range_wl,
                    )

                    # Flow Rate Chart
                    async def change_fl_range(new_range: str):
                        nonlocal active_range_fl
                        active_range_fl = new_range
                        pts = await dashboard_service.get_chart_data("flow_rate", new_range)
                        fl_chart_card.plot.figure = create_plotly_figure(
                            points=pts,
                            y_label="Flow Rate (L/min)",
                            line_color="#06B6D4",
                            min_threshold=5.0,
                            max_threshold=30.0,
                        )
                        fl_chart_card.plot.update()

                    fl_chart_card = create_chart_card(
                        title="Main Line Flow Rate Telemetry",
                        points=fl_points,
                        y_label="Flow Rate (L/min)",
                        line_color="#06B6D4",
                        min_threshold=5.0,
                        max_threshold=30.0,
                        on_range_change=change_fl_range,
                        active_range=active_range_fl,
                    )

                # Right Column: Live Alerts Panel (4 cols on desktop)
                with ui.column().classes("lg:col-span-4 w-full gap-4"):
                    with ui.card().classes("sw-card p-5 w-full"):
                        with ui.row().classes("w-full items-center justify-between mb-3"):
                            with ui.row().classes("items-center gap-2"):
                                ui.icon("warning").classes("text-[#F59E0B]")
                                ui.label("Active Alerts").classes("text-sm font-semibold text-[#111827]")

                            ui.link("View All", target="/history").classes("text-xs text-[#2563EB] hover:underline font-semibold")

                        alerts_container = ui.column().classes("w-full gap-2")

                        async def handle_dismiss(alert_id: str):
                            try:
                                await alert_service.dismiss_alert(alert_id, user_role, user.get("full_name"))
                                show_toast("Alert dismissed.", "info")
                                await refresh_data()
                            except Exception as e:
                                show_toast(str(e), "negative")

                        def render_alerts(alerts_list):
                            alerts_container.clear()
                            with alerts_container:
                                if not alerts_list:
                                    ui.label("No active alerts. System running nominally.").classes("text-xs text-[#6B7280] py-4 text-center w-full")
                                else:
                                    for a in alerts_list:
                                        create_alert_card(
                                            alert_id=a["id"],
                                            title=a["title"],
                                            message=a["message"],
                                            severity=a["severity"],
                                            created_at=a["created_at"],
                                            on_dismiss=handle_dismiss,
                                            can_dismiss=permissions.can_dismiss_alerts(user_role),
                                        )

                        render_alerts(overview["alerts"])

            # 3. Gate Status Cards Grid (2-column on desktop, stacked on mobile)
            with ui.row().classes("w-full items-center justify-between mt-2 mb-3"):
                with ui.row().classes("items-center gap-2"):
                    ui.icon("meeting_room").classes("text-[#2563EB]")
                    ui.label("Water Gates Control Room").classes("text-base font-bold text-[#111827]")

                ui.link("Full Control Room →", target="/water-gates").classes("text-xs text-[#2563EB] font-semibold hover:underline")

            gates_container = ui.element("div").classes("w-full grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6")

            async def handle_gate_action(gate_id: str, action: str):
                try:
                    await gate_service.execute_operation(
                        gate_id=gate_id,
                        operation=action,
                        user_role=user_role,
                        operator_name=user.get("full_name", "Operator"),
                    )
                    show_toast(f"Gate {gate_id} {action} operation dispatched.", "success")
                    await refresh_data()
                except Exception as e:
                    show_toast(str(e), "negative")

            async def handle_mode_toggle(gate_id: str, new_mode: str):
                try:
                    await gate_service.set_mode(
                        gate_id=gate_id,
                        mode=new_mode,
                        user_role=user_role,
                        operator_name=user.get("full_name", "Operator"),
                    )
                    show_toast(f"Gate {gate_id} set to {new_mode}.", "info")
                    await refresh_data()
                except Exception as e:
                    show_toast(str(e), "negative")

            def render_gates(gates_list):
                gates_container.clear()
                with gates_container:
                    for g in gates_list:
                        create_gate_card(
                            gate_id=g["id"],
                            name=g["name"],
                            location=g["location"],
                            status=g["status"],
                            mode=g["mode"],
                            is_connected=g["is_connected"],
                            last_changed_at=g["last_changed_at"],
                            on_open=lambda gid: handle_gate_action(gid, "OPEN"),
                            on_close=lambda gid: handle_gate_action(gid, "CLOSE"),
                            on_toggle_mode=handle_mode_toggle,
                            can_control=permissions.can_control_gate(user_role),
                        )

            render_gates(overview["gates"])

            # 4. System Statistics Footer Row (Full width bottom: 4 columns)
            stats = overview["system_stats"]
            with ui.card().classes("sw-card p-5 w-full"):
                ui.label("SYSTEM HEALTH & TELEMETRY AUDIT").classes("text-xs font-bold text-[#6B7280] uppercase tracking-wider mb-3")
                with ui.row().classes("w-full grid grid-cols-2 md:grid-cols-4 gap-4 text-center"):
                    with ui.column().classes("items-center"):
                        ui.label("Uptime").classes("text-xs text-[#6B7280]")
                        ui.label(stats["uptime"]).classes("text-xl font-bold text-[#10B981]")

                    with ui.column().classes("items-center"):
                        ui.label("Avg Water Level").classes("text-xs text-[#6B7280]")
                        ui.label(stats["avg_water"]).classes("text-xl font-bold text-[#2563EB]")

                    with ui.column().classes("items-center"):
                        ui.label("Total Operations").classes("text-xs text-[#6B7280]")
                        ui.label(str(stats["total_operations"])).classes("text-xl font-bold text-[#111827]")

                    with ui.column().classes("items-center"):
                        ui.label("Sensors Online").classes("text-xs text-[#6B7280]")
                        ui.label(stats["sensors_online"]).classes("text-xl font-bold text-[#10B981]")

            # Refresh helper
            async def refresh_data():
                new_ov = await dashboard_service.get_overview()
                render_stat_cards(new_ov["summary_cards"])
                render_alerts(new_ov["alerts"])
                render_gates(new_ov["gates"])

            # Seamless background telemetry refresh every 5 seconds (never reloads full page!)
            ui.timer(5.0, refresh_data)
