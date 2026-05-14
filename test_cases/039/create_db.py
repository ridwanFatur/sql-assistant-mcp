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
    cursor.execute('CREATE TABLE table_20037 ("Position" REAL, "Team" TEXT, "Points" REAL, "Played" REAL, "Won" REAL, "Drawn" REAL, "Lost" REAL, "For" REAL, "Against" REAL, "Difference" TEXT)')
    
    random.seed(20037)
    teams = ["Arsenal", "Chelsea", "Liverpool", "Man United", "Tottenham", "Man City"]
    
    data = []
    for i in range(1, 13):
        pos = i
        team = teams[i-1] if i <= len(teams) else f"Team {i}"
        points = random.randint(30, 90)
        played = random.randint(30, 38)
        won = random.randint(5, 30)
        drawn = random.randint(0, 10)
        lost = random.randint(0, 15)
        for_val = random.randint(30, 80)
        against = random.randint(20, 60)
        diff = str(for_val - against)
        data.append((pos, team, points, played, won, drawn, lost, for_val, against, diff))
    
    data.append((8, "Everton", 45, 38, 12, 9, 17, 48, 60, "-12"))
    data.append((9, "Brighton", 42, 38, 11, 9, 18, 45, 62, "-17"))
    
    cursor.executemany('INSERT INTO table_20037 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', data)
    conn.commit()
    print(f"Database created: {db_path}")
    print(f"Inserted {cursor.execute('SELECT COUNT(*) FROM table_20037').fetchone()[0]} rows")
    conn.close()

if __name__ == "__main__":
    create_database()
