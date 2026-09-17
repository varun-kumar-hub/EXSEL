from datetime import datetime, timedelta

INITIAL_ALERTS = [
    {
        "id": "alt-01",
        "alert_type": "high_water_level",
        "severity": "critical",
        "title": "Reservoir Level Critical",
        "message": "Water level crossed upper threshold at 82.5% during inflow peak.",
        "is_read": False,
        "created_at": datetime.utcnow() - timedelta(minutes=4),
    },
    {
        "id": "alt-02",
        "alert_type": "gate_offline",
        "severity": "warning",
        "title": "Gate 03 Telemetry Intermittent",
        "message": "Secondary telemetry channel experienced packet loss 2 minutes ago.",
        "is_read": False,
        "created_at": datetime.utcnow() - timedelta(minutes=14),
    },
    {
        "id": "alt-03",
        "alert_type": "distribution_complete",
        "severity": "info",
        "title": "Distribution Sequence Completed",
        "message": "Sector B distribution sequence finished successfully. 14,200 L distributed.",
        "is_read": False,
        "created_at": datetime.utcnow() - timedelta(minutes=42),
    },
    {
        "id": "alt-04",
        "alert_type": "sensor_heartbeat",
        "severity": "info",
        "title": "System Telemetry Online",
        "message": "All 5 sensor stations and gate actuators transmitting nominal heartbeat.",
        "is_read": True,
        "created_at": datetime.utcnow() - timedelta(hours=2),
    },
]
