from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum
from datetime import datetime

class MachineStatus(str, enum.Enum):
    DOWN = "down"
    FIXED = "fixed"
    IN_PROGRESS = "in_progress"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    machines = relationship("Machine", back_populates="technician")

class Machine(Base):
    __tablename__ = "machines"

    id = Column(Integer, primary_key=True, index=True)
    machine_number = Column(String, unique=True, index=True)
    serial_number = Column(String, unique=True)
    vendor = Column(String)
    date_down = Column(DateTime, default=datetime.utcnow)
    vendor_contacted = Column(Boolean, default=False)
    technician_id = Column(Integer, ForeignKey("users.id"))
    status = Column(Enum(MachineStatus), default=MachineStatus.DOWN)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    technician = relationship("User", back_populates="machines") 