# service.py
from vehicle_model import VehicleStatus
from database import get_connection


def get_vehicle(vin: str) -> VehicleStatus:
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT vin, locked, fuel_level, engine_running FROM vehicles WHERE vin = %s",
                (vin,)
            )
            row = cursor.fetchone()
            if row is None:
                raise ValueError("Vehicle not found")

            return VehicleStatus(
                vin=row[0],
                locked=row[1],
                fuel_level=row[2],
                engine_running=row[3],
            )
    finally:
        conn.close()


def update_vehicle(
    vin: str,
    locked: bool | None = None,
    engine_running: bool | None = None,
) -> VehicleStatus:
    if locked is None and engine_running is None:
        raise ValueError("Nothing to update")

    sets = []
    values = []

    if locked is not None:
        sets.append("locked = %s")
        values.append(locked)

    if engine_running is not None:
        sets.append("engine_running = %s")
        values.append(engine_running)

    values.append(vin)

    sql = f"""
        UPDATE vehicles
        SET {", ".join(sets)}
        WHERE vin = %s
        RETURNING vin, locked, fuel_level, engine_running
    """

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, tuple(values))
            row = cursor.fetchone()
            if row is None:
                raise ValueError("Vehicle not found")

            conn.commit()

            return VehicleStatus(
                vin=row[0],
                locked=row[1],
                fuel_level=row[2],
                engine_running=row[3],
            )
    finally:
        conn.close()


def lock_vehicle(vin: str) -> VehicleStatus:
    return update_vehicle(vin, locked=True)


def unlock_vehicle(vin: str) -> VehicleStatus:
    return update_vehicle(vin, locked=False)


def start_vehicle(vin: str) -> VehicleStatus:
    return update_vehicle(vin, engine_running=True)


def stop_vehicle(vin: str) -> VehicleStatus:
    return update_vehicle(vin, engine_running=False)
