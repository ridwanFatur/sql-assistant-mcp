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
        CREATE TABLE table_30476 (
            "Club" TEXT,
            "Location" TEXT,
            "Home Venue" TEXT,
            "Capacity" TEXT,
            "Founded" REAL,
            "Years Active" TEXT
        )
        """
    )

    random.seed(30476)
    clubs_data = [
        ("New Zealand Breakers", "Auckland", "Vector Arena", "12,000", 2003, "2003-present"),
        ("Sydney Kings", "Sydney", "Qudos Bank Arena", "21,032", 1988, "1988-present"),
        ("Melbourne United", "Melbourne", "John Cain Arena", "10,500", 1984, "1984-present"),
        ("Perth Wildcats", "Perth", "RAC Arena", "13,611", 1982, "1982-present"),
        ("Adelaide 36ers", "Adelaide", "Adelaide Entertainment Centre", "8,000", 1982, "1982-present"),
    ]

    cursor.executemany(
        'INSERT INTO table_30476 ("Club", "Location", "Home Venue", "Capacity", "Founded", "Years Active") VALUES (?, ?, ?, ?, ?, ?)',
        clubs_data,
    )

    conn.commit()
    table_count = len(cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())
    print(f"Database created: {db_path}")
    print(f"Created {table_count} table(s)")
    print(f"Inserted {cursor.execute('SELECT COUNT(*) FROM table_30476').fetchone()[0]} rows")
    conn.close()


if __name__ == "__main__":
    create_database()
