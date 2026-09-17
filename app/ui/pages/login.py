from nicegui import ui, app
from app.auth.service import auth_service
from app.ui.components.toast import show_toast
from app.ui.theme.styles import GLOBAL_CSS


def register_login_page():
    @ui.page("/login")
    def login_page():
        ui.add_head_html(f"<style>{GLOBAL_CSS}</style>")

        with ui.column().classes("w-full min-h-screen items-center justify-center bg-[#F7F8FA] p-4"):
            with ui.card().classes("sw-card p-6 sm:p-8 max-w-md w-full shadow-md bg-white"):
                # Header Logo
                with ui.column().classes("w-full items-center mb-6 text-center"):
                    with ui.element("div").classes("w-12 h-12 rounded-xl bg-[#2563EB] flex items-center justify-center text-white mb-3"):
                        ui.icon("water_drop").classes("text-2xl")
                    ui.label("Smart Water Distribution").classes("text-xl font-bold text-[#111827]")
                    ui.label("Sign in to access industrial monitoring & control").classes("text-xs text-[#6B7280]")

                # Form fields
                email_input = ui.input("Email address", placeholder="operator@smartwater.io").classes("w-full mb-3").props("outlined dense")
                password_input = ui.input("Password", placeholder="••••••••", password=True, password_toggle_button=True).classes("w-full mb-3").props("outlined dense")

                with ui.row().classes("w-full justify-between items-center mb-4 text-xs"):
                    remember_cb = ui.checkbox("Remember me", value=True).classes("text-xs text-[#4B5563]")
                    ui.link("Forgot password?", target="/forgot-password").classes("text-[#2563EB] font-medium no-underline hover:underline")

                # Submit Button
                async def handle_login():
                    if not email_input.value or not password_input.value:
                        show_toast("Please enter both email and password.", type="warning")
                        return
                    try:
                        user, token = await auth_service.login(email_input.value, password_input.value)
                        app.storage.user["user"] = {
                            "id": user.id,
                            "email": user.email,
                            "full_name": user.full_name,
                            "role": user.role,
                        }
                        app.storage.user["token"] = token
                        show_toast(f"Welcome back, {user.full_name}!", type="success")
                        ui.navigate.to("/dashboard")
                    except Exception as e:
                        show_toast(str(e), type="negative")

                submit_btn = ui.button("Sign In", on_click=handle_login).classes("w-full sw-btn-primary py-2 text-sm font-semibold mb-3")

                # Google OAuth
                async def handle_google_login():
                    try:
                        user, token = await auth_service.google_login("mock-token")
                        app.storage.user["user"] = {
                            "id": user.id,
                            "email": user.email,
                            "full_name": user.full_name,
                            "role": user.role,
                        }
                        app.storage.user["token"] = token
                        show_toast(f"Signed in via Google: {user.full_name}", type="success")
                        ui.navigate.to("/dashboard")
                    except Exception as e:
                        show_toast(str(e), type="negative")

                with ui.row().classes("w-full items-center justify-center my-2 text-xs text-[#9CA3AF]"):
                    ui.element("div").classes("flex-1 h-px bg-[#E5E7EB]")
                    ui.label("OR").classes("px-3")
                    ui.element("div").classes("flex-1 h-px bg-[#E5E7EB]")

                with ui.button(on_click=handle_google_login).classes("w-full sw-btn-secondary py-2 text-sm font-medium flex items-center justify-center gap-2 mb-4"):
                    ui.icon("login").classes("text-base text-[#4285F4]")
                    ui.label("Sign in with Google")

                # Quick Demo Logins for Fast Testing
                with ui.expansion("Quick Demo Credentials", icon="vpn_key").classes("w-full text-xs text-[#6B7280] bg-[#F9FAFB] rounded-md border border-[#E5E7EB] mb-4"):
                    with ui.column().classes("w-full gap-2 p-2"):
                        with ui.row().classes("w-full justify-between items-center"):
                            ui.label("Admin (Full Access)").classes("font-semibold text-[#111827]")
                            def fill_admin():
                                email_input.value = "admin@smartwater.io"
                                password_input.value = "Admin@123"
                            ui.button("Fill Admin", on_click=fill_admin).classes("text-xs py-0.5 px-2").props("flat dense")

                        with ui.row().classes("w-full justify-between items-center"):
                            ui.label("Operator (Gates & Distribution)").classes("font-semibold text-[#111827]")
                            def fill_operator():
                                email_input.value = "operator@smartwater.io"
                                password_input.value = "Operator@123"
                            ui.button("Fill Operator", on_click=fill_operator).classes("text-xs py-0.5 px-2").props("flat dense")

                        with ui.row().classes("w-full justify-between items-center"):
                            ui.label("Viewer (Read-Only)").classes("font-semibold text-[#111827]")
                            def fill_viewer():
                                email_input.value = "viewer@smartwater.io"
                                password_input.value = "Viewer@123"
                            ui.button("Fill Viewer", on_click=fill_viewer).classes("text-xs py-0.5 px-2").props("flat dense")

                # Link to Signup
                with ui.row().classes("w-full justify-center text-xs text-[#6B7280]"):
                    ui.label("Don't have an account?")
                    ui.link("Create Account", target="/signup").classes("text-[#2563EB] font-semibold no-underline hover:underline")
