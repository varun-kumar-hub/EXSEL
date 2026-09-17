from typing import Callable, Optional
from datetime import datetime
from nicegui import ui
from app.ui.components.status_badge import create_status_badge
from app.ui.components.confirmation_dialog import show_confirmation_dialog
from app.utils.datetime_utils import format_short_time


def create_gate_card(
    gate_id: str,
    name: str,
    location: str,
    status: str,
    mode: str,
    is_connected: bool,
    last_changed_at: datetime,
    on_open: Optional[Callable[[str], None]] = None,
    on_close: Optional[Callable[[str], None]] = None,
    on_toggle_mode: Optional[Callable[[str, str], None]] = None,
    can_control: bool = True,
) -> ui.card:
    """
    Dedicated Water Gate Control Card
    Includes status badges, mode toggle, connection indicator, and safety confirmation modals.
    """
    with ui.card().classes("sw-card p-5 w-full flex flex-col justify-between") as card:
        # Header: Name + Status Badge
        with ui.row().classes("w-full items-center justify-between"):
            with ui.column().classes("gap-0"):
                ui.label(name).classes("text-base font-bold text-[#111827]")
                ui.label(location).classes("text-xs text-[#6B7280]")

            create_status_badge(status)

        ui.separator().classes("my-3")

        # Metadata Row: Mode, Connection, Last Changed
        with ui.row().classes("w-full justify-between items-center text-xs text-[#6B7280] my-1"):
            with ui.row().classes("items-center gap-2"):
                create_status_badge(mode, size="sm")
                conn_badge = "CONNECTED" if is_connected else "OFFLINE"
                create_status_badge(conn_badge, size="sm")

            ui.label(f"Last changed: {format_short_time(last_changed_at)}").classes("text-[#9CA3AF]")

        # Action Buttons Row
        with ui.row().classes("w-full gap-2 mt-4"):
            def prompt_open():
                show_confirmation_dialog(
                    title=f"Open {name}?",
                    message=f"Are you sure you want to actuate {name} ({location}) to OPEN state? Water flow will immediately commence.",
                    on_confirm=lambda: on_open(gate_id) if on_open else None,
                    confirm_label="Open Gate",
                    is_danger=False,
                )

            def prompt_close():
                show_confirmation_dialog(
                    title=f"Close {name}?",
                    message=f"Are you sure you want to close {name} ({location})? Water conduit flow through this sector will cease.",
                    on_confirm=lambda: on_close(gate_id) if on_close else None,
                    confirm_label="Close Gate",
                    is_danger=True,
                )

            is_open = (status == "OPEN")
            is_closed = (status == "CLOSED")
            is_in_transit = status in ("OPENING", "CLOSING")

            open_btn = ui.button(
                "OPEN",
                on_click=prompt_open,
            ).classes(
                "flex-1 sw-btn-primary py-1.5 text-xs font-semibold"
            )
            if is_open or is_in_transit or not can_control:
                open_btn.props("disable")

            close_btn = ui.button(
                "CLOSE",
                on_click=prompt_close,
            ).classes(
                "flex-1 sw-btn-danger py-1.5 text-xs font-semibold"
            )
            if is_closed or is_in_transit or not can_control:
                close_btn.props("disable")

            if on_toggle_mode and can_control:
                next_mode = "MANUAL" if mode == "AUTO" else "AUTO"
                ui.button(
                    f"Set {next_mode}",
                    on_click=lambda: on_toggle_mode(gate_id, next_mode),
                ).classes("sw-btn-secondary px-3 py-1.5 text-xs")

    return card
