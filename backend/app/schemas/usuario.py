from pydantic import BaseModel, ConfigDict, Field, EmailStr

class UsuarioBase(BaseModel):
    nombre: str =Field(min_length=1, max_length=100)
    email: EmailStr
    activo: bool= True

class UsuarioCreate(UsuarioBase):
    password: str = Field(min_length=8, description="contraseña en texto plano")
    rol_id: int
class UsuarioUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None
    activo: bool | None = None

class UsuarioPasswordUpdate(BaseModel):
    password : str = Field(min_length=8)

class UsuarioResponse(UsuarioBase):
    id: int
    rol_id: int
   
    model_config = ConfigDict(from_attributes=True)