import sqlite3

def initialize_database():
    conn = sqlite3.connect('missing_persons.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS missing_persons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT,
            face_encoding BLOB NOT NULL,
            email TEXT
        )
    ''')
    conn.commit()
    conn.close()

def check_table():
    conn = sqlite3.connect('missing_persons.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='missing_persons';")
    table_exists = cursor.fetchone() is not None
    conn.close()
    return table_exists

initialize_database()

if check_table():
    print("Table 'missing_persons' created successfully.")
else:
    print("Failed to create table 'missing_persons'.")
