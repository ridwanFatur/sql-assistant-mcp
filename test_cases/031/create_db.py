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
    cursor.execute("CREATE TABLE table_11622829_1 (tournament TEXT, score TEXT)")
    
    random.seed(11622829)
    tournaments = ["Masters", "US Open", "British Open", "PGA", "Players Championship", "WGC"]
    scores = ["135 (-7)", "136 (-6)", "137 (-5)", "138 (-4)", "139 (-3)", "140 (-2)"]
    
    data = [(random.choice(tournaments), random.choice(scores)) for _ in range(12)]
    data.append(("Masters", "135 (-7)"))
    data.append(("US Open", "135 (-7)"))
    
    cursor.executemany("INSERT INTO table_11622829_1 VALUES (?, ?)", data)
    conn.commit()
    print(f"Database created: {db_path}")
    print(f"Inserted {cursor.execute('SELECT COUNT(*) FROM table_11622829_1').fetchone()[0]} rows")
    conn.close()

if __name__ == "__main__":
    create_database()
