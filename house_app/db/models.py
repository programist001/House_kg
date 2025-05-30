from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from house_app.db.database import Base
from typing import Optional


class HousePredict(Base):
    __tablename__ = "house_records"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    GrLivArea: Mapped[int] = mapped_column(Integer)
    YearBuilt: Mapped[int] = mapped_column(Integer)
    GarageCars: Mapped[int] = mapped_column(Integer)
    TotalBsmtSF: Mapped[int] = mapped_column(Integer)
    FullBath: Mapped[int] = mapped_column(Integer)
    OverallQual: Mapped[int] = mapped_column(Integer)
    Neighborhood: Mapped[str] = mapped_column(String(50))
    predicted_price: Mapped[Optional[float]] = mapped_column(nullable=True)
