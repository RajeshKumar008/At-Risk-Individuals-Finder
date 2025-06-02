import os
import sqlite3
from werkzeug.utils import secure_filename

def file_complaint(form_data, file):
    fname = form_data['fname']
    lname = form_data['lname']
    age = form_data['age']
    address = form_data['address']
    aadhaar = form_data['aadhaar']
    missing_date = form_data['missing_date']
    missing_location = form_data['missing_location']
    filename = secure_filename(file.filename)
    file_path = os.path.join('static/uploads', filename)
    file.save(file_path)

    conn = sqlite3.connect('missing_persons.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO complaints (fname, lname, age, address, aadhaar,
                     missing_date, missing_location, photo_path) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                   (fname, lname, age, address, aadhaar, missing_date, missing_location, file_path))
    conn.commit()
    conn.close()
import os
import sqlite3
from werkzeug.utils import secure_filename

def file_complaint(form_data, file):
    fname = form_data['fname']
    lname = form_data['lname']
    age = form_data['age']
    address = form_data['address']
    aadhaar = form_data['aadhaar']
    missing_date = form_data['missing_date']
    missing_location = form_data['missing_location']
    filename = secure_filename(file.filename)
    file_path = os.path.join('static/uploads', filename)
    file.save(file_path)

    conn = sqlite3.connect('missing_persons.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO complaints (fname, lname, age, address, aadhaar,
                     missing_date, missing_location, photo_path) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                   (fname, lname, age, address, aadhaar, missing_date, missing_location, file_path))
    conn.commit()
    conn.close()
