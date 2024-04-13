import sys
import time
from typing import Tuple

from PIL import Image
from pynput.mouse import Button, Controller
import pynput.keyboard as kbd

should_stop = False


# Failsafe if cursor goes rogue
def on_press(key):
    global should_stop
    if key == kbd.Key.home:
        print("Failsafe key hit, stopping execution")
        should_stop = True


kbd_listener = kbd.Listener(on_press=on_press)
kbd_listener.start()

# short delay so the user can let go of the mouse
time.sleep(2)

# if Paint is running on the primary display, set this value to 0
PRIMARY_SCREEN_WIDTH_PIXEL = 2560

# Paint's canvas dimensions
# CANVAS_WIDTH = 1024
# CANVAS_HEIGHT = 768
CANVAS_WIDTH = 100
CANVAS_HEIGHT = 100
# Paint's canvas' offset from the displays TOP LEFT corner
CANVAS_OFFSET_X = 5
CANVAS_OFFSET_Y = 144

mouse = Controller()
im = Image.open(sys.argv[1])
for y in range(CANVAS_HEIGHT):
    mouse.position = (PRIMARY_SCREEN_WIDTH_PIXEL + CANVAS_OFFSET_X, CANVAS_OFFSET_Y + y)
    for x in range(0, CANVAS_WIDTH):
        if should_stop:
            break
        px = im.getpixel([y, x])
        if (px[0] + px[1] + px[2]) / 3 < 50:
            mouse.click(Button.left)
        mouse.move(1, 0)
        # short delay because
        #  - without it the mouse goes rogue
        #  - Paint can't follow the clicks that fast visually
        time.sleep(0.001)
else:
    im.close()
