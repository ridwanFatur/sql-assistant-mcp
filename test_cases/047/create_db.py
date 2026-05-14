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
    cursor.execute('CREATE TABLE table_name_85 (class TEXT, laps TEXT, team TEXT)')
    
    random.seed(85)
    classes = ["GT1", "GT2", "LMP1", "LMP2", "Formula 3"]
    teams = ["Liqui Moly Equipe", "Ferrari Racing", "Porsche Team", "BMW Motorsport", "Audi Sport"]
    
    data = []
    for i in range(15):
        cls = random.choice(classes)
        laps = str(random.randint(50, 150))
        team = random.choice(teams)
        data.append((cls, laps, team))
    
    data.append(("GT1", "65", "Liqui Moly Equipe"))
    data.append(("GT2", "70", "Liqui Moly Equipe"))
    
    cursor.executemany('INSERT INTO table_name_85 VALUES (?, ?, ?)', data)
    conn.commit()
    print(f"Database created: {db_path}")
    print(f"Inserted {cursor.execute('SELECT COUNT(*) FROM table_name_85').fetchone()[0]} rows")
    conn.close()

if __name__ == "__main__":
    create_database()
