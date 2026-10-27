from fastapi import APIRouter,HTTPException,Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.models import Rol
from app.schemas.rol import RolCreate, RolResponse, RolUpdate

router = APIRouter(
    prefix="/roles",
    tags=["Roles"]
)

@router.get("/", response_model= list[RolResponse])
def listar_roles(db: Session = Depends(get_db)):
    consulta = select(Rol)
    resultado = db.execute(consulta)
    roles= resultado.scalars().all()

    return roles

@router.post("/",response_model=RolResponse)
def crear_rol(rol:RolCreate, db: Session = Depends(get_db)):
    rol_existente = db.query(Rol).filter(Rol.nombre == rol.nombre).first()
    
    if rol_existente:
        raise HTTPException (status_code=409, detail="El rol ya exisate")

    nuevo_rol= Rol(**rol.model_dump())
    db.add(nuevo_rol)
    db.commit()
    db.refresh(nuevo_rol)

    return nuevo_rol

@router.get("/{rol_id}", response_model=RolResponse)
def obtener_rol(rol_id:int, db: Session = Depends(get_db)):
    consulta= select(Rol).where(Rol.id == rol_id)
    resultado = db.execute(consulta)
    rol = resultado.scalar_one_or_none()

    if rol is None:
        raise HTTPException(status_code=404, detail="Rol no encontrado")

    return rol

@router.put("/{rol_id}",response_model=RolResponse)
def actualizar_rol(rol_id: int, datos:RolUpdate, db: Session = Depends(get_db)):
    rol_actualizado= db.get(Rol, rol_id)

    if rol_actualizado is None:
        raise HTTPException(status_code=404, detail="Nose encontro ningun rol")

    datos_nuevos=datos.model_dump(exclude_unset=True)
    for clave, valor in datos_nuevos.items():
        setattr(rol_actualizado, clave, valor)

    db.commit()
    db.refresh(rol_actualizado)

    return rol_actualizado

@router.delete("/{rol_id}")
def eliminar_rol(rol_id:int, db: Session = Depends(get_db)):
    rol_eliminado= db.get(Rol, rol_id)

    if rol_eliminado is None:
        raise HTTPException(status_code=404, detail="El rol no fue encontrado")

    db.delete(rol_eliminado)
    db.commit()

    return {"mensaje":"Rol eliminado correctamente"}