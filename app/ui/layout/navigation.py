"""
Navigation Routes and Metadata
"""

NAV_ITEMS = [
    {
        "id": "dashboard",
        "label": "Dashboard",
        "path": "/dashboard",
        "icon": "space_dashboard",
        "description": "System Overview & Telemetry",
    },
    {
        "id": "water_gates",
        "label": "Water Gates",
        "path": "/water-gates",
        "icon": "meeting_room",
        "description": "Actuator Status & Control",
    },
    {
        "id": "distribution",
        "label": "Distribution",
        "path": "/distribution",
        "icon": "alt_route",
        "description": "Sequential Distribution Control",
    },
    {
        "id": "sensors",
        "label": "Sensors",
        "path": "/sensors",
        "icon": "sensors",
        "description": "Telemetry & Thresholds",
    },
    {
        "id": "analytics",
        "label": "Analytics",
        "path": "/analytics",
        "icon": "analytics",
        "description": "Hydraulic Trends & Water Loss",
    },
    {
        "id": "history",
        "label": "History",
        "path": "/history",
        "icon": "manage_history",
        "description": "Audit Log & System Events",
    },
]

SECONDARY_NAV = [
    {
        "id": "settings",
        "label": "Settings",
        "path": "/settings",
        "icon": "settings",
        "description": "System & User Preferences",
    },
]
