from sqlalchemy import Column, Integer, String
from .database import Base
from sqlalchemy import ForeignKey, DateTime, Float
from sqlalchemy.sql import func

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    image_filename = Column(String, unique=True, index=True)
    prediction_result = Column(String)  # e.g., "fractured" or "not fractured"
    confidence_score = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)