from fastapi import APIRouter, HTTPException, Depends,status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.models import EspecificacionEquipo
from app.schemas.especificacion_equipo import EspecificacionEquipoCreate, EspecificacionEquipoResponse, EspecificacionEquipoUpdate

router = APIRouter(
    prefix="/especificaciones-equipo",
    tags=["Especificaciones de equipo"]
)

@router.get("/", response_model=list[EspecificacionEquipoResponse])
def listar_especificaciones_equipo(db: Session  =Depends(get_db)):
    consulta=select(EspecificacionEquipo)
    resultado = db.execute(consulta)
    especificaciones_equipo = resultado.scalars().all()

    return especificaciones_equipo

@router.post("/", response_model=EspecificacionEquipoResponse)
def crear_especificacion_equipo(especificacion_equipo: EspecificacionEquipoCreate, db: Session = Depends(get_db)):

    especificacion_equipo_existente = db.query(EspecificacionEquipo).filter(EspecificacionEquipo.clave == especificacion_equipo.clave, EspecificacionEquipo.equipo_id == especificacion_equipo.equipo_id).first()

    if especificacion_equipo_existente:
        raise HTTPException(status_code=409, detail="La especificacion del equipo ya existe")

    nueva_especificacion_equipo = EspecificacionEquipo(**especificacion_equipo.model_dump())
    db.add(nueva_especificacion_equipo)
    db.commit()
    db.refresh(nueva_especificacion_equipo)

    return nueva_especificacion_equipo

@router.get("/{especificacion_equipo_id}",response_model=EspecificacionEquipoResponse)
def obtener_especificacion_equipo(especificacion_equipo_id : int, db: Session = Depends(get_db)):
    consulta = select(EspecificacionEquipo).where(EspecificacionEquipo.id == especificacion_equipo_id)
    resultado = db.execute(consulta)
    especificacion_equipo = resultado.scalar_one_or_none()

    if not especificacion_equipo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Especificación de equipo no encontrada")

    return especificacion_equipo

@router.put("/{especificacion_equipo_id}",response_model=EspecificacionEquipoResponse)
def actualizar_especificacion_equipo(especificacion_equipo_id:int, datos:EspecificacionEquipoUpdate,db: Session = Depends(get_db)):
    especificacion_equipo_actualizado=db.get(EspecificacionEquipo, especificacion_equipo_id)

    if especificacion_equipo_actualizado is None:
        raise HTTPException (status_code=404,detail="No se puedo encontrar la especificacion del equipo")

    datos_nuevos= datos.model_dump(exclude_unset=True)
    for clave,valor in datos_nuevos.items():
        setattr(especificacion_equipo_actualizado,clave,valor)

    db.commit()
    db.refresh(especificacion_equipo_actualizado)

    return(especificacion_equipo_actualizado)

@router.delete("/{especificacion_equipo_id}")
def eliminar_especificacion_equipo(especificacion_equipo_id:int, db: Session = Depends(get_db)):
    especificacion_equipo_eliminada=db.get(EspecificacionEquipo, especificacion_equipo_id)

    if especificacion_equipo_eliminada is None:
        raise HTTPException(status_code=404, detail="La especificacion del equipo no exste")

    db.delete(especificacion_equipo_eliminada)
    db.commit()

    return {"mensaje":"Especificacion del equipo eliminada correctamente"}