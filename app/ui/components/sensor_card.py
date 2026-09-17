from typing import Optional, Callable
from datetime import datetime
from nicegui import ui
from app.ui.components.status_badge import create_status_badge
from app.utils.datetime_utils import format_short_time


def create_sensor_card(
    sensor_id: str,
    name: str,
    sensor_type: str,
    unit: str,
    last_reading: Optional[float],
    minimum_threshold: float,
    maximum_threshold: float,
    status: str,
    last_updated_at: datetime,
    on_view_history: Optional[Callable[[str], None]] = None,
) -> ui.card:
    """
    Standard Sensor Telemetry Card
    Displays metric value, unit, threshold boundaries, online status, and time.
    """
    with ui.card().classes("sw-card p-5 w-full flex flex-col justify-between") as card:
        # Header: Name + Status
        with ui.row().classes("w-full items-center justify-between"):
            ui.label(name).classes("text-sm font-semibold text-[#111827]")
            create_status_badge(status, size="sm")

        # Telemetry Value
        with ui.row().classes("items-baseline gap-1 my-3"):
            val_str = f"{last_reading:.1f}" if last_reading is not None else "--"
            ui.label(val_str).classes("text-3xl font-bold text-[#111827] tracking-tight")
            ui.label(unit).classes("text-sm font-semibold text-[#6B7280]")

        # Thresholds Boundary info
        with ui.row().classes("w-full justify-between items-center text-xs text-[#6B7280] py-1 border-t border-[#F3F4F6]"):
            ui.label(f"Thresholds: {minimum_threshold:.1f} – {maximum_threshold:.1f} {unit}").classes("text-[#6B7280]")
            ui.label(format_short_time(last_updated_at)).classes("text-[#9CA3AF]")

        # Footer Action
        if on_view_history:
            with ui.row().classes("w-full justify-end mt-2"):
                ui.button(
                    "View History",
                    on_click=lambda: on_view_history(sensor_id),
                ).classes("text-xs text-[#2563EB] hover:underline font-medium p-0").props("flat dense")

    return card
