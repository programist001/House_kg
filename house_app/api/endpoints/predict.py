from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from house_app.db.database import SessionLocal
from house_app.db.models import HousePredict
from house_app.db.schema import HousePredictSchema

predict_router = APIRouter(prefix="/predict", tags=["Predicts"])


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