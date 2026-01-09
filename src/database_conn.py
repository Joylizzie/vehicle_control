import os
import yaml
import logging
from psycopg_pool import AsyncConnectionPool

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def load_config():
    """Loads the database configuration from config.yaml."""
    # This looks one level up from 'src' to find config.yaml in the root
    config_path = os.path.join(os.path.dirname(__file__), "..", "config.yaml")
    try:
        with open(config_path, "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logger.error(f"❌ config.yaml not found at {config_path}")
        raise

# Global pool variable
pool = None

def get_conn_str():
    """Constructs the connection string using your exact YAML keys."""
    full_config = load_config()
    cfg = full_config["database"]
    
    # Priority: Environment Variable > config.yaml
    db_pass = os.getenv("VEHICLE_DB_PASSWORD", cfg.get("password"))
    db_name = cfg.get("dbname") 
    
    return f"postgresql://{cfg['user']}:{db_pass}@{cfg['host']}:{cfg['port']}/{db_name}"

def create_connection_pool():
    """Initializes the global AsyncConnectionPool."""
    global pool
    conn_str = get_conn_str()
    
    logger.info("Initializing asynchronous connection pool...")
    # open=False because we want to open it explicitly in FastAPI startup
    pool = AsyncConnectionPool(conn_str, open=False) 
    return pool

async def get_db_connection():
    """Returns a connection from the pool."""
    global pool
    if pool is None:
        create_connection_pool()
    return pool.connection()

# If this file is run directly, just test the connection pool creation
if __name__ == "__main__":
    create_connection_pool()
    logger.info("Connection pool created successfully.")    