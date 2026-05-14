import sqlite3
import os

def create_database():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "database.sqlite")
    if os.path.exists(db_path):
        os.remove(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('CREATE TABLE Customers (customer_id INTEGER, customer_first_name TEXT, customer_middle_initial TEXT, customer_last_name TEXT, gender TEXT, email_address TEXT, login_name TEXT, login_password TEXT, phone_number TEXT, town_city TEXT, state_county_province TEXT, country TEXT)')
    cursor.execute('CREATE TABLE Accounts (account_id INTEGER, customer_id INTEGER, date_account_opened DATETIME, account_name TEXT, other_account_details TEXT)')
    cursor.execute('CREATE TABLE Orders (order_id INTEGER, customer_id INTEGER, date_order_placed DATETIME, order_details TEXT)')
    cursor.execute('CREATE TABLE Products (product_id INTEGER, parent_product_id INTEGER, production_type_code TEXT, unit_price REAL, product_name TEXT, product_color TEXT, product_size TEXT)')
    cursor.execute('CREATE TABLE Product_Categories (production_type_code TEXT, product_type_description TEXT, vat_rating REAL)')
    cursor.execute('CREATE TABLE Order_Items (order_item_id INTEGER, order_id INTEGER, product_id INTEGER, product_quantity TEXT, other_order_item_details TEXT)')
    cursor.execute('CREATE TABLE Invoices (invoice_number INTEGER, order_id INTEGER, invoice_date DATETIME)')
    cursor.execute('CREATE TABLE Invoice_Line_Items (order_item_id INTEGER, invoice_number INTEGER, product_id INTEGER, product_title TEXT, product_quantity TEXT, product_price REAL, derived_product_cost REAL, derived_vat_payable REAL, derived_total_cost REAL)')
    cursor.execute('CREATE TABLE Financial_Transactions (transaction_id INTEGER, account_id INTEGER, invoice_number INTEGER, transaction_type TEXT, transaction_date DATETIME, transaction_amount REAL, transaction_comment TEXT, other_transaction_details TEXT)')
    
    cursor.executemany('INSERT INTO Customers VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', [
        (1, 'Meaghan', 'A', 'Smith', 'F', 'meaghan@email.com', 'msmith', 'pass123', '555-0001', 'New York', 'NY', 'USA'),
        (2, 'John', 'B', 'Doe', 'M', 'john@email.com', 'jdoe', 'pass456', '555-0002', 'Boston', 'MA', 'USA')
    ])
    
    cursor.executemany('INSERT INTO Accounts VALUES (?, ?, ?, ?, ?)', [
        (1, 1, '2024-01-15', 'Checking', 'Main account'),
        (2, 1, '2024-01-16', 'Savings', 'Secondary'),
        (3, 1, '2024-01-20', 'Investment', 'Long term'),
        (4, 2, '2024-02-01', 'Checking', 'Primary')
    ])
    
    cursor.executemany('INSERT INTO Product_Categories VALUES (?, ?, ?)', [('ELEC', 'Electronics', 0.2)])
    cursor.executemany('INSERT INTO Products VALUES (?, ?, ?, ?, ?, ?, ?)', [(1, None, 'ELEC', 99.99, 'Laptop', 'Black', 'Medium')])
    cursor.executemany('INSERT INTO Orders VALUES (?, ?, ?, ?)', [(1, 1, '2024-01-15', 'First order')])
    cursor.executemany('INSERT INTO Order_Items VALUES (?, ?, ?, ?, ?)', [(1, 1, 1, '2', 'None')])
    cursor.executemany('INSERT INTO Invoices VALUES (?, ?, ?)', [(1, 1, '2024-01-15')])
    cursor.executemany('INSERT INTO Invoice_Line_Items VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', [(1, 1, 1, 'Laptop', '2', 99.99, 199.98, 39.996, 239.976)])
    cursor.executemany('INSERT INTO Financial_Transactions VALUES (?, ?, ?, ?, ?, ?, ?, ?)', [(1, 1, 1, 'Payment', '2024-01-15', 239.98, 'Paid', 'None')])
    
    conn.commit()
    print(f"Database created: {db_path}")
    print(f"Accounts: {cursor.execute('SELECT COUNT(*) FROM Accounts').fetchone()[0]} rows")
    conn.close()

if __name__ == "__main__":
    create_database()
