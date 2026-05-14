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
        CREATE TABLE table_203_282 (
            id REAL,
            "date" TEXT,
            "racecourse" TEXT,
            "distance" TEXT,
            "race status" TEXT,
            "race" TEXT,
            "position" TEXT,
            "winning distance  ( lengths ) " REAL,
            "jockey" TEXT,
            "rating" REAL,
            "going" TEXT,
            "odds" TEXT,
            "prize money" TEXT
        )
        """
    )

    random.seed(203282)
    racecourses = ["Ascot", "Epsom", "Newmarket", "Goodwood", "Royal Ascot"]
    races = ["Soviet Song", "Northern Dancer", "Secretariat", "Man O War", "Citation"]
    jockeys = ["Willie Carson", "Lester Piggott", "Steve Cauthen", "Bill Shoemaker"]
    going_types = ["Good", "Firm", "Soft", "Heavy"]
    
    data = []
    for i in range(1, 16):
        date = f"2004-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
        racecourse = random.choice(racecourses)
        distance = f"{random.randint(5, 20)} furlongs"
        race_status = "Completed"
        race = random.choice(races)
        position = str(random.randint(1, 10))
        winning_distance = random.uniform(0.5, 5.0)
        jockey = random.choice(jockeys)
        rating = random.randint(70, 95)
        going = random.choice(going_types)
        odds = f"{random.randint(2, 20)}/1"
        prize_money = f"£{random.randint(5000, 50000):,}"
        data.append((i, date, racecourse, distance, race_status, race, position, winning_distance, jockey, rating, going, odds, prize_money))
    
    # Ensure Soviet Song with largest prize in 2004
    data.append((16, "2004-06-15", "Royal Ascot", "12 furlongs", "Completed", "Soviet Song", "1", 2.5, "Willie Carson", 92, "Good", "3/1", "£100,000"))

    cursor.executemany(
        'INSERT INTO table_203_282 (id, "date", "racecourse", "distance", "race status", "race", "position", "winning distance  ( lengths ) ", "jockey", "rating", "going", "odds", "prize money") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        data,
    )

    conn.commit()
    table_count = len(cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())
    print(f"Database created: {db_path}")
    print(f"Created {table_count} table(s)")
    print(f"Inserted {cursor.execute('SELECT COUNT(*) FROM table_203_282').fetchone()[0]} rows")
    conn.close()


if __name__ == "__main__":
    create_database()
