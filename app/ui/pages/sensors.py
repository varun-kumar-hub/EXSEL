from nicegui import ui
from app.ui.layout import app_layout
from app.ui.components.sensor_card import create_sensor_card
from app.ui.components.chart_card import create_plotly_figure
from app.services.sensor_service import sensor_service


def register_sensors_page():
    @ui.page("/sensors")
    async def sensors_page():
        with app_layout(page_title="Sensor Monitoring", subtitle="Real-time Hydraulic Telemetry & Calibration", current_path="/sensors"):
            with ui.row().classes("w-full items-center justify-between mb-4"):
                with ui.column().classes("gap-0"):
                    ui.label("Field Sensors & Transmitters").classes("text-base font-bold text-[#111827]")
                    ui.label("Live pressure, flow, volume, and quality telemetry with automated threshold alert monitoring.").classes("text-xs text-[#6B7280]")

            sensors_grid = ui.element("div").classes("w-full grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-6")

            # History modal
            async def show_sensor_history(sensor_id: str):
                sensor = await sensor_service.get_sensor(sensor_id)
                history = await sensor_service.get_sensor_history(sensor_id)

                with ui.dialog() as dialog, ui.card().classes("p-6 max-w-2xl w-full sw-card shadow-xl bg-white"):
                    with ui.row().classes("w-full items-center justify-between mb-3"):
                        with ui.row().classes("items-center gap-2"):
                            ui.icon("show_chart").classes("text-[#2563EB] text-xl")
                            ui.label(f"{sensor.name} — Telemetry History").classes("text-base font-bold text-[#111827]")
                        ui.button(icon="close", on_click=dialog.close).props("flat round dense")

                    fig = create_plotly_figure(
                        points=history,
                        y_label=f"{sensor.name} ({sensor.unit})",
                        line_color="#2563EB",
                        min_threshold=sensor.minimum_threshold,
                        max_threshold=sensor.maximum_threshold,
                    )
                    ui.plotly(fig).classes("w-full")

                    with ui.row().classes("w-full justify-between text-xs text-[#6B7280] mt-3 border-t pt-2"):
                        ui.label(f"Min Threshold: {sensor.minimum_threshold} {sensor.unit}")
                        ui.label(f"Max Threshold: {sensor.maximum_threshold} {sensor.unit}")
                        ui.label(f"Current: {sensor.last_reading:.1f} {sensor.unit}").classes("font-bold text-[#111827]")

                dialog.open()

            async def refresh_sensors():
                sensors = await sensor_service.get_all_sensors()
                sensors_grid.clear()
                with sensors_grid:
                    for s in sensors:
                        create_sensor_card(
                            sensor_id=s.id,
                            name=s.name,
                            sensor_type=s.sensor_type,
                            unit=s.unit,
                            last_reading=s.last_reading,
                            minimum_threshold=s.minimum_threshold,
                            maximum_threshold=s.maximum_threshold,
                            status=s.status,
                            last_updated_at=s.last_updated_at,
                            on_view_history=show_sensor_history,
                        )

            await refresh_sensors()
            ui.timer(3.0, refresh_sensors)
