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
    cursor.execute('CREATE TABLE table_34892 ("Rank" REAL, "Name" TEXT, "Nationality" TEXT, "1st  ( m ) " REAL, "2nd  ( m ) " REAL, "Points" REAL, "Overall WC points  ( Rank ) " TEXT)')
    
    random.seed(34892)
    nationalities = ["USA", "China", "Japan", "Germany", "France", "UK", "Canada"]
    
    data = []
    for i in range(1, 15):
        rank = i
        name = f"Athlete {i}"
        nationality = random.choice(nationalities)
        first = round(random.uniform(100, 200), 1)
        second = round(random.uniform(100, 200), 1)
        points = random.randint(500, 2000)
        wc_points = f"({random.randint(1, 50)})"
        data.append((rank, name, nationality, first, second, points, wc_points))
    
    data.append((15, "Champion", "USA", 119.5, 118.2, 1850, "(1)"))
    
    cursor.executemany('INSERT INTO table_34892 VALUES (?, ?, ?, ?, ?, ?, ?)', data)
    conn.commit()
    print(f"Database created: {db_path}")
    print(f"Inserted {cursor.execute('SELECT COUNT(*) FROM table_34892').fetchone()[0]} rows")
    conn.close()

if __name__ == "__main__":
    create_database()
