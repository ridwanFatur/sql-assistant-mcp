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
    
    cursor.execute('CREATE TABLE Reservations (Code INTEGER, Room TEXT, CheckIn TEXT, CheckOut TEXT, Rate REAL, LastName TEXT, FirstName TEXT, Adults INTEGER, Kids INTEGER)')
    cursor.execute('CREATE TABLE Rooms (RoomId TEXT, roomName TEXT, beds INTEGER, bedType TEXT, maxOccupancy INTEGER, basePrice INTEGER, decor TEXT)')
    
    random.seed(38)
    
    rooms_data = [
        ("R101", "Deluxe Suite", 2, "Queen", 4, 150, "Modern"),
        ("R102", "Standard Room", 1, "King", 2, 100, "Classic"),
        ("R103", "Family Room", 2, "Double", 4, 120, "Traditional"),
        ("R104", "Executive Suite", 2, "King", 3, 200, "Luxury"),
        ("R105", "Budget Room", 1, "Queen", 2, 80, "Simple"),
        ("R106", "Deluxe Room", 2, "Queen", 4, 140, "Modern"),
        ("R107", "Standard Suite", 1, "King", 2, 110, "Classic")
    ]
    cursor.executemany('INSERT INTO Rooms VALUES (?, ?, ?, ?, ?, ?, ?)', rooms_data)
    
    reservations_data = []
    for i in range(1, 16):
        code = i
        room = random.choice(["R101", "R102", "R103", "R104", "R105", "R106", "R107"])
        checkin = f"2024-0{random.randint(1,9)}-{random.randint(10,28):02d}"
        checkout = f"2024-0{random.randint(1,9)}-{random.randint(10,28):02d}"
        rate = random.uniform(80, 250)
        lastname = random.choice(["Smith", "Johnson", "Williams", "Brown", "Jones"])
        firstname = random.choice(["John", "Mary", "David", "Sarah", "James"])
        adults = random.randint(1, 3)
        kids = random.randint(0, 2)
        reservations_data.append((code, room, checkin, checkout, rate, lastname, firstname, adults, kids))
    
    cursor.executemany('INSERT INTO Reservations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', reservations_data)
    
    conn.commit()
    print(f"Database created: {db_path}")
    print(f"Rooms: {cursor.execute('SELECT COUNT(*) FROM Rooms').fetchone()[0]} rows")
    print(f"Reservations: {cursor.execute('SELECT COUNT(*) FROM Reservations').fetchone()[0]} rows")
    conn.close()

if __name__ == "__main__":
    create_database()
