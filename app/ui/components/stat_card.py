from typing import Optional
from nicegui import ui
from app.ui.components.status_badge import create_status_badge


def create_stat_card(
    title: str,
    value: str,
    unit: str = "",
    status_label: Optional[str] = None,
    status_color: Optional[str] = "success",
    subtext: str = "Updated recently",
    progress_pct: Optional[float] = None,
    icon: Optional[str] = None,
) -> ui.card:
    """
    Standard Metric / KPI Card
    Spec: 20px padding, 1px border #E5E7EB, 8px radius, subtle shadow, clean solid colors.
    """
    with ui.card().classes("sw-card p-5 w-full flex flex-col justify-between min-h-[140px]") as card:
        # Header: Title + Status Badge / Icon
        with ui.row().classes("w-full items-center justify-between"):
            with ui.row().classes("items-center gap-2"):
                if icon:
                    ui.icon(icon).classes("text-sm text-[#2563EB]")
                ui.label(title).classes("text-xs font-semibold text-[#6B7280] uppercase tracking-wider")

            if status_label:
                create_status_badge(status_label, size="sm")

        # Metric Value
        with ui.row().classes("items-baseline gap-1 my-2"):
            ui.label(value).classes("text-3xl font-bold text-[#111827] tracking-tight")
            if unit:
                ui.label(unit).classes("text-sm font-semibold text-[#6B7280]")

        # Optional Progress Bar (e.g. for Water Level)
        if progress_pct is not None:
            pct_val = min(100.0, max(0.0, progress_pct))
            bar_color = "#10B981" if pct_val < 80 else "#DC2626"
            with ui.element("div").classes("w-full bg-[#E5E7EB] h-1.5 rounded-full overflow-hidden my-1"):
                ui.element("div").classes("h-full rounded-full transition-all duration-500").style(
                    f"width: {pct_val}%; background-color: {bar_color};"
                )

        # Footer Subtext
        ui.label(subtext).classes("text-xs text-[#9CA3AF]")

    return card
