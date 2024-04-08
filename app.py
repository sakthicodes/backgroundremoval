# Importing necessary libraries
from flask import Flask, render_template, Response
import cv2
from pyzbar.pyzbar import decode

# Creating Flask app
app = Flask(__name__)

# Function to generate video frames
def gen_frames():
    cap = cv2.VideoCapture(0)  # Use 0 for default camera

    # Check if the camera is opened successfully
    if not cap.isOpened():
        print("Error opening camera")
        return

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error reading frame")
            break

        # Decode QR code
        decoded_objs = decode(frame)
        if decoded_objs:
            # Extract URL from QR code data
            url = decoded_objs[0].data.decode()
            # Open video capture using URL
            cap_mobile = cv2.VideoCapture(url)

            # Check if the mobile camera capture is opened successfully
            if cap_mobile.isOpened():
                while True:
                    ret_mobile, frame_mobile = cap_mobile.read()
                    if not ret_mobile:
                        print("Error reading mobile frame")
                        break

                    # Encode frame to JPEG format
                    ret, buffer = cv2.imencode('.jpg', frame_mobile)
                    frame = buffer.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            else:
                print("Error opening mobile camera")
                break

    # Release video captures
    cap.release()
    if 'cap_mobile' in locals():
        cap_mobile.release()

# Route for video feed
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Running the Flask app
if __name__ == '__main__':
    app.run(debug=True)
