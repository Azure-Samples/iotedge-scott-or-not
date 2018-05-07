from sense_hat import SenseHat
from time import sleep

sense = SenseHat()

def flash_yes():
    X = [0, 128, 0]  # Green
    O = [255, 255, 255]  # White
    
    pixels = [
    O,O,O,O,O,X,O,O,
    O,O,O,O,X,X,X,O,
    O,O,O,X,X,O,X,X,
    O,O,X,X,O,O,O,X,
    O,X,X,O,O,O,O,O,
    X,X,O,O,O,O,O,O,
    X,O,O,O,O,O,O,O,
    O,O,O,O,O,O,O,O
    ]

    sense.set_pixels(pixels)
    sleep(5)
    sense.clear()

def flash_no():
    X = [255, 0, 0]  # Red
    O = [255, 255, 255]  # White

    pixels = [
    X,O,O,O,O,O,O,X,
    O,X,O,O,O,O,X,O,
    O,O,X,O,O,X,O,O,
    O,O,O,X,X,O,O,O,
    O,O,O,X,X,O,O,O,
    O,O,X,O,O,X,O,O,
    O,X,O,O,O,O,X,O,
    X,O,O,O,O,O,O,X
    ]

    sense.set_pixels(pixels)
    sleep(2)
    sense.clear()