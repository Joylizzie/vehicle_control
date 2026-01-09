dbsql ="""-- kill all the other connections so that the database can be dropped.

SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = 'lzvehicles'
  AND pid <> pg_backend_pid();

drop database if exists lzvehicles;
create database lzvehicles;
"""

#Vehicle Control Schema
#VIN is always 17 characters (ISO 3779)
# VARCHAR(17) is correct and faster than UUID here
# src/create_tb_idx.py

table_sql = """
DROP TABLE IF EXISTS vehicle_status CASCADE; 
CREATE TABLE vehicle_status (
    vin VARCHAR(17) PRIMARY KEY,   -- Primary Key is VIN, so NO auto-increment
    locked BOOLEAN NOT NULL DEFAULT TRUE,
    fuel_level INTEGER NOT NULL CHECK (fuel_level BETWEEN 0 AND 100),
    engine_running BOOLEAN NOT NULL DEFAULT FALSE,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
"""

index_sql = """
CREATE INDEX IF NOT EXISTS idx_vehicle_status_vin
ON vehicle_status (vin);"""

