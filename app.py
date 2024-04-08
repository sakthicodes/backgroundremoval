# Importing necessary libraries
from flask import Flask, render_template, Response
import cv2
import numpy as np

# Creating Flask app
app = Flask(__name__)

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Function to generate video frames
def gen_frames():
    lower_green = np.array([35, 100, 100])  # Lower bounds (BGR)
    upper_green = np.array([77, 255, 255])  # Upper bounds (BGR)
    
    # Mobile camera feed
    cap_mobile = cv2.VideoCapture(0)  # Use 0 for default camera
    
    # Check if video capture is opened successfully
    if not cap_mobile.isOpened():
        print("Error opening video capture")
        return
    
    while True:
        ret_mobile, frame_mobile = cap_mobile.read()
        
        # Check if frame is read successfully
        if not ret_mobile:
            print("Error reading frame")
            break
        
        # Encode frame to JPEG format
        ret, buffer = cv2.imencode('.jpg', frame_mobile)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    # Release video capture
    cap_mobile.release()

# Route for video feed
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Running the Flask app
if __name__ == '__main__':
    app.run(debug=True)
