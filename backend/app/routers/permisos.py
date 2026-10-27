from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.rol_permiso import RolPermiso

from app.database.dependencies import get_db
from app.models import Permiso
from app.schemas.permiso import PermisoResponse, PermisoCreate, PermisoUpdate

router = APIRouter(
    prefix="/permisos",
    tags=["Permisos"]
)

@router.get("/",response_model=list[PermisoResponse])
def listar_permisos(db: Session = Depends(get_db)):
    consulta = select(Permiso).order_by(Permiso.id.asc())
    resultado = db.execute(consulta)
    permisos = resultado.scalars().all()

    return permisos

@router.post("/",response_model=PermisoResponse)
def crear_permiso(permiso:PermisoCreate, db: Session = Depends(get_db)):

    permiso_existente = db.query(Permiso).filter(Permiso.nombre == permiso.nombre).first()
    if permiso_existente:
        raise HTTPException(status_code=409, detail="El permiso ya existe")

    nuevo_permiso = Permiso(**permiso.model_dump())
    db.add(nuevo_permiso)
    db.commit()
    db.refresh(nuevo_permiso)

    return nuevo_permiso

@router.get("/{permiso_id}",response_model=PermisoResponse)
def obtener_permiso(permiso_id: int, db: Session = Depends(get_db)):
    consulta = select(Permiso).where(Permiso.id == permiso_id)
    resultado = db.execute(consulta)
    rol = resultado.scalar_one_or_none()

    if rol is None:
        raise HTTPException(status_code=404, detail="El permiso no fue encontrado")

    return rol

@router.put("/{permiso_id}",response_model=PermisoResponse)
def actualizar_permiso(permiso_id:int, datos: PermisoUpdate, db: Session = Depends(get_db)):
    permiso_actualizado= db.get(Permiso, permiso_id)

    if permiso_actualizado is None:
        raise HTTPException(status_code=404, detail="No se puedo encontrar el permiso")

    datos_nuevos= datos.model_dump(exclude_unset=True)
    for clave,valor in datos_nuevos.items():
        setattr(permiso_actualizado, clave, valor)

    db.commit()
    db.refresh(permiso_actualizado)

    return permiso_actualizado

@router.delete("/{permiso_id}")
def eliminar_permiso(permiso_id:int, db: Session = Depends(get_db)):
    permiso_eliminado= db.get(Permiso, permiso_id)

    if permiso_eliminado is None:
        raise HTTPException(status_code=404, detail="El permiso no fue encontrado")

    consulta = select(RolPermiso).where(RolPermiso.permiso_id == permiso_id)
    resultado = db.execute(consulta)
    relacion = resultado.scalars().first()

    if relacion is not None:
        raise HTTPException(status_code=409, detail="No se puede eliminar el permiso por que esta asignado a uno o mas roles")
    db.delete(permiso_eliminado)
    db.commit()

    return {"mensaje": "Permiso eliminado correctamente"}