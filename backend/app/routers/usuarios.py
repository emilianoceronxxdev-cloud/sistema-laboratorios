from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from pwdlib import PasswordHash

from app.database.dependencies import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, UsuarioUpdate, UsuarioPasswordUpdate
from app.models import Rol

password_hash = PasswordHash.recommended()

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

@router.get("/", response_model =list[UsuarioResponse])
def obtener_usuarios(db: Session = Depends(get_db)):
    consulta = select(Usuario)
    resultado = db.execute(consulta)
    usuarios = resultado.scalars().all()

    return usuarios


@router.post("/", response_model=UsuarioResponse)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    
    rol_existente =db.get(Rol, usuario.rol_id)

    if rol_existente is None:
        raise HTTPException(status_code=404, detail="El rol seleccionado no existe")

    consulta = select(Usuario).where(Usuario.email == usuario.email)

    resultado = db.execute(consulta)
    usuario_existente = resultado.scalar_one_or_none()

    if usuario_existente:
        raise HTTPException(status_code=409, detail="El usuario ya existe")

    hashed_password = password_hash.hash(usuario.password)
    
    nuevo_usuario = Usuario(
        nombre = usuario.nombre,
        email = usuario.email,
        password_hash=hashed_password,
        activo=usuario.activo,
        rol_id = usuario.rol_id
    ) 

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return nuevo_usuario

@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario(usuario_id : int, db: Session = Depends(get_db)):
    consulta = select(Usuario).where(Usuario.id == usuario_id)
    resultado = db.execute(consulta)
    usuario = resultado.scalar_one_or_none()

    if usuario is None:
        raise HTTPException(status_code=404, detail="El usuario no existe")

    return usuario


@router.put("/{usuario_id}", response_model=UsuarioResponse)
def actualizar_usuario(usuario_id: int, datos: UsuarioUpdate,  db: Session = Depends(get_db)):
    usuario_actualizado = db.get(Usuario, usuario_id)

    if usuario_actualizado is None:
        raise HTTPException(status_code=404, detail="El usuario no existe")

    datos_nuevos= datos.model_dump(exclude_unset=True)
    for clave, valor in datos_nuevos.items():
        setattr(usuario_actualizado, clave, valor)

    db.commit()
    db.refresh(usuario_actualizado)

    return usuario_actualizado

@router.put("/{usuario_id}/password")
def actualizar_contraseña(usuario_id: int, datos: UsuarioPasswordUpdate, db: Session = Depends(get_db)):
    usuario= db.get(Usuario, usuario_id)
    
    if usuario is None:
        raise HTTPException(status_code=404, detail="El usuario no existe")

    hashed_password = password_hash.hash(datos.password)
    usuario.password_hash = hashed_password

    db.commit()
    db.refresh(usuario)

    return {"mensaje":"Contraseña actualizada con exito"}

@router.delete("/{usuario_id}")
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario_eliminado = db.get(Usuario, usuario_id)

    if usuario_eliminado is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado ")

    db.delete(usuario_eliminado)
    db.commit()

    return{"mensaje":"Usuario eliminado con exito"}   
