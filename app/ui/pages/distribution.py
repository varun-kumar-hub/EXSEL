from nicegui import ui, app
from app.ui.layout import app_layout
from app.ui.components.status_badge import create_status_badge
from app.ui.components.toast import show_toast
from app.services.distribution_service import distribution_service
from app.auth.permissions import permissions


def register_distribution_page():
    @ui.page("/distribution")
    async def distribution_page():
        user = app.storage.user.get("user") or {"full_name": "Chief Operator", "role": "operator"}
        user_role = user.get("role", "operator")

        with app_layout(page_title="Sequential Water Distribution", subtitle="Automated Sector Routing Pipeline", current_path="/distribution"):
            # Header Controls
            with ui.card().classes("sw-card p-6 w-full mb-6"):
                with ui.row().classes("w-full items-center justify-between"):
                    with ui.column().classes("gap-1"):
                        ui.label("Intake-to-Sector Automated Sequence").classes("text-lg font-bold text-[#111827]")
                        ui.label("Coordinates sequential pump priming, gate routing, and pipeline pressurization.").classes("text-xs text-[#6B7280]")

                    # Action buttons
                    with ui.row().classes("items-center gap-3"):
                        async def handle_start():
                            try:
                                await distribution_service.start_sequence(user_role, user.get("full_name"))
                                show_toast("Sequential water distribution started.", "success")
                                await refresh_sequence()
                            except Exception as e:
                                show_toast(str(e), "negative")

                        async def handle_stop():
                            try:
                                await distribution_service.stop_sequence(user_role, user.get("full_name"))
                                show_toast("Distribution sequence stopped.", "warning")
                                await refresh_sequence()
                            except Exception as e:
                                show_toast(str(e), "negative")

                        can_exec = permissions.can_execute_distribution(user_role)
                        start_btn = ui.button("START SEQUENCE", icon="play_arrow", on_click=handle_start).classes(
                            "sw-btn-primary px-5 py-2 text-xs font-bold"
                        )
                        stop_btn = ui.button("EMERGENCY STOP", icon="stop", on_click=handle_stop).classes(
                            "sw-btn-danger px-5 py-2 text-xs font-bold"
                        )
                        if not can_exec:
                            start_btn.props("disable")
                            stop_btn.props("disable")

            # Sequence Flow Diagram Card
            flow_container = ui.card().classes("sw-card p-6 w-full mb-6")

            async def refresh_sequence():
                seq = await distribution_service.get_status()
                flow_container.clear()

                with flow_container:
                    with ui.row().classes("w-full items-center justify-between mb-4 border-b border-[#E5E7EB] pb-3"):
                        with ui.row().classes("items-center gap-2"):
                            ui.label("Pipeline Status:").classes("text-xs font-bold text-[#6B7280]")
                            create_status_badge(seq.status)

                        ui.label(f"Active Step: {min(len(seq.steps), seq.current_step_index + 1)} of {len(seq.steps)}").classes("text-xs text-[#9CA3AF]")

                    # Step Cards Progression Pipeline (Horizontal on desktop, vertical on mobile)
                    with ui.element("div").classes("w-full grid grid-cols-1 md:grid-cols-5 gap-3 my-4"):
                        for idx, step in enumerate(seq.steps):
                            # Border and background styling based on status
                            if step.status == "ACTIVE":
                                box_style = "border-[#2563EB] bg-[#EFF6FF] ring-2 ring-[#93C5FD]"
                                icon_color = "text-[#2563EB]"
                            elif step.status == "COMPLETED":
                                box_style = "border-[#10B981] bg-[#F0FDF4]"
                                icon_color = "text-[#10B981]"
                            elif step.status == "FAILED":
                                box_style = "border-[#DC2626] bg-[#FEF2F2]"
                                icon_color = "text-[#DC2626]"
                            else:
                                box_style = "border-[#E5E7EB] bg-white"
                                icon_color = "text-[#9CA3AF]"

                            with ui.element("div").classes(
                                f"border rounded-lg p-4 flex flex-col justify-between {box_style} transition-all shadow-xs min-h-[140px]"
                            ):
                                with ui.row().classes("items-center justify-between w-full mb-1"):
                                    ui.label(f"0{step.step_order}").classes("text-xs font-bold text-[#9CA3AF]")
                                    create_status_badge(step.status, size="sm")

                                with ui.column().classes("gap-0.5 my-2"):
                                    ui.label(step.step_name).classes("text-xs font-bold text-[#111827]")
                                    if step.gate_target:
                                        ui.label(f"Actuates: {step.gate_target}").classes("text-[11px] text-[#2563EB] font-medium")
                                    if step.target_flow:
                                        ui.label(f"Target: {step.target_flow} L/min").classes("text-[10px] text-[#6B7280]")

                                ui.label(step.notes or "").classes("text-[10px] text-[#6B7280] line-clamp-2 mt-1")

                    # Architectural Flow Schematic (ASCII / Visual Diagram)
                    with ui.expansion("View Pipeline Schematic Diagram", icon="schema").classes(
                        "w-full text-xs text-[#6B7280] bg-[#F9FAFB] rounded-md border border-[#E5E7EB] mt-4"
                    ):
                        with ui.element("pre").classes("p-4 text-xs font-mono text-[#1E293B] leading-relaxed bg-[#F1F5F9] rounded overflow-x-auto"):
                            ui.label("""
+--------------------+
|  Intake Reservoir  |  (Level Sensor SENS_LVL_01)
+---------+----------+
          |
          v
+--------------------+
|   Treatment Unit   |  (Gate 01 Feed Control)
+---------+----------+
          |
          v
+--------------------+
|    Primary Pump    |  (High Pressure Booster P1)
+---------+----------+
          |
          v
+--------------------+
| Distribution Main  |  (Main Flow SENS_FLW_01)
+---------+----------+
          |
    +-----+-----+
    |     |     |
    v     v     v
  [ A ] [ B ] [ C ]    (Sectors Controlled by Gate 02, Gate 03, Gate 04)
                            """)

            await refresh_sequence()
            ui.timer(2.0, refresh_sequence)
