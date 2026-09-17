from app.ui.pages.login import register_login_page
from app.ui.pages.signup import register_signup_page
from app.ui.pages.forgot_password import register_auth_support_pages
from app.ui.pages.dashboard import register_dashboard_page
from app.ui.pages.water_gates import register_water_gates_page
from app.ui.pages.distribution import register_distribution_page
from app.ui.pages.sensors import register_sensors_page
from app.ui.pages.analytics import register_analytics_page
from app.ui.pages.history import register_history_page
from app.ui.pages.settings import register_settings_page


def register_all_pages():
    """Register all NiceGUI web routes"""
    register_login_page()
    register_signup_page()
    register_auth_support_pages()
    register_dashboard_page()
    register_water_gates_page()
    register_distribution_page()
    register_sensors_page()
    register_analytics_page()
    register_history_page()
    register_settings_page()


__all__ = ["register_all_pages"]
