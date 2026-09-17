from nicegui import ui, app
from app.auth.service import auth_service
from app.utils.validators import check_password_strength
from app.ui.components.toast import show_toast
from app.ui.theme.styles import GLOBAL_CSS


def register_signup_page():
    @ui.page("/signup")
    def signup_page():
        ui.add_head_html(f"<style>{GLOBAL_CSS}</style>")

        with ui.column().classes("w-full min-h-screen items-center justify-center bg-[#F7F8FA] p-4"):
            with ui.card().classes("sw-card p-6 sm:p-8 max-w-md w-full shadow-md bg-white"):
                with ui.column().classes("w-full items-center mb-6 text-center"):
                    with ui.element("div").classes("w-12 h-12 rounded-xl bg-[#2563EB] flex items-center justify-center text-white mb-3"):
                        ui.icon("person_add").classes("text-2xl")
                    ui.label("Create Operator Account").classes("text-xl font-bold text-[#111827]")
                    ui.label("Join the smart water management network").classes("text-xs text-[#6B7280]")

                full_name_input = ui.input("Full Name", placeholder="Jane Doe").classes("w-full mb-3").props("outlined dense")
                email_input = ui.input("Email address", placeholder="jane@smartwater.io").classes("w-full mb-3").props("outlined dense")

                password_input = ui.input(
                    "Password", placeholder="••••••••", password=True, password_toggle_button=True
                ).classes("w-full mb-2").props("outlined dense")

                # Live Password Strength Requirements Checklist
                with ui.column().classes("w-full bg-[#F9FAFB] p-3 rounded-md border border-[#E5E7EB] mb-3 text-xs gap-1.5"):
                    ui.label("Password Requirements:").classes("font-semibold text-[#4B5563] text-[11px]")
                    rule_len = ui.label("✕ At least 8 characters").classes("text-[#DC2626]")
                    rule_upper = ui.label("✕ At least one uppercase letter").classes("text-[#DC2626]")
                    rule_num = ui.label("✕ At least one number").classes("text-[#DC2626]")
                    rule_special = ui.label("✕ At least one special character (@, #, $, etc.)").classes("text-[#DC2626]")

                def update_strength_indicators():
                    val = password_input.value or ""
                    checks = check_password_strength(val)

                    rule_len.set_text("✓ At least 8 characters" if checks["min_length"] else "✕ At least 8 characters")
                    rule_len.classes(replace="text-[#10B981]" if checks["min_length"] else "text-[#DC2626]")

                    rule_upper.set_text("✓ At least one uppercase letter" if checks["uppercase"] else "✕ At least one uppercase letter")
                    rule_upper.classes(replace="text-[#10B981]" if checks["uppercase"] else "text-[#DC2626]")

                    rule_num.set_text("✓ At least one number" if checks["number"] else "✕ At least one number")
                    rule_num.classes(replace="text-[#10B981]" if checks["number"] else "text-[#DC2626]")

                    rule_special.set_text("✓ At least one special character" if checks["special_char"] else "✕ At least one special character (@, #, $, etc.)")
                    rule_special.classes(replace="text-[#10B981]" if checks["special_char"] else "text-[#DC2626]")

                password_input.on("input", update_strength_indicators)

                confirm_input = ui.input(
                    "Confirm Password", placeholder="••••••••", password=True, password_toggle_button=True
                ).classes("w-full mb-3").props("outlined dense")

                terms_cb = ui.checkbox("I accept the terms of operation and privacy policy", value=True).classes(
                    "text-xs text-[#4B5563] mb-4"
                )

                async def handle_signup():
                    if not full_name_input.value or not email_input.value or not password_input.value:
                        show_toast("Please fill in all required fields.", type="warning")
                        return
                    if not terms_cb.value:
                        show_toast("Please accept the terms to proceed.", type="warning")
                        return

                    try:
                        user = await auth_service.signup(
                            email=email_input.value,
                            password=password_input.value,
                            confirm_password=confirm_input.value,
                            full_name=full_name_input.value,
                        )
                        show_toast("Account created! Please sign in with your credentials.", type="success")
                        ui.navigate.to("/login")
                    except Exception as e:
                        show_toast(str(e), type="negative")

                ui.button("Create Account", on_click=handle_signup).classes(
                    "w-full sw-btn-primary py-2 text-sm font-semibold mb-4"
                )

                with ui.row().classes("w-full justify-center text-xs text-[#6B7280]"):
                    ui.label("Already have an account?")
                    ui.link("Sign In", target="/login").classes("text-[#2563EB] font-semibold no-underline hover:underline")
