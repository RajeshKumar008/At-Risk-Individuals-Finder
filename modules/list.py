import sqlite3
import face_recognition
from PIL import Image
import numpy as np

def get_complaints():
    conn = sqlite3.connect('missing_persons.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM complaints WHERE status='active'")
    complaints = cursor.fetchall()
    conn.close()
    return complaints

def respond_to_complaint(complaint_id, responder_name, response_photo):
    response_image_path = f'static/uploads/{response_photo.filename}'
    response_photo.save(response_image_path)

    conn = sqlite3.connect('missing_persons.db')
    cursor = conn.cursor()
    cursor.execute("SELECT photo_path FROM complaints WHERE id=?", (complaint_id,))
    original_photo_path = cursor.fetchone()[0]

    original_image = face_recognition.load_image_file(original_photo_path)
    response_image = face_recognition.load_image_file(response_image_path)

    original_encoding = face_recognition.face_encodings(original_image)[0]
    response_encoding = face_recognition.face_encodings(response_image)[0]

    match = face_recognition.compare_faces([original_encoding], response_encoding)[0]
    matched = 1 if match else 0

    cursor.execute('''INSERT INTO responses (complaint_id, responder_name, response_photo_path, matched)
                      VALUES (?, ?, ?, ?)''', (complaint_id, responder_name, response_image_path, matched))

    # Update status if match found
    if match:
        cursor.execute("UPDATE complaints SET status='resolved' WHERE id=?", (complaint_id,))
    conn.commit()
    conn.close()
    
    return match
