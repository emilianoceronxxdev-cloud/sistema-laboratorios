from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base

class RolPermiso(Base):
    __tablename__ = "rol_permisos"

    rol_id:Mapped[int] = mapped_column(
        ForeignKey ("roles.id"),
        primary_key=True
    )

    permiso_id : Mapped[int] = mapped_column(
        ForeignKey ("permisos.id"),
        primary_key=True
    )