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
    cursor.execute('CREATE TABLE table_name_98 (points INTEGER, goals TEXT)')
    
    random.seed(98)
    data = []
    for i in range(15):
        points = random.randint(10, 100)
        goals = f"{random.randint(10, 40)} {random.randint(10, 40)}"
        data.append((points, goals))
    
    data.append((75, "29 30"))
    
    cursor.executemany('INSERT INTO table_name_98 VALUES (?, ?)', data)
    conn.commit()
    print(f"Database created: {db_path}")
    print(f"Inserted {cursor.execute('SELECT COUNT(*) FROM table_name_98').fetchone()[0]} rows")
    conn.close()

if __name__ == "__main__":
    create_database()
