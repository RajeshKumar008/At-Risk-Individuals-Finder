import sqlite3

def init_db():
    conn = sqlite3.connect('rajesh.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS complaints (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        fname TEXT,
                        lname TEXT,
                        age INTEGER,
                        address TEXT,
                        aadhaar TEXT,
                        missing_date TEXT,
                        missing_location TEXT,
                        photo_path TEXT,
                        status TEXT DEFAULT "active")''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS responses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        complaint_id INTEGER,
                        responder_name TEXT,
                        response_photo_path TEXT,
                        matched BOOLEAN)''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
