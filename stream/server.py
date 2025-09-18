import threading
import asyncio
import cv2
from aiohttp import web
from stream import streamer
from stream.config import PORT

async def mjpeg_handler(request):
    response = web.StreamResponse(
        status=200,
        reason="OK",
        headers={"Content-Type": "multipart/x-mixed-replace; boundary=frame"},
    )
    await response.prepare(request)

    try:
        while True:
            if streamer.frame is None:
                await asyncio.sleep(0.01)
                continue

            # Encode latest streamer.frame
            _, jpg = cv2.imencode(".jpg", streamer.frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50])

            await response.write(b"--frame\r\n")
            await response.write(b"Content-Type: image/jpeg\r\n\r\n")
            await response.write(jpg.tobytes())
            await response.write(b"\r\n")

            await asyncio.sleep(1 / 60) 
    except (asyncio.CancelledError, ConnectionResetError):
        pass
    finally:
        return response


async def main():
    app = web.Application()
    app.router.add_get("/", mjpeg_handler)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()

    print(f"🚀 Server running at http://0.0.0.0:{PORT}/")

    while True:
        await asyncio.sleep(3600)


def run_server():
    threading.Thread(target=streamer.screen_capture, daemon=True).start()

    asyncio.run(main())
