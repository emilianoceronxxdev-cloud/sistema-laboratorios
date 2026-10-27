from fastapi import FastAPI

from app.routers.laboratorios import router as laboratorios_router
from app.routers.categorias_equipo import router as categorias_equipo_router
from app.routers.equipos import router as equipos_router
from app.routers.especificaciones_equipo import router as especificaciones_equipo_router
from app.routers.roles import router as roles_router

app = FastAPI(
    title="Gestor de Inventario de Laboratorios",
    version="1.0.0",
)

app.include_router(laboratorios_router)
app.include_router(categorias_equipo_router)
app.include_router(equipos_router)
app.include_router(especificaciones_equipo_router)
app.include_router(roles_router)