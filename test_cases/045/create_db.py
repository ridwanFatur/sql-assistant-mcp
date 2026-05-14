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
    cursor.execute('CREATE TABLE table_name_76 (termination_of_mission TEXT, appointed_by TEXT)')
    
    random.seed(76)
    presidents = ["Franklin Pierce", "James Buchanan", "Abraham Lincoln", "Andrew Johnson", "Ulysses Grant"]
    terminations = ["Recalled", "Resigned", "Died in Office", "Retired", "Dismissed", "End of Term"]
    
    data = []
    for i in range(12):
        term = random.choice(terminations)
        pres = random.choice(presidents)
        data.append((term, pres))
    
    data.append(("Resigned", "Franklin Pierce"))
    data.append(("Recalled", "Franklin Pierce"))
    
    cursor.executemany('INSERT INTO table_name_76 VALUES (?, ?)', data)
    conn.commit()
    print(f"Database created: {db_path}")
    print(f"Inserted {cursor.execute('SELECT COUNT(*) FROM table_name_76').fetchone()[0]} rows")
    conn.close()

if __name__ == "__main__":
    create_database()
