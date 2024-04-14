import sys
import time

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


def main():
    if len(sys.argv) not in [6, 7]:
        print_help()
        return
    image_path = sys.argv[1]

    # Paint's canvas dimensions
    canvas_width = int(sys.argv[2])
    canvas_height = int(sys.argv[3])
    # Paint's canvas' offset from the displays TOP LEFT corner
    canvas_offset_x = int(sys.argv[4])
    canvas_offset_y = int(sys.argv[5])

    # if Paint is running on the primary display, set this value to 0
    if len(sys.argv) == 6:
        primary_screen_width_pixel = 0
    else:
        primary_screen_width_pixel = int(sys.argv[6])

    # short delay so the user can let go of the mouse
    time.sleep(2)

    mouse_controller = Controller()
    im = Image.open(image_path)

    avg_gray = get_avg_grey_from_image(im)

    for y in range(canvas_height):
        mouse_controller.position = (primary_screen_width_pixel + canvas_offset_x,
                                     canvas_offset_y + y)
        for x in range(0, canvas_width):
            if should_stop:
                break
            px = im.getpixel((x, y))
            if (px[0] + px[1] + px[2]) / 3 < avg_gray:
                mouse_controller.click(Button.left)
            mouse_controller.move(1, 0)
            # short delay because
            #  - without it the mouse goes rogue
            #  - Paint can't follow the clicks that fast visually
            time.sleep(0.001)
    else:
        im.close()


def print_help():
    print('Usage:')
    print('    python main.py <image_path> <canvas_width> <canvas_height> <canvas_offset_x>'
          ' <canvas_offset_y> [primary_screen_width]')
    print('Arguments:')
    print('    image_path: The path of the image for the application to draw in paint')
    print("    canvas_width: Width of Paint's canvas")
    print("    canvas_height: Height of Paint's canvas")
    print("    canvas_offset_x: Paint's canvas' (TOP-LEFT corner) offset"
          " from the display's left side in pixels")
    print("    canvas_offset_y: Paint's canvas' (TOP-LEFT corner) offset"
          " from the display's top in pixels")
    print('    primary_screen_width: (Optional) default 0. If Paint is running on the'
          ' primary display leave out or set to 0.'
          '\n        This application assumes that Paint is running ON or to the RIGHT of the'
          ' primary display.'
          '\n        If Paint is running to the RIGHT of the primary display set to the'
          ' width of all the displays (in pixels) to the LEFT of Paint.')


def get_avg_grey_from_image(image: Image):
    grays = []
    for y in range(image.height):
        for x in range(image.width):
            px = image.getpixel((x, y))
            grays.append((px[0] + px[1] + px[2]) / 3)
    return sum(grays) / len(grays)


if __name__ == '__main__':
    main()
