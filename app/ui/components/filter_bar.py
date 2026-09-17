from typing import Callable, List, Optional
from nicegui import ui


def create_filter_bar(
    search_placeholder: str = "Search events...",
    filter_options: Optional[List[str]] = None,
    default_filter: str = "All",
    on_search_change: Optional[Callable[[str], None]] = None,
    on_filter_change: Optional[Callable[[str], None]] = None,
    on_export: Optional[Callable[[], None]] = None,
) -> ui.row:
    """Standard Search and Filter Controls Toolbar"""
    with ui.row().classes("w-full items-center justify-between gap-3 mb-4") as row:
        with ui.row().classes("items-center gap-3 flex-1"):
            # Search Input
            search_input = ui.input(
                placeholder=search_placeholder,
                on_change=lambda e: on_search_change(e.value) if on_search_change else None,
            ).classes("max-w-xs w-full bg-white").props("outlined dense clearable")
            with search_input.add_slot("prepend"):
                ui.icon("search").classes("text-[#9CA3AF]")

            # Category filter
            if filter_options:
                ui.select(
                    options=filter_options,
                    value=default_filter,
                    on_change=lambda e: on_filter_change(e.value) if on_filter_change else None,
                ).classes("w-40 bg-white").props("outlined dense")

        if on_export:
            ui.button("Export CSV", icon="download", on_click=on_export).classes(
                "sw-btn-secondary text-xs px-3 py-1.5"
            )

    return row


def create_empty_state(title: str = "No data available", message: str = "Data will appear here once telemetry begins.") -> ui.column:
    """Standard Minimalist Empty State"""
    with ui.column().classes("w-full items-center justify-center py-12 text-center") as col:
        ui.icon("inbox").classes("text-3xl text-[#D1D5DB] mb-2")
        ui.label(title).classes("text-sm font-semibold text-[#6B7280]")
        ui.label(message).classes("text-xs text-[#9CA3AF] max-w-sm mt-0.5")
    return col


def create_loading_skeleton() -> ui.element:
    """Minimal skeleton loader"""
    return ui.skeleton(height="120px").classes("w-full rounded-md")
