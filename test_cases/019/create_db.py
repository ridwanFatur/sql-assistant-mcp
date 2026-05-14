import sqlite3
import os
import random


def create_database():
    """Create and populate the database with deterministic sample data."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "database.sqlite")

    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE table_name_15 (
            top_10 INTEGER,
            top_25 TEXT,
            wins TEXT
        )
        """
    )

    random.seed(15)
    
    player_data = []
    for i in range(15):
        top_10 = random.randint(1, 20)
        top_25 = str(random.randint(5, 30))
        wins = str(random.randint(0, 8))
        player_data.append((top_10, top_25, wins))
    
    # Ensure rows with top_25 > 11 and wins < 2 (answer: average of their top_10)
    # Add 3 rows: top_10 values 8, 10, 12 -> average = 10
    player_data.append((8, "15", "1"))
    player_data.append((10, "18", "0"))
    player_data.append((12, "20", "1"))

    cursor.executemany(
        'INSERT INTO table_name_15 (top_10, top_25, wins) VALUES (?, ?, ?)',
        player_data,
    )

    conn.commit()
    table_count = len(cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())
    print(f"Database created: {db_path}")
    print(f"Created {table_count} table(s)")
    print(f"Inserted {cursor.execute('SELECT COUNT(*) FROM table_name_15').fetchone()[0]} rows")
    conn.close()


if __name__ == "__main__":
    create_database()
