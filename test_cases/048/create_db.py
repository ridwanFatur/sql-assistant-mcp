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
    cursor.execute('CREATE TABLE table_78467 ("Color" TEXT, "mass  ( g/mol ) " TEXT, "Absorb  ( nm ) " TEXT, "Emit  ( nm ) " TEXT, "ε  ( M -1 cm -1  ) " TEXT)')
    
    random.seed(78467)
    colors = ["Red", "Blue", "Green", "Yellow", "Purple", "Orange"]
    
    data = []
    for i in range(12):
        color = random.choice(colors)
        mass = str(random.randint(200, 2000))
        absorb = str(random.randint(300, 600))
        emit = str(random.randint(400, 700))
        epsilon = str(random.randint(1000, 50000))
        data.append((color, mass, absorb, emit, epsilon))
    
    data.append(("Cyan", "1078", "450", "520", "15000"))
    
    cursor.executemany('INSERT INTO table_78467 VALUES (?, ?, ?, ?, ?)', data)
    conn.commit()
    print(f"Database created: {db_path}")
    print(f"Inserted {cursor.execute('SELECT COUNT(*) FROM table_78467').fetchone()[0]} rows")
    conn.close()

if __name__ == "__main__":
    create_database()
