from pydantic import BaseModel, ConfigDict, Field

class LaboratorioBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    ubicacion: str = Field(min_length=1, max_length=150)
    activo: bool = True

class LaboratorioCreate(LaboratorioBase):
    pass

class LaboratorioUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=100)
    ubicacion: str | None = Field(default=None, min_length=1, max_length=150)
    activo: bool | None = None


class LaboratorioResponse(LaboratorioBase):
    id: int

    model_config = ConfigDict(from_attributes=True)