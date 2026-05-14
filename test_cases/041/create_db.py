import sqlite3
import os
import random

def create_database():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "database.sqlite")
    if os.path.exists(db_path):
        os.remove(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE products_for_hire (product_type_code TEXT)')
    
    random.seed(41)
    types = ["PT001", "PT002", "PT003", "PT004", "PT005", "PT006", "PT007", "PT008"]
    
    data = [(random.choice(types),) for _ in range(20)]
    
    cursor.executemany('INSERT INTO products_for_hire VALUES (?)', data)
    conn.commit()
    print(f"Database created: {db_path}")
    print(f"Inserted {cursor.execute('SELECT COUNT(*) FROM products_for_hire').fetchone()[0]} rows")
    conn.close()

if __name__ == "__main__":
    create_database()
