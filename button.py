from gpiozero import Button
import cv2
import numpy as np
from datetime import datetime
import os

# Set up the button on GPIO17, using the Pi's internal pull-up resistor
button = Button(17, pull_up=True, bounce_time=0.2)

# Set up the webcam (0 is usually the first/only USB camera)
camera = cv2.VideoCapture(0)

# Make sure the save folder exists
save_dir = os.path.expanduser("~/Pictures")
os.makedirs(save_dir, exist_ok=True)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Skin-color range for hand detection in HSV. This is highly dependent on
# lighting and skin tone - tune these if gestures aren't being picked up.
SKIN_LOWER = np.array([0, 30, 60], dtype=np.uint8)
SKIN_UPPER = np.array([20, 150, 255], dtype=np.uint8)

print("Ready. Thumbs up enables the face effect, thumbs down disables it.")
print("Press the button to take a photo. Press 'q' in the preview window (or Ctrl+C) to quit.")

capture_requested = False
effect_enabled = False


def request_capture():
    global capture_requested
    capture_requested = True


button.when_pressed = request_capture


def detect_thumb_gesture(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, SKIN_LOWER, SKIN_UPPER)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None

    hand = max(contours, key=cv2.contourArea)
    if cv2.contourArea(hand) < 3000:
        return None

    _, y, w, h = cv2.boundingRect(hand)
    if h < w:
        # A thumbs up/down fist is taller than it is wide.
        return None

    moments = cv2.moments(hand)
    if moments["m00"] == 0:
        return None
    centroid_y = moments["m01"] / moments["m00"]
    relative_pos = (centroid_y - y) / h  # 0 = top of box, 1 = bottom

    if relative_pos > 0.6:
        return "up"
    elif relative_pos < 0.4:
        return "down"
    return None


def apply_face_effect(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))
    for (fx, fy, fw, fh) in faces:
        center = (fx + fw // 2, fy + int(fh * 0.35))
        axes = (fw // 2, int(fh * 0.4))
        overlay = frame.copy()
        cv2.ellipse(overlay, center, axes, 0, 0, 360, (0, 0, 255), -1)
        cv2.addWeighted(overlay, 0.35, frame, 0.65, 0, frame)
        cv2.ellipse(frame, center, axes, 0, 0, 360, (0, 0, 255), 3)
    return frame


def save_photo(frame):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{save_dir}/photo_{timestamp}.jpg"
    cv2.imwrite(filename, frame)
    print(f"Saved: {filename}")


try:
    while True:
        ret, frame = camera.read()
        if not ret:
            print("Failed to grab frame from webcam.")
            break

        gesture = detect_thumb_gesture(frame)
        if gesture == "up":
            effect_enabled = True
        elif gesture == "down":
            effect_enabled = False

        display_frame = apply_face_effect(frame.copy()) if effect_enabled else frame

        cv2.imshow("Camera Preview", display_frame)

        if capture_requested:
            save_photo(display_frame)
            capture_requested = False

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    print("Stopping.")
finally:
    camera.release()
    cv2.destroyAllWindows()
