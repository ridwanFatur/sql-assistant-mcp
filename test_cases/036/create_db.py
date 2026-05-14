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
    cursor.execute('CREATE TABLE table_8438 ("Team 1" TEXT, "Agg." TEXT, "Team 2" TEXT, "1st leg" TEXT, "2nd leg" TEXT)')
    
    random.seed(8438)
    teams = ["Everton", "Liverpool", "Manchester", "Arsenal", "Chelsea", "Tottenham"]
    
    data = []
    for i in range(12):
        team1 = random.choice(teams)
        team2 = random.choice([t for t in teams if t != team1])
        leg1 = f"{random.randint(0,3)}-{random.randint(0,3)}"
        leg2 = f"{random.randint(0,3)}-{random.randint(0,3)}"
        agg = f"{random.randint(0,6)}-{random.randint(0,6)}"
        data.append((team1, agg, team2, leg1, leg2))
    
    data.append(("Everton", "3-2", "Liverpool", "2-1", "1-1"))
    
    cursor.executemany('INSERT INTO table_8438 VALUES (?, ?, ?, ?, ?)', data)
    conn.commit()
    print(f"Database created: {db_path}")
    print(f"Inserted {cursor.execute('SELECT COUNT(*) FROM table_8438').fetchone()[0]} rows")
    conn.close()

if __name__ == "__main__":
    create_database()
