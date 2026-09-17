from datetime import datetime


def format_metric(value: float, unit: str = "", decimals: int = 1) -> str:
    """Format numeric metrics cleanly (e.g. '72.4 %', '18.4 L/min')"""
    if value is None:
        return "--"
    if decimals == 0:
        formatted = f"{int(round(value))}"
    else:
        formatted = f"{value:.{decimals}f}"
    return f"{formatted} {unit}".strip()


def format_percentage(value: float) -> str:
    return f"{value:.1f}%" if value is not None else "--"


def format_flow_rate(value: float) -> str:
    return f"{value:.1f} L/min" if value is not None else "--"


def format_status_label(status: str) -> str:
    """Convert raw uppercase state to display title"""
    return status.replace("_", " ").title()
