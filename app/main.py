from fastapi import FastAPI
from app.database.crud import init_db
from app.api.client_routes import router as client_router
from app.intrusion.intrusion_routes import router as intrusion_router
from fastapi import FastAPI
from app.api import auth_routes, admin_routes
from app.api import admin_routes
from app.api import ws_routes




app = FastAPI(title="Central Security Server")
app.include_router(ws_routes.router)
app.include_router(admin_routes.router)

@app.on_event("startup")
def startup():
    init_db()

app.include_router(client_router)
app.include_router(intrusion_router)
app.include_router(auth_routes.router)
app.include_router(admin_routes.router)


@app.get("/")
def root():
    return {"message": "Central Server Fully Running 🚀"}
