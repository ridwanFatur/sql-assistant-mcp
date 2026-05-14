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
    cursor.execute('CREATE TABLE table_39155 ("Game" REAL, "October" REAL, "Opponent" TEXT, "Score" TEXT, "Record" TEXT, "Points" REAL)')
    
    random.seed(39155)
    opponents = ["Patriots", "Packers", "Cowboys", "49ers", "Ravens", "Steelers", "Chiefs"]
    records = ["8-2-0", "7-3-0", "6-4-0", "5-5-0", "9-1-0", "10-0-0"]
    
    data = []
    for i in range(1, 15):
        game = i
        october = random.randint(1, 31)
        opponent = random.choice(opponents)
        score = f"{random.randint(10, 35)}-{random.randint(0, 30)}"
        record = random.choice(records)
        points = random.randint(5, 25)
        data.append((game, october, opponent, score, record, points))
    
    data.append((5, 15, "Packers", "24-17", "8-2-0", 17))
    
    cursor.executemany('INSERT INTO table_39155 VALUES (?, ?, ?, ?, ?, ?)', data)
    conn.commit()
    print(f"Database created: {db_path}")
    print(f"Inserted {cursor.execute('SELECT COUNT(*) FROM table_39155').fetchone()[0]} rows")
    conn.close()

if __name__ == "__main__":
    create_database()
