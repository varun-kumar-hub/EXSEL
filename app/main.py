from fastapi import FastAPI
from nicegui import app as nicegui_app, ui
from app.config.settings import settings
from app.core.logging_config import setup_logging
from app.api.router import api_router
from app.ui.pages import register_all_pages


def create_application() -> FastAPI:
    """
    Initialize FastAPI + NiceGUI Application Shell
    Mounts REST API routers and registers all NiceGUI UI screens.
    """
    setup_logging()

    # Mount REST API
    nicegui_app.include_router(api_router)

    # Register all NiceGUI Pages
    register_all_pages()

    return nicegui_app


app = create_application()


def run():
    """Application Development Server Launcher"""
    ui.run(
        title=settings.APP_NAME,
        host=settings.HOST,
        port=settings.PORT,
        reload=False,
        show=False,
        storage_secret=settings.SECRET_KEY,
    )


if __name__ == "__main__":
    run()
