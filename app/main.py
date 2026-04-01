from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.infrastructure.api.routes import router as api_router
from app.infrastructure.web.web_routes import router as web_router
from app.infrastructure.repositories.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

# ✅ WEB (HTML)
app.include_router(web_router)

# ✅ API (POST, PUT, DELETE)
app.include_router(api_router)

app.mount("/static", StaticFiles(directory="app/infrastructure/web/static"), name="static")