from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app import models, schemas
import os

Base.metadata.create_all(bind=engine)

app = FastAPI(title="OTA Firmware Update Server")

FIRMWARE_DIR = "firmware_storage"
os.makedirs(FIRMWARE_DIR, exist_ok=True)

@app.get("/")
def root():
    return {"message": "OTA Firmware Update Server is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/firmware/upload", response_model=schemas.FirmwareReleaseOut)
async def upload_firmware(
    version: str = Form(...),
    build_number: int = Form(...),
    sha256_hash: str = Form(...),
    signature_hex: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    file_path = os.path.join(FIRMWARE_DIR, f"{version}.bin")
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    firmware = models.FirmwareRelease(
        version=version,
        build_number=build_number,
        sha256_hash=sha256_hash,
        signature_hex=signature_hex,
        file_path=file_path
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

@app.get("/firmware/{version}/download")
def download_firmware(version: str, db: Session = Depends(get_db)):
    firmware = db.query(models.FirmwareRelease).filter(models.FirmwareRelease.version == version).first()
    if not firmware:
        raise HTTPException(status_code=404, detail="Firmware version not found")
    if not os.path.exists(firmware.file_path):
        raise HTTPException(status_code=404, detail="Firmware file missing from storage")
    return FileResponse(firmware.file_path, media_type="application/octet-stream", filename=f"{version}.bin")

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

# ============ NEW TODAY (Day 4) ============

@app.get("/devices/{device_id}/check-update")
def check_update(device_id: str, db: Session = Depends(get_db)):
    device = db.query(models.Device).filter(models.Device.device_id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not registered")

    latest = db.query(models.FirmwareRelease).order_by(models.FirmwareRelease.build_number.desc()).first()
    if not latest:
        raise HTTPException(status_code=404, detail="No firmware available")

    if latest.build_number > device.current_build_number:
        return {
            "update_available": True,
            "firmware_id": latest.id,
            "latest_version": latest.version,
            "latest_build_number": latest.build_number,
            "sha256_hash": latest.sha256_hash,
            "signature_hex": latest.signature_hex,
            "download_url": f"/firmware/{latest.version}/download"
        }
    return {"update_available": False, "current_version": device.current_version}

@app.post("/devices/{device_id}/report")
def report_update_status(device_id: str, firmware_id: int, status: str, db: Session = Depends(get_db)):
    device = db.query(models.Device).filter(models.Device.device_id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not registered")

    log = models.UpdateLog(device_id=device_id, firmware_id=firmware_id, status=status)
    db.add(log)

    if status == "success":
        firmware = db.query(models.FirmwareRelease).filter(models.FirmwareRelease.id == firmware_id).first()
        if firmware:
            device.current_version = firmware.version
            device.current_build_number = firmware.build_number

    db.commit()
    return {"message": "Status logged", "device_id": device_id, "status": status}

@app.get("/logs")
def get_logs(db: Session = Depends(get_db)):
    logs = db.query(models.UpdateLog).all()
    return [
        {
            "id": l.id,
            "device_id": l.device_id,
            "firmware_id": l.firmware_id,
            "status": l.status,
            "timestamp": l.timestamp
        }
        for l in logs
    ]