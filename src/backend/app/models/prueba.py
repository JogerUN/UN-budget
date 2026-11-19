from datetime import date
from sqlalchemy import String, Date, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# Tabla 'item' de prueba
class Item(DeclarativeBase):
    __tablename__ = "item"

    id: Mapped[int] = mapped_column(primary_key=True)
    item: Mapped[str] = mapped_column(String(255))
    fecha: Mapped[date] = mapped_column(Date, server_default=func.current_date())
