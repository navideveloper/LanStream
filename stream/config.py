import json, os
SETTINGS_FILE = "settings.json"

# Default values
JPEG_QUALITY = 50
TARGET_FPS = 12
MONITOR_INDEX = 1
CURSOR_SIZE = 30
PORT = 80
CURSOR = "cursor1.png"

def load_config():
    global JPEG_QUALITY, TARGET_FPS, MONITOR_INDEX, CURSOR_SIZE, PORT, CURSOR
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            data = json.load(f)
            JPEG_QUALITY = int(data.get("quality", JPEG_QUALITY))
            TARGET_FPS = int(data.get("fps", TARGET_FPS))
            MONITOR_INDEX = int(data.get("monitor", MONITOR_INDEX))
            CURSOR_SIZE = int(data.get("cursor_size", CURSOR_SIZE))
            PORT = int(data.get("port", PORT))
            # cursor_type dan tanlangan faylni olish
            cursor_map = {1: "cursor1.png", 2: "cursor4.png", 3: "cursor3.png"}
            CURSOR = cursor_map.get(data.get("cursor_type", 1), "cursor1.png")
load_config()