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
    cursor.execute('CREATE TABLE table_name_33 (weight INTEGER, position TEXT)')
    
    random.seed(33)
    positions = ["Fullback", "Halfback", "Quarterback", "Tackle", "Guard", "Center"]
    
    data = []
    for i in range(15):
        weight = random.randint(180, 320)
        position = random.choice(positions)
        data.append((weight, position))
    
    data.append((285, "Fullback"))
    data.append((290, "Fullback"))
    
    cursor.executemany('INSERT INTO table_name_33 VALUES (?, ?)', data)
    conn.commit()
    print(f"Database created: {db_path}")
    print(f"Inserted {cursor.execute('SELECT COUNT(*) FROM table_name_33').fetchone()[0]} rows")
    conn.close()

if __name__ == "__main__":
    create_database()
