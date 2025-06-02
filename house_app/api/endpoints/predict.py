from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from house_app.db.database import SessionLocal
from house_app.db.models import HousePredict
from house_app.db.schema import HousePredictSchema
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

predict_router = APIRouter(prefix="/predict", tags=["Predicts"])

BASE_DIR = Path(__file__).resolve().parent.parent
model_path = BASE_DIR / 'house_price_model_job.pkl'
scaler_path = BASE_DIR / 'scaler.pkl'

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@predict_router.post('/create/', response_model=HousePredictSchema)
async def create_predict(predict: HousePredictSchema, db: Session = Depends(get_db)):
    predict_record = HousePredict(**predict.dict())
    db.add(predict_record)
    db.commit()
    db.refresh(predict_record)
    return predict_record


@predict_router.get("/", response_model=List[HousePredictSchema])
async def list_predicts(db: Session = Depends(get_db)):
    return db.query(HousePredict).all()


@predict_router.get("/{predict_id}/", response_model=HousePredictSchema)
async def get_predict(predict_id: int, db: Session = Depends(get_db)):
    predict = db.query(HousePredict).filter(HousePredict.id == predict_id).first()
    if predict is None:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return predict


@predict_router.delete("/{predict_id}/")
async def delete_predict(predict_id: int, db: Session = Depends(get_db)):
    predict = db.query(HousePredict).filter(HousePredict.id == predict_id).first()
    if predict is None:
        raise HTTPException(status_code=404, detail="Prediction not found")
    db.delete(predict)
    db.commit()
    return {"message": "Prediction deleted"}

model_columns = [
    'GrLivArea',
    'YearBuilt',
    'GarageCars',
    'TotalBsmtSF',
    'FullBath',
    'OverallQual'
]


@predict_router.post('/predict/')
async def delete_predict(house: HousePredictSchema, db: Session = Depends(get_db)):
    input_data = {
        'GrLivArea': house.area,
        'YearBuilt': house.year,
        'GarageCars': house.garage,
        'TotalBsmtSF': house.total_basement,
        'FullBath': house.bath,
        'OverallQual': house.overall_quality
    }
    input_df = pd.DataFrame([input_data])
    scaled_df = scaler.transform(input_df)
    predicted_price = model.predict(scaled_df)[0]
    return {'predicted_price': round(predicted_price)}
