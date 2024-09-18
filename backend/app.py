# Developed by Dhanush RS

import os
import cv2
import numpy as np
from flask import Flask, render_template, Response, jsonify
from keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

# Initialize Flask app
app = Flask(__name__)

# Load the trained FER2013 model
model = load_model('backend/emotion_model.h5')
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Function to process video stream and detect emotions in real-time
def generate_frames():
    camera = cv2.VideoCapture(0)  # Access the webcam
    while True:
        success, frame = camera.read()  # Capture frame-by-frame
        if not success:
            break
        else:
            # Convert frame to grayscale
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_classifier.detectMultiScale(gray_frame, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)  # Draw rectangle around detected face
                roi_gray = gray_frame[y:y+h, x:x+w]
                roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

                # Preprocess the face image for emotion detection
                roi = roi_gray.astype("float") / 255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi, axis=0)

                # Predict the emotion
                prediction = model.predict(roi)[0]
                max_index = np.argmax(prediction)
                emotion = emotion_labels[max_index]

                # Display the detected emotion on the video frame
                cv2.putText(frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Video feed route for real-time emotion detection
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# API for emotion detection from image input (optional if you want image upload support)
@app.route('/detect_emotion', methods=['POST'])
def detect_emotion():
    # This function can handle image uploads and process emotions
    return jsonify({"message": "Emotion detection from uploaded images is not implemented yet"})

if __name__ == "__main__":
    app.run(debug=True)
