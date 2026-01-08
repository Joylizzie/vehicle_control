# database.py
import psycopg2



def get_connection():
    return psycopg2.connect(
        dbname="lzvehicles",
        user="postgres",
        password="postgres123",
        host="localhost",
        port=5432
    )


def create_table():
    conn = get_connection()
    with conn.cursor() as cursor:   
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehicles (
            vin VARCHAR(17) PRIMARY KEY,
            locked BOOLEAN NOT NULL DEFAULT FALSE,
            fuel_level INT NOT NULL DEFAULT 100,
            engine_running BOOLEAN NOT NULL DEFAULT FALSE
        )
        """)
    conn.commit()
    conn.close()    

if __name__ == "__main__":
    create_table()
    print("Database and vehicles table created.")