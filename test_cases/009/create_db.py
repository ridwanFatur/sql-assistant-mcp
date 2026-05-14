import sqlite3
import os

def create_database():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "database.sqlite")
    if os.path.exists(db_path):
        os.remove(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    

    cursor.execute('CREATE TABLE patients (row_id INTEGER, subject_id INTEGER, gender TEXT, dob TEXT, dod TEXT)')
    cursor.execute('CREATE TABLE admissions (row_id INTEGER, subject_id INTEGER, hadm_id INTEGER, admittime TEXT, dischtime TEXT, admission_type TEXT, diagnosis TEXT)')
    cursor.execute('CREATE TABLE diagnoses_icd (row_id INTEGER, subject_id INTEGER, hadm_id INTEGER, icd9_code TEXT, charttime TEXT)')
    cursor.execute('CREATE TABLE d_icd_diagnoses (row_id INTEGER, icd9_code TEXT, short_title TEXT, long_title TEXT)')
    cursor.execute('CREATE TABLE procedures_icd (row_id INTEGER, subject_id INTEGER, hadm_id INTEGER, icd9_code TEXT, charttime TEXT)')
    cursor.execute('CREATE TABLE d_icd_procedures (row_id INTEGER, icd9_code TEXT, short_title TEXT, long_title TEXT)')
    cursor.execute('CREATE TABLE prescriptions (row_id INTEGER, subject_id INTEGER, hadm_id INTEGER, startdate TEXT, enddate TEXT, drug TEXT, dose_val_rx TEXT)')
    cursor.execute('CREATE TABLE labevents (row_id INTEGER, subject_id INTEGER, hadm_id INTEGER, itemid INTEGER, charttime TEXT, valuenum REAL, valueuom TEXT)')
    cursor.execute('CREATE TABLE d_labitems (row_id INTEGER, itemid INTEGER, label TEXT)')
    cursor.execute('CREATE TABLE d_items (row_id INTEGER, itemid INTEGER, label TEXT, linksto TEXT)')
    cursor.execute('CREATE TABLE chartevents (row_id INTEGER, subject_id INTEGER, hadm_id INTEGER, icustay_id INTEGER, itemid INTEGER, charttime TEXT, valuenum REAL, valueuom TEXT)')
    cursor.execute('CREATE TABLE icustays (row_id INTEGER, subject_id INTEGER, hadm_id INTEGER, icustay_id INTEGER, first_careunit TEXT, last_careunit TEXT, intime TEXT, outtime TEXT)')
    cursor.execute('CREATE TABLE inputevents_cv (row_id INTEGER, subject_id INTEGER, hadm_id INTEGER, icustay_id INTEGER, charttime TEXT, itemid INTEGER, amount REAL)')
    cursor.execute('CREATE TABLE outputevents (row_id INTEGER, subject_id INTEGER, hadm_id INTEGER, icustay_id INTEGER, charttime TEXT, itemid INTEGER, value REAL)')
    cursor.execute('CREATE TABLE microbiologyevents (row_id INTEGER, subject_id INTEGER, hadm_id INTEGER, charttime TEXT, spec_type_desc TEXT, org_name TEXT)')
    cursor.execute('CREATE TABLE cost (row_id INTEGER, subject_id INTEGER, hadm_id INTEGER, event_type TEXT, event_id INTEGER, chargetime TEXT, cost REAL)')
    cursor.execute('CREATE TABLE transfers (row_id INTEGER, subject_id INTEGER, hadm_id INTEGER, icustay_id INTEGER, eventtype TEXT, careunit TEXT, intime TEXT, outtime TEXT)')
    

    cursor.executemany('INSERT INTO patients VALUES (?, ?, ?, ?, ?)', [(1, 1001, 'M', '1950-01-01', None), (2, 1002, 'F', '1960-05-15', None)])
    cursor.executemany('INSERT INTO admissions VALUES (?, ?, ?, ?, ?, ?, ?)', [(1, 1001, 2001, '2024-01-01', '2024-01-10', 'EMERGENCY', 'Pneumonia')])
    cursor.executemany('INSERT INTO d_icd_diagnoses VALUES (?, ?, ?, ?)', [(1, '486', 'Pneumonia', 'Pneumonia organism unspecified')])
    cursor.executemany('INSERT INTO diagnoses_icd VALUES (?, ?, ?, ?, ?)', [(1, 1001, 2001, '486', '2024-01-01')])
    cursor.executemany('INSERT INTO d_labitems VALUES (?, ?, ?)', [(1, 50912, 'Creatinine')])
    cursor.executemany('INSERT INTO labevents VALUES (?, ?, ?, ?, ?, ?, ?)', [(1, 1001, 2001, 50912, '2024-01-01', 1.2, 'mg/dL')])
    
    conn.commit()
    print(f"Database created: {db_path}")
    print(f"Patients: {cursor.execute('SELECT COUNT(*) FROM patients').fetchone()[0]} rows")
    conn.close()

if __name__ == "__main__":
    create_database()
