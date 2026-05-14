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
        CREATE TABLE table_66960 (
            "D 48" TEXT,
            "D 47" TEXT,
            "D 46" TEXT,
            "D 45" TEXT,
            "D 44" TEXT,
            "D 43" TEXT,
            "D 42" TEXT,
            "D 41" TEXT
        )
        """
    )

    random.seed(66960)
    values = ["d 10", "d 15", "d 20", "d 22", "d 25", "d 30", "d 35", "d 40"]
    
    data_rows = []
    for i in range(12):
        row = tuple(random.choice(values) for _ in range(8))
        data_rows.append(row)
    
    # Ensure specific row: D 42 = d 22, D 47 = d 35
    data_rows.append(("d 15", "d 35", "d 20", "d 25", "d 30", "d 10", "d 22", "d 40"))

    cursor.executemany(
        'INSERT INTO table_66960 ("D 48", "D 47", "D 46", "D 45", "D 44", "D 43", "D 42", "D 41") VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
        data_rows,
    )

    conn.commit()
    table_count = len(cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())
    print(f"Database created: {db_path}")
    print(f"Created {table_count} table(s)")
    print(f"Inserted {cursor.execute('SELECT COUNT(*) FROM table_66960').fetchone()[0]} rows")
    conn.close()


if __name__ == "__main__":
    create_database()
