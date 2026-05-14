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
        CREATE TABLE table_203_692 (
            id REAL,
            "name" TEXT,
            "pos." TEXT,
            "caps" REAL,
            "goals" REAL,
            "club" TEXT
        )
        """
    )

    random.seed(203692)
    positions = ["FW", "MF", "DF", "GK"]
    clubs = ["AIK", "IFK Göteborg", "Malmö FF", "Hammarby", "Djurgården", "Helsingborg"]
    
    players_data = []
    for i in range(1, 16):
        name = f"Player {i}"
        pos = random.choice(positions)
        caps = random.randint(5, 100)
        goals = random.randint(0, 30)
        club = random.choice(clubs)
        players_data.append((i, name, pos, caps, goals, club))
    
    # Ensure Olle Ahlund exists with specific club and position
    players_data.append((16, "Olle Ahlund", "MF", 45, 12, "IFK Göteborg"))

    cursor.executemany(
        'INSERT INTO table_203_692 (id, "name", "pos.", "caps", "goals", "club") VALUES (?, ?, ?, ?, ?, ?)',
        players_data,
    )

    conn.commit()
    table_count = len(cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())
    print(f"Database created: {db_path}")
    print(f"Created {table_count} table(s)")
    print(f"Inserted {cursor.execute('SELECT COUNT(*) FROM table_203_692').fetchone()[0]} rows")
    conn.close()


if __name__ == "__main__":
    create_database()
