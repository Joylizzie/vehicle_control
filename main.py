
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
import random

app = FastAPI(title="Vehicle Control API Demo")


# -----------------------------
# Data Models
# -----------------------------
class VehicleCommand(BaseModel):
    vin: str


class VehicleStatus(BaseModel):
    vin: str
    locked: bool
    fuel_level: int
    engine_running: bool


# -----------------------------
# In-memory mock database
# -----------------------------
def create_vehicle_store() -> Dict[str, VehicleStatus]:
    """
    Create a mock vehicle store with random initial values.
    """
    return {
        "VIN123": VehicleStatus(
            vin="VIN123",
            locked=random.choice([True, False]),
            fuel_level=random.randint(10, 100),
            engine_running=False
        ),
        "VIN456": VehicleStatus(
            vin="VIN456",
            locked=random.choice([True, False]),
            fuel_level=random.randint(10, 100),
            engine_running=False
        )
    }


vehicle_store = create_vehicle_store()


# -----------------------------
# Service-layer functions
# -----------------------------
def get_vehicle(vin: str) -> VehicleStatus:
    if vin not in vehicle_store:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle_store[vin]


def lock_vehicle(vin: str) -> VehicleStatus:
    vehicle = get_vehicle(vin)
    vehicle.locked = True
    return vehicle


def unlock_vehicle(vin: str) -> VehicleStatus:
    vehicle = get_vehicle(vin)
    vehicle.locked = False
    return vehicle


def start_engine(vin: str) -> VehicleStatus:
    vehicle = get_vehicle(vin)
    if vehicle.engine_running:
        raise HTTPException(status_code=400, detail="Engine already running")
    vehicle.engine_running = True
    return vehicle


def stop_engine(vin: str) -> VehicleStatus:
    vehicle = get_vehicle(vin)
    if not vehicle.engine_running:
        raise HTTPException(status_code=400, detail="Engine already stopped")
    vehicle.engine_running = False
    return vehicle


# -----------------------------
# API Endpoints
# -----------------------------
@app.get("/vehicle/{vin}/status", response_model=VehicleStatus)
def read_status(vin: str):
    return get_vehicle(vin)


@app.post("/vehicle/{vin}/lock", response_model=VehicleStatus)
def lock(vin: str):
    return lock_vehicle(vin)


@app.post("/vehicle/{vin}/unlock", response_model=VehicleStatus)
def unlock(vin: str):
    return unlock_vehicle(vin)


@app.post("/vehicle/{vin}/start", response_model=VehicleStatus)
def start(vin: str):
    return start_engine(vin)


@app.post("/vehicle/{vin}/stop", response_model=VehicleStatus)
def stop(vin: str):
    return stop_engine(vin)
