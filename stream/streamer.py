import mss
import cv2
import numpy as np
from pynput import mouse
from stream import config, helpers

mouse_controller = mouse.Controller()
cursor_img = helpers.load_cursor()

frame = None
min_interval = 1.0 / config.TARGET_FPS if config.TARGET_FPS > 0 else 0

def screen_capture():
    global frame
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # full screen
        while True:
            img = np.array(sct.grab(monitor))
            frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

            x, y = mouse_controller.position
            rel_x = x - monitor["left"]
            rel_y = y - monitor["top"]

            if 0 <= rel_x < frame.shape[1] and 0 <= rel_y < frame.shape[0]:
                helpers.overlay_image(frame, cursor_img, rel_x, rel_y)
