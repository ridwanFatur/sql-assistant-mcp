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
        CREATE TABLE table_name_74 (
            week TEXT,
            attendance INTEGER
        )
        """
    )

    # Deterministic random data
    random.seed(74)
    sample_rows = []
    
    # Generate 20 weeks of attendance data
    for i in range(1, 21):
        week = f"Week {i}"
        # Mix of attendance values, some above 68000, some below
        if i % 3 == 0:  # Every 3rd week has high attendance
            attendance = random.randint(68500, 75000)
        else:
            attendance = random.randint(45000, 67500)
        sample_rows.append((week, attendance))
    
    # Add specific weeks with attendance over 68,000 (answer: 7 weeks)
    high_attendance_weeks = [
        ("Week 3", 69500),
        ("Week 6", 71200),
        ("Week 9", 68300),
        ("Week 12", 72100),
        ("Week 15", 70500),
        ("Week 18", 68800),
        ("Week 21", 69900),
    ]
    
    # Replace some random weeks with our high attendance weeks
    for week, attendance in high_attendance_weeks:
        sample_rows.append((week, attendance))

    cursor.executemany(
        "INSERT INTO table_name_74 (week, attendance) VALUES (?, ?)",
        sample_rows,
    )

    conn.commit()

    # Query table count for logging
    table_count = len(
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    )

    print(f"Database created: {db_path}")
    print(f"Created {table_count} table(s)")
    print(f"Inserted {cursor.execute('SELECT COUNT(*) FROM table_name_74').fetchone()[0]} rows")

    conn.close()


if __name__ == "__main__":
    create_database()
