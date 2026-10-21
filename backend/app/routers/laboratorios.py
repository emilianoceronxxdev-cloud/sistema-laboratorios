
from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.models import Laboratorio
from app.schemas.laboratorio import LaboratorioResponse,LaboratorioCreate,LaboratorioUpdate


router = APIRouter(
    prefix="/laboratorios",
    tags=["Laboratorios"]
)

@router.get("/",response_model=list[LaboratorioResponse])
def listar_laboratorios(db:Session= Depends(get_db)):
    consulta = select(Laboratorio)
    resultado = db.execute(consulta)
    laboratorios = resultado.scalars().all()

    return laboratorios


@router.post ("/",response_model=LaboratorioResponse)
def crear_laboratorio(laboratorio : LaboratorioCreate, db: Session =Depends(get_db)):

    laboratorio_existente = db.query(Laboratorio).filter(Laboratorio.nombre == laboratorio.nombre).first()
    if laboratorio_existente :
        raise HTTPException(status_code=409, detail="El laboratorio ya existe")

    nuevo_laboratorio = Laboratorio(**laboratorio.model_dump())
    db.add(nuevo_laboratorio)
    db.commit()
    db.refresh(nuevo_laboratorio)

    return nuevo_laboratorio

@router.put("/{laboratorio_id}", response_model=LaboratorioResponse)
def actualizar_laboratorio(laboratorio_id: int, datos: LaboratorioUpdate, db : Session =Depends(get_db)):
    laboratorio_actualizado = db.get(Laboratorio, laboratorio_id )

    if laboratorio_actualizado is None:
        raise HTTPException(status_code=404, detail="No se pudo encontrar el laboratorio")

    datos_nuevos = datos.model_dump(exclude_unset=True)
    for clave,valor in datos_nuevos.items():
        setattr(laboratorio_actualizado,clave,valor)

    db.commit()
    db.refresh(laboratorio_actualizado)

    return laboratorio_actualizado


@router.delete("/{laboratorio_id}")
def eliminar_laboratorio(laboratorio_id:int, db : Session = Depends(get_db)):
    laboratorio_eliminado = db.get(Laboratorio, laboratorio_id)

    if laboratorio_eliminado is None:
        raise HTTPException(status_code=404, detail="El laboratorio no existe")

    db.delete(laboratorio_eliminado)
    db.commit()

    return {"mensaje": "Laboratorio Eliminado con exito"}
