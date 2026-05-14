import sqlite3
import os
import random


def create_database():
    """Create and populate the database with deterministic sample data."""
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "database.sqlite")

    # Remove existing database if present
    if os.path.exists(db_path):
        os.remove(db_path)

    # Connect to database (will create if not exists)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create table
    cursor.execute(
        """
        CREATE TABLE table_name_28 (
            built_as TEXT,
            ship TEXT
        )
        """
    )

    # Deterministic random data
    random.seed(28)
    ship_types = ["Destroyer", "Cruiser", "Carrier", "Battleship", "Frigate", "Submarine"]
    ship_names = [
        "Dahlgren",
        "USS Arizona",
        "HMS Victory",
        "USS Enterprise",
        "Bismarck",
        "Yamato",
        "USS Missouri",
        "HMS Hood",
        "USS Nimitz",
        "USS Iowa",
    ]

    sample_rows = set()
    while len(sample_rows) < 12:
        sample_rows.add((random.choice(ship_types), random.choice(ship_names)))

    # Ensure the row required by the question exists
    key_row = ("Destroyer", "Dahlgren")
    sample_rows.add(key_row)

    cursor.executemany(
        "INSERT INTO table_name_28 (built_as, ship) VALUES (?, ?)",
        list(sample_rows),
    )

    conn.commit()

    # Query table count for logging
    table_count = len(
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    )

    print(f"Database created: {db_path}")
    print(f"Created {table_count} table(s)")
    print(f"Inserted {cursor.execute('SELECT COUNT(*) FROM table_name_28').fetchone()[0]} rows")

    conn.close()


if __name__ == "__main__":
    create_database()
