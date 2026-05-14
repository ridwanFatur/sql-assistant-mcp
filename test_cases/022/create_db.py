import sqlite3
import os
import random

def create_database():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "database.sqlite")
    if os.path.exists(db_path):
        os.remove(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('CREATE TABLE aircraft (aid REAL, name TEXT, distance REAL)')
    cursor.execute('CREATE TABLE flight (flno REAL, origin TEXT, destination TEXT, distance REAL, departure_date DATE, arrival_date DATE, price REAL, aid REAL)')
    cursor.execute('CREATE TABLE employee (eid REAL, name TEXT, salary REAL)')
    cursor.execute('CREATE TABLE certificate (eid REAL, aid REAL)')
    
    random.seed(22)
    
    aircraft_data = [
        (1, "Boeing 737", 3000),
        (2, "Airbus A320", 3500),
        (3, "Boeing 777", 8000),
        (4, "Airbus A380", 9000),
        (5, "Cessna 172", 800)
    ]
    cursor.executemany('INSERT INTO aircraft VALUES (?, ?, ?)', aircraft_data)
    
    destinations = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio"]
    flight_data = []
    for i in range(1, 21):
        flno = i
        origin = random.choice(destinations)
        dest = random.choice([d for d in destinations if d != origin])
        distance = random.randint(500, 5000)
        dep_date = f"2024-0{random.randint(1,9)}-{random.randint(10,28):02d}"
        arr_date = f"2024-0{random.randint(1,9)}-{random.randint(10,28):02d}"
        price = random.uniform(100, 1000)
        aid = random.choice([1, 2, 3, 4, 5])
        flight_data.append((flno, origin, dest, distance, dep_date, arr_date, price, aid))
    cursor.executemany('INSERT INTO flight VALUES (?, ?, ?, ?, ?, ?, ?, ?)', flight_data)
    
    employee_data = []
    for i in range(1, 11):
        eid = i
        name = f"Employee {i}"
        salary = random.randint(40000, 120000)
        employee_data.append((eid, name, salary))
    cursor.executemany('INSERT INTO employee VALUES (?, ?, ?)', employee_data)
    
    certificate_data = []
    for i in range(1, 16):
        eid = random.randint(1, 10)
        aid = random.randint(1, 5)
        certificate_data.append((eid, aid))
    cursor.executemany('INSERT INTO certificate VALUES (?, ?)', certificate_data)
    
    conn.commit()
    print(f"Database created: {db_path}")
    print(f"Aircraft: {cursor.execute('SELECT COUNT(*) FROM aircraft').fetchone()[0]} rows")
    print(f"Flight: {cursor.execute('SELECT COUNT(*) FROM flight').fetchone()[0]} rows")
    print(f"Employee: {cursor.execute('SELECT COUNT(*) FROM employee').fetchone()[0]} rows")
    print(f"Certificate: {cursor.execute('SELECT COUNT(*) FROM certificate').fetchone()[0]} rows")
    conn.close()

if __name__ == "__main__":
    create_database()
