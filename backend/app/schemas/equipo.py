from pydantic import BaseModel, ConfigDict, Field
from app.models.equipo import EstadoEquipo
from datetime import date, datetime

class EquipoBase(BaseModel):
    marca: str = Field(min_length=1, max_length=100)
    modelo: str = Field(min_length=1, max_length=100)
    numero_serie: str = Field(min_length=1, max_length=100)
    estado: EstadoEquipo = EstadoEquipo.ACTIVO
    fecha_adquisicion: date
    laboratorio_id : int
    categoria_equipo_id: int

class EquipoCreate(EquipoBase):
    pass

class EquipoUpdate(BaseModel):
    marca: str | None = Field(default= None, min_length=1, max_length=100)
    modelo: str | None = Field(default= None, min_length=1, max_length=100)
    numero_serie: str | None = Field(default= None, min_length=1, max_length=100)
    estado: EstadoEquipo | None = None
    fecha_adquisicion: date | None = None
    laboratorio_id : int | None = None
    categoria_equipo_id: int | None = None

class EquipoResponse(EquipoBase):
    id: int
    fecha_registro: datetime
    fecha_actualizacion: datetime

    model_config= ConfigDict(from_attributes=True)

