from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class HousePredictSchema(BaseModel):
    id: int
    area: int
    year: int
    garage: int
    total_basement: int
    bath: int
    overall_quality: int
    neighborhood: str
    price: Optional[float] = None

    class Config:
        from_attributes = True
