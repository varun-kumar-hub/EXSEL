from typing import Dict, Any, List
from datetime import datetime
from app.database.repositories import (
    gate_repository,
    sensor_repository,
    alert_repository,
    event_repository,
)
from app.hardware import get_hardware
from app.mock.dashboard import generate_timeseries


class DashboardService:
    def __init__(self):
        self.hardware = get_hardware()

    async def get_overview(self) -> Dict[str, Any]:
        """Aggregate all primary metrics and telemetry for the main dashboard"""
        gates = await gate_repository.get_all_gates()
        sensors = await sensor_repository.get_all_sensors()
        alerts = await alert_repository.get_active_alerts(limit=4)

        # Telemetry values from hardware or sensors
        hardware_readings = await self.hardware.read_all_sensors()

        water_level = hardware_readings.get("SENS_LVL_01", 72.4)
        flow_rate = hardware_readings.get("SENS_FLW_01", 18.4)
        pump_state = await self.hardware.get_pump_status()

        # Update sensor repository with latest readings
        for s_id, val in hardware_readings.items():
            await sensor_repository.update_reading(s_id, val)

        open_gates_count = sum(1 for g in gates if g.status == "OPEN")
        total_gates = len(gates)

        # Gate cards summary
        gate_summaries = []
        for g in gates:
            # Sync with hardware limit switches
            hw_status = await self.hardware.get_gate_status(g.id)
            if hw_status != g.status:
                await gate_repository.update_status(g.id, hw_status)
                g.status = hw_status

            gate_summaries.append({
                "id": g.id,
                "name": g.name,
                "location": g.location,
                "status": g.status,
                "mode": g.mode,
                "is_connected": g.is_connected,
                "last_changed_at": g.last_changed_at,
            })

        # Water level status evaluation
        if water_level < 30.0:
            level_status = "Low"
            level_color = "warning"
        elif water_level > 80.0:
            level_status = "High"
            level_color = "critical"
        else:
            level_status = "Normal"
            level_color = "success"

        return {
            "system_online": await self.hardware.is_connected(),
            "last_updated": datetime.utcnow(),
            "summary_cards": {
                "water_level": {
                    "value": round(water_level, 1),
                    "unit": "%",
                    "status_label": level_status,
                    "status_color": level_color,
                    "subtext": "Updated 10 sec ago",
                    "progress_pct": min(100.0, max(0.0, water_level)),
                },
                "flow_rate": {
                    "value": round(flow_rate, 1),
                    "unit": "L/min",
                    "status_label": "Current flow",
                    "status_color": "info",
                    "subtext": "Updated 10 sec ago",
                },
                "water_gates": {
                    "value": f"{open_gates_count} / {total_gates}",
                    "unit": "",
                    "status_label": "Gates Open",
                    "status_color": "success" if open_gates_count > 0 else "muted",
                    "subtext": "Updated 15 sec ago",
                },
                "pump": {
                    "value": pump_state,
                    "unit": "",
                    "status_label": "Running" if pump_state == "ON" else "Standby",
                    "status_color": "success" if pump_state == "ON" else "muted",
                    "subtext": "Updated 5 sec ago",
                },
            },
            "gates": gate_summaries,
            "alerts": [
                {
                    "id": a.id,
                    "title": a.title,
                    "message": a.message,
                    "severity": a.severity,
                    "created_at": a.created_at,
                    "is_read": a.is_read,
                }
                for a in alerts
            ],
            "system_stats": {
                "uptime": "99.8%",
                "avg_water": "68%",
                "total_operations": 142,
                "sensors_online": f"{sum(1 for s in sensors if s.status == 'ONLINE')} / {len(sensors)}",
            },
        }

    async def get_chart_data(self, chart_type: str, time_range: str = "24H") -> List[Dict[str, Any]]:
        """Return timeseries for 1H, 6H, 24H, or 7D"""
        range_hours = {
            "1H": 1,
            "6H": 6,
            "24H": 24,
            "7D": 168,
        }.get(time_range, 24)

        pts_count = 25
        if chart_type == "water_level":
            return generate_timeseries(hours=range_hours, base_val=72.0, variance=4.0, points_count=pts_count)
        else:
            return generate_timeseries(hours=range_hours, base_val=18.4, variance=2.5, points_count=pts_count)


dashboard_service = DashboardService()
