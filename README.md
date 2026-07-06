# Camera 📸

A camera that allows you to take pictures using a joystick OR through sound (EG. a clap)!

## Features

* ~~Show a thumbs up to the camera --> glasses will appear on your face! Show a thumbs down for the glasses to disappear. Effects will appear in any photos that you take.~~
* Move the joystick UP to enable a glasses effect on your face in the live feed! Move the joystick LEFT to disable the effect. Effects will appear in any photos that you take.
* Ability to take photos by making a sound; for example, CLAP and a photo will be clicked.
* Ability to name file to whatever you would like. Leaving the name prompt blank saves it in a date-time format.
* There is a 3 second delay before photos are taken to prepare.

## Potential enhancements

* Utilizing MediaPipe framework for live feed detection (hand signals, etc.); unfortunately currently unavailable due to its lagging behind recent Python updates.
* Using sound sensor module's AO pin to have a zoom in/zoom out feature based on sound volume; cannot be done through GPIO (only supports digital output)

# Update (7/6/26) 🌟
Users can now take images hands-free using sound + 3 second delay before images are taken!

## Updated Required Components

* Raspberry Pi 3 Model B+
* Joystick module (5 pin)
* Sound sensor module
* Breadboard
* 16 male-to-female jumper cables
* Webcam

## Updated setup

Joystick setup:
1. Attach the female end of 5 of the jumper cables to the 5 pins on the joystick module, attaching one to each pin. Plug the male end of each jumper cable into an empty row of the breadboard; there must be at most one cable in any row.
2. In each of the rows of the breadboard where a jumper cable is now attached, plug in the male end of ONE of 5 additional jumper cables (on the same side of the gap as the preexisting cable). You should end up with all 10 cables being plugged into the breadboard, with 2 per row.
3. For the row connected to the GND pin of the joystick: attach the loose female end of the jumper cable to a GND pin on the Pi.
4. For the row connected to the +5V pin of the joystick: attach the loose female end of the jumper cable to a 3.3V pin on the Pi.
5. For the row connected to the VRx pin of the joystick: attach the loose female end of the jumper cable to the GPIO22 pin on the Pi.
6. For the row connected to the VRy pin of the joystick: attach the loose female end of the jumper cable to the GPIO27 pin on the Pi.
7. For the row connected to the SW pin of the joystick: attach the loose female end of the jumper cable to the GPIO17 pin on the Pi.

Sound sensor setup:
1. Attach the female end of 3 of the jumper cables to the G, +, and DO pins on the sound sensor module, attaching one to each pin. Plug the male end of each jumper cable into an empty row of the breadboard; there must be at most one cable in any row.
2. In each of the rows of the breadboard where a jumper cable is now attached from the sound sensor, plug in the male end of ONE of 3 additional jumper cables (on the same side of the gap as the preexisting cable). You should end up with all 6 cables being plugged into the breadboard, with 2 per row.
3. For the row connected to the G pin of the sound sensor module: attach the loose female end of the jumper cable to a GND pin on the Pi.
4. For the row connected to the + pin of the sound sensor module: attach the loose female end of the jumper cable to a 3.3V pin on the Pi.
5. For the row connected to the DO pin (Digital Output) of the sound sensor module: attach the loose female end of the jumper cable to the GPIO26 pin on the Pi.

Additional setup:
1. Plug in a webcam into one of the USB-A ports of your Pi.
2. Clone this repository on your Pi.
3. Run `python button.py` and follow the instructions that follow in the command prompt. Images will be saved in your Pi's `home\Pictures` directory.
4. Note: After taking an image, the live feed will freeze until you enter a file name (or click "Enter" in command prompt). You can click the live feed popup to refocus to the camera after naming the file.

# Update (7/5/26) ⭐
Camera now functions using a joystick rather than a button!

## Updated Required Components [outdated as of 7/6/26]

* Raspberry Pi 3 Model B+
* Joystick module (5 pin)
* Breadboard
* 10 male-to-female jumper cables
* Webcam

## Updated setup [outdated as of 7/6/26]

1. Attach the female end of 5 of the jumper cables to the 5 pins on the joystick module, attaching one to each pin. Plug the male end of each jumper cable into an empty row of the breadboard; there must be at most one cable in any row.
2. In each of the rows of the breadboard where a jumper cable is now attached, plug in the male end of ONE of the remaining 5 jumper cables (on the same side of the gap as the preexisting cable). You should end up with all 10 cables being plugged into the breadboard, with 2 per row.
3. For the row connected to the GND pin of the joystick: attach the loose female end of the jumper cable to a GND pin on the Pi.
4. For the row connected to the +5V pin of the joystick: attach the loose female end of the jumper cable to a 3.3V pin on the Pi.
5. For the row connected to the VRx pin of the joystick: attach the loose female end of the jumper cable to the GPIO22 pin on the Pi.
6. For the row connected to the VRy pin of the joystick: attach the loose female end of the jumper cable to the GPIO27 pin on the Pi.
7. For the row connected to the SW pin of the joystick: attach the loose female end of the jumper cable to the GPIO17 pin on the Pi.
8. Plug in a webcam into one of the USB-A ports of your Pi.
9. Clone this repository on your Pi.
10. Run `python button.py` and follow the instructions that follow in the command prompt. Images will be saved in your Pi's `home\Pictures` directory.
11. Note: After taking an image, the live feed will freeze until you enter a file name (or click "Enter" in command prompt). You can click the live feed popup to refocus to the camera after naming the file.

# Starting point (7/4/26) ⭐

## Required Components [outdated as of 7/5/26]

* Raspberry Pi 3 Model B+
* Button
* Breadboard
* 2 male-to-female jumper cables
* Webcam

## Setup [outdated as of 7/5/26]

1. Attach a button along the middle of the breadboard, with the legs spanning across the center such that there are 2 legs on either side firmly plugged into the holes of the breadboard.
2. Attach the female end of one jumper cable on the GPIO17 pin of the Pi and the male end in line with one of the legs of the button (in the same row) on one side of the center line.
3. Attach the female end of the other jumper cable on the GND pin of the Pi and the male end in line with one of the legs on the button on the opposite side as the other jumper cable.
4. Plug in a webcam into one of the USB-A ports of your Pi.
5. Clone this repository on your Pi.
6. Run `python button.py` and follow the instructions that follow in the command prompt. Images will be saved in your Pi's `home\Pictures` directory.
7. Note: After taking an image, the live feed will freeze until you enter a file name (or click "Enter" in command prompt). You can click the live feed popup to refocus to the camera after naming the file.
