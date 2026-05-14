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
        CREATE TABLE table_name_39 (
            name TEXT,
            current_age TEXT,
            years_on_death_row TEXT
        )
        """
    )

    random.seed(39)
    names = ["John Doe", "Mike Smith", "Robert Johnson", "David Williams", "James Brown", 
             "William Davis", "Richard Miller", "Thomas Wilson", "Charles Moore", "Joseph Taylor"]
    
    prisoners_data = []
    for name in names:
        age = random.randint(35, 65)
        years = random.randint(5, 30)
        prisoners_data.append((name, str(age), str(years)))
    
    # Ensure specific prisoner: older than 45 and less than 22 years on death row
    prisoners_data.append(("Daniel Anderson", "52", "18"))
    prisoners_data.append(("Michael Thompson", "48", "20"))

    cursor.executemany(
        'INSERT INTO table_name_39 (name, current_age, years_on_death_row) VALUES (?, ?, ?)',
        prisoners_data,
    )

    conn.commit()
    table_count = len(cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())
    print(f"Database created: {db_path}")
    print(f"Created {table_count} table(s)")
    print(f"Inserted {cursor.execute('SELECT COUNT(*) FROM table_name_39').fetchone()[0]} rows")
    conn.close()


if __name__ == "__main__":
    create_database()
