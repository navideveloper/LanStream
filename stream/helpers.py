import cv2
import numpy as np
from stream import config

def load_cursor(path="assets/cursor.png", size=config.CURSOR_SIZE):
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if img is None:
        img = np.zeros((size, size, 4), dtype=np.uint8)
        cv2.circle(img, (size//2, size//2), size//2, (255, 255, 255, 255), -1)
    else:
        img = cv2.resize(img, (size, size), interpolation=cv2.INTER_AREA)
    return img

def overlay_image(bg, fg, x, y):
    bh, bw = bg.shape[:2]
    ch, cw = fg.shape[:2]
    if x >= bw or y >= bh or x+cw <= 0 or y+ch <= 0:
        return bg

    x1, y1 = max(x, 0), max(y, 0)
    x2, y2 = min(x+cw, bw), min(y+ch, bh)

    fg_x1, fg_y1 = max(0, -x), max(0, -y)
    fg_x2, fg_y2 = fg_x1 + (x2-x1), fg_y1 + (y2-y1)

    fg_crop = fg[fg_y1:fg_y2, fg_x1:fg_x2]
    bg_crop = bg[y1:y2, x1:x2]

    alpha_fg = fg_crop[:, :, 3:4] / 255.0
    alpha_bg = 1.0 - alpha_fg

    bg[y1:y2, x1:x2] = (alpha_fg * fg_crop[:, :, :3] +
                        alpha_bg * bg_crop).astype(np.uint8)
    return bg