from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.infrastructure.api.routes import router
from app.infrastructure.repositories.database import engine, Base
from app.infrastructure.web.web_routes import router as web_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(web_router)
app.mount("/static", StaticFiles(directory="app/infrastructure/web/static"), name="static")

