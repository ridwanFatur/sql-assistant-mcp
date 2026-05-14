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
    cursor.execute('CREATE TABLE table_204_700 (id REAL, "name" TEXT, "developer" TEXT, "release" TEXT, "type" TEXT, "game flow" TEXT, "setting" TEXT)')
    
    random.seed(204700)
    developers = ["EA Sports", "Activision", "Ubisoft", "Fubra", "Rockstar Games", "Bethesda"]
    types = ["Action", "RPG", "Strategy", "Sports", "Adventure", "Puzzle"]
    flows = ["Turn-based", "Real-time", "Hybrid"]
    settings = ["Fantasy", "Sci-Fi", "Modern", "Historical", "Post-Apocalyptic"]
    
    data = []
    for i in range(1, 15):
        game_id = i
        name = f"Game {i}"
        developer = random.choice(developers)
        release = f"20{random.randint(10, 23)}"
        game_type = random.choice(types)
        flow = random.choice(flows)
        setting = random.choice(settings)
        data.append((game_id, name, developer, release, game_type, flow, setting))
    
    data.append((15, "Mystery Quest", "Fubra", "2015", "Adventure", "Turn-based", "Fantasy"))
    
    cursor.executemany('INSERT INTO table_204_700 VALUES (?, ?, ?, ?, ?, ?, ?)', data)
    conn.commit()
    print(f"Database created: {db_path}")
    print(f"Inserted {cursor.execute('SELECT COUNT(*) FROM table_204_700').fetchone()[0]} rows")
    conn.close()

if __name__ == "__main__":
    create_database()
