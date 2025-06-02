from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from house_app.db.database import Base
from typing import Optional


class HousePredict(Base):
    __tablename__ = "house_records"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    area: Mapped[int] = mapped_column(Integer)
    year: Mapped[int] = mapped_column(Integer)
    garage: Mapped[int] = mapped_column(Integer)
    total_basement: Mapped[int] = mapped_column(Integer)
    bath: Mapped[int] = mapped_column(Integer)
    overall_quality: Mapped[int] = mapped_column(Integer)
    neighborhood: Mapped[str] = mapped_column(String(50))
    price: Mapped[Optional[float]] = mapped_column(nullable=True)
