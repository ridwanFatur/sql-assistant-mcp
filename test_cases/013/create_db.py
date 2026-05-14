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
        CREATE TABLE table_15407 (
            "Date" TEXT,
            "City" TEXT,
            "Event" TEXT,
            "Winner" TEXT,
            "Prize" TEXT
        )
        """
    )

    random.seed(15407)
    cities = ["Las Vegas", "Los Angeles", "New York", "Miami", "Chicago"]
    events = ["Poker Championship", "Blackjack Tournament", "Texas Hold'em", "World Series"]
    winners = ["Aaron Gustavson", "John Smith", "Mike Johnson", "Sarah Williams", "Tom Brown"]
    prizes = ["$50,000", "$75,000", "$100,000", "$125,000", "$150,000"]
    
    events_data = []
    for i in range(12):
        date = f"2023-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
        city = random.choice(cities)
        event = random.choice(events)
        winner = random.choice(winners)
        prize = random.choice(prizes)
        events_data.append((date, city, event, winner, prize))
    
    # Ensure Aaron Gustavson won on specific date
    events_data.append(("2023-06-15", "Las Vegas", "World Poker Tour", "Aaron Gustavson", "$200,000"))

    cursor.executemany(
        'INSERT INTO table_15407 ("Date", "City", "Event", "Winner", "Prize") VALUES (?, ?, ?, ?, ?)',
        events_data,
    )

    conn.commit()
    table_count = len(cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())
    print(f"Database created: {db_path}")
    print(f"Created {table_count} table(s)")
    print(f"Inserted {cursor.execute('SELECT COUNT(*) FROM table_15407').fetchone()[0]} rows")
    conn.close()


if __name__ == "__main__":
    create_database()
