from fastapi import FastAPI
from app.database import Base, engine
from app.routers import auth, upload, predict   # these are APIRouter instances

# create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "XVision backend is running!"}

# since auth, upload, predict *are* routers already:
app.include_router(auth,    prefix="/auth",    tags=["Auth"])
app.include_router(upload,  prefix="/upload",  tags=["Upload"])
app.include_router(predict, prefix="/predict", tags=["Prediction"])
