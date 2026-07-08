from fastapi import FastAPI
from app.database import engine, Base
from app import models  # important: import so SQLAlchemy sees the model classes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="OTA Firmware Update Server")

@app.get("/")
def root():
    return {"message": "OTA Firmware Update Server is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}