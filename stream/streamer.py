import time
import mss
import cv2
import numpy as np
from pynput import mouse
from . import config, helpers
import threading as th

mouse_controller = mouse.Controller()
cursor_img = helpers.load_cursor()

frame = None
frame_lock = th.Lock()

min_interval = 1.0 / config.TARGET_FPS if config.TARGET_FPS > 0 else 0

def screen_mjpeg():
    global frame
    with mss.mss() as sct:
        monitor = (
            sct.monitors[config.MONITOR_INDEX]
            if config.MONITOR_INDEX < len(sct.monitors)
            else sct.monitors[1]
        )
        while True:
            time.sleep(min_interval)
            img = np.array(sct.grab(monitor))
            f = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

            x, y = mouse_controller.position
            rel_x = x - monitor["left"]
            rel_y = y - monitor["top"]

            if 0 <= rel_x < f.shape[1] and 0 <= rel_y < f.shape[0]:
                helpers.overlay_image(f, cursor_img, rel_x, rel_y)

            success, encoded_image = cv2.imencode(
                ".jpg", f, [int(cv2.IMWRITE_JPEG_QUALITY), config.JPEG_QUALITY]
            )
            if not success:
                continue

            jpg_bytes = encoded_image.tobytes()
            mjpeg_frame = (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + jpg_bytes + b"\r\n"
            )

            # store latest frame safely
            with frame_lock:
                frame = mjpeg_frame

def generate_mjpeg():
    global frame
    last_time = 0
    while True:
        if frame is None:
            time.sleep(0.01)
            continue

        now = time.perf_counter()
        if now - last_time < min_interval:
            time.sleep(min_interval - (now - last_time))
        last_time = time.perf_counter()

        with frame_lock:
            yield frame

# start background thread
th.Thread(target=screen_mjpeg, daemon=True).start()