from pydantic import BaseModel, ConfigDict, Field

class EspecificacionEquipo(BaseModel):
    clave: str = Field(min_length=1, max_length=100)
    valor: str = Field(min_length=1,max_length=100)
    equipo_id: int

class EspecificacionEquipoCreate(EspecificacionEquipo):
    pass

class EspecificacionEquipoUpdate(BaseModel):
    clave: str | None= Field(default=None, min_length=1, max_length=100)
    valor: str | None= Field(default=None, min_length=1,max_length=100)
    equipo_id: int | None = None

class EspecificacionEquipoResponse(EspecificacionEquipo):
    id:int

    model_config = ConfigDict(from_attributes=True)
