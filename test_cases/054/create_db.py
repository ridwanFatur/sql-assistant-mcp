import sqlite3
import os

def create_database():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "database.sqlite")
    if os.path.exists(db_path):
        os.remove(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('CREATE TABLE regions (REGION_ID REAL, REGION_NAME TEXT)')
    cursor.execute('CREATE TABLE countries (COUNTRY_ID TEXT, COUNTRY_NAME TEXT, REGION_ID REAL)')
    cursor.execute('CREATE TABLE locations (LOCATION_ID REAL, STREET_ADDRESS TEXT, POSTAL_CODE TEXT, CITY TEXT, STATE_PROVINCE TEXT, COUNTRY_ID TEXT)')
    cursor.execute('CREATE TABLE departments (DEPARTMENT_ID REAL, DEPARTMENT_NAME TEXT, MANAGER_ID REAL, LOCATION_ID REAL)')
    cursor.execute('CREATE TABLE jobs (JOB_ID TEXT, JOB_TITLE TEXT, MIN_SALARY REAL, MAX_SALARY REAL)')
    cursor.execute('CREATE TABLE employees (EMPLOYEE_ID REAL, FIRST_NAME TEXT, LAST_NAME TEXT, EMAIL TEXT, PHONE_NUMBER TEXT, HIRE_DATE DATE, JOB_ID TEXT, SALARY REAL, COMMISSION_PCT REAL, MANAGER_ID REAL, DEPARTMENT_ID REAL)')
    cursor.execute('CREATE TABLE job_history (EMPLOYEE_ID REAL, START_DATE DATE, END_DATE DATE, JOB_ID TEXT, DEPARTMENT_ID REAL)')
    
    cursor.executemany('INSERT INTO regions VALUES (?, ?)', [(1, 'Europe'), (2, 'Americas'), (3, 'Asia')])
    cursor.executemany('INSERT INTO countries VALUES (?, ?, ?)', [('US', 'United States', 2), ('UK', 'United Kingdom', 1), ('CN', 'China', 3)])
    cursor.executemany('INSERT INTO locations VALUES (?, ?, ?, ?, ?, ?)', [(1, '123 Main St', '10001', 'New York', 'NY', 'US'), (2, '456 Oak Ave', 'SW1A', 'London', 'England', 'UK')])
    cursor.executemany('INSERT INTO departments VALUES (?, ?, ?, ?)', [(10, 'IT', 250, 1), (20, 'Sales', 300, 1), (30, 'HR', 150, 2)])
    cursor.executemany('INSERT INTO jobs VALUES (?, ?, ?, ?)', [('IT_PROG', 'Programmer', 40000, 120000), ('SA_REP', 'Sales Rep', 30000, 80000)])
    
    employees_data = [
        (101, 'John', 'Doe', 'jdoe@email.com', '555-0101', '2020-01-15', 'IT_PROG', 75000, None, None, 10),
        (102, 'Jane', 'Smith', 'jsmith@email.com', '555-0102', '2020-03-22', 'IT_PROG', 80000, None, None, 10),
        (103, 'Bob', 'Johnson', 'bjohnson@email.com', '555-0103', '2021-05-10', 'SA_REP', 60000, 0.1, None, 20),
        (104, 'Alice', 'Williams', 'awilliams@email.com', '555-0104', '2021-07-18', 'IT_PROG', 85000, None, None, 30),
        (105, 'Charlie', 'Brown', 'cbrown@email.com', '555-0105', '2022-02-28', 'SA_REP', 55000, 0.15, None, 30)
    ]
    cursor.executemany('INSERT INTO employees VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', employees_data)
    
    cursor.executemany('INSERT INTO job_history VALUES (?, ?, ?, ?, ?)', [(101, '2018-01-01', '2019-12-31', 'IT_PROG', 10)])
    
    conn.commit()
    print(f"Database created: {db_path}")
    print(f"Employees: {cursor.execute('SELECT COUNT(*) FROM employees').fetchone()[0]} rows")
    conn.close()

if __name__ == "__main__":
    create_database()
