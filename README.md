
# LanStream

LanStream is an open-source Python application for **live screen streaming over a local network**. It allows others to view your screen directly in their browser using just an IP address, without requiring an internet connection. The program provides a smooth and customizable streaming experience, including cursor settings, video quality, and FPS control.

![Example Screenshot](https://raw.githubusercontent.com/navideveloper/LanStream/main/assets/screenshot.jpg)  
*Example Screenshot*

## Features

- **Local Network Streaming:** Stream your screen to other devices on the same network.
- **Browser-Based Viewing:** View streams via any web browser using the IP address.
- **Cursor Customization:** Adjust cursor visibility and size.
- **Video Settings:** Control resolution, FPS, and overall video quality.
- **User-Friendly Setup:** Easy installation with provided executable.
- **Open Source:** Completely free and open for contributions.

## Technologies Used

- **Python**
- **Flet:** For creating the desktop UI.
- **MSS:** For screen capture.
- **OpenCV (cv2):** For video processing.
- **aiohttp:** For asynchronous streaming over HTTP.

## Installation

You can download the latest setup version here:  
[Download LanStream 1.0](https://github.com/navideveloper/LanStream/raw/main/setup/Lan%20Stream%201.0.exe)

Alternatively, you can clone the repository and run it directly using Python:

```bash
git clone https://github.com/navideveloper/LanStream.git
cd LanStream
pip install -r requirements.txt
python run_app.py
