from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta
import models
import schemas
from database import engine, get_db
from auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    get_current_active_user,
    get_password_hash,
    verify_password
)

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Casino Machine Tracker")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/machines/", response_model=List[schemas.Machine])
def get_all_machines(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    machines = db.query(models.Machine).offset(skip).limit(limit).all()
    return machines

@app.post("/machines/", response_model=schemas.Machine)
def add_machine(
    machine: schemas.MachineCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_machine = models.Machine(**machine.dict(), technician_id=current_user.id)
    db.add(db_machine)
    db.commit()
    db.refresh(db_machine)
    return db_machine

@app.patch("/machines/{machine_number}", response_model=schemas.Machine)
def update_machine(
    machine_number: str,
    update_data: schemas.MachineUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    machine = db.query(models.Machine).filter(models.Machine.machine_number == machine_number).first()
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    
    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(machine, field, value)
    
    db.commit()
    db.refresh(machine)
    return machine

@app.get("/machines/{machine_number}", response_model=schemas.Machine)
def get_machine(
    machine_number: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    machine = db.query(models.Machine).filter(models.Machine.machine_number == machine_number).first()
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    return machine
