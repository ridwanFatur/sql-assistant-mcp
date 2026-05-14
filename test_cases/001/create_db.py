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
        CREATE TABLE table_name_89 (
            score TEXT,
            visitor TEXT,
            record TEXT
        )
        """
    )

    # Deterministic random data for additional variety
    random.seed(89)
    visitors = [
        "toronto",
        "montreal",
        "vancouver",
        "calgary",
        "edmonton",
        "ottawa",
    ]
    records = [
        "31-20-5",
        "18-25-7",
        "29-17-8",
        "23-19-10",
        "35-15-6",
        "27-21-9",
    ]
    scores = ["4-2", "3-1", "2-1", "5-4", "6-3", "1-0", "4-3"]

    sample_rows = set()
    while len(sample_rows) < 15:
        sample_rows.add(
            (
                random.choice(scores),
                random.choice(visitors),
                random.choice(records),
            )
        )

    # Ensure the row required by the question exists (unique answer)
    key_row = ("5-2", "toronto", "29-17-8")
    sample_rows.add(key_row)

    cursor.executemany(
        "INSERT INTO table_name_89 (score, visitor, record) VALUES (?, ?, ?)",
        list(sample_rows),
    )

    conn.commit()

    # Query table count for logging
    table_count = len(
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    )

    print(f"Database created: {db_path}")
    print(f"Created {table_count} table(s)")
    print(f"Inserted {cursor.execute('SELECT COUNT(*) FROM table_name_89').fetchone()[0]} rows")

    conn.close()


if __name__ == "__main__":
    create_database()
