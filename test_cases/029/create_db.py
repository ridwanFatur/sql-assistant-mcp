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
    
    cursor.execute('CREATE TABLE Ref_Detention_Type (detention_type_description TEXT, detention_type_code TEXT)')
    cursor.execute('CREATE TABLE Detention (detention_type_code TEXT)')
    
    random.seed(29)
    
    ref_data = [
        ("Administrative", "ADM"),
        ("Criminal", "CRM"),
        ("Civil", "CVL"),
        ("Temporary", "TMP"),
        ("Preventive", "PRV")
    ]
    cursor.executemany('INSERT INTO Ref_Detention_Type VALUES (?, ?)', ref_data)
    
    detention_data = []
    # Ensure CRM appears less frequently than others
    # Add multiple instances of other detention types
    for code in ["ADM", "CVL", "TMP"]:
        for _ in range(5):  # Each appears 5 times
            detention_data.append((code,))
    # Add two instances of PRV to ensure CRM is the least frequent
    detention_data.append(("PRV",))
    detention_data.append(("PRV",))
    # Add only one instance of CRM
    detention_data.append(("CRM",))
    
    cursor.executemany('INSERT INTO Detention VALUES (?)', detention_data)
    
    conn.commit()
    print(f"Database created: {db_path}")
    print(f"Ref_Detention_Type: {cursor.execute('SELECT COUNT(*) FROM Ref_Detention_Type').fetchone()[0]} rows")
    print(f"Detention: {cursor.execute('SELECT COUNT(*) FROM Detention').fetchone()[0]} rows")
    conn.close()

if __name__ == "__main__":
    create_database()
