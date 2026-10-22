from pydantic import BaseModel, ConfigDict, Field

class CategoriaEquipoBase(BaseModel):
    nombre : str = Field(min_length=1, max_length=100)
    descripcion : str | None = Field(default=None, max_length=150)
    activo : bool = True

class CategoriaEquipoCreate(CategoriaEquipoBase):
    pass

class CategoriaEquipoUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=100)
    descripcion: str | None = Field(default=None, min_length=1, max_length=150)
    activo: bool | None = None

class CategoriaEquipoResponse(CategoriaEquipoBase):
    id:int

    model_config = ConfigDict(from_attributes=True)
