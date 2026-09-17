import sys
import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

# Ensure root directory is on Python path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from app.api.router import api_router
from app.core.logging_config import setup_logging

setup_logging()

# Serverless FastAPI Application
app = FastAPI(
    title="Smart Water Distribution & Sequential Control System",
    description="Industrial Water Network Telemetry & Gate Actuation API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount REST API
app.include_router(api_router)

# Read static HTML template
HTML_FILE_PATH = os.path.join(root_dir, "static", "index.html")


def get_html_content() -> str:
    try:
        with open(HTML_FILE_PATH, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"<h1>Smart Water System</h1><p>Error reading UI template: {e}</p>"


# Serve complete web interface for all primary client routes
@app.get("/", response_class=HTMLResponse)
@app.get("/dashboard", response_class=HTMLResponse)
@app.get("/water-gates", response_class=HTMLResponse)
@app.get("/distribution", response_class=HTMLResponse)
@app.get("/sensors", response_class=HTMLResponse)
@app.get("/analytics", response_class=HTMLResponse)
@app.get("/history", response_class=HTMLResponse)
@app.get("/settings", response_class=HTMLResponse)
@app.get("/login", response_class=HTMLResponse)
@app.get("/signup", response_class=HTMLResponse)
async def serve_ui():
    return HTMLResponse(content=get_html_content(), status_code=200)
