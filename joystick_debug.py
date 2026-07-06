from gpiozero import DigitalInputDevice
from time import sleep

# Prints the raw VRy reading on GPIO27 several times a second so you can see
# exactly what the pin reports as you move the joystick through its full
# range (up / center / down). Ctrl+C to stop.
joystick_y = DigitalInputDevice(27, pull_up=None)

print("Move the joystick through up / center / down and watch the values below.")
print("Ctrl+C to quit.\n")

try:
    while True:
        print(joystick_y.value)
        sleep(0.1)
except KeyboardInterrupt:
    print("Stopping.")
