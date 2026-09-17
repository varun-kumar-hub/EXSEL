from typing import Callable, Optional
from datetime import datetime
from nicegui import ui
from app.ui.theme.colors import ALERT_STYLES
from app.utils.datetime_utils import format_relative_time


def create_alert_card(
    alert_id: str,
    title: str,
    message: str,
    severity: str,
    created_at: datetime,
    on_dismiss: Optional[Callable[[str], None]] = None,
    can_dismiss: bool = True,
) -> ui.element:
    """
    Standard Alert Notification Card
    Color-coded left border and background per PRD specs.
    """
    style_spec = ALERT_STYLES.get(severity.lower(), ALERT_STYLES["info"])
    bg_hex = style_spec["bg"]
    border_hex = style_spec["border"]
    icon_name = style_spec["icon"]

    with ui.element("div").classes(
        "w-full rounded-md p-3.5 mb-2.5 flex items-start justify-between border-l-4 transition-all"
    ).style(f"background-color: {bg_hex}; border-left-color: {border_hex}; border-top: 1px solid #E5E7EB; border-right: 1px solid #E5E7EB; border-bottom: 1px solid #E5E7EB;") as container:
        with ui.row().classes("items-start gap-3 flex-1"):
            ui.icon(icon_name).classes("text-lg mt-0.5").style(f"color: {border_hex};")
            with ui.column().classes("gap-0.5 flex-1"):
                ui.label(title).classes("text-sm font-bold text-[#111827]")
                ui.label(message).classes("text-xs text-[#4B5563] leading-normal")
                ui.label(format_relative_time(created_at)).classes("text-xs text-[#9CA3AF] mt-1")

        if on_dismiss and can_dismiss:
            ui.button(
                icon="close",
                on_click=lambda: on_dismiss(alert_id),
            ).classes("text-[#9CA3AF] hover:text-[#111827] -mr-1 -mt-1").props("flat round dense size=sm")

    return container
