from sqlalchemy import  String, ForeignKey, Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from enum import Enum as PyEnum
from sqlalchemy import Enum as SQLEnum
from datetime import datetime

from app.database.base import Base

class EstadoEquipo(PyEnum):
    ACTIVO = "activo"
    REPARACION = "en reparacion"
    DADO_BAJA = "dado de baja"
    PRESTADO = "prestado"

class Equipo(Base):
    __tablename__ = "equipos"

    id: Mapped[int] = mapped_column(primary_key=True)
    marca : Mapped[str] = mapped_column(String(100), nullable=False)
    modelo:Mapped[str]=mapped_column(String(100), nullable=False)
    numero_serie:Mapped[str]=mapped_column(String(100), unique=True, nullable=False)
    estado:Mapped[EstadoEquipo]=mapped_column(SQLEnum(EstadoEquipo, name="estado_equipo"),nullable=False, default=EstadoEquipo.ACTIVO)
    fecha_adquisicion:Mapped[Date] =mapped_column(Date, nullable=False)
    fecha_registro:Mapped[DateTime]=mapped_column(DateTime, nullable=False,default=datetime.now)
    fecha_actualizacion : Mapped[DateTime]=mapped_column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    laboratorio_id:Mapped[int] = mapped_column(ForeignKey ("laboratorios.id"), nullable=False)

    categoria_equipo_id:Mapped[int]= mapped_column(ForeignKey ("categoria_equipo.id"),nullable=False)
