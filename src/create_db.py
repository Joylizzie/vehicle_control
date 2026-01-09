import asyncio
import os
import logging
from database_conn import load_config
from psycopg import AsyncConnection

# Setup professional logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

async def create_database_system():
    cfg_all = load_config()
    cfg = cfg_all['database']
    db_pass = os.getenv("VEHICLE_DB_PASSWORD", cfg.get("password"))
    
    # We must connect to the 'postgres' DB to drop/create other DBs
    conn_str = f"postgresql://{cfg['user']}:{db_pass}@{cfg['host']}:{cfg['port']}/postgres"
    
    logger.info("Connecting to system database...")
    
    # 1. Open connection manually (bypassing the 'async with' context manager)
    conn = await AsyncConnection.connect(conn_str)
    
    try:
        # 2. Set autocommit immediately
        await conn.set_autocommit(True)
        
        async with conn.cursor() as cur:
            # Command A: Kill lingering connections (prevent "database is being accessed" error)
            logger.info("Cleaning up active connections to lzvehicles...")
            await cur.execute("""
                SELECT pg_terminate_backend(pg_stat_activity.pid)
                FROM pg_stat_activity
                WHERE pg_stat_activity.datname = 'lzvehicles'
                  AND pid <> pg_backend_pid();
            """)

            # Command B: Drop the DB
            logger.info("Dropping database 'lzvehicles'...")
            await cur.execute("DROP DATABASE IF EXISTS lzvehicles;")

            # Command C: Create the DB
            logger.info("Creating fresh database 'lzvehicles'...")
            await cur.execute("CREATE DATABASE lzvehicles;")
            
        logger.info("✅ Database reset successfully.")

    except Exception as e:
        logger.error(f"❌ Failed to reset database: {e}")
        raise
    finally:
        # 3. Close connection manually
        await conn.close()

if __name__ == "__main__":
    asyncio.run(create_database_system())