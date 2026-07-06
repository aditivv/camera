from gpiozero import DigitalInputDevice
from time import sleep

# Prints the raw VRy (GPIO27) and VRx (GPIO22) readings several times a
# second so you can see exactly what each pin reports as you move the
# joystick through its full range. Ctrl+C to stop.
joystick_y = DigitalInputDevice(27, pull_up=None, active_state=True)
joystick_x = DigitalInputDevice(22, pull_up=None, active_state=True)

print("Move the joystick through up / center / down / left / right and watch the values below.")
print("Format: VRy VRx")
print("Ctrl+C to quit.\n")

try:
    while True:
        print(joystick_y.value, joystick_x.value)
        sleep(0.1)
except KeyboardInterrupt:
    print("Stopping.")
