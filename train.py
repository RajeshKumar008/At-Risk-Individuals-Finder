import cv2
import os

if not os.path.exists('uploads'):
    os.makedirs('uploads')

name = input("Enter name: ")

cap = cv2.VideoCapture(0)

print("Press 'c' to capture an image or 'q' to quit.")

while True:
    success, frame = cap.read()
    if not success:
        print("Failed to capture video.")
        break

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == ord('c'):  
        filename = f'uploads/{name}.jpg'
        cv2.imwrite(filename, frame)
        print(f"Image saved: {filename}")
    elif key == ord('q'):  
        break

cap.release()
cv2.destroyAllWindows()


