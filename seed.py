# seed.py
import random
from database import get_connection
from vehicle_id import fake_vins

def seed_vehicles():
    """Generate 20 random vehicles and insert into lzvehicles DB"""
    conn = get_connection()
    with conn.cursor() as cursor:
        for vin in fake_vins(20):
            locked = random.choice([True, False])
            fuel_level = random.randint(0, 100)
            engine_running = random.choice([True, False])

            cursor.execute("""
                INSERT INTO vehicles (vin, locked, fuel_level, engine_running)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (vin) DO NOTHING
            """, (vin, locked, fuel_level, engine_running))

    conn.commit()  # commit all inserts
    conn.close()   # close connection
    print("Seeded 20 vehicles into DB lzvehicles")

def is_connected():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT vin FROM vehicles;")
    vins = [row[0] for row in cur.fetchall()]
    print(vins)
    cur.close()
    conn.close()

if __name__ == "__main__":
    # seed_vehicles()
    is_connected()
