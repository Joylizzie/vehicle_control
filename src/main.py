from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from fastapi.staticfiles import StaticFiles
from database_conn import create_connection_pool
from service import get_health_status, get_vehicle_data, set_vehicle_lock, set_vehicle_engine
from sql.vehicle_sql import SQL
from vehicle_model import VehicleStatus
import uvicorn

def create_app():
    pool = create_connection_pool()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await pool.open() # High performance pre-warming
        yield
        await pool.close()

    app = FastAPI(lifespan=lifespan)
    # 1. Enable CORS (Must be added for your HTML buttons to work)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], 
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 2. Mount Static Files (Allows you to see dashboard.html at /static)
    app.mount("/static", StaticFiles(directory="static"), name="static")

    # Dependency for DB connection
    async def conn_dep():
        async with pool.connection() as conn:
            yield conn

    @app.get("/health")
    async def health(conn=Depends(conn_dep)):
        return await get_health_status(conn)

    @app.get("/vehicle/{vin}", response_model=VehicleStatus)
    async def read_vehicle(vin: str, conn=Depends(conn_dep)):
        r = await get_vehicle_data(conn, vin)
        # 1. Check if r is None (Vehicle not found in DB)
        if r is None:
            raise HTTPException(status_code=404, detail=f"Vehicle {vin} not found")
        
        # 2. If it exists, return the data
        return VehicleStatus(vin=r[0], locked=r[1], fuel_level=r[2], engine_running=r[3])

    @app.get("/vehicles")
    async def list_vehicles(conn = Depends(conn_dep)): # Using your updated dependency
        async with conn.cursor() as cur:
            # Fetching the random VINs you generated
            await cur.execute("SELECT vin, locked, fuel_level, engine_running FROM vehicle_status LIMIT 100")
            rows = await cur.fetchall()
            
            return [
                {
                    "vin": r[0], 
                    "locked": r[1], 
                    "fuel_level": r[2], 
                    "engine_running": r[3]
                } for r in rows
            ]

    @app.patch("/vehicle/{vin}/lock")
    async def update_lock(vin: str, locked: bool, conn = Depends(conn_dep)):
        async with conn.cursor() as cur:
        # Use your 'update_lock' query from vehicle_sql.py
            await cur.execute(SQL["update_lock"], (locked, vin))
            row = await cur.fetchone()
            await conn.commit() # Don't forget to commit the change!
        
        if not row:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        return {"vin": row[0], "locked": row[1]}

    @app.patch("/vehicle/{vin}/engine")
    async def update_engine(vin: str, running: bool, conn = Depends(conn_dep)):
        async with conn.cursor() as cur:
            # Use your 'set_engine' query from vehicle_sql.py
            await cur.execute(SQL["set_engine"], (running, vin))
            row = await cur.fetchone()
            await conn.commit()
            
        if not row:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        return {"vin": row[0], "engine_running": row[1]}

    @app.post("/vehicle/{vin}/lock")
    async def lock(vin: str, conn=Depends(conn_dep)):
        return await set_vehicle_lock(conn, vin, True)

    @app.post("/vehicle/{vin}/unlock")
    async def unlock(vin: str, conn=Depends(conn_dep)):
        return await set_vehicle_lock(conn, vin, False)

    @app.post("/vehicle/{vin}/start")
    async def start(vin: str, conn=Depends(conn_dep)):
        return await set_vehicle_engine(conn, vin, True)

    @app.post("/vehicle/{vin}/stop")
    async def stop(vin: str, conn=Depends(conn_dep)):
        return await set_vehicle_engine(conn, vin, False)

    return app


if __name__ == '__main__':
    app = create_app()
    uvicorn.run(app, host="127.0.0.1", port=8000,reload=True, log_level="info")