from typing import Optional, Callable
from nicegui import ui, app
from app.ui.layout.navigation import NAV_ITEMS, SECONDARY_NAV
from app.ui.components.status_badge import create_status_badge


def create_sidebar(current_path: str = "/dashboard", user: Optional[dict] = None) -> ui.left_drawer:
    """
    Standard Desktop Fixed Sidebar (256px width)
    """
    with ui.left_drawer(value=None).classes(
        "bg-white border-r border-[#E5E7EB] p-0 flex flex-col justify-between select-none"
    ).props("show-if-above width=256 breakpoint=1024") as drawer:
        # Top Section: Brand & Nav
        with ui.column().classes("w-full gap-0"):
            # Brand Header (48px height, 16px padding)
            with ui.row().classes("w-full h-16 px-5 items-center justify-between border-b border-[#E5E7EB]"):
                with ui.row().classes("items-center gap-2.5"):
                    with ui.element("div").classes("w-8 h-8 rounded-lg bg-[#2563EB] flex items-center justify-center text-white"):
                        ui.icon("water_drop").classes("text-lg")
                    with ui.column().classes("gap-0"):
                        ui.label("SMART WATER").classes("text-sm font-bold tracking-wider text-[#111827]")
                        ui.label("DISTRIBUTION SYSTEM").classes("text-[10px] font-semibold text-[#6B7280] tracking-widest")

            # Main Navigation Links
            with ui.column().classes("w-full py-3 px-2 gap-1"):
                ui.label("OPERATIONS").classes("text-[10px] font-bold text-[#9CA3AF] px-3 py-1 tracking-wider uppercase")
                for item in NAV_ITEMS:
                    is_active = (current_path == item["path"])
                    active_cls = "sw-nav-active" if is_active else "sw-nav-item"

                    with ui.link(target=item["path"]).classes(
                        f"w-full flex items-center gap-3 px-3 py-2.5 rounded-md text-sm font-medium no-underline {active_cls}"
                    ):
                        icon_color = "text-[#2563EB]" if is_active else "text-[#6B7280]"
                        ui.icon(item["icon"]).classes(f"text-lg {icon_color}")
                        ui.label(item["label"]).classes("flex-1")

            ui.separator().classes("my-2")

            # Secondary Navigation (Settings)
            with ui.column().classes("w-full px-2 gap-1"):
                ui.label("PREFERENCES").classes("text-[10px] font-bold text-[#9CA3AF] px-3 py-1 tracking-wider uppercase")
                for item in SECONDARY_NAV:
                    is_active = (current_path == item["path"])
                    active_cls = "sw-nav-active" if is_active else "sw-nav-item"
                    with ui.link(target=item["path"]).classes(
                        f"w-full flex items-center gap-3 px-3 py-2.5 rounded-md text-sm font-medium no-underline {active_cls}"
                    ):
                        icon_color = "text-[#2563EB]" if is_active else "text-[#6B7280]"
                        ui.icon(item["icon"]).classes(f"text-lg {icon_color}")
                        ui.label(item["label"]).classes("flex-1")

        # Bottom Section: User Role Preview & Logout
        with ui.column().classes("w-full p-4 border-t border-[#E5E7EB] bg-[#FAFAFA] gap-3"):
            user_data = user or app.storage.user.get("user") or {
                "full_name": "Chief Operator",
                "email": "operator@smartwater.io",
                "role": "operator",
            }

            with ui.row().classes("w-full items-center justify-between"):
                with ui.row().classes("items-center gap-2.5"):
                    # Avatar initials
                    initials = "".join([part[0] for part in user_data.get("full_name", "OP").split()[:2]]).upper()
                    ui.label(initials).classes(
                        "w-8 h-8 rounded-full bg-[#EBF8FF] text-[#2563EB] font-bold text-xs flex items-center justify-center border border-[#BFDBFE]"
                    )
                    with ui.column().classes("gap-0"):
                        ui.label(user_data.get("full_name", "Operator")).classes("text-xs font-bold text-[#111827] truncate max-w-[110px]")
                        ui.label(user_data.get("email", "")).classes("text-[10px] text-[#9CA3AF] truncate max-w-[110px]")

                create_status_badge(user_data.get("role", "viewer").upper(), size="sm")

            # Sign out link
            with ui.link(target="/login").classes(
                "w-full flex items-center justify-center gap-2 py-1.5 rounded-md text-xs font-semibold text-[#DC2626] bg-[#FEF2F2] hover:bg-[#FEE2E2] no-underline border border-[#FECACA] transition-colors"
            ):
                ui.icon("logout").classes("text-sm")
                ui.label("Sign Out")

    return drawer
