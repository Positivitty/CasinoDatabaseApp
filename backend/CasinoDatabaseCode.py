from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


machines = []


class Machine(BaseModel):
    machine_number: str
    serial_number: str
    vendor: str
    date_down: str
    vendor_contacted: bool
    technician: str
    status: str  


@app.post("/machines/")
def add_machine(machine: Machine):
    machines.append(machine.dict())  
    return {"message": "Added", "machine": machine}


@app.get("/machines/", response_model=List[Machine])
def get_all():
    return machines


@app.patch("/machines/{machine_number}")
def update_machine(machine_number: str, update: dict):
    for machine in machines:
        if machine["machine_number"] == machine_number:
            machine.update(update)
            return machine
    raise HTTPException(status_code=404, detail="Machine not found")
