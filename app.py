import cv2
import numpy as np
# Define green screen color range (adjust these values if needed)
lower_green = np.array([35, 115, 110])  # Lower bounds (BGR)
upper_green = np.array([87, 265, 265])  # Upper bounds (BGR)
cap_video = cv2.VideoCapture("green.mp4")
cap_webcam = cv2.VideoCapture(0)  # 0 for default webcam
if not cap_video.isOpened() or not cap_webcam.isOpened():
    print("Error opening video capture(s)")
    exit()
while True:
    ret_video, frame_video = cap_video.read()
    ret_webcam, frame_webcam = cap_webcam.read()
    if not ret_video or not ret_webcam:
        print("Error reading frames")
        break
    hsv_video = cv2.cvtColor(frame_video, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_video, lower_green, upper_green)
    inv_mask = cv2.bitwise_not(mask)
    foreground = cv2.bitwise_and(frame_video, frame_video, mask=inv_mask)
    mask = cv2.resize(mask, (frame_webcam.shape[1], frame_webcam.shape[0]))
    background = cv2.bitwise_and(frame_webcam, frame_webcam, mask=mask)
    foreground = cv2.resize(foreground, (frame_webcam.shape[1], frame_webcam.shape[0]))
    background = cv2.resize(background, (frame_webcam.shape[1], frame_webcam.shape[0]))
    final_frame = cv2.add(foreground, background)
    cv2.imshow("Green Screen Replacement", final_frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap_video.release()
cap_webcam.release()
cv2.destroyAllWindows()
