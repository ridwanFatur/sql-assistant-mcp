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
    cursor.execute('CREATE TABLE table_40457 ("Election" REAL, "First member" TEXT, "First party" TEXT, "Second member" TEXT, "Second party" TEXT, "Third member" TEXT, "Third party" TEXT)')
    
    random.seed(40457)
    members = ["John Smith", "Mary Johnson", "David Williams", "Sarah Brown", "James Davis", "Patricia Miller"]
    parties = ["Conservative", "Liberal", "Labour", "Green", "Independent"]
    
    data = []
    for i in range(1, 12):
        election = i
        first_m = random.choice(members)
        first_p = random.choice(parties)
        second_m = random.choice([m for m in members if m != first_m])
        second_p = random.choice([p for p in parties if p != first_p])
        third_m = random.choice([m for m in members if m not in [first_m, second_m]])
        third_p = random.choice([p for p in parties if p not in [first_p, second_p]])
        data.append((election, first_m, first_p, second_m, second_p, third_m, third_p))
    
    data.append((3, "Alice", "Conservative", "Bob", "Liberal", "Charlie", "Conservative"))
    
    cursor.executemany('INSERT INTO table_40457 VALUES (?, ?, ?, ?, ?, ?, ?)', data)
    conn.commit()
    print(f"Database created: {db_path}")
    print(f"Inserted {cursor.execute('SELECT COUNT(*) FROM table_40457').fetchone()[0]} rows")
    conn.close()

if __name__ == "__main__":
    create_database()
