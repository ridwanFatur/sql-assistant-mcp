import sqlite3
import os

def create_database():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "database.sqlite")
    if os.path.exists(db_path):
        os.remove(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('CREATE TABLE Apartment_Buildings (building_id INTEGER, building_short_name TEXT, building_full_name TEXT, building_description TEXT, building_address TEXT, building_manager TEXT, building_phone TEXT)')
    cursor.execute('CREATE TABLE Apartments (apt_id INTEGER, building_id INTEGER, apt_type_code TEXT, apt_number TEXT, bathroom_count INTEGER, bedroom_count INTEGER, room_count TEXT)')
    cursor.execute('CREATE TABLE Guests (guest_id INTEGER, gender_code TEXT, guest_first_name TEXT, guest_last_name TEXT, date_of_birth DATETIME)')
    cursor.execute('CREATE TABLE Apartment_Bookings (apt_booking_id INTEGER, apt_id INTEGER, guest_id INTEGER, booking_status_code TEXT, booking_start_date DATETIME, booking_end_date DATETIME)')
    cursor.execute('CREATE TABLE Apartment_Facilities (apt_id INTEGER, facility_code TEXT)')
    cursor.execute('CREATE TABLE View_Unit_Status (apt_id INTEGER, apt_booking_id INTEGER, status_date DATETIME, available_yn BIT)')
    
    cursor.executemany('INSERT INTO Apartment_Buildings VALUES (?, ?, ?, ?, ?, ?, ?)', [
        (1, 'Bldg A', 'Building A', 'Main building', '123 Main St', 'John Manager', '555-0001')
    ])
    
    cursor.executemany('INSERT INTO Apartments VALUES (?, ?, ?, ?, ?, ?, ?)', [
        (1, 1, 'Studio', '101', 1, 1, '2'),
        (2, 1, '1BR', '102', 1, 1, '3'),
        (3, 1, '2BR', '201', 2, 2, '4')
    ])
    
    cursor.executemany('INSERT INTO Guests VALUES (?, ?, ?, ?, ?)', [
        (1, 'M', 'John', 'Doe', '1990-01-01'),
        (2, 'F', 'Jane', 'Smith', '1992-05-15')
    ])
    
    cursor.executemany('INSERT INTO Apartment_Bookings VALUES (?, ?, ?, ?, ?, ?)', [
        (1, 1, 1, 'Confirmed', '2024-01-01', '2024-01-07'),
        (2, 1, 2, 'Confirmed', '2024-02-01', '2024-02-05'),
        (3, 2, 1, 'Confirmed', '2024-01-15', '2024-01-20'),
        (4, 3, 2, 'Confirmed', '2024-03-01', '2024-03-10')
    ])
    
    cursor.executemany('INSERT INTO Apartment_Facilities VALUES (?, ?)', [(1, 'GYM'), (2, 'POOL')])
    cursor.executemany('INSERT INTO View_Unit_Status VALUES (?, ?, ?, ?)', [(1, 1, '2024-01-01', 0)])
    
    conn.commit()
    print(f"Database created: {db_path}")
    print(f"Bookings: {cursor.execute('SELECT COUNT(*) FROM Apartment_Bookings').fetchone()[0]} rows")
    conn.close()

if __name__ == "__main__":
    create_database()
