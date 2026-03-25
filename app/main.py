from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.infrastructure.api.routes import router as api_router
from app.infrastructure.web.web_routes import router as web_router
from app.infrastructure.repositories.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Rutas WEB (HTML)
app.include_router(web_router)

# Rutas API (JSON)
app.include_router(api_router, prefix="/api")

app.mount("/static", StaticFiles(directory="app/infrastructure/web/static"), name="static")