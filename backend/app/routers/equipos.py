from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.models import Equipo
from app.schemas.equipo import EquipoCreate, EquipoResponse, EquipoUpdate

router = APIRouter(
    prefix="/equipos",
    tags=["Equipos"])

@router.get("/", response_model= list [EquipoResponse])
def listar_equipos(db:Session=Depends(get_db)):
    consulta = select(Equipo)
    resultado = db.execute(consulta)
    equipos=resultado.scalars().all()

    return equipos

@router.post("/", response_model=EquipoResponse)
def crear_equipo(equipo: EquipoCreate, db:Session=Depends(get_db)):
    equipo_existente = db.query(Equipo).filter(Equipo.numero_serie == equipo.numero_serie).first()
    if equipo_existente:
        raise HTTPException(status_code=409,detail="El equipo ya existe")

    nuevo_equipo = Equipo(**equipo.model_dump())
    db.add(nuevo_equipo)
    db.commit()
    db.refresh(nuevo_equipo)

    return nuevo_equipo

@router.put("/{equipo_id}",response_model=EquipoResponse)
def actualizar_equipo(equipo_id:int, datos:EquipoUpdate, db:Session=Depends(get_db)):
    equipo_actualizado= db.get(Equipo, equipo_id)

    if equipo_actualizado is None:
        raise HTTPException(status_code=404, detail="no se pudo encontrar el equiupo")

    datos_nuevos = datos.model_dump(exclude_unset=True)
    for clave, valor in datos_nuevos.items():
        setattr(equipo_actualizado,clave,valor)

    db.commit()
    db.refresh(equipo_actualizado)

    return equipo_actualizado

@router.delete("/{equipo_id}")
def eliminar_equipo(equipo_id:int, db:Session=Depends(get_db)):
    equipo_eliminado=db.get(Equipo, equipo_id)

    if equipo_eliminado is None:
        raise HTTPException(status_code=404, detail="El equipo no fue encontrado")

    db.delete(equipo_eliminado)
    db.commit()

    return{"mensaje" : "Equipo eliminado con exito"}