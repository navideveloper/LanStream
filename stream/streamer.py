import mss
import cv2,time,asyncio
import numpy as np
from pynput import mouse
from stream import config, helpers

mouse_controller = mouse.Controller()
cursor_img = helpers.load_cursor()

frame = None
last_reload = 0
reload_interval = 10

def screen_capture():
    global frame, min_interval,last_reload,cursor_img
    with mss.mss() as sct:
        monitor = sct.monitors[config.MONITOR_INDEX]
        while True:
            if time.time() - last_reload > reload_interval:
                config.load_config()
                monitor = sct.monitors[config.MONITOR_INDEX]
                min_interval = 1.0 / config.TARGET_FPS if config.TARGET_FPS > 0 else 0
                cursor_img = helpers.load_cursor()
                last_reload = time.time()

            img = np.array(sct.grab(monitor))
            frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

            x, y = mouse_controller.position
            rel_x = x - monitor["left"]
            rel_y = y - monitor["top"]

            if 0 <= rel_x < frame.shape[1] and 0 <= rel_y < frame.shape[0]:
                helpers.overlay_image(frame, cursor_img, rel_x, rel_y)

            if min_interval > 0:
                time.sleep(min_interval)

async def capture_loop():
    global frame, last_reload, cursor_img
    with mss.mss() as sct:
        monitor = sct.monitors[config.MONITOR_INDEX]
        while config.RUN:
            if time.time() - last_reload > reload_interval:
                config.load_config()
                monitor = sct.monitors[config.MONITOR_INDEX]
                cursor_img = helpers.load_cursor()
                last_reload = time.time()

            img = np.array(sct.grab(monitor))
            frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

            x, y = mouse_controller.position
            rel_x = x - monitor["left"]
            rel_y = y - monitor["top"]

            if 0 <= rel_x < frame.shape[1] and 0 <= rel_y < frame.shape[0]:
                helpers.overlay_image(frame, cursor_img, rel_x, rel_y)

            await asyncio.sleep(1.0 / config.TARGET_FPS if config.TARGET_FPS > 0 else 0.01)