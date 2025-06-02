import cv2
import face_recognition
import sqlite3
from flask_mail import Message

def monitor_surveillance():
    video_capture = cv2.VideoCapture(0)
    conn = sqlite3.connect('missing_persons.db')
    cursor = conn.cursor()
    cursor.execute("SELECT photo_path FROM complaints WHERE status='active'")
    photos = cursor.fetchall()

    known_encodings = []
    for photo in photos:
        img = face_recognition.load_image_file(photo[0])
        encoding = face_recognition.face_encodings(img)[0]
        known_encodings.append(encoding)

    while True:
        ret, frame = video_capture.read()
        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            if True in matches:
                # Send alert via email
                send_email_alert()
                cv2.putText(frame, "Match Found!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break   

    video_capture.release()
    cv2.destroyAllWindows()
    conn.close()

def send_email_alert():
    msg = Message("Missing Person Found!", sender="umarfaheej11@gmail.com", recipients=["recipient_email@gmail.com"])
    msg.body = "A missing person matching the database records has been spotted on camera!"
    mail.send(msg)
