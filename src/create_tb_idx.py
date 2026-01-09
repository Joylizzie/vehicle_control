import asyncio
import os
import yaml
import random
import logging
from database_conn import load_config
from psycopg import AsyncConnection
from sql import db_schema as schema
from gen_vehicle_id  import generate_vin

# Setup professional logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

async def setup_schema_and_data():
    # 1. Load the full config to get both DB details and App settings
    with open("config.yaml", "r") as f:
        full_config = yaml.safe_load(f)
    
    cfg = full_config["database"]
    # Get seed_count from config, default to 10 if missing
    seed_count = full_config.get("app_settings", {}).get("seed_count", 10)
    
    db_pass = os.getenv("VEHICLE_DB_PASSWORD", cfg.get("password"))
    conn_str = f"postgresql://{cfg['user']}:{db_pass}@{cfg['host']}:{cfg['port']}/{cfg['dbname']}"
    
    logger.info(f"Connecting to database '{cfg['dbname']}'...")
    
    try:
        async with await AsyncConnection.connect(conn_str) as conn:
            async with conn.cursor() as cur:
                # Create Table
                await cur.execute(schema.table_sql)

                # Create Index
                await cur.execute(schema.index_sql)

                # 2. Seed the Data using the number from CONFIG
                logger.info(f"Seeding {seed_count} vehicles based on config.yaml...")
                for i in range(1, seed_count + 1):
                    vin = generate_vin()
                    locked = random.choice([True, False])
                    fuel_level = random.randint(0, 100)
                    engine_running = random.choice([True, False])
                    
                    await cur.execute(
                        "INSERT INTO vehicle_status (vin, locked, fuel_level, engine_running) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING",
                        (vin, locked, fuel_level, engine_running)
                    )
                
                await conn.commit()
                logger.info(f"✅ Setup complete. {seed_count} rows processed.")

    except Exception as e:
        logger.error(f"❌ Failed to setup schema/data: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(setup_schema_and_data())