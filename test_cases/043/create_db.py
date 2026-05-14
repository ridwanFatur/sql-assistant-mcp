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
    cursor.execute('CREATE TABLE table_50429 ("Track" REAL, "Song" TEXT, "Author" TEXT, "Worship Leader" TEXT, "Lead Supporting Vocal" TEXT, "Time" TEXT)')
    
    random.seed(50429)
    leaders = ["John Smith", "Mary Johnson", "David Williams", "Sarah Brown", "James Davis"]
    vocals = ["Alice", "Bob", "Carol", "David", "Eve"]
    songs = ["Amazing Grace", "How Great Thou Art", "Jesus Loves Me", "Holy Holy Holy", "Great Is Thy Faithfulness"]
    
    data = []
    for i in range(1, 15):
        track = i
        song = random.choice(songs)
        author = random.choice(leaders)
        leader = random.choice(leaders)
        vocal = random.choice(vocals)
        time = f"{random.randint(3, 8)}:{random.randint(0, 59):02d}"
        data.append((track, song, author, leader, vocal, time))
    
    data.append((15, "Praise Song", "Unknown", "John Smith", "Alice", "7:05"))
    
    cursor.executemany('INSERT INTO table_50429 VALUES (?, ?, ?, ?, ?, ?)', data)
    conn.commit()
    print(f"Database created: {db_path}")
    print(f"Inserted {cursor.execute('SELECT COUNT(*) FROM table_50429').fetchone()[0]} rows")
    conn.close()

if __name__ == "__main__":
    create_database()
