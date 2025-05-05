# app/routers/predict.py

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import uuid
import os

from app.ml_model import predict_fracture
from app.token import get_current_user
from app import models, database

router = APIRouter(
    prefix="/predict",
    tags=["Prediction"],
)


# Dependency to get a DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/fracture")
async def predict_fracture_route(
    file: UploadFile = File(...),
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Receive an X-ray image, run the fracture model, save both the upload
    and its prediction in the DB, and return label + confidence.
    """
    try:
        # read image bytes
        image_bytes = await file.read()

        # run inference
        probability = predict_fracture(image_bytes)
        label = "fractured" if probability > 0.5 else "not fractured"

        # ensure uploads folder exists
        os.makedirs("uploads", exist_ok=True)

        # save the raw upload
        filename = f"{uuid.uuid4()}.png"
        file_path = os.path.join("uploads", filename)
        with open(file_path, "wb") as out_file:
            out_file.write(image_bytes)

        # record in database
        record = models.Prediction(
            user_id=user_id,
            image_filename=filename,
            prediction_result=label,
            confidence_score=probability,
        )
        db.add(record)
        db.commit()
        db.refresh(record)

        return {
            "label": label,
            "confidence": round(probability, 4),
            "image_filename": filename,
        }

    except Exception as e:
        # any uncaught error becomes a 500
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")
