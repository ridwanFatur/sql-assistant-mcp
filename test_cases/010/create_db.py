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
        CREATE TABLE table_12114 (
            "County" TEXT,
            "Per capita income" TEXT,
            "Median household income" TEXT,
            "Median family income" TEXT,
            "Population" REAL,
            "Number of households" REAL
        )
        """
    )

    # Deterministic random data
    random.seed(12114)
    counties = [
        "Valley County",
        "Mountain County",
        "River County",
        "Lake County",
        "Forest County",
        "Plains County",
        "Hill County",
        "Coastal County",
    ]

    sample_rows = []
    for county in counties:
        per_capita = f"${random.randint(25000, 55000):,}"
        median_household = f"${random.randint(45000, 85000):,}"
        median_family = f"${random.randint(55000, 95000):,}"
        population = random.randint(50000, 500000)
        households = int(population / random.uniform(2.3, 2.8))
        sample_rows.append(
            (county, per_capita, median_household, median_family, population, households)
        )

    # Ensure Valley County has specific median household income
    valley_row = ("Valley County", "$42,500", "$67,800", "$78,200", 125000, 48000)
    # Replace or add Valley County
    sample_rows = [row for row in sample_rows if row[0] != "Valley County"]
    sample_rows.append(valley_row)

    cursor.executemany(
        """INSERT INTO table_12114 
           ("County", "Per capita income", "Median household income", "Median family income", "Population", "Number of households") 
           VALUES (?, ?, ?, ?, ?, ?)""",
        sample_rows,
    )

    conn.commit()

    # Query table count for logging
    table_count = len(
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    )

    print(f"Database created: {db_path}")
    print(f"Created {table_count} table(s)")
    print(f"Inserted {cursor.execute('SELECT COUNT(*) FROM table_12114').fetchone()[0]} rows")

    conn.close()


if __name__ == "__main__":
    create_database()
