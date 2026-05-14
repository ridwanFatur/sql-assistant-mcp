import sqlite3
import os

def create_database():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "database.sqlite")
    if os.path.exists(db_path):
        os.remove(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    

    cursor.execute('CREATE TABLE tv_series (sid INTEGER, title TEXT, release_year INTEGER, num_of_seasons INTEGER, num_of_episodes INTEGER, budget TEXT)')
    cursor.execute('CREATE TABLE director (did INTEGER, gender TEXT, name TEXT, nationality TEXT, birth_city TEXT, birth_year INTEGER)')
    cursor.execute('CREATE TABLE producer (pid INTEGER, gender TEXT, name TEXT, nationality TEXT, birth_city TEXT, birth_year INTEGER)')
    cursor.execute('CREATE TABLE made_by (msid INTEGER, pid INTEGER)')
    cursor.execute('CREATE TABLE directed_by (id INTEGER, msid INTEGER, did INTEGER)')
    cursor.execute('CREATE TABLE actor (aid INTEGER, gender TEXT, name TEXT, nationality TEXT, birth_city TEXT, birth_year INTEGER)')
    cursor.execute('CREATE TABLE cast (id INTEGER, msid INTEGER, aid INTEGER, role TEXT)')
    cursor.execute('CREATE TABLE movie (mid INTEGER, title TEXT, release_year INTEGER, budget TEXT)')
    cursor.execute('CREATE TABLE genre (gid INTEGER, genre TEXT)')
    cursor.execute('CREATE TABLE classification (id INTEGER, msid INTEGER, gid INTEGER)')
    cursor.execute('CREATE TABLE keyword (id INTEGER, keyword TEXT)')
    cursor.execute('CREATE TABLE tags (id INTEGER, msid INTEGER, kid INTEGER)')
    cursor.execute('CREATE TABLE writer (wid INTEGER, gender TEXT, name TEXT, nationality TEXT, birth_city TEXT, birth_year INTEGER)')
    cursor.execute('CREATE TABLE written_by (id INTEGER, msid INTEGER, wid INTEGER)')
    cursor.execute('CREATE TABLE copyright (id INTEGER, msid INTEGER, cid INTEGER)')
    cursor.execute('CREATE TABLE company (cid INTEGER, name TEXT, country TEXT)')
    

    cursor.executemany('INSERT INTO tv_series VALUES (?, ?, ?, ?, ?, ?)', [(1, 'House of Cards', 2013, 6, 73, '100M')])
    cursor.executemany('INSERT INTO director VALUES (?, ?, ?, ?, ?, ?)', [(1, 'M', 'David Fincher', 'USA', 'Denver', 1962)])
    cursor.executemany('INSERT INTO producer VALUES (?, ?, ?, ?, ?, ?)', [(1, 'M', 'Netflix Producer', 'USA', 'LA', 1970)])
    cursor.executemany('INSERT INTO company VALUES (?, ?, ?)', [(1, 'Netflix', 'USA')])
    cursor.executemany('INSERT INTO made_by VALUES (?, ?)', [(1, 1)])
    cursor.executemany('INSERT INTO directed_by VALUES (?, ?, ?)', [(1, 1, 1)])
    cursor.executemany('INSERT INTO copyright VALUES (?, ?, ?)', [(1, 1, 1)])
    
    conn.commit()
    print(f"Database created: {db_path}")
    print(f"TV Series: {cursor.execute('SELECT COUNT(*) FROM tv_series').fetchone()[0]} rows")
    conn.close()

if __name__ == "__main__":
    create_database()
