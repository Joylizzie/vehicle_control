from sql.vehicle_sql import SQL

async def db_check_health(conn):
    async with conn.cursor() as cur:
        # Directly hardcoded as it is a protocol-level smoke test
        await cur.execute("SELECT 1")
        return await cur.fetchone()

async def fetch_vehicle(conn, vin: str):
    async with conn.cursor() as cur:
        await cur.execute(SQL["get_one"], (vin,))
        return await cur.fetchone()

async def update_status(conn, vin: str, field: str, value: bool):
    # Whitelist validation for column names (Security Best Practice)
    if field not in ["locked", "engine_running"]:
        raise ValueError(f"Invalid column: {field}")
        
    query = f"UPDATE vehicle_status SET {field} = %s WHERE vin = %s RETURNING vin, {field}"
    async with conn.cursor() as cur:
        await cur.execute(query, (value, vin))
        return await cur.fetchone()

if __name__ == "__main__":

    print("Database functions loaded. Whitelisted fields: locked, engine_running")