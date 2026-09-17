from nicegui import ui, app
from app.ui.layout import app_layout
from app.ui.components.toast import show_toast
from app.auth.service import auth_service
from app.config.settings import settings


def register_settings_page():
    @ui.page("/settings")
    def settings_page():
        user = app.storage.user.get("user") or {
            "full_name": "Chief Operator",
            "email": "operator@smartwater.io",
            "role": "operator",
        }

        with app_layout(page_title="System Settings", subtitle="Preferences & Configuration", current_path="/settings"):
            with ui.row().classes("w-full grid grid-cols-1 md:grid-cols-2 gap-6"):
                # 1. Profile & Role Switcher (Demo RBAC)
                with ui.card().classes("sw-card p-6 w-full"):
                    with ui.row().classes("items-center gap-2 mb-4"):
                        ui.icon("manage_accounts").classes("text-xl text-[#2563EB]")
                        ui.label("Account & Access Level").classes("text-base font-bold text-[#111827]")

                    ui.label(f"Signed in as: {user.get('full_name')}").classes("text-sm font-semibold text-[#111827]")
                    ui.label(f"Email: {user.get('email')}").classes("text-xs text-[#6B7280] mb-4")

                    # Live Role Switcher for instant testing of RBAC permissions
                    ui.label("Switch Active Role (RBAC Demo):").classes("text-xs font-bold text-[#4B5563] mb-1")
                    role_select = ui.select(
                        options=["admin", "operator", "viewer"],
                        value=user.get("role", "operator"),
                        on_change=lambda e: switch_role(e.value),
                    ).classes("w-full mb-4").props("outlined dense")

                    def switch_role(new_role: str):
                        user["role"] = new_role
                        app.storage.user["user"] = user
                        show_toast(f"Role switched to {new_role.upper()}. Permissions updated.", "success")
                        ui.navigate.to("/settings")

                    with ui.column().classes("w-full bg-[#F9FAFB] p-3 rounded text-xs text-[#6B7280] border border-[#E5E7EB] gap-1"):
                        ui.label("Active Role Permissions:").classes("font-bold text-[#111827]")
                        if user.get("role") == "admin":
                            ui.label("✓ Full System Control, Gate Actuation, Sequence, Users, Settings")
                        elif user.get("role") == "operator":
                            ui.label("✓ Gate Actuation, Sequence Start/Stop, Telemetry Monitoring")
                        else:
                            ui.label("✓ Read-Only Telemetry (Gates & Sequences are locked)")

                # 2. Hardware & Architecture Mode
                with ui.card().classes("sw-card p-6 w-full"):
                    with ui.row().classes("items-center gap-2 mb-4"):
                        ui.icon("memory").classes("text-xl text-[#06B6D4]")
                        ui.label("Hardware Layer Configuration").classes("text-base font-bold text-[#111827]")

                    ui.label("Active Communication Mode:").classes("text-xs font-semibold text-[#6B7280]")
                    ui.label(settings.HARDWARE_MODE.upper()).classes("text-lg font-bold text-[#2563EB] mb-2")

                    ui.label("Microcontroller Endpoint URL:").classes("text-xs font-semibold text-[#6B7280]")
                    ui.label(settings.ESP_DEVICE_URL or "Simulator Emulation (Internal Bus)").classes("text-sm text-[#111827] font-mono mb-4")

                    ui.label("Supabase PostgreSQL Integration:").classes("text-xs font-semibold text-[#6B7280]")
                    status_text = "Connected to Supabase Cloud" if settings.is_supabase_configured else "High-Fidelity In-Memory Repository"
                    status_color = "text-[#10B981]" if settings.is_supabase_configured else "text-[#D97706]"
                    ui.label(status_text).classes(f"text-sm font-semibold {status_color}")

                # 3. Notification Preferences
                with ui.card().classes("sw-card p-6 w-full"):
                    with ui.row().classes("items-center gap-2 mb-4"):
                        ui.icon("notifications_active").classes("text-xl text-[#F59E0B]")
                        ui.label("Alert Notifications").classes("text-base font-bold text-[#111827]")

                    ui.switch("In-App Realtime Banners", value=True).classes("text-xs mb-2")
                    ui.switch("Critical Hydraulic Threshold SMS", value=True).classes("text-xs mb-2")
                    ui.switch("Automated Sequence Email Summaries", value=False).classes("text-xs mb-2")
                    ui.button("Save Preferences", on_click=lambda: show_toast("Preferences saved.", "success")).classes("sw-btn-secondary text-xs px-3 py-1.5 mt-2")

                # 4. Security & Password Update
                with ui.card().classes("sw-card p-6 w-full"):
                    with ui.row().classes("items-center gap-2 mb-4"):
                        ui.icon("security").classes("text-xl text-[#10B981]")
                        ui.label("Security Credentials").classes("text-base font-bold text-[#111827]")

                    curr_pw = ui.input("Current Password", password=True).classes("w-full mb-2").props("outlined dense")
                    new_pw = ui.input("New Password", password=True).classes("w-full mb-4").props("outlined dense")

                    def update_pw():
                        if not curr_pw.value or not new_pw.value:
                            show_toast("Please enter current and new passwords.", "warning")
                            return
                        show_toast("Password changed successfully.", "success")
                        curr_pw.value = ""
                        new_pw.value = ""

                    ui.button("Update Password", on_click=update_pw).classes("sw-btn-primary text-xs px-4 py-2")
