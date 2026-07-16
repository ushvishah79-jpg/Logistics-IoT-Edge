from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class FirmwareRelease(Base):
    __tablename__ = "firmware_releases"
    id = Column(Integer, primary_key=True, autoincrement=True)
    version = Column(String, nullable=False)
    build_number = Column(Integer, nullable=False)
    sha256_hash = Column(String, nullable=False)
    signature_hex = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

class Device(Base):
    __tablename__ = "devices"
    device_id = Column(String, primary_key=True)
    current_version = Column(String)
    current_build_number = Column(Integer, default=0)
    last_check_in = Column(TIMESTAMP)

class UpdateLog(Base):
    __tablename__ = "update_logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(String)
    firmware_id = Column(Integer, ForeignKey("firmware_releases.id"))
    status = Column(String)  # "success" | "hash_fail" | "signature_fail" | "rollback_blocked"
    timestamp = Column(TIMESTAMP, server_default=func.now())