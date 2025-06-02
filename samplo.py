import face_recognition
import cv2

# Load a sample image and get face encodings
image = face_recognition.load_image_file("test.jpg")  # Replace with a valid image path
face_encodings = face_recognition.face_encodings(image)

if face_encodings:
    print("Face encodings found:", face_encodings)
else:
    print("No face encodings found.")

# Test video capture
video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    rgb_frame = frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_frame)

    print("Face Locations:", face_locations)

    if face_locations:
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        print("Face Encodings in Frame:", face_encodings)

    cv2.imshow("Video", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
