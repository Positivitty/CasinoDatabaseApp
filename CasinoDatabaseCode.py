from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS for React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

machines = []  # replace with DB later

class Machine(BaseModel):
    machine_number: str
    serial_number: str
    vendor: str
    date_down: str
    vendor_contacted: bool
    technician: str
    status: str  # "Needs Work" or "Fixed"

@app.post("/machines/")
def add_machine(machine: Machine):
    machines.append(machine)
    return {"message": "Added", "machine": machine}

@app.get("/machines/", response_model=List[Machine])
def get_all():
    return machines
