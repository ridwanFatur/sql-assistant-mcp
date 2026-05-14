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
        CREATE TABLE table_51663 (
            "Tournament" TEXT,
            "Wins" REAL,
            "Top-10" REAL,
            "Top-25" REAL,
            "Events" REAL,
            "Cuts made" REAL
        )
        """
    )

    random.seed(51663)
    tournaments = ["Masters", "US Open", "British Open", "PGA Championship", 
                   "Players Championship", "WGC Match Play", "Memorial Tournament"]
    
    tournament_data = []
    for tournament in tournaments:
        wins = random.randint(0, 5)
        top_10 = random.randint(wins, 15)
        top_25 = random.randint(top_10, 25)
        events = random.randint(20, 50)
        cuts_made = random.randint(10, events)
        tournament_data.append((tournament, wins, top_10, top_25, events, cuts_made))
    
    # Ensure specific tournament with 4 Top-25 and highest cuts (answer: Masters with 35 cuts)
    tournament_data.append(("Masters", 2, 3, 4, 40, 35))
    tournament_data.append(("US Open", 1, 2, 4, 38, 28))
    tournament_data.append(("British Open", 0, 1, 4, 42, 30))

    cursor.executemany(
        'INSERT INTO table_51663 ("Tournament", "Wins", "Top-10", "Top-25", "Events", "Cuts made") VALUES (?, ?, ?, ?, ?, ?)',
        tournament_data,
    )

    conn.commit()
    table_count = len(cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())
    print(f"Database created: {db_path}")
    print(f"Created {table_count} table(s)")
    print(f"Inserted {cursor.execute('SELECT COUNT(*) FROM table_51663').fetchone()[0]} rows")
    conn.close()


if __name__ == "__main__":
    create_database()
