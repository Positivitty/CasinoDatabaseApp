from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
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
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

class Machine(Base):
    __tablename__ = "machines"

    id = Column(Integer, primary_key=True, index=True)
    machine_number = Column(String, unique=True, index=True)
    serial_number = Column(String, unique=True)
    vendor = Column(String)
    notes = Column(Text, nullable=True)
    status = Column(Enum(MachineStatus), default=MachineStatus.DOWN)
    date_down = Column(DateTime(timezone=True), default=datetime.now)
    location = Column(String)
    machine_type = Column(String)  # e.g., "Slot Machine", "Video Poker", etc.
    is_out_of_service = Column(Boolean, default=False)
    current_issue = Column(Text, nullable=True)
    last_maintenance = Column(DateTime(timezone=True), server_default=func.now())
    maintenance_records = relationship("MaintenanceRecord", back_populates="machine")

class Technician(Base):
    __tablename__ = "technicians"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    employee_id = Column(String, unique=True, index=True)
    contact_number = Column(String)
    maintenance_records = relationship("MaintenanceRecord", back_populates="technician")

class MaintenanceRecord(Base):
    __tablename__ = "maintenance_records"

    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(Integer, ForeignKey("machines.id"))
    technician_id = Column(Integer, ForeignKey("technicians.id"))
    issue_description = Column(Text)
    repair_description = Column(Text, nullable=True)
    reported_time = Column(DateTime(timezone=True), server_default=func.now())
    resolved_time = Column(DateTime(timezone=True), nullable=True)
    is_resolved = Column(Boolean, default=False)
    
    machine = relationship("Machine", back_populates="maintenance_records")
    technician = relationship("Technician", back_populates="maintenance_records") 