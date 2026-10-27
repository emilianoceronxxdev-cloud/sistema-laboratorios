from pydantic import BaseModel, ConfigDict, Field

class PermisoBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    descripcion: str = Field(min_length=1,max_length=255)

class PermisoCreate(PermisoBase):
    pass

class PermisoUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=100)
    descripcion: str | None = Field(default=None, min_length=1,max_length=255)

class PermisoResponse(PermisoBase):
    id:int

    model_config = ConfigDict(from_attributes=True)