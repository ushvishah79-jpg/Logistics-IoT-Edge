from fastapi import FastAPI, Depends, HTTPException         
from sqlalchemy.orm import Session                           
from app.database import engine, Base, get_db                
from app import models, schemas                               

Base.metadata.create_all(bind=engine)

app = FastAPI(title="OTA Firmware Update Server")

@app.get("/")
def root():
    return {"message": "OTA Firmware Update Server is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/firmware/register", response_model=schemas.FirmwareReleaseOut)
def register_firmware(manifest: schemas.FirmwareManifest, db: Session = Depends(get_db)):
    firmware = models.FirmwareRelease(
        version=manifest.version,
        build_number=manifest.build_number,
        sha256_hash=manifest.sha256_hash,
        signature_hex=manifest.signature_hex,
        file_path=f"firmware_storage/{manifest.version}.bin"
    )
    db.add(firmware)
    db.commit()
    db.refresh(firmware)
    return firmware

@app.get("/firmware/latest", response_model=schemas.FirmwareReleaseOut)
def get_latest_firmware(db: Session = Depends(get_db)):
    firmware = db.query(models.FirmwareRelease).order_by(models.FirmwareRelease.build_number.desc()).first()
    if not firmware:
        raise HTTPException(status_code=404, detail="No firmware releases found")
    return firmware

@app.get("/firmware/all", response_model=list[schemas.FirmwareReleaseOut])
def list_firmware(db: Session = Depends(get_db)):
    return db.query(models.FirmwareRelease).all()

@app.post("/devices/register", response_model=schemas.DeviceOut)
def register_device(device: schemas.DeviceRegister, db: Session = Depends(get_db)):
    existing = db.query(models.Device).filter(models.Device.device_id == device.device_id).first()
    if existing:
        return existing
    new_device = models.Device(device_id=device.device_id, current_build_number=0)
    db.add(new_device)
    db.commit()
    db.refresh(new_device)
    return new_device