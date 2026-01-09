
import vehicle_db
from fastapi import HTTPException

async def get_health_status(conn):
    try:
        await vehicle_db.db_check_health(conn)
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

async def get_vehicle_data(conn, vin: str):
    row = await vehicle_db.fetch_vehicle(conn, vin)
    if not row:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return row

async def set_vehicle_lock(conn, vin: str, state: bool):
    row = await vehicle_db.update_status(conn, vin, "locked", state)
    if not row:
        raise HTTPException(status_code=404, detail="Update failed")
    return {"vin": row[0], "locked": row[1]}

async def set_vehicle_engine(conn, vin: str, state: bool):
    row = await vehicle_db.update_status(conn, vin, "engine_running", state)
    if not row:
        raise HTTPException(status_code=404, detail="Update failed")
    return {"vin": row[0], "engine_running": row[1]}

if __name__ == "__main__":
    print("Service layer ready for orchestration.")