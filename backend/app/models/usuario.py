from sqlalchemy import ForeignKey, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre : Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    email : Mapped [str]= mapped_column(String(100), unique=True, nullable=False)
    password_hash : Mapped[str]=mapped_column(String(255), nullable=False)
    activo : Mapped[bool]=mapped_column(Boolean,  nullable=False)




    rol_id :Mapped[int] = mapped_column (
        ForeignKey ("roles.id"),
        nullable=False
    )