from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, ForeignKey, UniqueConstraint

from app.database.base import Base

class EspecificacionEquipo(Base):
    __tablename__ = "especificaciones_equipo"

    id:Mapped[int] = mapped_column(primary_key=True)
    clave:Mapped[str] = mapped_column(String(50), nullable=False)
    valor:Mapped[str] = mapped_column(String(150), nullable=False)

    equipo_id:Mapped[int]=mapped_column(ForeignKey("equipos.id", ondelete="CASCADE"), nullable=False)

    __table_args__ =(
        UniqueConstraint("equipo_id", "clave"),
    )