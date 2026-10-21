from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from app.database.base import Base

class Permiso(Base):
    __tablename__ = "permisos"

    id: Mapped[int] =mapped_column(primary_key=True)
    nombre :Mapped[str]=mapped_column(String(100), unique=True, nullable=False)
    descripcion : Mapped[str | None]= mapped_column(String(255))