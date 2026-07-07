from gpiozero import LED
from time import sleep

# Turns each segment of the 1-digit 7-segment display on by itself for 1
# second so you can confirm the wiring/pin mapping segment by segment.
segments = {
    "a": LED(18),
    "b": LED(23),
    "c": LED(8),
    "d": LED(25),
    "e": LED(24),
    "f": LED(15),
    "g": LED(14),
}

print("Each segment will light for 1 second. Watch the display.")

try:
    while True:
        for name, led in segments.items():
            print(f"Segment {name} (GPIO{led.pin.number}) ON")
            led.on()
            sleep(1)
            led.off()
except KeyboardInterrupt:
    print("Stopping.")
