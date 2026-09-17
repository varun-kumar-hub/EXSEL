from nicegui import ui
from app.ui.layout.navigation import NAV_ITEMS


def create_mobile_nav(current_path: str = "/dashboard") -> ui.footer:
    """
    Standard Mobile Bottom Navigation Bar (< 640px)
    Touch targets >= 44px
    """
    with ui.footer().classes("lg:hidden bg-white border-t border-[#E5E7EB] p-0 z-30 shadow-md h-14"):
        with ui.row().classes("w-full h-full items-center justify-around"):
            for item in NAV_ITEMS[:5]:
                is_active = (current_path == item["path"])
                text_color = "text-[#2563EB] font-bold" if is_active else "text-[#6B7280]"

                with ui.link(target=item["path"]).classes(
                    f"flex flex-col items-center justify-center min-w-[48px] min-h-[44px] no-underline {text_color}"
                ):
                    ui.icon(item["icon"]).classes("text-lg mb-0.5")
                    ui.label(item["label"]).classes("text-[10px] leading-tight")
