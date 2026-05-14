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
    cursor.execute('CREATE TABLE table_204_70 (id REAL, "pick #" REAL, "nfl team" TEXT, "player" TEXT, "position" TEXT, "college" TEXT)')
    
    random.seed(204)
    teams = ["Patriots", "Packers", "Cowboys", "49ers", "Ravens", "Steelers"]
    positions = ["QB", "RB", "WR", "OL", "DL", "LB"]
    colleges = ["Alabama", "Ohio State", "Clemson", "LSU", "Georgia", "Oklahoma"]
    
    data = []
    for i in range(1, 200):
        pick = i
        team = random.choice(teams)
        player = f"Player {i}"
        pos = random.choice(positions)
        college = random.choice(colleges)
        data.append((i, pick, team, player, pos, college))
    
    data.append((208, 208, "Patriots", "David Williams", "WR", "Alabama"))
    data.append((186, 186, "Packers", "Greg Schaum", "OL", "Ohio State"))
    
    cursor.executemany('INSERT INTO table_204_70 VALUES (?, ?, ?, ?, ?, ?)', data)
    conn.commit()
    print(f"Database created: {db_path}")
    print(f"Inserted {cursor.execute('SELECT COUNT(*) FROM table_204_70').fetchone()[0]} rows")
    conn.close()

if __name__ == "__main__":
    create_database()
