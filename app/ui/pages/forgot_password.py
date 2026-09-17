from nicegui import ui
from app.auth.service import auth_service
from app.ui.components.toast import show_toast
from app.ui.theme.styles import GLOBAL_CSS


def register_auth_support_pages():
    @ui.page("/forgot-password")
    def forgot_password_page():
        ui.add_head_html(f"<style>{GLOBAL_CSS}</style>")

        with ui.column().classes("w-full min-h-screen items-center justify-center bg-[#F7F8FA] p-4"):
            with ui.card().classes("sw-card p-8 max-w-md w-full shadow-md bg-white"):
                with ui.column().classes("w-full items-center mb-6 text-center"):
                    with ui.element("div").classes("w-12 h-12 rounded-xl bg-[#EFF6FF] flex items-center justify-center text-[#2563EB] mb-3"):
                        ui.icon("lock_reset").classes("text-2xl")
                    ui.label("Reset Password").classes("text-xl font-bold text-[#111827]")
                    ui.label("Enter your registered email address to receive a secure password recovery link.").classes("text-xs text-[#6B7280]")

                email_input = ui.input("Email address", placeholder="operator@smartwater.io").classes("w-full mb-4").props("outlined dense")

                async def handle_send():
                    if not email_input.value:
                        show_toast("Please enter your email address.", type="warning")
                        return
                    token = await auth_service.request_password_reset(email_input.value)
                    show_toast("Password reset instructions dispatched.", type="success")
                    ui.navigate.to(f"/reset-password?token={token}")

                ui.button("Send Reset Link", on_click=handle_send).classes("w-full sw-btn-primary py-2 text-sm font-semibold mb-3")

                with ui.row().classes("w-full justify-center text-xs text-[#6B7280]"):
                    ui.link("← Back to Sign In", target="/login").classes("text-[#2563EB] font-semibold no-underline hover:underline")

    @ui.page("/reset-password")
    def reset_password_page(token: str = ""):
        ui.add_head_html(f"<style>{GLOBAL_CSS}</style>")

        with ui.column().classes("w-full min-h-screen items-center justify-center bg-[#F7F8FA] p-4"):
            with ui.card().classes("sw-card p-8 max-w-md w-full shadow-md bg-white"):
                with ui.column().classes("w-full items-center mb-6 text-center"):
                    ui.label("Set New Password").classes("text-xl font-bold text-[#111827]")
                    ui.label("Choose a strong new password for your account.").classes("text-xs text-[#6B7280]")

                new_pass = ui.input("New Password", password=True, password_toggle_button=True).classes("w-full mb-3").props("outlined dense")
                confirm_pass = ui.input("Confirm Password", password=True, password_toggle_button=True).classes("w-full mb-4").props("outlined dense")

                async def handle_reset():
                    try:
                        await auth_service.reset_password(token, new_pass.value, confirm_pass.value)
                        show_toast("Password updated successfully! Please sign in.", type="success")
                        ui.navigate.to("/login")
                    except Exception as e:
                        show_toast(str(e), type="negative")

                ui.button("Update Password", on_click=handle_reset).classes("w-full sw-btn-primary py-2 text-sm font-semibold mb-3")
                ui.link("Cancel", target="/login").classes("w-full text-center text-xs text-[#6B7280]")

    @ui.page("/verify-email")
    def verify_email_page(email: str = "operator@smartwater.io"):
        ui.add_head_html(f"<style>{GLOBAL_CSS}</style>")

        with ui.column().classes("w-full min-h-screen items-center justify-center bg-[#F7F8FA] p-4"):
            with ui.card().classes("sw-card p-8 max-w-md w-full shadow-md bg-white text-center"):
                ui.icon("mark_email_read").classes("text-4xl text-[#10B981] mb-2 mx-auto")
                ui.label("Check Your Email").classes("text-xl font-bold text-[#111827]")
                ui.label(f"We sent a verification link to {email}. Please follow the link to activate telemetry access.").classes("text-xs text-[#6B7280] my-2")
                ui.button("Resend Verification Link", on_click=lambda: show_toast("Verification link resent.", "info")).classes("sw-btn-secondary text-xs w-full mb-3")
                ui.link("Sign In", target="/login").classes("text-xs text-[#2563EB] font-semibold")

    @ui.page("/unauthorized")
    def unauthorized_page():
        ui.add_head_html(f"<style>{GLOBAL_CSS}</style>")

        with ui.column().classes("w-full min-h-screen items-center justify-center bg-[#F7F8FA] p-4 text-center"):
            with ui.card().classes("sw-card p-8 max-w-md w-full shadow-md bg-white"):
                ui.icon("gpp_bad").classes("text-4xl text-[#DC2626] mb-2 mx-auto")
                ui.label("Access Restricted").classes("text-xl font-bold text-[#111827]")
                ui.label("You do not have the required operational permissions (Admin or Operator) to perform this action.").classes("text-xs text-[#6B7280] my-3 leading-relaxed")
                ui.button("Return to Dashboard", on_click=lambda: ui.navigate.to("/dashboard")).classes("sw-btn-primary text-sm w-full")
