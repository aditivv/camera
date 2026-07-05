# Camera

A camera that allows you to take pictures by clicking a button!

## Required Components

* Raspberry Pi 3 Model B+
* Button
* Breadboard
* 2 male-to-female jumper cables
* Webcam

## Setup

1. Attach a button along the middle of the breadboard, with the legs spanning across the center such that there are 2 legs on either side firmly plugged into the holes of the breadboard.
2. Attach the female end of one jumper cable on the GPIO17 pin of the Pi and the male end in line with one of the legs of the button (in the same row) on one side of the center line.
3. Attach the female end of the other jumper cable on the GND pin of the Pi and the male end in line with one of the legs on the button on the opposite side as the other jumper cable.
4. Plug in a webcam into one of the USB-A ports of your Pi.
5. Clone this repository on your Pi.
6. Run `python button.py` and follow the instructions that follow in the command prompt. Images will be saved in your Pi's `home\Pictures` directory.

## Fun features
* Show a thumbs up to the camera --> glasses will appear on your face! Show a thumbs down for the glasses to disappear. Effects will appear in any photos that you take.

## Potential enhancements

* Utilizing MediaPipe framework for live feed detection (hand signals, etc.); unfortunately currently unavailable due to its lagging behind recent Python updates.
