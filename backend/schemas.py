from pydantic import BaseModel, EmailStr
from typing import Optional
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
    serial_number: str
    vendor: str
    vendor_contacted: bool = False
    notes: Optional[str] = None

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
    date_down: datetime
    status: MachineStatus
    technician_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 