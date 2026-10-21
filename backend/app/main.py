from fastapi import FastAPI

from app.routers.laboratorios import router as laboratorios_router


app = FastAPI(
    title="Gestor de Inventario de Laboratorios",
    version="1.0.0",
)

app.include_router(laboratorios_router)