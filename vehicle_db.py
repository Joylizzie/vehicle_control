# vehicle_database.py
from vehicle_model import VehicleStatus, create_random_vehicle
from threading import Lock
from typing import Dict, Optional

class VehicleDatabase:
    def __init__(self):
        self.store: Dict[str, VehicleStatus] = {}
        self.lock = Lock()
        # Initialize some vehicles
        for _ in range(10):
            vehicle = create_random_vehicle()
            self.store[vehicle.vin] = vehicle

    def get_vehicle(self, vin: str) -> Optional[VehicleStatus]:
        return self.store.get(vin)

    def update_vehicle(self, vin: str, **kwargs) -> Optional[VehicleStatus]:
        with self.lock:
            vehicle = self.store.get(vin)
            if not vehicle:
                return None
            vehicle = vehicle.copy(update=kwargs)
            self.store[vin] = vehicle
            return vehicle
if __name__ == "__main__":
    db = VehicleDatabase()
    for vin, vehicle in db.store.items():
        print(f"VIN: {vin}, Status: {vehicle.model_dump()}")