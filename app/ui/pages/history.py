from nicegui import ui
from app.ui.layout import app_layout
from app.ui.components.status_badge import create_status_badge
from app.ui.components.toast import show_toast
from app.services.history_service import history_service


def register_history_page():
    @ui.page("/history")
    async def history_page():
        current_page = 1
        page_size = 10
        search_query = ""
        selected_type = "All"
        selected_status = "All"

        with app_layout(page_title="Audit History & Logs", subtitle="Immutable System Event Chronicle", current_path="/history"):
            # Header with Search, Filter & Export Toolbar
            with ui.card().classes("sw-card p-4 w-full mb-6"):
                with ui.row().classes("w-full items-center justify-between gap-3 flex-wrap"):
                    # Search Input
                    search_input = ui.input(
                        placeholder="Search devices, operators, actions...",
                        on_change=lambda e: handle_search(e.value),
                    ).classes("w-full sm:w-72 bg-white").props("outlined dense clearable")

                    # Filters
                    with ui.row().classes("items-center gap-2 sm:gap-3 w-full sm:w-auto flex-wrap sm:flex-nowrap"):
                        type_select = ui.select(
                            options=["All", "Gate Operation", "Sensor Alert", "Sequence", "Auth", "System"],
                            value="All",
                            label="Event Type",
                            on_change=lambda e: handle_type_change(e.value),
                        ).classes("flex-1 sm:w-40 bg-white").props("outlined dense")

                        status_select = ui.select(
                            options=["All", "Success", "Warning", "Failed", "Info"],
                            value="All",
                            label="Status",
                            on_change=lambda e: handle_status_change(e.value),
                        ).classes("flex-1 sm:w-36 bg-white").props("outlined dense")

                        # Export Button
                        async def handle_export():
                            csv_content = await history_service.export_csv()
                            ui.download(csv_content.encode("utf-8"), "smart_water_audit_log.csv")
                            show_toast("Audit history exported to CSV.", "success")

                        ui.button("Export CSV", icon="download", on_click=handle_export).classes(
                            "sw-btn-secondary text-xs px-3 py-1.5 w-full sm:w-auto"
                        )

            # Events Table Container (Horizontal scroll on mobile)
            table_container = ui.card().classes("sw-card p-0 w-full overflow-x-auto mb-6")
            pagination_row = ui.row().classes("w-full flex-col sm:flex-row items-center justify-between py-3 px-4 bg-white border-t border-[#E5E7EB] gap-2")

            async def load_events():
                result = await history_service.get_events(
                    search=search_query,
                    event_type=selected_type if selected_type != "All" else None,
                    status=selected_status if selected_status != "All" else None,
                    page=current_page,
                    page_size=page_size,
                )

                table_container.clear()
                with table_container:
                    with ui.column().classes("min-w-[700px] w-full gap-0"):
                        # Table Headers
                        with ui.row().classes("w-full bg-[#F9FAFB] border-b border-[#E5E7EB] py-3 px-6 text-xs font-bold text-[#6B7280] uppercase tracking-wider"):
                            ui.label("Timestamp").classes("w-36")
                            ui.label("Event Type").classes("w-36")
                            ui.label("Device").classes("w-36")
                            ui.label("Action").classes("w-28")
                            ui.label("Status").classes("w-28")
                            ui.label("Operator").classes("flex-1")

                        items = result["items"]
                        if not items:
                            with ui.column().classes("w-full items-center justify-center py-10 text-center"):
                                ui.icon("find_in_page").classes("text-3xl text-[#D1D5DB] mb-1")
                                ui.label("No matching events found").classes("text-xs text-[#9CA3AF]")
                        else:
                            for item in items:
                                with ui.row().classes(
                                    "w-full border-b border-[#F3F4F6] py-3.5 px-6 items-center text-xs text-[#111827] hover:bg-[#F9FAFB] transition-colors"
                                ):
                                    ui.label(item["timestamp"]).classes("w-36 font-mono text-[#6B7280]")
                                    ui.label(item["event_type"]).classes("w-36 font-semibold")
                                    ui.label(item["device"]).classes("w-36 text-[#2563EB] font-medium")
                                    ui.label(item["action"]).classes("w-28 font-mono")
                                    with ui.element("div").classes("w-28"):
                                        create_status_badge(item["status"], size="sm")
                                    ui.label(item["operator"]).classes("flex-1 text-[#4B5563]")

                    # Pagination Controls
                    pagination_row.clear()
                    with pagination_row:
                        total = result["total"]
                        total_pages = result["total_pages"]
                        ui.label(f"Showing page {current_page} of {total_pages} ({total} events)").classes("text-xs text-[#6B7280]")

                        with ui.row().classes("items-center gap-2"):
                            async def prev_page():
                                nonlocal current_page
                                if current_page > 1:
                                    current_page -= 1
                                    await load_events()

                            async def next_page():
                                nonlocal current_page
                                if current_page < total_pages:
                                    current_page += 1
                                    await load_events()

                            prev_btn = ui.button("Previous", on_click=prev_page).classes("sw-btn-secondary text-xs px-3 py-1")
                            if current_page <= 1:
                                prev_btn.props("disable")

                            next_btn = ui.button("Next", on_click=next_page).classes("sw-btn-secondary text-xs px-3 py-1")
                            if current_page >= total_pages:
                                next_btn.props("disable")

            async def handle_search(val: str):
                nonlocal search_query, current_page
                search_query = val or ""
                current_page = 1
                await load_events()

            async def handle_type_change(val: str):
                nonlocal selected_type, current_page
                selected_type = val
                current_page = 1
                await load_events()

            async def handle_status_change(val: str):
                nonlocal selected_status, current_page
                selected_status = val
                current_page = 1
                await load_events()

            await load_events()
