import sqlite3
import os
import random
from datetime import datetime, timedelta


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
        CREATE TABLE table_33880 (
            "Date" TEXT,
            "Opponent" TEXT,
            "Score" TEXT,
            "Loss" TEXT,
            "Record" TEXT
        )
        """
    )

    random.seed(33880)
    opponents = ["Red Sox", "Yankees", "Blue Jays", "Orioles", "Rays", "Tigers", "Indians"]
    scores = ["4-2", "3-1", "5-3", "2-1", "6-4", "3-2", "7-5"]
    pitchers = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller"]
    
    games_data = []
    start_date = datetime(2023, 4, 1)
    wins = 0
    losses = 0
    
    for i in range(15):
        date = (start_date + timedelta(days=i*3)).strftime("%B %d")
        opponent = random.choice(opponents)
        score = random.choice(scores)
        pitcher = random.choice(pitchers)
        
        # Determine if win or loss
        score_parts = score.split("-")
        if int(score_parts[0]) > int(score_parts[1]):
            wins += 1
        else:
            losses += 1
        
        record = f"{wins}-{losses}"
        games_data.append((date, opponent, score, pitcher, record))
    
    # Ensure specific row for question: Score of 3-2 had what record?
    games_data.append(("May 15", "Mariners", "3-2", "Anderson", "12-8"))

    cursor.executemany(
        'INSERT INTO table_33880 ("Date", "Opponent", "Score", "Loss", "Record") VALUES (?, ?, ?, ?, ?)',
        games_data,
    )

    conn.commit()
    table_count = len(cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())
    print(f"Database created: {db_path}")
    print(f"Created {table_count} table(s)")
    print(f"Inserted {cursor.execute('SELECT COUNT(*) FROM table_33880').fetchone()[0]} rows")
    conn.close()


if __name__ == "__main__":
    create_database()
