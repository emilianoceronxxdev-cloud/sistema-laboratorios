from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean

from app.database.base import Base

class CategoriaEquipo(Base):
    __tablename__ = "categoria_equipo"

    id:Mapped[int] = mapped_column(primary_key=True)
    nombre : Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    descripcion : Mapped[str | None] = mapped_column(String(255))
    activo : Mapped[bool] = mapped_column(Boolean, nullable=False )
