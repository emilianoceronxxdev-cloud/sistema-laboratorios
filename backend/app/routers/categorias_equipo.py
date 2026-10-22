from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.models import CategoriaEquipo
from app.schemas.categoria_equipo import CategoriaEquipoResponse, CategoriaEquipoUpdate, CategoriaEquipoCreate

router = APIRouter(
    prefix="/categorias-equipo",
    tags=["Categorías de equipo"]
)

@router.get("/", response_model=list[CategoriaEquipoResponse])
def listar_categorias_equipo(db:Session=Depends(get_db)):
    consulta = select(CategoriaEquipo)
    resultado= db.execute(consulta)
    categorias_equipo = resultado.scalars().all()

    return categorias_equipo

@router.post("/",response_model=CategoriaEquipoResponse)
def crear_categoria_equipo (categoria_equipo : CategoriaEquipoCreate, db:Session=Depends(get_db)):
    categoria_equipo_existente = db.query(CategoriaEquipo).filter(CategoriaEquipo.nombre == categoria_equipo.nombre).first()
    if categoria_equipo_existente:
        raise HTTPException(status_code=409, detail="esta categoria ya existe")

    nueva_categoria_equipo = CategoriaEquipo(**categoria_equipo.model_dump())
    db.add(nueva_categoria_equipo)
    db.commit()
    db.refresh(nueva_categoria_equipo)

    return nueva_categoria_equipo

@router.put("/{categoria_equipo_id}", response_model=CategoriaEquipoResponse)
def actualizar_categoria_equipo(categoria_equipo_id:int, datos:CategoriaEquipoUpdate,db:Session=Depends(get_db)):
    categoria_equipo_actualizada=db.get(CategoriaEquipo,categoria_equipo_id)
    if categoria_equipo_actualizada is None:
        raise HTTPException(status_code=404, detail="no se puedo encontrar la categoria del equipo")

    datos_nuevos=datos.model_dump(exclude_unset=True)
    for clave, valor in datos_nuevos.items():
        setattr(categoria_equipo_actualizada,clave,valor)

    db.commit()
    db.refresh(categoria_equipo_actualizada)

    return categoria_equipo_actualizada

@router.delete("/{categoria_equipo_id}", response_model=CategoriaEquipoResponse)
def eliminar_categoria_equipo(categoria_equipo_id: int, db:Session=Depends(get_db)):
    categoria_equipo_eliminado = db.get(CategoriaEquipo, categoria_equipo_id)
    if categoria_equipo_eliminado is None:
        raise HTTPException(status_code=404, detail="la categoria del equipo no existe")

    db.delete(categoria_equipo_eliminado)
    db.commit()

    return categoria_equipo_eliminado
