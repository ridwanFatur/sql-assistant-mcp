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
        CREATE TABLE table_name_8 (
            result TEXT,
            location TEXT,
            year TEXT
        )
        """
    )

    random.seed(8)
    locations = ["Warsaw", "Berlin", "Prague", "Vienna", "Budapest", "Moscow", "Krakow"]
    results = ["Win", "Loss", "Draw", "1-0", "2-1", "0-0", "3-2"]
    
    data = []
    for i in range(15):
        result = random.choice(results)
        location = random.choice(locations)
        year = str(random.randint(1920, 1940))
        data.append((result, location, year))
    
    # Ensure specific row: Warsaw 1929
    data.append(("2-1", "Warsaw", "1929"))

    cursor.executemany(
        'INSERT INTO table_name_8 (result, location, year) VALUES (?, ?, ?)',
        data,
    )

    conn.commit()
    table_count = len(cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())
    print(f"Database created: {db_path}")
    print(f"Created {table_count} table(s)")
    print(f"Inserted {cursor.execute('SELECT COUNT(*) FROM table_name_8').fetchone()[0]} rows")
    conn.close()


if __name__ == "__main__":
    create_database()
