import sqlite3
import os

def create_database():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "database.sqlite")
    if os.path.exists(db_path):
        os.remove(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('CREATE TABLE addresses (address_id REAL, address_content TEXT, city TEXT, zip_postcode TEXT, state_province_county TEXT, country TEXT, other_address_details TEXT)')
    cursor.execute('CREATE TABLE customers (customer_id REAL, payment_method TEXT, customer_name TEXT, date_became_customer TIME, other_customer_details TEXT)')
    cursor.execute('CREATE TABLE products (product_id REAL, product_details TEXT)')
    cursor.execute('CREATE TABLE customer_contact_channels (customer_id REAL, channel_code TEXT, active_from_date TIME, active_to_date TIME, contact_number TEXT)')
    cursor.execute('CREATE TABLE customer_orders (order_id REAL, customer_id REAL, order_status TEXT, order_date TIME, order_details TEXT)')
    cursor.execute('CREATE TABLE order_items (order_id REAL, product_id REAL, order_quantity TEXT)')
    cursor.execute('CREATE TABLE customer_addresses (customer_id REAL, address_id REAL, date_address_from TIME, address_type TEXT, date_address_to TIME)')
    
    cursor.executemany('INSERT INTO addresses VALUES (?, ?, ?, ?, ?, ?, ?)', [
        (1, '123 Main St', 'East Julianaside', '75001', 'Texas', 'USA', 'None'),
        (2, '456 Oak Ave', 'Gleasonmouth', '85001', 'Arizona', 'USA', 'None'),
        (3, '789 Pine Rd', 'New York', '10001', 'New York', 'USA', 'None')
    ])
    
    cursor.executemany('INSERT INTO customers VALUES (?, ?, ?, ?, ?)', [(1, 'Credit Card', 'John Doe', '2024-01-01', 'None')])
    cursor.executemany('INSERT INTO products VALUES (?, ?)', [(1, 'Product A')])
    cursor.executemany('INSERT INTO customer_contact_channels VALUES (?, ?, ?, ?, ?)', [(1, 'EMAIL', '2024-01-01', '2024-12-31', 'john@email.com')])
    cursor.executemany('INSERT INTO customer_orders VALUES (?, ?, ?, ?, ?)', [(1, 1, 'Completed', '2024-01-15', 'None')])
    cursor.executemany('INSERT INTO order_items VALUES (?, ?, ?)', [(1, 1, '2')])
    cursor.executemany('INSERT INTO customer_addresses VALUES (?, ?, ?, ?, ?)', [(1, 1, '2024-01-01', 'Home', '2024-12-31')])
    
    conn.commit()
    print(f"Database created: {db_path}")
    print(f"Addresses: {cursor.execute('SELECT COUNT(*) FROM addresses').fetchone()[0]} rows")
    conn.close()

if __name__ == "__main__":
    create_database()
