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
        CREATE TABLE table_name_64 (
            scored INTEGER,
            competition TEXT,
            date TEXT
        )
        """
    )

    random.seed(64)
    competitions = ["Long Teng Cup", "Asian Cup", "World Cup", "Olympic Games", "Regional Championship"]
    
    data = []
    for i in range(15):
        scored = random.randint(0, 5)
        competition = random.choice(competitions)
        date = f"{random.randint(1, 12):02d} {random.choice(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])} {random.randint(2000, 2020)}"
        data.append((scored, competition, date))
    
    # Ensure specific rows: 2011 Long Teng Cup and 2 October 2011
    data.append((3, "Long Teng Cup", "2 October 2011"))
    data.append((2, "Long Teng Cup", "2 October 2011"))

    cursor.executemany(
        'INSERT INTO table_name_64 (scored, competition, date) VALUES (?, ?, ?)',
        data,
    )

    conn.commit()
    table_count = len(cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())
    print(f"Database created: {db_path}")
    print(f"Created {table_count} table(s)")
    print(f"Inserted {cursor.execute('SELECT COUNT(*) FROM table_name_64').fetchone()[0]} rows")
    conn.close()


if __name__ == "__main__":
    create_database()
