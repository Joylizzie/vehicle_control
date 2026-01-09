# vehicle_sql.py
SQL = {
    "get_one": "SELECT vin, locked, fuel_level, engine_running FROM vehicle_status WHERE vin = %s",
    "get_batch": "SELECT vin, locked, fuel_level, engine_running FROM vehicle_status WHERE vin = ANY(%s)",
    "update_lock": "UPDATE vehicle_status SET locked = %s WHERE vin = %s RETURNING vin, locked",
    "set_engine": "UPDATE vehicle_status SET engine_running = %s WHERE vin = %s RETURNING vin, engine_running"
}