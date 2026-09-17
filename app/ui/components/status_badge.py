from nicegui import ui


def create_status_badge(status: str, size: str = "sm") -> ui.element:
    """Create a standardized color-coded status badge"""
    status_upper = status.upper().strip()

    color_map = {
        # Gate States
        "OPEN": ("bg-[#DCFCE7]", "text-[#15803D]", "border-[#86EFAC]", "● Open"),
        "CLOSED": ("bg-[#F3F4F6]", "text-[#4B5563]", "border-[#D1D5DB]", "● Closed"),
        "OPENING": ("bg-[#EBF8FF]", "text-[#1D4ED8]", "border-[#93C5FD]", "↻ Opening"),
        "CLOSING": ("bg-[#FEF3C7]", "text-[#B45309]", "border-[#FCD34D]", "↻ Closing"),
        "ERROR": ("bg-[#FEE2E2]", "text-[#B91C1C]", "border-[#FCA5A5]", "✕ Error"),
        # Connectivity / System
        "ONLINE": ("bg-[#DCFCE7]", "text-[#15803D]", "border-[#86EFAC]", "● Online"),
        "OFFLINE": ("bg-[#F3F4F6]", "text-[#6B7280]", "border-[#D1D5DB]", "○ Offline"),
        "CONNECTED": ("bg-[#DCFCE7]", "text-[#15803D]", "border-[#86EFAC]", "● Connected"),
        # Mode
        "AUTO": ("bg-[#EFF6FF]", "text-[#2563EB]", "border-[#BFDBFE]", "AUTO"),
        "MANUAL": ("bg-[#FEF3C7]", "text-[#D97706]", "border-[#FDE68A]", "MANUAL"),
        # General Status
        "NORMAL": ("bg-[#DCFCE7]", "text-[#15803D]", "border-[#86EFAC]", "Normal"),
        "WARNING": ("bg-[#FEF3C7]", "text-[#B45309]", "border-[#FCD34D]", "Warning"),
        "CRITICAL": ("bg-[#FEE2E2]", "text-[#B91C1C]", "border-[#FCA5A5]", "Critical"),
        "ACTIVE": ("bg-[#EBF8FF]", "text-[#2563EB]", "border-[#93C5FD]", "● Active"),
        "COMPLETED": ("bg-[#DCFCE7]", "text-[#15803D]", "border-[#86EFAC]", "✓ Completed"),
        "WAITING": ("bg-[#F3F4F6]", "text-[#6B7280]", "border-[#D1D5DB]", "Waiting"),
        "FAILED": ("bg-[#FEE2E2]", "text-[#B91C1C]", "border-[#FCA5A5]", "Failed"),
        "SUCCESS": ("bg-[#DCFCE7]", "text-[#15803D]", "border-[#86EFAC]", "Success"),
        "INFO": ("bg-[#EFF6FF]", "text-[#2563EB]", "border-[#BFDBFE]", "Info"),
    }

    bg_cls, text_cls, border_cls, label = color_map.get(
        status_upper, ("bg-[#F3F4F6]", "text-[#4B5563]", "border-[#D1D5DB]", status)
    )

    py = "py-0.5" if size == "sm" else "py-1"
    px = "px-2" if size == "sm" else "px-2.5"
    text_size = "text-xs" if size == "sm" else "text-sm"

    badge = ui.label(label).classes(
        f"{bg_cls} {text_cls} {border_cls} border {px} {py} rounded-full font-medium {text_size} inline-flex items-center gap-1 leading-none select-none"
    )
    return badge
