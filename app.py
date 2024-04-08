# Importing necessary libraries
from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import base64
import io

# Creating Flask app
app = Flask(__name__)

# Load background video
background_video = cv2.VideoCapture("green.mp4")

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route for receiving video feed
@app.route('/video_feed', methods=['POST'])
def video_feed():
    data = request.json
    if 'image' in data:
        # Decode base64 image
        img_data = base64.b64decode(data['image'].split(',')[1])
        nparr = np.frombuffer(img_data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Read next frame from background video
        ret, background_frame = background_video.read()
        if not ret:
            background_video.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reset video to start if it ends
        
        # Resize background frame to match client's camera frame size
        background_frame = cv2.resize(background_frame, (frame.shape[1], frame.shape[0]))
        
        # Apply green screen effect (replace green pixels with background frame)
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_frame, (35, 100, 100), (77, 255, 255))  # Green color range
        result_frame = cv2.bitwise_and(frame, frame, mask=cv2.bitwise_not(mask))  # Remove green pixels
        result_frame += cv2.bitwise_and(background_frame, background_frame, mask=mask)  # Add background
        
        # Encode processed frame to send back to client
        retval, buffer = cv2.imencode('.jpg', result_frame)
        img_str = base64.b64encode(buffer).decode('utf-8')
        return jsonify(image=img_str)
    else:
        return jsonify(error='No image data received.')

# Running the Flask app
if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0', port=5000, **options)
