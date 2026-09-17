from contextlib import contextmanager
from nicegui import ui, app
from app.ui.theme.styles import GLOBAL_CSS
from app.ui.layout.sidebar import create_sidebar
from app.ui.layout.header import create_header
from app.ui.layout.mobile_nav import create_mobile_nav


@contextmanager
def app_layout(page_title: str, subtitle: str = "System Overview", current_path: str = "/dashboard"):
    """
    Master Application Shell Context Manager
    Injects global design system CSS, desktop sidebar, top header, and mobile navigation.
    """
    # Inject design system stylesheet
    ui.add_head_html(f"<style>{GLOBAL_CSS}</style>")

    # Top Header
    drawer = create_sidebar(current_path=current_path)
    create_header(page_title=page_title, subtitle=subtitle, sidebar_drawer=drawer)

    # Mobile Bottom Nav
    create_mobile_nav(current_path=current_path)

    # Main Scrollable Content Area
    with ui.column().classes("w-full min-h-screen bg-[#F7F8FA] p-4 md:p-8 max-w-7xl mx-auto pb-20 lg:pb-8"):
        yield
