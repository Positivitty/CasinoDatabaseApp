from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import timedelta
from database import get_db, engine
import models, schemas
from auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    get_password_hash,
    verify_password,
    get_current_active_user
)
from fastapi.middleware.cors import CORSMiddleware
from typing import List

# Create all tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Casino Database API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app's address
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Find the user
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if username already exists
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Check if email already exists
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Validate password
    try:
        schemas.UserCreate.validate_password(user.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    # Return user data with token
    return {
        "id": db_user.id,
        "username": db_user.username,
        "email": db_user.email,
        "is_active": db_user.is_active,
        "is_admin": db_user.is_admin,
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(get_current_active_user)):
    return current_user

@app.get("/")
def read_root():
    return {"message": "Welcome to Casino Database API"}

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        # Try to use the database connection
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}

# New Machine Endpoints
@app.get("/machines/", response_model=List[schemas.Machine])
def get_machines(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    machines = db.query(models.Machine).all()
    return machines

@app.post("/machines/", response_model=schemas.Machine)
def create_machine(
    machine: schemas.MachineCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_machine = models.Machine(**machine.dict())
    db.add(db_machine)
    db.commit()
    db.refresh(db_machine)
    return db_machine

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

@app.patch("/machines/{machine_number}", response_model=schemas.Machine)
def update_machine(
    machine_number: str,
    updates: schemas.MachineUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    machine = db.query(models.Machine).filter(models.Machine.machine_number == machine_number).first()
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(machine, key, value)
    
    db.commit()
    db.refresh(machine)
    return machine 