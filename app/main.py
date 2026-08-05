from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import hashlib
from app.database import engine, Base, get_db
from app import models, schemas

import os


Base.metadata.create_all(bind=engine)

app = FastAPI(title="OTA Firmware Update Server")

# ---------------------------------------------------
# Firmware Storage Directory
# ---------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

FIRMWARE_DIR = os.path.join(PROJECT_ROOT, "firmware_storage")
os.makedirs(FIRMWARE_DIR, exist_ok=True)

# ---------------------------------------------------
# Dashboard
# ---------------------------------------------------

DASHBOARD_PATH = os.path.join(PROJECT_ROOT, "dashboard", "ota.html")


# ---------------------------------------------------
# Root
# ---------------------------------------------------

@app.get("/")
def root():
    return {"message": "OTA Firmware Update Server is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/dashboard")
def serve_dashboard():
    if not os.path.isfile(DASHBOARD_PATH):
        raise HTTPException(status_code=404, detail="Dashboard file not found on server")
    return FileResponse(DASHBOARD_PATH, media_type="text/html")


# ---------------------------------------------------
# Upload Firmware
# ---------------------------------------------------

@app.post("/firmware/upload", response_model=schemas.FirmwareReleaseOut)
async def upload_firmware(
    version: str = Form(...),
    build_number: int = Form(...),
    sha256_hash: str = Form(...),
    signature_hex: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    content = await file.read()

    # -----------------------------
    # Verify SHA256
    # -----------------------------

    actual_hash = hashlib.sha256(content).hexdigest()

    if actual_hash != sha256_hash:

        raise HTTPException(
            status_code=400,
            detail="SHA256 hash mismatch"
        )

    # -----------------------------
    # Verify Signature Format
    # -----------------------------

    try:
        bytes.fromhex(signature_hex)

    except ValueError:

        raise HTTPException(
            status_code=400,
            detail="Invalid signature format"
        )

    # -----------------------------
    # Save Firmware
    # -----------------------------

    filename = f"{version}-build{build_number}.bin"

    file_path = os.path.join(
        FIRMWARE_DIR,
        filename
    )

    # Make sure directory exists
    os.makedirs(FIRMWARE_DIR, exist_ok=True)

    with open(file_path, "wb") as buffer:
        buffer.write(content)

    # -----------------------------
    # Save Database Record
    # -----------------------------

    firmware = models.FirmwareRelease(

        version=version,

        build_number=build_number,

        sha256_hash=actual_hash,

        signature_hex=signature_hex,

        file_path=file_path

    )

    db.add(firmware)

    db.commit()

    db.refresh(firmware)

    return firmware

# ---------------------------------------------------
# Latest Firmware
# ---------------------------------------------------

@app.get("/firmware/latest", response_model=schemas.FirmwareReleaseOut)
def get_latest_firmware(db: Session = Depends(get_db)):

    firmware = (
        db.query(models.FirmwareRelease)
        .order_by(models.FirmwareRelease.build_number.desc())
        .first()
    )

    if not firmware:
        raise HTTPException(status_code=404, detail="No firmware releases found")

    return firmware


# ---------------------------------------------------
# List Firmware
# ---------------------------------------------------

@app.get("/firmware/all", response_model=list[schemas.FirmwareReleaseOut])
def list_firmware(db: Session = Depends(get_db)):
    return db.query(models.FirmwareRelease).all()


# ---------------------------------------------------
# Download Firmware
# ---------------------------------------------------

@app.get("/firmware/{version}/download")
def download_firmware(version: str, db: Session = Depends(get_db)):

    firmware = (
        db.query(models.FirmwareRelease)
        .filter(models.FirmwareRelease.version == version)
        .order_by(models.FirmwareRelease.build_number.desc())
        .first()
    )

    if not firmware:
        raise HTTPException(status_code=404, detail="Firmware version not found")

    if not os.path.isfile(firmware.file_path):
        raise HTTPException(
            status_code=404,
            detail=f"Firmware file not found: {firmware.file_path}"
        )

    return FileResponse(
        firmware.file_path,
        media_type="application/octet-stream",
        filename=os.path.basename(firmware.file_path)
    )


# ---------------------------------------------------
# Register Device
# ---------------------------------------------------

@app.post("/devices/register", response_model=schemas.DeviceOut)
def register_device(device: schemas.DeviceRegister, db: Session = Depends(get_db)):

    existing = (
        db.query(models.Device)
        .filter(models.Device.device_id == device.device_id)
        .first()
    )

    if existing:
        return existing

    new_device = models.Device(
        device_id=device.device_id,
        current_build_number=0
    )

    db.add(new_device)
    db.commit()
    db.refresh(new_device)

    return new_device


# ---------------------------------------------------
# Check Update
# ---------------------------------------------------

@app.get("/devices/{device_id}/check-update")
def check_update(device_id: str, db: Session = Depends(get_db)):

    device = (
        db.query(models.Device)
        .filter(models.Device.device_id == device_id)
        .first()
    )

    if not device:
        raise HTTPException(status_code=404, detail="Device not registered")

    latest = (
        db.query(models.FirmwareRelease)
        .order_by(models.FirmwareRelease.build_number.desc())
        .first()
    )

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

    return {
        "update_available": False,
        "current_version": device.current_version
    }


# ---------------------------------------------------
# Report Update Status
# ---------------------------------------------------


@app.post("/devices/{device_id}/report")
def report_update_status(
    device_id: str,
    firmware_id: int,
    status: str,
    db: Session = Depends(get_db)
):

    device = (
        db.query(models.Device)
        .filter(models.Device.device_id == device_id)
        .first()
    )

    if not device:
        raise HTTPException(status_code=404, detail="Device not registered")

    firmware = (
        db.query(models.FirmwareRelease)
        .filter(models.FirmwareRelease.id == firmware_id)
        .first()
    )

    # ------------------------------------------------------------
    # Anti-rollback enforcement (Week 4)
    #
    # check-update already refuses to OFFER an older build, but this
    # endpoint previously had no check at all on what it accepted as
    # a completed install. A client (attacker, buggy device, or manual
    # test) could report success on an old firmware_id and silently
    # move the device's recorded version backward. This block closes
    # that gap by rejecting any "success" report whose build_number is
    # not strictly newer than what the device already has on record.
    # ------------------------------------------------------------
    if status == "success" and firmware:
        if firmware.build_number <= device.current_build_number:
            log = models.UpdateLog(
                device_id=device_id,
                firmware_id=firmware_id,
                status="rollback_blocked"
            )
            db.add(log)
            db.commit()
            raise HTTPException(
                status_code=403,
                detail=(
                    f"Rollback attempt blocked: reported build_number "
                    f"({firmware.build_number}) is not newer than device's "
                    f"current build_number ({device.current_build_number})."
                )
            )

        device.current_version = firmware.version
        device.current_build_number = firmware.build_number

    log = models.UpdateLog(
        device_id=device_id,
        firmware_id=firmware_id,
        status=status
    )
    db.add(log)
    db.commit()

    return {
        "message": "Status logged",
        "device_id": device_id,
        "status": status
    }


# ---------------------------------------------------
# Logs
# ---------------------------------------------------

@app.get("/logs")
def get_logs(db: Session = Depends(get_db)):

    logs = db.query(models.UpdateLog).all()

    return [
        {
            "id": log.id,
            "device_id": log.device_id,
            "firmware_id": log.firmware_id,
            "status": log.status,
            "timestamp": log.timestamp
        }
        for log in logs
    ]

# ---------------------------------------------------
# Device Update History (Week 4 - Day 2)
# ---------------------------------------------------

@app.get("/devices/{device_id}/history")
def device_history(device_id: str, db: Session = Depends(get_db)):

    # Check whether the device exists
    device = (
        db.query(models.Device)
        .filter(models.Device.device_id == device_id)
        .first()
    )

    if not device:
        raise HTTPException(
            status_code=404,
            detail="Device not registered"
        )

    # Get update history
    logs = (
        db.query(models.UpdateLog)
        .filter(models.UpdateLog.device_id == device_id)
        .order_by(models.UpdateLog.timestamp.desc())
        .all()
    )

    history = []

    for log in logs:

        firmware = (
            db.query(models.FirmwareRelease)
            .filter(models.FirmwareRelease.id == log.firmware_id)
            .first()
        )

        history.append(
            {
                "timestamp": log.timestamp,
                "device_id": log.device_id,
                "status": log.status,
                "firmware_version": firmware.version if firmware else None,
                "build_number": firmware.build_number if firmware else None
            }
        )

    return history