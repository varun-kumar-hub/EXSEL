from typing import Callable, Awaitable
from nicegui import ui


def show_confirmation_dialog(
    title: str,
    message: str,
    on_confirm: Callable[[], Awaitable[None] or None],
    confirm_label: str = "Confirm",
    is_danger: bool = False,
):
    """
    Standard safety confirmation dialog modal
    Ensures accidental clicks never trigger physical equipment actuation.
    """
    with ui.dialog() as dialog, ui.card().classes("p-5 sm:p-6 max-w-md w-[92vw] sm:w-full sw-card shadow-lg bg-white"):
        with ui.row().classes("items-center gap-3 mb-2"):
            icon_name = "warning" if is_danger else "help"
            icon_color = "text-[#DC2626]" if is_danger else "text-[#2563EB]"
            ui.icon(icon_name).classes(f"text-2xl {icon_color}")
            ui.label(title).classes("text-lg font-semibold text-[#111827]")

        ui.label(message).classes("text-sm text-[#4B5563] mb-6 leading-relaxed")

        with ui.row().classes("w-full justify-end gap-3"):
            ui.button("Cancel", on_click=dialog.close).classes("sw-btn-secondary px-4 py-1.5 text-sm")

            async def handle_confirm():
                dialog.close()
                if callable(on_confirm):
                    res = on_confirm()
                    if hasattr(res, "__await__"):
                        await res

            btn_cls = "sw-btn-danger" if is_danger else "sw-btn-primary"
            ui.button(confirm_label, on_click=handle_confirm).classes(f"{btn_cls} px-4 py-1.5 text-sm")

    dialog.open()
    return dialog
