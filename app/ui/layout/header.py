from datetime import datetime
from nicegui import ui, app
from app.utils.datetime_utils import format_timestamp


def create_header(page_title: str, subtitle: str = "System Overview", sidebar_drawer: ui.left_drawer = None) -> ui.header:
    """
    Standard Top Header (64px height)
    """
    with ui.header().classes("bg-white text-[#111827] border-b border-[#E5E7EB] h-16 px-3 sm:px-6 flex items-center justify-between z-20 shadow-none"):
        # Left Section: Hamburger + Title
        with ui.row().classes("items-center gap-2 sm:gap-3 min-w-0"):
            if sidebar_drawer:
                ui.button(
                    icon="menu",
                    on_click=sidebar_drawer.toggle,
                ).classes("lg:hidden text-[#4B5563]").props("flat round dense")

            with ui.column().classes("gap-0 min-w-0"):
                ui.label(page_title).classes("text-base sm:text-lg font-bold text-[#111827] leading-tight truncate max-w-[170px] sm:max-w-[280px] md:max-w-none")
                ui.label(subtitle).classes("hidden sm:block text-xs text-[#6B7280] truncate max-w-[280px] md:max-w-none")

        # Right Section: Status Indicator + Clock + Notifications + Profile
        with ui.row().classes("items-center gap-2 sm:gap-4 shrink-0"):
            # Realtime Status indicator
            with ui.row().classes("items-center gap-1.5 bg-[#F0FDF4] border border-[#BBF7D0] px-2 sm:px-3 py-1 rounded-full text-xs font-medium text-[#15803D]"):
                ui.element("span").classes("w-2 h-2 rounded-full bg-[#10B981] status-pulse")
                ui.label("Online").classes("font-semibold sm:hidden")
                ui.label("System Online").classes("hidden sm:inline font-semibold")

            # Realtime clock label
            clock_label = ui.label(f"Last updated: {datetime.utcnow().strftime('%I:%M:%S %p')}").classes(
                "hidden md:block text-xs text-[#9CA3AF]"
            )

            # Auto-update clock every 1 second
            ui.timer(1.0, lambda: clock_label.set_text(f"Last updated: {datetime.utcnow().strftime('%I:%M:%S %p')}"))

            # Notification Bell with Badge
            with ui.button(icon="notifications").classes("text-[#4B5563]").props("flat round dense"):
                ui.badge("3", color="red").props("floating")
                with ui.menu().classes("w-72 p-2"):
                    ui.label("System Notifications").classes("text-xs font-bold text-[#111827] px-2 py-1")
                    ui.separator().classes("my-1")
                    ui.item("Reservoir level critical").classes("text-xs text-[#DC2626]")
                    ui.item("Gate 03 offline alert").classes("text-xs text-[#D97706]")
                    ui.item("Sector B sequence complete").classes("text-xs text-[#2563EB]")
                    ui.separator().classes("my-1")
                    ui.button("View All in History", on_click=lambda: ui.navigate.to("/history")).classes(
                        "w-full text-xs sw-btn-secondary py-1"
                    )

            # User Profile Quick Menu
            user = app.storage.user.get("user", {"full_name": "Chief Operator", "role": "operator"})
            with ui.row().classes("items-center gap-2 cursor-pointer"):
                initials = "".join([part[0] for part in user.get("full_name", "OP").split()[:2]]).upper()
                ui.label(initials).classes(
                    "w-8 h-8 rounded-full bg-[#EBF8FF] text-[#2563EB] font-bold text-xs flex items-center justify-center border border-[#BFDBFE]"
                )
                with ui.menu():
                    ui.item(f"Signed in as {user.get('full_name')}").classes("text-xs font-semibold text-[#111827]")
                    ui.separator()
                    ui.item("System Settings", on_click=lambda: ui.navigate.to("/settings")).classes("text-xs")
                    ui.item("Sign Out", on_click=lambda: ui.navigate.to("/login")).classes("text-xs text-[#DC2626]")
