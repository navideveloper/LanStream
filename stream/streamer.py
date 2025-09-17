import time
import mss
import cv2
import numpy as np
from pynput import mouse
from . import config, helpers

mouse_controller = mouse.Controller()
cursor_img = helpers.load_cursor()

def generate_mjpeg():
    with mss.mss() as sct:
        monitor = sct.monitors[config.MONITOR_INDEX] if config.MONITOR_INDEX < len(sct.monitors) else sct.monitors[1]
        min_interval = 1.0 / config.TARGET_FPS if config.TARGET_FPS > 0 else 0
        last_time = 0

        while True:
            now = time.perf_counter()
            if now - last_time < min_interval:
                time.sleep(min_interval - (now - last_time))
            last_time = time.perf_counter()

            img = np.array(sct.grab(monitor))
            frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

            x, y = mouse_controller.position
            rel_x = x - monitor["left"]
            rel_y = y - monitor["top"]

            if 0 <= rel_x < frame.shape[1] and 0 <= rel_y < frame.shape[0]:
                helpers.overlay_image(frame, cursor_img, rel_x, rel_y)

            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), config.JPEG_QUALITY]
            success, encoded_image = cv2.imencode('.jpg', frame, encode_param)
            if not success:
                continue

            jpg_bytes = encoded_image.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpg_bytes + b'\r\n')
