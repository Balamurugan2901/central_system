from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.database.crud import init_db
from app.api.client_routes import router as client_router
from app.intrusion.intrusion_routes import router as intrusion_router
from app.api import auth_routes, admin_routes, ws_routes, block_routes
import os

app = FastAPI(title="Central Security Server")

# CORS — allow dashboard requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ──────────────────────────────────────────────────────────────────
app.include_router(ws_routes.router)
app.include_router(admin_routes.router)
app.include_router(client_router)
app.include_router(intrusion_router)
app.include_router(auth_routes.router)
app.include_router(block_routes.router)

# ── Startup ───────────────────────────────────────────────────────────────────
@app.on_event("startup")
def startup():
    init_db()

# ── Serve dashboard HTML files ────────────────────────────────────────────────
DASHBOARD_DIR = os.path.join(os.path.dirname(__file__), "..", "dashboard")

@app.get("/", include_in_schema=False)
def root():
    """Redirect root to the admin login page."""
    return FileResponse(os.path.join(DASHBOARD_DIR, "login.html"))

@app.get("/login", include_in_schema=False)
def login_page():
    return FileResponse(os.path.join(DASHBOARD_DIR, "login.html"))

@app.get("/dashboard", include_in_schema=False)
def dashboard_page():
    return FileResponse(os.path.join(DASHBOARD_DIR, "index.html"))

@app.get("/test")
def test():
    return {"status": "ok"}