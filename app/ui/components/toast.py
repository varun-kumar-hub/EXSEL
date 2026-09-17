from nicegui import ui


def show_toast(message: str, type: str = "info", duration: float = 3.5):
    """
    Standard clean toast notifications
    type: 'positive' (green), 'negative' (red), 'warning' (amber), 'info' (blue)
    """
    color_map = {
        "success": "positive",
        "positive": "positive",
        "error": "negative",
        "negative": "negative",
        "critical": "negative",
        "warning": "warning",
        "info": "info",
    }
    q_type = color_map.get(type.lower(), "info")

    ui.notify(
        message,
        type=q_type,
        position="top-right",
        timeout=int(duration * 1000),
        close_button=True,
    )
