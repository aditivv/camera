from gpiozero import Button
import cv2

button = Button(17, pull_up=True, bounce_time=0.2)
camera = cv2.VideoCapture(0)

capture_requested = False

def request_capture():
    global capture_requested
    capture_requested = True

button.when_pressed = request_capture

while True:
    ret, frame = camera.read()
    if not ret:
        print("Failed to grab frame from webcam.")
        break
    cv2.imshow("Camera Preview", frame)
    if capture_requested:
        print("capture requested!")
        capture_requested = False
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
