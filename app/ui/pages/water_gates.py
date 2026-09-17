from nicegui import ui, app
from app.ui.layout import app_layout
from app.ui.components.gate_card import create_gate_card
from app.ui.components.toast import show_toast
from app.services.gate_service import gate_service
from app.auth.permissions import permissions


def register_water_gates_page():
    @ui.page("/water-gates")
    async def water_gates_page():
        user = app.storage.user.get("user") or {"full_name": "Chief Operator", "role": "operator"}
        user_role = user.get("role", "operator")

        with app_layout(page_title="Water Gates Control", subtitle="Sluice & Diverter Actuator Management", current_path="/water-gates"):
            with ui.row().classes("w-full items-center justify-between mb-4"):
                with ui.column().classes("gap-0"):
                    ui.label("Gate Actuation & Safety Interlocks").classes("text-base font-bold text-[#111827]")
                    ui.label("Direct command interface for physical spillway, intake, and diversion motors.").classes("text-xs text-[#6B7280]")

                # Role indicator pill
                with ui.row().classes("items-center gap-2 bg-white border border-[#E5E7EB] px-3 py-1.5 rounded-md text-xs"):
                    ui.label("Current Authority:").classes("text-[#6B7280]")
                    ui.label(user_role.upper()).classes("font-bold text-[#2563EB]")

            gates_grid = ui.element("div").classes("w-full grid grid-cols-1 md:grid-cols-2 gap-6 mb-6")

            async def handle_open(gate_id: str):
                try:
                    await gate_service.execute_operation(
                        gate_id=gate_id,
                        operation="OPEN",
                        user_role=user_role,
                        operator_name=user.get("full_name", "Operator"),
                    )
                    show_toast(f"Gate {gate_id} opening sequence dispatched.", "success")
                    await refresh_gates()
                except Exception as e:
                    show_toast(str(e), "negative")

            async def handle_close(gate_id: str):
                try:
                    await gate_service.execute_operation(
                        gate_id=gate_id,
                        operation="CLOSE",
                        user_role=user_role,
                        operator_name=user.get("full_name", "Operator"),
                    )
                    show_toast(f"Gate {gate_id} closing sequence dispatched.", "success")
                    await refresh_gates()
                except Exception as e:
                    show_toast(str(e), "negative")

            async def handle_mode(gate_id: str, new_mode: str):
                try:
                    await gate_service.set_mode(
                        gate_id=gate_id,
                        mode=new_mode,
                        user_role=user_role,
                        operator_name=user.get("full_name", "Operator"),
                    )
                    show_toast(f"Gate {gate_id} mode switched to {new_mode}.", "info")
                    await refresh_gates()
                except Exception as e:
                    show_toast(str(e), "negative")

            async def refresh_gates():
                gates = await gate_service.get_all_gates()
                gates_grid.clear()
                with gates_grid:
                    for g in gates:
                        create_gate_card(
                            gate_id=g.id,
                            name=g.name,
                            location=g.location,
                            status=g.status,
                            mode=g.mode,
                            is_connected=g.is_connected,
                            last_changed_at=g.last_changed_at,
                            on_open=handle_open,
                            on_close=handle_close,
                            on_toggle_mode=handle_mode,
                            can_control=permissions.can_control_gate(user_role),
                        )

            await refresh_gates()
            ui.timer(4.0, refresh_gates)
