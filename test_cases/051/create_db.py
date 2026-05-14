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
    cursor.execute('CREATE TABLE table_name_24 (constructor TEXT, laps TEXT, driver TEXT)')
    
    random.seed(24)
    constructors = ["Ferrari", "McLaren", "Williams", "Benetton", "Jordan", "Minardi"]
    drivers = ["Michael Schumacher", "Ayrton Senna", "Alain Prost", "Nigel Mansell", "Juan Pablo Montoya"]
    
    data = []
    for i in range(15):
        constructor = random.choice(constructors)
        laps = str(random.randint(35, 80))
        driver = random.choice(drivers)
        data.append((constructor, laps, driver))
    
    data.append(("Ferrari", "28", "Michael Schumacher"))
    
    cursor.executemany('INSERT INTO table_name_24 VALUES (?, ?, ?)', data)
    conn.commit()
    print(f"Database created: {db_path}")
    print(f"Inserted {cursor.execute('SELECT COUNT(*) FROM table_name_24').fetchone()[0]} rows")
    conn.close()

if __name__ == "__main__":
    create_database()
