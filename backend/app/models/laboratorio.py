from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean

from app.database.base import Base

class Laboratorio(Base):
    __tablename__ = "laboratorios"

    id : Mapped[int] = mapped_column(primary_key=True)
    nombre : Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    ubicacion : Mapped[str] = mapped_column (String (150),  nullable=False)
    activo : Mapped[bool] = mapped_column(Boolean, nullable=False)
