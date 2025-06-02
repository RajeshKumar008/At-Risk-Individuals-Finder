import cv2
import face_recognition
from app import send_alert_email, check_for_match

def run_surveillance():
    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding in face_encodings:
            match = check_for_match(face_encoding)

            if match:
                send_alert_email(match['email'], match['name'], match['location'])
                print(f"Match found for {match['name']}")

        cv2.imshow('Video Feed', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
