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
        CREATE TABLE table_1359212_2 (
            winner TEXT,
            second_place TEXT
        )
        """
    )

    random.seed(1359212)
    countries = ["United States", "Canada", "United Kingdom", "Germany", "France", 
                 "Australia", "Japan", "Brazil", "Italy", "Spain"]
    
    competitions_data = []
    for i in range(15):
        winner = random.choice(countries)
        second = random.choice([c for c in countries if c != winner])
        competitions_data.append((winner, second))
    
    # Ensure specific row: winner from United Kingdom
    competitions_data.append(("United Kingdom", "Germany"))
    competitions_data.append(("France", "United Kingdom"))
    competitions_data.append(("United States", "United Kingdom"))

    cursor.executemany(
        'INSERT INTO table_1359212_2 (winner, second_place) VALUES (?, ?)',
        competitions_data,
    )

    conn.commit()
    table_count = len(cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())
    print(f"Database created: {db_path}")
    print(f"Created {table_count} table(s)")
    print(f"Inserted {cursor.execute('SELECT COUNT(*) FROM table_1359212_2').fetchone()[0]} rows")
    conn.close()


if __name__ == "__main__":
    create_database()
