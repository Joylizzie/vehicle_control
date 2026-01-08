from fastapi import FastAPI
from vehicle_model import VehicleStatus
from service import get_vehicle, lock_vehicle, unlock_vehicle, start_vehicle, stop_vehicle

app = FastAPI(title="Vehicle Control API with PostgreSQL (psycopg2)")

@app.get("/vehicle/{vin}/status", response_model=VehicleStatus)
def read_status(vin: str):
    return get_vehicle(vin)

@app.post("/vehicle/{vin}/lock", response_model=VehicleStatus)
def api_lock_vehicle(vin: str):
    return lock_vehicle(vin)

@app.post("/vehicle/{vin}/unlock", response_model=VehicleStatus)
def api_unlock_vehicle(vin: str):
    return unlock_vehicle(vin)

@app.post("/vehicle/{vin}/start", response_model=VehicleStatus)
def api_start_engine(vin: str):
    return start_vehicle(vin)

@app.post("/vehicle/{vin}/stop", response_model=VehicleStatus)
def api_stop_engine(vin: str):
    return stop_vehicle(vin)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    