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
        CREATE TABLE table_name_98 (
            goals TEXT,
            appearances TEXT,
            crewe_alexandra_career TEXT,
            nationality TEXT,
            position TEXT
        )
        """
    )

    random.seed(98)
    nationalities = ["England", "Scotland", "Wales", "Ireland", "France", "Germany"]
    positions = ["FW", "MF", "DF", "GK"]
    
    data = []
    for i in range(15):
        goals = str(random.randint(0, 50))
        appearances = str(random.randint(50, 300))
        career = f"{random.randint(1950, 1980)} {random.randint(1960, 1990)}"
        nationality = random.choice(nationalities)
        position = random.choice(positions)
        data.append((goals, appearances, career, nationality, position))
    
    # Ensure specific row: England, DF, 1958-1962, <170 appearances, specific goals
    data.append(("15", "165", "1958 1962", "England", "DF"))
    data.append(("8", "120", "1958 1962", "England", "DF"))

    cursor.executemany(
        'INSERT INTO table_name_98 (goals, appearances, crewe_alexandra_career, nationality, position) VALUES (?, ?, ?, ?, ?)',
        data,
    )

    conn.commit()
    table_count = len(cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())
    print(f"Database created: {db_path}")
    print(f"Created {table_count} table(s)")
    print(f"Inserted {cursor.execute('SELECT COUNT(*) FROM table_name_98').fetchone()[0]} rows")
    conn.close()


if __name__ == "__main__":
    create_database()
