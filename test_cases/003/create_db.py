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
        CREATE TABLE table_26006 (
            "Pos" REAL,
            "Driver" TEXT,
            "Starts" REAL,
            "Finishes" REAL,
            "Wins" REAL,
            "Podiums" REAL,
            "Stage wins" REAL,
            "Power stage wins" REAL,
            "Points" REAL
        )
        """
    )

    # Deterministic random data
    random.seed(26006)
    drivers = [
        "Hamilton",
        "Verstappen",
        "Leclerc",
        "Sainz",
        "Russell",
        "Norris",
        "Alonso",
        "Ocon",
        "Gasly",
        "Bottas",
    ]

    sample_rows = []
    for i, driver in enumerate(drivers):
        pos = i + 1
        starts = random.randint(15, 22)
        finishes = random.randint(10, starts)
        wins = random.randint(0, 5)
        podiums = random.randint(wins, 10)
        stage_wins = random.randint(0, 8)
        power_stage_wins = random.randint(0, 6)
        points = random.randint(50, 400)
        sample_rows.append(
            (pos, driver, starts, finishes, wins, podiums, stage_wins, power_stage_wins, points)
        )

    # Ensure a driver with exactly 2 points exists at a specific position
    key_row = (11, "Vettel", 18, 12, 0, 1, 2, 1, 2)
    sample_rows.append(key_row)

    cursor.executemany(
        """INSERT INTO table_26006 
           ("Pos", "Driver", "Starts", "Finishes", "Wins", "Podiums", "Stage wins", "Power stage wins", "Points") 
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        sample_rows,
    )

    conn.commit()

    # Query table count for logging
    table_count = len(
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    )

    print(f"Database created: {db_path}")
    print(f"Created {table_count} table(s)")
    print(f"Inserted {cursor.execute('SELECT COUNT(*) FROM table_26006').fetchone()[0]} rows")

    conn.close()


if __name__ == "__main__":
    create_database()
