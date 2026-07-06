from gpiozero import Button, DigitalInputDevice, LED
import cv2
from datetime import datetime
import os
import time

# SW pin on the joystick, wired the same as the old standalone button
button = Button(17, pull_up=True, bounce_time=0.2)

# VRy/VRx pins on the joystick. With the module's VCC wired to the Pi's 3.3V
# rail (not 5V - GPIO inputs only tolerate up to 3.3V), pushing the stick up
# swings VRy below the GPIO's digital threshold (reads LOW), and pushing left
# does the same for VRx. Center and the opposite direction (down/right) both
# read HIGH on their respective pins - there's no ADC here, so those
# directions can't be told apart from center. active_state=False means
# "active" = pushed toward the direction we can reliably detect.
joystick_y = DigitalInputDevice(27, pull_up=None, active_state=False, bounce_time=0.02)
joystick_x = DigitalInputDevice(22, pull_up=None, active_state=False, bounce_time=0.02)

# 1-digit common-cathode 7-segment display, used for the pre-capture countdown.
# Each segment lights up when its GPIO pin is driven HIGH.
segments = {
    "a": LED(25),
    "b": LED(26),
    "c": LED(13),
    "d": LED(12),
    "e": LED(16),
    "f": LED(24),
    "g": LED(23),
}

DIGIT_SEGMENTS = {
    1: "bc",
    2: "abged",
    3: "abgcd",
}


def display_digit(digit):
    lit = DIGIT_SEGMENTS.get(digit, "")
    for name, led in segments.items():
        led.value = name in lit

# Set up the webcam (0 is usually the first/only USB camera)
camera = cv2.VideoCapture(0)

# Make sure the save folder exists
save_dir = os.path.expanduser("~/Pictures")
os.makedirs(save_dir, exist_ok=True)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

print("Ready. Push the joystick up to enable the glasses effect, left to disable it.")
print("Press the joystick in to start a 3 second countdown and take a photo. Press 'q' in the preview window (or Ctrl+C) to quit.")

COUNTDOWN_SECONDS = 3

effect_enabled = False
countdown_active = False
countdown_start = None
countdown_displayed = None


def request_capture():
    global countdown_active, countdown_start, countdown_displayed
    if not countdown_active:
        countdown_active = True
        countdown_start = time.time()
        countdown_displayed = None


def enable_effect():
    global effect_enabled
    effect_enabled = True

def disable_effect():
    global effect_enabled
    effect_enabled = False

button.when_pressed = request_capture
joystick_y.when_activated = enable_effect
joystick_x.when_activated = disable_effect

# draws glasses over any face detected in the frame
def apply_face_effect(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))
    for (fx, fy, fw, fh) in faces:
        eye_y = fy + int(fh * 0.42)
        left_eye_x = fx + int(fw * 0.28)
        right_eye_x = fx + int(fw * 0.72)
        lens_radius = int(fw * 0.16)
        thickness = max(2, lens_radius // 4)

        cv2.circle(frame, (left_eye_x, eye_y), lens_radius, (0, 0, 0), thickness)
        cv2.circle(frame, (right_eye_x, eye_y), lens_radius, (0, 0, 0), thickness)
        # bridge connecting the two lenses
        cv2.line(frame, (left_eye_x + lens_radius, eye_y), (right_eye_x - lens_radius, eye_y), (0, 0, 0), thickness)
        # temple arms extending toward the sides of the face
        cv2.line(frame, (left_eye_x - lens_radius, eye_y), (fx, eye_y - int(fh * 0.05)), (0, 0, 0), thickness)
        cv2.line(frame, (right_eye_x + lens_radius, eye_y), (fx + fw, eye_y - int(fh * 0.05)), (0, 0, 0), thickness)
    return frame

# function to allow user to enter a name for the photo (optional)
def prompt_photo_name():
    name = input("Name this photo (leave blank to use a timestamp): ").strip()
    if not name:
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.splitext(os.path.basename(name))[0]


def save_photo(frame):
    name = prompt_photo_name()
    filename = os.path.join(save_dir, f"{name}.jpg")
    counter = 1
    while os.path.exists(filename):
        filename = os.path.join(save_dir, f"{name}_{counter}.jpg")
        counter += 1
    cv2.imwrite(filename, frame)
    print(f"Saved: {filename}")


try:
    while True:
        ret, frame = camera.read()
        if not ret:
            print("Failed to grab frame from webcam.")
            break

        display_frame = apply_face_effect(frame.copy()) if effect_enabled else frame

        cv2.imshow("Camera Preview", display_frame)

        if countdown_active:
            elapsed = time.time() - countdown_start
            if elapsed >= COUNTDOWN_SECONDS:
                display_digit(None)
                save_photo(display_frame)
                countdown_active = False
            else:
                digit_to_show = COUNTDOWN_SECONDS - int(elapsed)
                if digit_to_show != countdown_displayed:
                    display_digit(digit_to_show)
                    countdown_displayed = digit_to_show

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    print("Stopping.")
finally:
    camera.release()
    cv2.destroyAllWindows()
