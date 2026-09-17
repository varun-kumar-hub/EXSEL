"""
Theme Colors matching PRD Specifications Exactly
"""

# Palette
COLOR_BG = "#F7F8FA"
COLOR_SURFACE = "#FFFFFF"
COLOR_TEXT_PRIMARY = "#111827"
COLOR_TEXT_SECONDARY = "#6B7280"
COLOR_BORDER = "#E5E7EB"

# Brand
COLOR_PRIMARY = "#2563EB"       # Blue
COLOR_PRIMARY_HOVER = "#1D4ED8"
COLOR_PRIMARY_ACTIVE = "#1E40AF"
COLOR_ACCENT = "#06B6D4"        # Water Teal

# Status
COLOR_SUCCESS = "#10B981"       # Green
COLOR_WARNING = "#F59E0B"       # Amber
COLOR_CRITICAL = "#DC2626"      # Red
COLOR_INFO = "#3B82F6"          # Blue
COLOR_MUTED = "#9CA3AF"         # Gray

# Alert background / border pairs
ALERT_STYLES = {
    "critical": {
        "bg": "#FEF2F2",
        "border": "#DC2626",
        "text": "#991B1B",
        "icon": "error",
    },
    "warning": {
        "bg": "#FFFBEB",
        "border": "#F59E0B",
        "text": "#92400E",
        "icon": "warning",
    },
    "info": {
        "bg": "#EBF8FF",
        "border": "#3B82F6",
        "text": "#1E40AF",
        "icon": "info",
    },
}
