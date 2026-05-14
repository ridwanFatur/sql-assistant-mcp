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
    cursor.execute('CREATE TABLE table_name_14 (attendance TEXT, date TEXT)')
    
    random.seed(14)
    data = []
    for i in range(1, 20):
        attendance = str(random.randint(5000, 50000))
        date = f"{random.randint(1,12):02d} January {random.randint(2000, 2010)}"
        data.append((attendance, date))
    
    data.append(("32500", "7 January 2003"))
    
    cursor.executemany('INSERT INTO table_name_14 VALUES (?, ?)', data)
    conn.commit()
    print(f"Database created: {db_path}")
    print(f"Inserted {cursor.execute('SELECT COUNT(*) FROM table_name_14').fetchone()[0]} rows")
    conn.close()

if __name__ == "__main__":
    create_database()
