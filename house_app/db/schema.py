from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class HousePredictSchema(BaseModel):
    GrLivArea: int
    YearBuilt: int
    GarageCars: int
    TotalBsmtSF: int
    FullBath: int
    OverallQual: int
    Neighborhood: str
    predicted_price: Optional[float] = None

    class Config:
        from_attributes = True
