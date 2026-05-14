import sqlite3
import os

def create_database():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "database.sqlite")
    if os.path.exists(db_path):
        os.remove(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('CREATE TABLE stadium (ID INTEGER, name TEXT, Capacity INTEGER, City TEXT, Country TEXT, Opening_year INTEGER)')
    cursor.execute('CREATE TABLE event (ID INTEGER, Name TEXT, Stadium_ID INTEGER, Year TEXT)')
    cursor.execute('CREATE TABLE swimmer (ID INTEGER, name TEXT, Nationality TEXT, meter_100 REAL, meter_200 TEXT, meter_300 TEXT, meter_400 TEXT, meter_500 TEXT, meter_600 TEXT, meter_700 TEXT, Time TEXT)')
    cursor.execute('CREATE TABLE record (ID INTEGER, Result TEXT, Swimmer_ID INTEGER, Event_ID INTEGER)')
    
    cursor.executemany('INSERT INTO stadium VALUES (?, ?, ?, ?, ?, ?)', [
        (1, 'Olympic Pool', 5000, 'Beijing', 'China', 2008)
    ])
    
    cursor.executemany('INSERT INTO event VALUES (?, ?, ?, ?)', [
        (1, '100m Freestyle', 1, '2024')
    ])
    
    cursor.executemany('INSERT INTO swimmer VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', [
        (1, 'Michael Phelps', 'USA', 47.5, '1:54', '2:45', '3:40', '4:35', '5:30', '6:25', '10:00'),
        (2, 'Ian Thorpe', 'AUS', 48.2, '1:56', '2:48', '3:42', '4:38', '5:32', '6:28', '10:30'),
        (3, 'Ryan Lochte', 'USA', 48.8, '1:58', '2:50', '3:45', '4:40', '5:35', '6:30', '11:00')
    ])
    
    cursor.executemany('INSERT INTO record VALUES (?, ?, ?, ?)', [
        (1, 'Gold', 1, 1),
        (2, 'Silver', 2, 1)
    ])
    
    conn.commit()
    print(f"Database created: {db_path}")
    print(f"Swimmers: {cursor.execute('SELECT COUNT(*) FROM swimmer').fetchone()[0]} rows")
    conn.close()

if __name__ == "__main__":
    create_database()
