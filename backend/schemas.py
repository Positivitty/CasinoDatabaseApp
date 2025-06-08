from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from models import MachineStatus

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool

    class Config:
        from_attributes = True

class MachineBase(BaseModel):
    machine_number: str
    location: str
    machine_type: str
    is_out_of_service: bool = False
    current_issue: Optional[str] = None

class MachineCreate(MachineBase):
    pass

class MachineUpdate(BaseModel):
    serial_number: Optional[str] = None
    vendor: Optional[str] = None
    vendor_contacted: Optional[bool] = None
    status: Optional[MachineStatus] = None
    notes: Optional[str] = None

class Machine(MachineBase):
    id: int
    last_maintenance: datetime

    class Config:
        from_attributes = True

class TechnicianBase(BaseModel):
    name: str
    employee_id: str
    contact_number: str

class TechnicianCreate(TechnicianBase):
    pass

class Technician(TechnicianBase):
    id: int

    class Config:
        from_attributes = True

class MaintenanceRecordBase(BaseModel):
    machine_id: int
    technician_id: int
    issue_description: str
    repair_description: Optional[str] = None
    is_resolved: bool = False

class MaintenanceRecordCreate(MaintenanceRecordBase):
    pass

class MaintenanceRecord(MaintenanceRecordBase):
    id: int
    reported_time: datetime
    resolved_time: Optional[datetime] = None

    class Config:
        from_attributes = True 