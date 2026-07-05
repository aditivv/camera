from gpiozero import Button
import cv2
from datetime import datetime
import os

# Set up the button on GPIO17, using the Pi's internal pull-up resistor
button = Button(17, pull_up=True, bounce_time=0.2)

# WHAT IS HAPPENING HERE:
    # bounce_time: handles DEBOUNCE, which prevents button from detecting multiple presses due to the button mechanism
    # pull_up: ensures the button reads HIGH when not pressed and LOW when pressed, which is standard for GPIO buttons
    # 17: button is connected to GPIO pin 17 on the Raspberry Pi 3

# Set up the webcam (0 is usually the first/only USB camera)
camera = cv2.VideoCapture(0)

# Make sure the save folder exists
save_dir = os.path.expanduser("~/Pictures")
os.makedirs(save_dir, exist_ok=True)

print("Ready. Press the button to take a photo. Press 'q' in the preview window (or Ctrl+C) to quit.")

capture_requested = False

def request_capture():
    global capture_requested
    capture_requested = True

def save_photo(frame):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{save_dir}/photo_{timestamp}.jpg"
    cv2.imwrite(filename, frame)
    print(f"Saved: {filename}")

button.when_pressed = request_capture

try:
    while True:
        ret, frame = camera.read()
        if not ret:
            print("Failed to grab frame from webcam.")
            break

        cv2.imshow("Camera Preview", frame)

        if capture_requested:
            save_photo(frame)
            capture_requested = False

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    print("Stopping.")
finally:
    camera.release()
    cv2.destroyAllWindows()
