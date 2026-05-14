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
    cursor.execute('CREATE TABLE table_19688 ("Year  ( Ceremony ) " TEXT, "Film title used in nomination" TEXT, "Original title" TEXT, "Language  ( s ) " TEXT, "Director ( s ) " TEXT, "Result" TEXT)')
    
    random.seed(19688)
    years = ["2020", "2021", "2022", "2023", "2024"]
    films = ["The Farewell", "Parasite", "Nomadland", "Minari", "Drive My Car"]
    languages = ["English", "Korean", "Mandarin", "Japanese", "Spanish"]
    directors = ["Lulu Wang", "Bong Joon-ho", "Chloé Zhao", "Lee Isaac Chung", "Ryusuke Hamaguchi"]
    results = ["Nominated", "Won", "Nominated", "Nominated", "Won"]
    
    data = []
    for i in range(12):
        year = random.choice(years)
        film = random.choice(films)
        original = film
        lang = random.choice(languages)
        director = random.choice(directors)
        result = random.choice(results)
        data.append((year, film, original, lang, director, result))
    
    data.append(("2023", "Parasite", "Parasite", "Korean", "Bong Joon-ho", "Nominated"))
    
    cursor.executemany('INSERT INTO table_19688 VALUES (?, ?, ?, ?, ?, ?)', data)
    conn.commit()
    print(f"Database created: {db_path}")
    print(f"Inserted {cursor.execute('SELECT COUNT(*) FROM table_19688').fetchone()[0]} rows")
    conn.close()

if __name__ == "__main__":
    create_database()
