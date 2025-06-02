import cv2
import face_recognition
import numpy as np
import sqlite3
from flask_mail import Mail, Message
from app import send_alert_email  # Import the email function from app.py

# Load known face encodings from the database
def load_known_faces():
    conn = sqlite3.connect('missing_persons.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, image, email FROM complaints")
    data = cursor.fetchall()
    conn.close()
    
    known_face_encodings = []
    known_face_names = []
    known_face_emails = []
    
    for record in data:
        face_id, name, image_path, email = record
        image = face_recognition.load_image_file(image_path)
        encoding = face_recognition.face_encodings(image)
        
        if encoding:
            known_face_encodings.append(encoding[0])
            known_face_names.append(name)
            known_face_emails.append(email)
    
    return known_face_encodings, known_face_names, known_face_emails

# Load known faces
known_face_encodings, known_face_names, known_face_emails = load_known_faces()

# Initialize video capture
video_capture = cv2.VideoCapture(0)

print("Starting surveillance...")

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for face_encoding, face_location in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            email = known_face_emails[best_match_index]
            print(f"ALERT: Match found! Missing person '{name}' detected.")

            # Trigger email alert
            send_alert_email(email, name, "Location of Camera")  # Adjust location as needed

            # Draw a rectangle and label
            top, right, bottom, left = face_location
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)

    cv2.imshow("Surveillance Camera", frame)
    
    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
video_capture.release()
cv2.destroyAllWindows()
