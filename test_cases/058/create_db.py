import sqlite3
import os

def create_database():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "database.sqlite")
    if os.path.exists(db_path):
        os.remove(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('CREATE TABLE Addresses (address_id INTEGER, line_1_number_building TEXT, city TEXT, zip_postcode TEXT, state_province_county TEXT, country TEXT)')
    cursor.execute('CREATE TABLE Customers (customer_id INTEGER, customer_address_id INTEGER, customer_status_code TEXT, date_became_customer DATETIME, date_of_birth DATETIME, first_name TEXT, last_name TEXT, amount_outstanding REAL, email_address TEXT, phone_number TEXT, cell_mobile_phone_number TEXT)')
    cursor.execute('CREATE TABLE Staff (staff_id INTEGER, staff_address_id INTEGER, nickname TEXT, first_name TEXT, middle_name TEXT, last_name TEXT, date_of_birth DATETIME, date_joined_staff DATETIME, date_left_staff DATETIME)')
    cursor.execute('CREATE TABLE Vehicles (vehicle_id INTEGER, vehicle_details TEXT)')
    cursor.execute('CREATE TABLE Lessons (lesson_id INTEGER, customer_id INTEGER, lesson_status_code TEXT, staff_id INTEGER, vehicle_id INTEGER, lesson_date DATETIME, lesson_time TEXT, price REAL)')
    cursor.execute('CREATE TABLE Customer_Payments (customer_id INTEGER, datetime_payment DATETIME, payment_method_code TEXT, amount_payment REAL)')
    
    cursor.executemany('INSERT INTO Addresses VALUES (?, ?, ?, ?, ?, ?)', [(1, '123 Main', 'NYC', '10001', 'NY', 'USA')])
    
    cursor.executemany('INSERT INTO Customers VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', [
        (1, 1, 'Active', '2024-01-01', '1990-01-01', 'John', 'Doe', 0, 'john@email.com', '555-0001', '555-0001'),
        (2, 1, 'Active', '2024-01-02', '1992-05-15', 'Jane', 'Smith', 100, 'jane@email.com', '555-0002', '555-0002'),
        (3, 1, 'Inactive', '2024-01-03', '1988-03-20', 'Bob', 'Johnson', 50, 'bob@email.com', '555-0003', '555-0003')
    ])
    
    cursor.executemany('INSERT INTO Staff VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', [(1, 1, 'Mike', 'Michael', 'A', 'Brown', '1985-01-01', '2020-01-01', None)])
    cursor.executemany('INSERT INTO Vehicles VALUES (?, ?)', [(1, 'Toyota Camry')])
    cursor.executemany('INSERT INTO Lessons VALUES (?, ?, ?, ?, ?, ?, ?, ?)', [(1, 1, 'Completed', 1, 1, '2024-01-15', '10:00', 50.0)])
    cursor.executemany('INSERT INTO Customer_Payments VALUES (?, ?, ?, ?)', [(1, '2024-01-15', 'Cash', 50.0)])
    
    conn.commit()
    print(f"Database created: {db_path}")
    print(f"Customers: {cursor.execute('SELECT COUNT(*) FROM Customers').fetchone()[0]} rows")
    conn.close()

if __name__ == "__main__":
    create_database()
