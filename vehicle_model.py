# vehicle_model.py
from pydantic import BaseModel, Field

class VehicleStatus(BaseModel):
    vin: str = Field(..., min_length=17, max_length=17)
    locked: bool
    fuel_level: int = Field(..., ge=0, le=100)
    engine_running: bool

    model_config = {
        "from_attributes": True  # Pydantic v2 replacement for orm_mode
    }


if __name__ == "__main__":
    # Example usage
    example_vehicle = VehicleStatus(
        vin="MZV0BP3LP8VXNPZ27",
        locked=True,
        fuel_level=15,
        engine_running=False
    )
    print(example_vehicle.model_dump_json())