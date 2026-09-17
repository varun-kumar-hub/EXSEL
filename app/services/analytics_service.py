from typing import Dict, Any, List
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from app.mock.dashboard import generate_timeseries
from app.database.repositories import event_repository


class AnalyticsService:
    async def get_analytics(self, date_filter: str = "7D") -> Dict[str, Any]:
        """Compute system telemetry analytics and distributions with Pandas/NumPy"""
        days = {
            "Today": 1,
            "7D": 7,
            "30D": 30,
        }.get(date_filter, 7)

        hours = days * 24
        water_points = generate_timeseries(hours=hours, base_val=72.0, variance=5.0, points_count=35)
        flow_points = generate_timeseries(hours=hours, base_val=18.4, variance=3.5, points_count=35)

        # Convert to Pandas DataFrame for calculations
        df_water = pd.DataFrame(water_points)
        df_flow = pd.DataFrame(flow_points)

        avg_water = float(df_water["value"].mean()) if not df_water.empty else 72.0
        max_flow = float(df_flow["value"].max()) if not df_flow.empty else 21.5
        min_flow = float(df_flow["value"].min()) if not df_flow.empty else 14.2

        # Daily gate operations calculation
        daily_ops = []
        today = datetime.utcnow()
        for i in range(days - 1, -1, -1):
            d = today - timedelta(days=i)
            # Simulated ops count per day between 8 and 24
            daily_ops.append({
                "date": d.strftime("%b %d"),
                "count": int(12 + np.random.randint(-4, 9)),
            })

        total_ops = sum(item["count"] for item in daily_ops)
        estimated_loss = round(total_ops * 18.5, 1)  # Liters

        return {
            "summary": {
                "avg_water_level": round(avg_water, 1),
                "max_flow_rate": round(max_flow, 1),
                "min_flow_rate": round(min_flow, 1),
                "system_uptime_pct": 99.8,
                "total_gate_operations": total_ops,
                "estimated_water_loss_liters": estimated_loss,
            },
            "water_level_trend": water_points,
            "flow_rate_trend": flow_points,
            "gate_operations_daily": daily_ops,
        }


analytics_service = AnalyticsService()
