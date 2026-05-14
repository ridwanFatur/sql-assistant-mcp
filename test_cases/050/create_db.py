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
    cursor.execute('CREATE TABLE table_28215780_4 (title TEXT, written_by TEXT)')
    
    random.seed(28215780)
    writers = ["Aron Eli Coleite", "Andrew Kreisberg", "Greg Berlanti", "Marc Guggenheim", "Geoff Johns"]
    episodes = ["Pilot", "Fastest Man Alive", "Things You Can't Outrun", "Going Rogue", "Plastique", "The Flash is Born"]
    
    data = []
    for i in range(12):
        title = random.choice(episodes)
        writer = random.choice(writers)
        data.append((title, writer))
    
    data.append(("Fastest Man Alive", "Aron Eli Coleite"))
    data.append(("Going Rogue", "Aron Eli Coleite"))
    
    cursor.executemany('INSERT INTO table_28215780_4 VALUES (?, ?)', data)
    conn.commit()
    print(f"Database created: {db_path}")
    print(f"Inserted {cursor.execute('SELECT COUNT(*) FROM table_28215780_4').fetchone()[0]} rows")
    conn.close()

if __name__ == "__main__":
    create_database()
