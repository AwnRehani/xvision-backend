from fastapi import FastAPI
from app.routers import auth, upload

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "XVision backend is running!"}

# Register all routers
app.include_router(auth.router)
app.include_router(upload.router)
