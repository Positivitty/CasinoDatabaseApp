from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List
from datetime import datetime
from models import MachineStatus

class UserBase(BaseModel):
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserBase):
    password: str

    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one number')
        return v

class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool = False

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    is_admin: bool
    access_token: Optional[str] = None
    token_type: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Machine Schemas
class MachineBase(BaseModel):
    machine_number: str
    serial_number: str
    vendor: str
    notes: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class MachineCreate(MachineBase):
    status: MachineStatus = MachineStatus.DOWN
    date_down: datetime = datetime.now()

class MachineUpdate(BaseModel):
    status: Optional[MachineStatus] = None
    notes: Optional[str] = None
    date_down: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

class Machine(MachineBase):
    id: int
    status: MachineStatus
    date_down: datetime

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