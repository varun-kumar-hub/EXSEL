from datetime import datetime, timedelta

INITIAL_GATES = [
    {
        "id": "GATE_01",
        "name": "Gate 01",
        "location": "Main Canal - Intake Feed",
        "status": "OPEN",
        "mode": "AUTO",
        "is_connected": True,
        "last_changed_at": datetime.utcnow() - timedelta(minutes=15),
    },
    {
        "id": "GATE_02",
        "name": "Gate 02",
        "location": "Treatment Diversion North",
        "status": "OPEN",
        "mode": "AUTO",
        "is_connected": True,
        "last_changed_at": datetime.utcnow() - timedelta(minutes=35),
    },
    {
        "id": "GATE_03",
        "name": "Gate 03",
        "location": "Distribution Bypass East",
        "status": "OPEN",
        "mode": "AUTO",
        "is_connected": True,
        "last_changed_at": datetime.utcnow() - timedelta(hours=2),
    },
    {
        "id": "GATE_04",
        "name": "Gate 04",
        "location": "Secondary Spillway South",
        "status": "CLOSED",
        "mode": "MANUAL",
        "is_connected": True,
        "last_changed_at": datetime.utcnow() - timedelta(hours=6),
    },
]
