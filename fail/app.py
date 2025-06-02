from flask import Flask, render_template, request, redirect, url_for, flash, Response
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import os
import sys
import face_recognition
import cv2

app = Flask(__name__)

# Configuration for the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///missing_persons.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

# Initialize database and mail extensions
db = SQLAlchemy(app)

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'umarfaheej11@gmail.com'
app.config['MAIL_PASSWORD'] = 'zvvu mdob oezo ptqn'  # Use environment variables in production
mail = Mail(app)

# Model for the Complaint (Database table)
class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/complaint', methods=['GET', 'POST'])
def file_complaint():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        email = request.form['email']
        image_file = request.files['image']
        image_path = os.path.join('static/uploads', image_file.filename)
        image_file.save(image_path)

        new_complaint = Complaint(name=name, location=location, image=image_path, email=email)
        db.session.add(new_complaint)
        db.session.commit()

        flash('Complaint Filed Successfully!')
        return redirect(url_for('index'))
    return render_template('complaint_form.html')

@app.route('/found', methods=['GET', 'POST'])
def found_person():
    if request.method == 'POST':
        found_image = request.files['found_image']
        image_path = os.path.join('static/uploads', found_image.filename)
        found_image.save(image_path)

        match = check_for_match(image_path)
        if match:
            send_alert_email(match['email'], match['name'], match['location'])
            return render_template('match_result.html', match=True, person=match)
        else:
            flash("No matches found. Please ensure the images are clear and try again.")
            return render_template('match_result.html', match=False)
    return render_template('found_form.html')

@app.route('/complaints')
def complaints():
    all_complaints = Complaint.query.all()
    return render_template('complaints.html', complaints=all_complaints)

@app.route('/surveillance')
def surveillance():
    return render_template('surveillance.html')

def generate_frames():
    camera = cv2.VideoCapture(0)  # Use the first camera
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def check_for_match(image_path):
    found_image = face_recognition.load_image_file(image_path)
    found_encoding = face_recognition.face_encodings(found_image)

    if not found_encoding:
        print("No face found in the uploaded image.")
        return None

    found_encoding = found_encoding[0]  # Get the first encoding

    all_complaints = Complaint.query.all()
    for person in all_complaints:
        db_image = face_recognition.load_image_file(person.image)
        db_encoding = face_recognition.face_encodings(db_image)

        if not db_encoding:
            print(f"No face found for {person.name}. Skipping.")
            continue

        db_encoding = db_encoding[0]
        results = face_recognition.compare_faces([db_encoding], found_encoding)
        face_distances = face_recognition.face_distance([db_encoding], found_encoding)

        if results[0] or face_distances[0] < 0.6:  # Adjust threshold as necessary
            return {'name': person.name, 'location': person.location, 'email': person.email}
    return None

def send_alert_email(email, person_name, location):
    msg = Message('Match Found: Missing Person', sender='your-email@gmail.com', recipients=[email])
    msg.body = f'A match for {person_name} was found last seen at {location}.'
    mail.send(msg)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the tables
    app.run(debug=True)
