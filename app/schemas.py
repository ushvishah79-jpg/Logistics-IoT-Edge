from pydantic import BaseModel
from datetime import datetime

class FirmwareManifest(BaseModel):
    version: str
    build_number: int
    sha256_hash: str
    signature_hex: str

class FirmwareReleaseOut(BaseModel):
    id: int
    version: str
    build_number: int
    sha256_hash: str
    file_path: str
    created_at: datetime

    class Config:
        from_attributes = True   # lets Pydantic read SQLAlchemy objects directly

class DeviceRegister(BaseModel):
    device_id: str

class DeviceOut(BaseModel):
    device_id: str
    current_version: str | None
    current_build_number: int

    class Config:
        from_attributes = True