from pydantic import BaseModel,ConfigDict, Field

class RolBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=50)

class RolCreate(RolBase):
    pass

class RolUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=50 )

class RolResponse(RolBase):
    id: int

    model_config = ConfigDict(from_attributes=True)